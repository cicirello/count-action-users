# Copyright (c) 2021-2025 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License.

FROM ghcr.io/cicirello/pyaction:3.13.6-gh-2.76.2

COPY ActionUserCounter.py /ActionUserCounter.py
ENTRYPOINT ["/ActionUserCounter.py"]
