#!/bin/bash

echo "$@"
echo $TNP_BASE
cd $TNP_BASE
python tnpEGM_fitter.py "$@"
