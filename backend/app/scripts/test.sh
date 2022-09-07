#!/usr/bin/env bash
set -e
set -x

pytest --cov=app app/tests "${@}"
