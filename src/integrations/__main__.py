"""Run the MCP stdio server: ``python -m src.integrations``."""

import sys

from .server import main

if __name__ == "__main__":
    sys.exit(main())
