# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

FROM librecores/ci:2020.6-rc2
# TODO: This is the branch where I test integration of FuseSoC into Python
# Needed later, but now not usable as edalized tools always print to C stdout
# RUN pip3 install git+https://github.com/wallento/fusesoc@integration
COPY entrypoint.py /tmp/entrypoint.py
ENTRYPOINT [ "/tmp/entrypoint.py" ]
