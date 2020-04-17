from AFBElectronCommon import *
import etc.inputs.tnpSampleDef as tnpSamples
samplesDef = {
    'data'   : tnpSamples.AFB['data2018'].clone(),
    'mcNom'  : tnpSamples.AFB['mg2018'].clone(),
    'mcAlt'  : tnpSamples.AFB['amc2018'].clone(),
    'tagSel' : tnpSamples.AFB['mg2018'].clone(),
}
samplesDef['tagSel'].rename('mcAltSel_'+samplesDef['tagSel'].name)
samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

baseOutDir = 'results/AFBElectronID2018_v1/'
tnpTreeDir = 'tnpEleIDs'
cutBase   = 'tag_Ele_pt > 34 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'MediumID_QPlus' : 'el_q > 0',
    'MediumID_QMinus' : 'el_q < 0',
    'TightID_QPlus' : 'el_q > 0',
    'TightID_QMinus' : 'el_q < 0',
    'TightID_Selective_QPlus' : 'el_q > 0',
    'TightID_Selective_QMinus' : 'el_q < 0',
}
flags = {
    'MediumID_QPlus' : '(passingMedium94XV2 == 1)',
    'MediumID_QMinus' : '(passingMedium94XV2 == 1)',
    'TightID_QPlus'  : '(passingTight94XV2  == 1)',
    'TightID_QMinus'  : '(passingTight94XV2  == 1)',
    'TightID_Selective_QPlus'  : '(passingTight94XV2  == 1 && el_3charge)',
    'TightID_Selective_QMinus'  : '(passingTight94XV2  == 1 && el_3charge)',
}
