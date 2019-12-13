from AFBElectronCommon import *
from AFBElectron2018Common import *
baseOutDir = 'results/AFBElectronID2018/'
tnpTreeDir = 'tnpEleIDs'
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'MediumID_QPlus' : 'el_q > 0',
    'MediumID_QMinus' : 'el_q < 0',
    'TightID_Selective_QPlus' : 'el_q > 0',
    'TightID_Selective_QMinus' : 'el_q < 0',
}
flags = {
    'MediumID_QPlus' : '(passingMedium94XV2 == 1)',
    'MediumID_QMinus' : '(passingMedium94XV2 == 1)',
    'TightID_Selective_QMinus'  : '(passingTight94XV2  == 1 && el_3charge)',
    'TightID_Selective_QPlus'  : '(passingTight94XV2  == 1 && el_3charge)',
}
