# Cognitive Case Diagrams Scripts

This directory contains the thin orchestrators for the Cognitive Case Diagrams project.

## 🚀 Quick Start

To generate all figures for the manuscript:

```bash
python3 generate_diagrams.py
```

## 📂 Contents

- `generate_diagrams.py`: Main orchestration script that generates all canonical figures for the project. Output is saved to `../../output/figures/`.
- `AGENTS.md`: Detailed architectural guidelines for creating and maintaining scripts in this directory.

## ⚠️ Core Requirement

All scripts here must remain **thin orchestrators**. Scientific logic and computations belong in `../src/`.
