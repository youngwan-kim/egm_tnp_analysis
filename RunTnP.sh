#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
    echo "usage: $0 CONFIGFILE FLAG [NCORE=10]"
    echo "example: $0 etc/config/2017ID.py passingMedium 50"
    exit 1
fi
CONFIGFILE=$1
FLAG=$2
NCORE=${3:-60}
WAITLIST1=()
WAITLIST2=()

echo "createBins"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --createBins || exit 1

echo "createHists"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --createHists -n $NCORE || exit 1

echo "doFit"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --mcSig --altSig -n $NCORE &
WAITLIST1+=($!)
sleep 60
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit -n $NCORE &
WAITLIST2+=($!)
sleep 60
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --altBkg -n $NCORE &
WAITLIST2+=($!)
sleep 60
wait ${WAITLIST1[@]}
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --doFit --altSig -n $NCORE || exit 1
wait ${WAITLIST2[@]}

echo "sumUp"
python tnpEGM_fitter.py $CONFIGFILE --flag $FLAG --sumUp || exit 1
