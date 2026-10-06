"""يسمح بالتشغيل عبر: python3 -m lsnprog"""
from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
