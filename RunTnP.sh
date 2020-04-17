#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
    echo "usage: $0 CONFIGFILE FLAG [NCORE=60] [NMAX=100]"
    echo "example: $0 etc/config/AFBElectronID2017.py MediumID_QPlus 50"
    exit 1
fi
CONFIGFILE=$1
FLAG=$2
NCORE=${3:-60}
NMAX=${4:-100}
WAITLIST1=()
WAITLIST2=()

echo "createBins"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --createBins || exit 1

echo "createHists"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --createHists -n $NCORE --nmax $NMAX || exit 1

echo "doFit"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --mcSig --altSig -n $NCORE --nmax $NMAX &
WAITLIST1+=($!)

python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit -n $NCORE --nmax $NMAX &
WAITLIST2+=($!)

python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --altBkg -n $NCORE --nmax $NMAX &
WAITLIST2+=($!)

wait ${WAITLIST1[@]}
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --altSig -n $NCORE --nmax $NMAX || exit 1
wait ${WAITLIST2[@]}

echo "sumUp"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --sumUp || exit 1
