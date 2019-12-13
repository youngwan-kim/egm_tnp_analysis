from AFBElectronCommon import *
from AFBElectron2018Common import *
baseOutDir = 'results/AFBElectronTrigger2018/'
tnpTreeDir = 'tnpEleTrig'
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'MediumID_Ele32_QPlus' : 'el_pt > 30 && el_q > 0 && passingMedium94XV2 == 1',
    'MediumID_Ele23_QPlus' : 'el_pt > 20 && el_q > 0 && passingMedium94XV2 == 1',
    'MediumID_Ele12_QPlus' : 'el_pt > 10 && el_q > 0 && passingMedium94XV2 == 1',
    'MediumID_Ele32_QMinus' : 'el_pt > 30 && el_q < 0 && passingMedium94XV2 == 1',
    'MediumID_Ele23_QMinus' : 'el_pt > 20 && el_q < 0 && passingMedium94XV2 == 1',
    'MediumID_Ele12_QMinus' : 'el_pt > 10 && el_q < 0 && passingMedium94XV2 == 1',
    'TightID_Selective_Ele32_QPlus' : 'el_pt > 30 && el_q > 0 && passingTight94XV2 == 1 && el_3charge',
    'TightID_Selective_Ele23_QPlus' : 'el_pt > 20 && el_q > 0 && passingTight94XV2 == 1 && el_3charge',
    'TightID_Selective_Ele12_QPlus' : 'el_pt > 10 && el_q > 0 && passingTight94XV2 == 1 && el_3charge',
    'TightID_Selective_Ele32_QMinus' : 'el_pt > 30 && el_q < 0 && passingTight94XV2 == 1 && el_3charge',
    'TightID_Selective_Ele23_QMinus' : 'el_pt > 20 && el_q < 0 && passingTight94XV2 == 1 && el_3charge',
    'TightID_Selective_Ele12_QMinus' : 'el_pt > 10 && el_q < 0 && passingTight94XV2 == 1 && el_3charge',
}
flags = {
    'MediumID_Ele32_QPlus' : '(passHltEle32WPTightGsf == 1)',
    'MediumID_Ele23_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1 == 1)',
    'MediumID_Ele12_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'MediumID_Ele32_QMinus' : '(passHltEle32WPTightGsf == 1)',
    'MediumID_Ele23_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1 == 1)',
    'MediumID_Ele12_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'TightID_Selective_Ele32_QPlus' : '(passHltEle32WPTightGsf == 1)',
    'TightID_Selective_Ele23_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1 == 1)',
    'TightID_Selective_Ele12_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'TightID_Selective_Ele32_QMinus' : '(passHltEle32WPTightGsf == 1)',
    'TightID_Selective_Ele23_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1 == 1)',
    'TightID_Selective_Ele12_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
}
