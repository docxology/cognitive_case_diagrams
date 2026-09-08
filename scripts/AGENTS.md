# Script agent notes

Follow [project guidance](../AGENTS.md). Keep entry points thin: imports, argument parsing, calls to source functions, and explicit reporting. Do not suppress generator errors or claim partial output as complete. Canonical figure dispatch records per-domain failures and updates the registry with file hashes. Scripts may import source helpers; do not copy algorithms here.

Read [command inventory](README.md). Use project-local manuscript substitution consistently in standalone and template contexts. After changing script behavior, run the relevant real-subprocess tests and full quality gate, then regenerate and validate artifacts. No content subfolders are present; caches and generated output are excluded.
