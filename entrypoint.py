#!/usr/bin/env python3
# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

import subprocess
import sys, os

if __name__ == "__main__":
  if "INPUT_PRE-RUN-COMMAND" in os.environ:
    subprocess.call(os.environ.get("INPUT_PRE-RUN-COMMAND"), shell=True)

  from fusesoc.main import main
  from fusesoc.version import version
  print("::debug::FuseSoC version: {}".format(version))

  if "INPUT_ARGUMENTS" in os.environ:
    args = os.environ.get("INPUT_ARGUMENTS").split(" ")
  else:
    args  = ["--cores-root", "."]
    args += [os.environ.get("INPUT_FLOW")]
    if "INPUT_TARGET" in os.environ:
      args += ["--target", os.environ.get("INPUT_TARGET")]
    if "INPUT_TOOL" in os.environ:
      args += ["--tool", os.environ.get("INPUT_TOOL")]
    args += [os.environ.get("INPUT_CORE")]

  exit(main(args))
