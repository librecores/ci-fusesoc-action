# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 python3-pip python-is-python3 git docker.io
RUN pip install fusesoc eda-container-wrapper
COPY entrypoint.py /tmp/entrypoint.py
ENTRYPOINT [ "/tmp/entrypoint.py" ]

