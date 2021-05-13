#!/usr/bin/env python3
# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

import subprocess
import sys, os, re
import tempfile
from uuid import uuid4

# Handle that envvars are always there, but empty
def env_get(id):
  v = os.getenv(id, default='')
  if v and len(v) == 0:
    return None
  return v

if __name__ == "__main__":
  if env_get("INPUT_PRE-RUN-COMMAND"):
    ret = subprocess.run(env_get("INPUT_PRE-RUN-COMMAND"), shell=True)
    if ret.returncode != 0:
      exit(ret.returncode)

  _, logfile = tempfile.mkstemp(suffix=".log")

  libs = env_get("INPUT_LIBRARIES")
  if libs:
    for lib in libs.split(","):
      subprocess.call(f"fusesoc library add {uuid4()} {lib}", shell=True)

  args = ["fusesoc"]
  if env_get("INPUT_ARGUMENTS"):
    args += ["--log-file", logfile] + env_get("INPUT_ARGUMENTS").split(" ")
  else:
    args += ["--cores-root", "."]
    args += ["--log-file", logfile]
    args += "run"
    if env_get("INPUT_TARGET"):
      args += ["--target", env_get("INPUT_TARGET")]
    if env_get("INPUT_TOOL"):
      args += ["--tool", os.environ.get("INPUT_TOOL")]
    if env_get("INPUT_COMMAND-ARGUMENTS"):
      args += env_get("INPUT_COMMAND-ARGUMENTS").split(" ")
    args += [env_get("INPUT_CORE")]
    if env_get("INPUT_CORE-ARGUMENTS"):
      args += env_get("INPUT_CORE-ARGUMENTS").split(" ")

  ret = subprocess.run(" ".join(args), shell=True, capture_output=True)
  stdout = ret.stdout
  stderr = ret.stderr
  rc = ret.returncode

  print("=== log:")
  with open(logfile) as f:
    print("".join(f.readlines()))

  if env_get("INPUT_COMMAND") == "run" and env_get("INPUT_TARGET") == "lint" and env_get("INPUT_TOOL") == "verilator":
    rx = re.compile(r"%((Warning|Error)-\w+: \.\./\.\./\.\./(.*?):(\d+):(\d+): (.*?)\\n\s*:([^%]*))")
    for m in rx.finditer(str(stderr)):
      severity = m.group(2).lower()
      msg = m.group(6) + "%0A"
      msg += m.group(7).replace('%', '%25').replace('\\n', '%0A').replace('\\r', '%0D').replace("\\'", "\'")
      print("::{} file={},line={},col={}::{}".format(severity, m.group(3), m.group(4), m.group(5), msg))

  else:
    print("=== stdout:")
    print(str(stdout))
    print("=== stderr:")
    print(str(stderr))

  exit(rc)
