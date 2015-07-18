#!/bin/bash

set -x

linkname=${1##*/}
linkname=${linkname%.html}

sed -i "/class=\"header\".\+${linkname}/s/\(<.*>\)/<span class=\"semibold\">\1<\/span>/" "$1"
