# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

FROM librecores/ci:2021.5-rc1
RUN pip install -U fusesoc edalize eda-container-wrapper
COPY entrypoint.py /tmp/entrypoint.py
ENTRYPOINT [ "/tmp/entrypoint.py" ]

