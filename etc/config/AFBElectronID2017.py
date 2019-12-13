from AFBElectronCommon import *
from AFBElectron2017Common import *
baseOutDir = 'results/AFBElectronID2017/'
tnpTreeDir = 'tnpEleIDs'
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'passingMedium_QPlus' : 'el_q > 0',
    'passingTight_QPlus' : 'el_q > 0',
    'passingMedium_QMinus' : 'el_q < 0',
    'passingTight_QMinus' : 'el_q < 0',
}
flags = {
    'passingMedium_QPlus' : '(passingMedium94XV2 == 1)',
    'passingTight_QPlus'  : '(passingTight94XV2  == 1)',
    'passingMedium_QMinus' : '(passingMedium94XV2 == 1)',
    'passingTight_QMinus'  : '(passingTight94XV2  == 1)',
}
