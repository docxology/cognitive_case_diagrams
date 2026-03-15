# 🤖 AGENTS.md - Cognitive Case Diagrams Scripts

## 🎯 System Overview

This directory contains the thin orchestrators for the `cognitive_case_diagrams` project. These scripts coordinate the generation of figures and analysis outputs by importing domain-specific logic from `projects/cognitive_case_diagrams/src/` and utilizing utilities from the `infrastructure/` layer.

## 🏗️ Architecture

Following the template's Two-Layer Architecture, scripts in this directory contain NO core scientific business logic. They strictly:

1. Orchestrate inputs/outputs.
2. Delegate computation to `src/`.
3. Handle rendering and formatting of results.

### Key Orchestrators

- `generate_diagrams.py`: The master figure generator. It produces all 10+ canonical visualizations (Category diagrams, String diagrams, Enriched diagrams, Functor diagrams, DisCoPy diagrams, Complexity figures, Active Inference figures, Quantum figures, Security figures, and Fluid-S figures) required by the manuscript.

## 📋 Best Practices

- **No Mocks**: All scripts must execute real methods with real data.
- **Thin Design**: If a script starts growing complex mathematical or domain logic, that logic must be refactored into `projects/cognitive_case_diagrams/src/`.
- **Idempotency**: Scripts should cleanly overwrite previous outputs in `projects/cognitive_case_diagrams/output/` without side effects.
