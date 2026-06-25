# Copyright (c) 2021-2025 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License.

FROM ghcr.io/cicirello/pyaction:3.14.5-gh-2.94.0

COPY ActionUserCounter.py /ActionUserCounter.py
ENTRYPOINT ["/ActionUserCounter.py"]
