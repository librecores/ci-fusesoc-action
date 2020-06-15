# Copyright 2020, LibreCores CI contributors
# SPDX-License-Identifier: MIT

FROM librecores/ci:2020.6-rc1
COPY entrypoint.py /tmp/entrypoint.py
ENTRYPOINT [ "/tmp/entrypoint.py" ]
