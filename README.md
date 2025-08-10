ArchEvoViz is a Python tool that extracts UML class diagrams directly from source code at selected commits, then renders a color‑coded diff to highlight added/removed classes and relationships. It also links each snapshot to key repository metrics such as churn and the number of issues closed and assembles everything into a single timeline SVG for quick storytelling.
Demonstration case study in our paper: spring-projects/spring-petclinic, showcasing its transition from a monolithic architecture to a microservices-based design.

# Key Features
- Three commit‑selection strategies: churn‑based, keyword‑based, and LLM‑assisted ranking.
- UML directly from source code (Java), parse AST with javalang, emit PlantUML
- Diff diagrams with clear semantics:
  - Added classes/relations → light green with green dotted edges.
  - Removed classes/relations → salmon with red dotted edges.
  - Unchanged → neutral.
- Automated architectural analysis and final report generation: for each commit diff, generates a concise multi‑paragraph interpretation using ChatGPT APIs, covering architectural intent, responsibility shifts, and maintainability impacts, and compiles these into a consolidated final report.
- Repository metrics and commit info shown under each panel: date, churn, commits since previous snapshot, #closed bugs, #closed features.
- One‑shot overview: uml_overview.svg shows the full evolution across selected commits

# Installation
## Prerequisites
- Python 3.10+
- Java (JRE/JDK 11+), required by PlantUML
```bash
pip install pydriller javalang PyGithub matplotlib python-dotenv
```
## Setup
1. **Environment Variables**  
   Create a `.env` file in the project root with the following keys:  
   ```env
   OPENAI_API_KEY=your_chatgpt_api_key_here
   GITHUB_TOKEN=your_github_personal_access_token_here
# Quickstart
Run all three strategies and build the consolidated report:
```bash
python main.py
```
## What you’ll get
### Per‑commit folders with:
- diagram.puml (snapshot UML)
- diagram_diff.{puml,svg,png} (diff vs previous)
- -diff_summary.md and architecture_analysis.md
### Per‑strategy files:
- metrics.csv
- uml_overview.svg (timeline panel of diagrams + metadata)
- final_report.md (consolidated analysis)
## Changing Strategies and Scope
- Pick strategies in the STRATEGIES dict (bottom of the script).
- Adjust sample size via COMMIT_COUNT.
- Tune keywords via KEYWORD_REGEX.
- Switch models by editing gpt_arch_commits / build_final_report (e.g., gpt-4o-mini for cheaper runs).
# Output Location
All generated snapshots, UML diagrams, diffs, metrics, and reports are stored in the data folder:
```text
data/
└─ snapshots/
   ├─ churn/
   ├─ keyword/
   └─ gpt/
