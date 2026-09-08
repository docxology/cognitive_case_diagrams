# Test agent guidance

Follow [project guidance](../AGENTS.md). Run tests through uv in the project environment, not a bare pytest shim. Use analytic numerical examples and fixed RNG seeds, real temporary files, real local services when needed, and real subprocesses. `unittest.mock`, `MagicMock`, and patch fixtures are prohibited.

Do not reduce the 90% combined line-and-branch floor or omit implementation code to make a gate pass. Reproduce changed behavior with a failing counterexample before fixing it. Test the negative boundary of validators as well as valid inputs. A naming claim (Morita, Bellman, Bethe, quantum, security) is not itself a testable mathematical contract.

Coverage artifacts and runtime caches are derived, local-only outputs. If environment or storage errors occur, isolate caches and report the actual failure instead of changing scientific code to accommodate them. See [test guide](README.md). No authored test subfolders currently require additional documentation.
