#!/usr/bin/env bash

set -x

mypy
black app --check
isort --check-only app
