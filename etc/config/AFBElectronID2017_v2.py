from AFBElectronCommon import *
import etc.inputs.tnpSampleDef as tnpSamples
samplesDef = {
    'data'   : tnpSamples.AFB['data2017_official'].clone(),
    'mcNom'  : tnpSamples.AFB['amc2017_official'].clone(),
    'mcAlt'  : tnpSamples.AFB['mg2017_official'].clone(),
    'tagSel' : tnpSamples.AFB['amc2017_official'].clone(),
}
samplesDef['tagSel'].rename('mcAltSel_'+samplesDef['tagSel'].name)
samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

baseOutDir = 'results/AFBElectronID2017_v2/'
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
    'MediumID_QPlus' : '(passingCutBasedMedium94XV2 == 1)',
    'MediumID_QMinus' : '(passingCutBasedMedium94XV2 == 1)',
    'TightID_QPlus'  : '(passingCutBasedTight94XV2  == 1)',
    'TightID_QMinus'  : '(passingCutBasedTight94XV2  == 1)',
    'TightID_Selective_QPlus'  : '(passingCutBasedTight94XV2  == 1 && el_3charge)',
    'TightID_Selective_QMinus'  : '(passingCutBasedTight94XV2  == 1 && el_3charge)',
}
