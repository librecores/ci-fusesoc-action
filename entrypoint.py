#!/usr/bin/env python3

import subprocess
import sys, os

from fusesoc.main import main


if __name__ == "__main__":
  args  = ["fusesoc", "--cores-root", "."]
  args += [os.environ.get("INPUT_FLOW")]
  if "INPUT_TARGET" in os.environ:
    args += ["--target", os.environ.get("INPUT_TARGET")]
  if "INPUT_TOOL" in os.environ:
    args += ["--tool", os.environ.get("INPUT_TOOL")]
  args += [os.environ.get("INPUT_CORE")]

  if "INPUT_PRE-RUN-COMMAND" in os.environ:
    subprocess.call(os.environ.get("INPUT_PRE-RUN-COMMAND"), shell=True)
  sys.argv = args
  exit(main())
