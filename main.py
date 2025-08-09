import os
import re
import heapq
import subprocess
import openai
import pandas as pd
import shutil
from javalang.parser import JavaSyntaxError
from javalang.tree import ClassDeclaration, InterfaceDeclaration
from git import Repo as GitRepo
from pydriller import Repository
from javalang.parse import parse
from github import Github
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from dotenv import load_dotenv
from typing import Set, Tuple
from matplotlib.backends.backend_svg import FigureCanvasSVG
load_dotenv()

matplotlib.use('Agg')

PLANTUML_JAR = str(Path(__file__).parent / "plantuml-1.2025.4.jar")

REPO_URL        = "https://github.com/spring-projects/spring-petclinic.git"
REPO_PATH       = "data/repo/spring-petclinic-microservices"
BRANCH          = None
OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY")
GITHUB_TOKEN    = os.environ.get("GITHUB_TOKEN")
COMMIT_COUNT    = 10
SNAPSHOT_DIR    = Path("data/snapshots")
REL_STYLE_RED   = {
    "-->": "-[#red,dotted]->",
    "<|--": "<|--[#red,dotted]",
    "<|..": "<|..[#red,dotted]",
}
REL_STYLE_GREEN = {
    "-->": "-[#green,dotted]->",
    "<|--": "<|--[#green,dotted]",
    "<|..": "<|..[#green,dotted]",
}

if not OPENAI_API_KEY or not GITHUB_TOKEN:
    raise RuntimeError("Must set the OPENAI_API_KEY and GITHUB_TOKEN env vars")


KEYWORD_REGEX = re.compile(
    r'\b(refactor|modul|architectur|service|component|merge)\b',
    re.I
)

os.makedirs(REPO_PATH, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

if not (Path(REPO_PATH) / ".git").exists():
    print(f"Cloning {REPO_URL} → {REPO_PATH}")
    GitRepo.clone_from(REPO_URL, REPO_PATH)


git_repo = GitRepo(REPO_PATH)
try:
    BRANCH = git_repo.active_branch.name
except TypeError:
    head = git_repo.git.symbolic_ref('refs/remotes/origin/HEAD')
    BRANCH = head.split('/')[-1]
print(f"Using branch: {BRANCH}")

openai.api_key = OPENAI_API_KEY
github_token = Github(GITHUB_TOKEN)
gh_repo = github_token.get_repo("spring-projects/spring-petclinic")

def churn_score(commit):
    return commit.insertions + commit.deletions

def traverse_java_commits():
    return Repository(
        REPO_PATH,
        only_in_branch=BRANCH,
        only_modifications_with_file_types=['.java']
    ).traverse_commits()

def top_churn_commits(n=COMMIT_COUNT):
    scored = [(churn_score(commit), commit) for commit in traverse_java_commits()]
    top = heapq.nlargest(n, scored, key=lambda x: x[0])
    return [c for _, c in top]

def keyword_commits(n=COMMIT_COUNT):
    candidates = []
    for commit in traverse_java_commits():
        if KEYWORD_REGEX.search(commit.msg):
            candidates.append((churn_score(commit), commit))
    return [c for _, c in heapq.nlargest(n, candidates)]

def gpt_arch_commits(n=COMMIT_COUNT, n_candidates=50):
    scored = [(churn_score(c), c) for c in traverse_java_commits()]
    candidates = [c for _, c in heapq.nlargest(n_candidates, scored, key=lambda x: x[0])]
    if not candidates:
        return []

    lines = [
        "You are an expert software architect.",
        "From the list of commits below, select the 10 that represent the most **architectural changes (e.g., module boundary shifts, package restructuring, major refactors).",
        "Consider metrics like churn, number of files touched, Java-file count, and presence of refactoring keywords.",
        "Reply with a comma-separated list of commit numbers (1–%d) only.\n" % len(candidates)
    ]
    for i, c in enumerate(candidates, start=1):
        files_changed = len(c.modified_files)
        java_files = sum(1 for m in c.modified_files if m.filename.endswith(".java"))
        kw_hit = bool(KEYWORD_REGEX.search(c.msg))
        msg_summary = c.msg.splitlines()[0]
        lines.append(
            f"{i}. {c.hash[:10]} | date={c.committer_date.date()} | churn={churn_score(c)} "
            f"| files={files_changed} | java_files={java_files} | refactor_keyword={kw_hit} "
            f"| msg=\"{msg_summary}\""
        )
    prompt = "\n".join(lines)
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.0
    )
    content = resp.choices[0].message.content.strip()
    numbers = [int(x) for x in re.findall(r"\b([1-9]\d*)\b", content)]
    selected = [candidates[i-1] for i in numbers if 1 <= i <= len(candidates)]
    return selected[:n]



def run_strategy(name, commits):
    global SNAPSHOT_DIR
    strat_dir = SNAPSHOT_DIR / name
    metrics_csv = strat_dir / "metrics.csv"
    overview_svg = strat_dir / "uml_overview.svg"

    strat_dir.mkdir(parents=True, exist_ok=True)

    old_snapshots = SNAPSHOT_DIR
    SNAPSHOT_DIR = strat_dir
    dump_and_generate_uml(commits)
    df = mine_metrics(commits)
    df.to_csv(metrics_csv, index=False)
    print(f"Saved metrics → {metrics_csv}")
    correlate_and_plot(df, overview_svg)
    SNAPSHOT_DIR = old_snapshots
    print(f"Strategy '{name}' done.\n")

def extract_class_names(src_dir: Path) -> Set[str]:
    names = set()
    for f in src_dir.rglob("*.java"):
        try:
            tree = parse(f.read_text(encoding="utf-8", errors="ignore"))
        except JavaSyntaxError:
            continue
        if tree.types:
            names.add(tree.types[0].name)
    return names

def extract_relationships(src_dir: Path) -> Set[Tuple[str,str,str]]:
    class_names = extract_class_names(src_dir)
    rels = set()
    for f in src_dir.rglob("*.java"):
        try:
            tree = parse(f.read_text(encoding="utf-8", errors="ignore"))
        except JavaSyntaxError:
            continue
        if not tree.types:
            continue
        td = tree.types[0]
        src = td.name

        for field in td.fields:
            tree_name = getattr(field.type, "name", str(field.type))
            if tree_name in class_names:
                rels.add((src, "-->", tree_name))

        extends = getattr(td, "extends", None)
        if extends:
            items = extends if isinstance(extends, list) else [extends]
            for p in items:
                if p.name in class_names:
                    rels.add((p.name, "<|--", src))

        for implements in getattr(td, "implements", []) or []:
            if implements.name in class_names:
                rels.add((implements.name, "<|..", src))

    return rels

def extract_class_details(src_dir: Path):
    details = {}
    for f in src_dir.rglob("*.java"):
        try:
            tree = parse(f.read_text(encoding="utf-8", errors="ignore"))
        except JavaSyntaxError:
            continue
        if not tree.types:
            continue
        td = tree.types[0]
        name = td.name
        kind = "interface" if isinstance(td, InterfaceDeclaration) else "class"
        fields = []
        for field in td.fields:
            tname = getattr(field.type, "name", str(field.type))
            for decl in field.declarators:
                fields.append(f"{decl.name}: {tname}")
        details[name] = {"kind": kind, "fields": fields}
    return details

def generate_diff_puml(old_src: Path, new_src: Path, out_puml: Path):
    old_info = extract_class_details(old_src)
    new_info = extract_class_details(new_src)
    old_classes = set(old_info)
    new_classes = set(new_info)

    removed = old_classes - new_classes
    added = new_classes - old_classes
    kept = old_classes & new_classes

    old_rels = extract_relationships(old_src)
    new_rels = extract_relationships(new_src)
    removed_rels = old_rels - new_rels
    kept_rels = old_rels & new_rels
    added_rels = new_rels - old_rels

    lines = [
        "@startuml",
        "skinparam classAttributeIconSize 0",
        "left to right direction",
    ]

    lines.append('package "Classes (Removed · Unchanged · Added)" <<Rectangle>> {')

    for cls in sorted(removed):
        info = old_info[cls]
        lines.append(f'  {info["kind"]} {cls} <<REMOVED>> #LightSalmon {{')
        for fld in info["fields"]:
            lines.append(f'    + {fld}')
        lines.append("  }")

    for cls in sorted(kept):
        info = new_info[cls]
        lines.append(f'  {info["kind"]} {cls} {{')
        for fld in info["fields"]:
            lines.append(f'    + {fld}')
        lines.append("  }")

    for cls in sorted(added):
        info = new_info[cls]
        lines.append(f'  {info["kind"]} {cls} <<ADDED>> #LightGreen {{')
        for fld in info["fields"]:
            lines.append(f'    + {fld}')
        lines.append("  }")

    lines.append("}")

    for src, arrow, tgt in sorted(removed_rels):
        styled = REL_STYLE_RED.get(arrow, arrow + "[#red,dotted]")
        lines.append(f"{src} {styled} {tgt}")

    for src, arrow, tgt in sorted(kept_rels):
        lines.append(f"{src} {arrow} {tgt}")

    for src, arrow, tgt in sorted(added_rels):
        styled = REL_STYLE_GREEN.get(arrow, arrow + "[#green,dotted]")
        lines.append(f"{src} {styled} {tgt}")

    lines.append("@enduml")
    out_puml.write_text("\n".join(lines))

def dump_and_generate_uml(commits):
    git_repo.git.checkout(BRANCH)
    prev_src = None
    prev_sha = None
    for c in commits:
        sha = c.hash
        snap_dir = SNAPSHOT_DIR / sha
        src_root = snap_dir / "src"
        puml = snap_dir / "diagram.puml"
        png = snap_dir / "diagram.png"

        print(f"Dumping snapshot {sha[:8]}")
        git_repo.git.checkout(sha)

        snap_dir.mkdir(parents=True, exist_ok=True)
        src_root.mkdir(parents=True, exist_ok=True)

        for java_root in Path(REPO_PATH).rglob("src/main/java"):
            rel = java_root.relative_to(REPO_PATH)
            if rel.parts and rel.parts[0] == "src":
                rel = Path(*rel.parts[1:])
            dest = src_root / rel
            print(f"Copying {rel} → {dest}")
            shutil.copytree(java_root, dest, dirs_exist_ok=True)

        if not puml.exists():
            print(f"Generating PlantUML for {sha}")
            generate_puml_for_snapshot(src_root, puml)
            if prev_src is not None:
                diff_puml = snap_dir / "diagram_diff.puml"
                print(f"Generating diff UML {prev_sha[:8]}→{sha}")
                generate_diff_puml(prev_src, src_root, diff_puml)
                old_info = extract_class_details(prev_src)
                new_info = extract_class_details(src_root)
                removed_cls = set(old_info) - set(new_info)
                added_cls = set(new_info) - set(old_info)
                kept_cls = set(old_info) & set(new_info)
                old_rels = extract_relationships(prev_src)
                new_rels = extract_relationships(src_root)
                removed_rels = old_rels - new_rels
                added_rels = new_rels - old_rels
                kept_rels = old_rels & new_rels
                summary_lines = [
                    f"# Commit {sha[:8]}",
                    f"- Date: {c.committer_date.date()}",
                    f"- Churn: {churn_score(c)}",
                ]

                if added_cls:
                    summary_lines.append("### Added classes")
                    summary_lines += [f"- {cls}" for cls in sorted(added_cls)]
                if removed_cls:
                    summary_lines.append("### Removed classes")
                    summary_lines += [f"- {cls}" for cls in sorted(removed_cls)]
                if kept_cls:
                    summary_lines.append("### Unchanged classes")
                    summary_lines += [f"- {cls}" for cls in sorted(kept_cls)]

                if added_rels:
                    summary_lines.append("\n### Added relationships")
                    summary_lines += [f"- {src} {arrow} {tgt}"
                                      for src, arrow, tgt in sorted(added_rels)]
                if removed_rels:
                    summary_lines.append("\n### Removed relationships")
                    summary_lines += [f"- {src} {arrow} {tgt}"
                                      for src, arrow, tgt in sorted(removed_rels)]
                if kept_rels:
                    summary_lines.append("\n### Unchanged relationships")
                    summary_lines += [f"- {src} {arrow} {tgt}"
                                      for src, arrow, tgt in sorted(kept_rels)]

                with open(snap_dir / "diff_summary.md", "w") as f:
                    f.write("\n".join(summary_lines))

                try:
                    summary_md = (snap_dir / "diff_summary.md").read_text()
                    diff_puml_text = diff_puml.read_text()

                    analysis_prompt = f"""You are an expert software architect. Below is a commit summary and its PlantUML diff.
                    Commit Summary
                    {summary_md}
                    PlantUML Diff
                    {diff_puml_text}
                    Write a concise 3–5 paragraph analysis covering:
                    1) architectural intent (new abstractions, boundary shifts, removals),
                    2) responsibility shifts and coupling/cohesion changes,
                    3) potential risks/benefits and impact on maintainability and defects."""

                    resp = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system",
                             "content": "You are a senior software architect providing objective analyses."},
                            {"role": "user", "content": analysis_prompt},
                        ],
                        temperature=0.0,
                        max_tokens=350,
                    )
                    analysis = resp.choices[0].message.content.strip()
                    (snap_dir / "architecture_analysis.md").write_text(analysis)
                    print(f"  ✓ Saved GPT analysis → {snap_dir / 'architecture_analysis.md'}")
                except Exception as e:
                    print(f"GPT analysis skipped: {e}")

                subprocess.run(["java", "-jar", PLANTUML_JAR, "-tsvg", str(diff_puml)], check=True)
                subprocess.run(["java", "-jar", PLANTUML_JAR, "-tpng", str(diff_puml)], check=True)
                diff_png = diff_puml.with_suffix(".png")
                renamed = SNAPSHOT_DIR / f"{prev_sha[:8]}_{sha[:8]}_diff.png"
                shutil.copy(diff_png, renamed)
                diff_svg = diff_puml.with_suffix(".svg")
                target = snap_dir / "diagram.svg"
                shutil.copy(diff_svg, target, follow_symlinks=True)

                subprocess.run(["java", "-jar", PLANTUML_JAR, "-tsvg", str(diff_puml)], check = True)
                subprocess.run(["java", "-jar", PLANTUML_JAR, "-tpng", str(diff_puml)], check=True)
                diff_png = diff_puml.with_suffix(".png")
                renamed = SNAPSHOT_DIR / f"{prev_sha[:8]}_{sha[:8]}_diff.png"
                shutil.copy(diff_png, renamed)
                diff_svg = diff_puml.with_suffix(".svg")
                target = snap_dir / "diagram.svg"
                shutil.copy(diff_svg, target, follow_symlinks=True)
            prev_src = src_root
            prev_sha = sha

        if not png.exists():
            print(f"Rendering PNG for {sha[:8]}")
            subprocess.run(
                ["java", "-jar", PLANTUML_JAR, "-tpng", str(puml)],
                check=True
            )
    git_repo.git.checkout(BRANCH)

def generate_puml_for_snapshot(src_dir: Path, puml_path: Path):
    class_names = set()
    for f in src_dir.rglob("*.java"):
        try:
            tree = parse(f.read_text(encoding="utf-8", errors="ignore"))
        except JavaSyntaxError:
            continue
        if tree.types:
            class_names.add(tree.types[0].name)

    lines = ["@startuml", "skinparam classAttributeIconSize 0", "left to right direction"]
    rels  = set()

    for f in src_dir.rglob("*.java"):
        try:
            tree = parse(f.read_text(encoding="utf-8", errors="ignore"))
        except JavaSyntaxError:
            continue
        if not tree.types:
            continue

        td = tree.types[0]
        name = td.name
        kind = "interface" if td.__class__.__name__ == "InterfaceDeclaration" else "class"

        lines.append(f"{kind} {name} {{")
        for field in td.fields:
            tname = getattr(field.type, "name", str(field.type))
            for decl in field.declarators:
                lines.append(f"  + {decl.name}: {tname}")
                if tname in class_names:
                    rels.add(f"{name} --> {tname}")
        lines.append("}")


        ex = getattr(td, "extends", None)
        if ex:
            if isinstance(ex, list):
                for p in ex:
                    if p.name in class_names:
                        rels.add(f"{p.name} <|-- {name}")
            else:
                if ex.name in class_names:
                    rels.add(f"{ex.name} <|-- {name}")

        for impl in getattr(td, "implements", []) or []:
            if impl.name in class_names:
                rels.add(f"{impl.name} <|.. {name}")

    for r in sorted(rels):
        lines.append(r)

    lines.append("@enduml")
    puml_path.write_text("\n".join(lines))

def mine_metrics(commits):
    rows = []
    prev_date = None

    for c in sorted(commits, key=lambda x: x.committer_date):
        date = c.committer_date
        churn = churn_score(c)

        if prev_date:
            count_commits = sum(
                1
                for _ in Repository(
                    REPO_PATH,
                    only_in_branch=BRANCH,
                    since=prev_date,
                    to=date
                ).traverse_commits()
            )
        else:
            count_commits = 1

        since = prev_date or date.replace(year=date.year - 1)

        bug_issues = gh_repo.get_issues(state="closed", labels=["bug"], since=since)
        feat_issues = gh_repo.get_issues(state="closed", labels=["enhancement"], since=since)

        bugs_filtered = [bug for bug in bug_issues if bug.closed_at and bug.closed_at < date]
        feats_filtered = [feat for feat in feat_issues if feat.closed_at and feat.closed_at < date]

        bugs = 0
        for issue in bugs_filtered:
            bugs += 1
        feats = 0
        for issue in feats_filtered:
            feats += 1

        rows.append({
            "sha":      c.hash,
            "date":     date,
            "churn":    churn,
            "commits":  count_commits,
            "bugs":     bugs,
            "features": feats
        })
        prev_date = date


    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], utc=True)
    return df


def correlate_and_plot(df, out_svg: Path):
    n = len(df)
    fig, axes = plt.subplots(1, n, figsize=(30 * n, 30), constrained_layout=True)
    if n == 1:
        axes = [axes]
    prev_sha = None
    for idx, (ax, row) in enumerate(zip(axes, df.itertuples())):

        if idx > 0:
            candidate = SNAPSHOT_DIR / f"{prev_sha}_{row.sha[:8]}_diff.png"
            if candidate.exists():
                img_path = candidate
            else:
                img_path = SNAPSHOT_DIR / row.sha / "diagram.png"
        else:
            img_path = SNAPSHOT_DIR / row.sha / "diagram.png"

        img = mpimg.imread(str(img_path))
        ax.imshow(img)
        ax.axis('off')
        prev_sha = row.sha[:8]
        metadata_text = (
            f"Commit: {row.sha}\n"
            f"Date: {row.date.date()}\n"
            f"Churn: {row.churn}\n"
            f"Commits since last snapshot: {row.commits}\n"
            f"Bugs closed: {row.bugs}\n"
            f"Features closed: {row.features}\n"
            f"Commit message: {get_commit_message(row.sha)}\n"
        )

        ax.text(
            0.5, -0.05,  metadata_text, ha='center', va='top', fontsize=8, transform=ax.transAxes, wrap=True)

    out_svg.parent.mkdir(parents=True, exist_ok=True)
    canvas = FigureCanvasSVG(fig)
    canvas.embed_images = False
    canvas.print_svg(str(out_svg))
    plt.close(fig)
    print(f"Saved UML overview with metadata → {out_svg}")

def get_commit_message(sha):
    commit = git_repo.commit(sha)
    return commit.message.splitlines()[0]

def build_final_report(strat_dir: Path):

    framing = (
        "In this study, we present a comprehensive framework for analyzing "
        "code and architecture evolution by focusing on a curated sequence of "
        "commits from open-source GitHub repositories. We extract UML diagrams "
        "at successive points in time and compare class and interface structures across "
        "each commit—augmented with commit metadata such as churn, closed-bug counts, and "
        "feature completions, to uncover patterns of module restructuring, "
        "introduction or removal of abstractions, and shifts in responsibility. "
        "Our approach delivers a deep, data-driven analysis of how design decisions "
        "impact system maintainability and defect rates over time, empowering developers "
        "and researchers with clear insights to guide future architectural evolution."
    )

    sections = []
    for commit_dir in sorted(strat_dir.iterdir()):
        summary_md = commit_dir / "diff_summary.md"
        analysis_md = commit_dir / "architecture_analysis.md"
        if summary_md.exists() and analysis_md.exists():
            sha = commit_dir.name
            sections.append(f"### Commit {sha}\n\n")
            sections.append(summary_md.read_text())
            sections.append("\n\n")
            sections.append(analysis_md.read_text())
            sections.append("\n\n---\n\n")

    all_content = framing + "\n\n" + "".join(sections)

    prompt = (
        f"{all_content}\n\n"
        "Please write a single, well-structured report that:\n"
        "1. Summarizes the major architectural trends across all selected commits.\n"
        "2. Highlights key patterns (e.g., where responsibilities shifted, "
        "new abstractions introduced, modules merged/split).\n"
        "3. Correlates these changes with your bug/feature metrics where relevant.\n"
        "4. Concludes with recommendations or insights for future evolution.\n\n"
        "Use formal academic style, with section headings and coherent narrative."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a software-architecture researcher."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.0,
    )
    report = resp.choices[0].message.content.strip()
    final_path = strat_dir / "final_report.md"
    final_path.write_text(report)
    print(f"Saved consolidated report in {final_path}")

STRATEGIES = {
    "churn":   lambda: top_churn_commits(),
    "keyword": lambda: keyword_commits(),
    "gpt":     lambda: gpt_arch_commits(),
}

if __name__ == "__main__":
    for name, fn in STRATEGIES.items():
        print(f"\nRunning strategy: {name}")
        commits = fn()
        commits = sorted(commits, key=lambda c: c.committer_date)
        run_strategy(name, commits)
        build_final_report(SNAPSHOT_DIR / name)