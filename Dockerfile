# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

FROM librecores/ci:2021.5-rc1
ADD requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt
COPY entrypoint.py /tmp/entrypoint.py
ENTRYPOINT [ "/tmp/entrypoint.py" ]

