# Copyright (c) 2021 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License.

FROM ghcr.io/cicirello/pyaction:4.9.0

COPY ActionUserCounter.py /ActionUserCounter.py
ENTRYPOINT ["/ActionUserCounter.py"]
