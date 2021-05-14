#!/usr/bin/env python3
# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

from fusesoc.main import parse_args, fusesoc
import subprocess
import sys, os, re
import tempfile
from uuid import uuid4

def get_arguments():
  arguments = {}
  supported = ["tool", "libraries", "pre-run-command", "arguments", "target", "run-arguments", "core", "core-arguments", "path"]
  for arg in supported:
    v = os.getenv(f"INPUT_{arg.upper()}")
    v = None if v and len(v) == 0 else v
    arguments[arg] = v

  # some post-processing
  arguments["libraries"] = arguments["libraries"].split(",") if arguments["libraries"] else []
  arguments["path"] = arguments["path"] if arguments["path"] else os.getenv("GITHUB_REPOSITORY").split("/")[1]

  return arguments


if __name__ == "__main__":
  arguments = get_arguments()
  if arguments["pre-run-command"]:
    ret = subprocess.run(arguments["pre-run-command"], shell=True)
    if ret.returncode != 0:
      exit(ret.returncode)

  _, logfile = tempfile.mkstemp(suffix=".log")

  for lib in arguments["libraries"]:
    args = parse_args(["library", "add", str(uuid4()), lib])
    fusesoc(args)

  args = ["fusesoc"]
  if arguments["arguments"]:
    args += ["--log-file", logfile] + arguments["arguments"].split(" ")
  else:
    args += ["--cores-root", "."]
    args += ["--log-file", logfile]
    args += ["run"]
    if arguments["target"]:
      args += ["--target", arguments["target"]]
    if arguments["tool"]:
      args += ["--tool", arguments["tool"]]
    if arguments["run-arguments"]:
      args += arguments["run-arguments"].split(" ")
    args += [arguments["core"]]
    if arguments["core-arguments"]:
      args += arguments["core-arguments"].split(" ")

  runner_path = os.path.join(os.getenv('RUNNER_WORKSPACE'), arguments["path"])
  os.putenv("EDALIZE_LAUNCHER", f"eda-container-wrapper --split-cwd-tail=1 --cwd-base {runner_path}:/github/workspace --non-interactive {arguments['tool']} --")

  ret = subprocess.run(" ".join(args), shell=True, capture_output=True)
  stdout = ret.stdout
  stderr = ret.stderr
  rc = ret.returncode

  print("=== log:")
  with open(logfile) as f:
    print("".join(f.readlines()))

  if arguments["target"] == "lint" and arguments["tool"] == "verilator":
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
