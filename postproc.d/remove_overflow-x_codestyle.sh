#!/bin/bash

set -x

sed -i 's/overflow-x: auto;//' "$1"
