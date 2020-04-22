from AFBElectronCommon import *
import etc.inputs.tnpSampleDef as tnpSamples
samplesDef = {
    'data'   : tnpSamples.AFB['data2016_official_L1matched'].clone(),
    'mcNom'  : tnpSamples.AFB['mg2016_official_L1matched'].clone(),
    'mcAlt'  : tnpSamples.AFB['amc2016_official_L1matched'].clone(),
    'tagSel' : tnpSamples.AFB['mg2016_official_L1matched'].clone(),
}
samplesDef['tagSel'].rename('mcAltSel_'+samplesDef['tagSel'].name)
samplesDef['tagSel'].set_cut('tag_Ele_pt > 35')

baseOutDir = 'results/AFBElectronTrigger2016_v1_3/'
tnpTreeDir = 'tnpEleTrig'
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'Ele27_MediumID_QPlus' : 'el_pt > 25 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele27_MediumID_QMinus' : 'el_pt > 25 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele23Leg1_MediumID_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele23Leg1_MediumID_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele12Leg2_MediumID_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele12Leg2_MediumID_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele27_TightID_QPlus' : 'el_pt > 25 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele27_TightID_QMinus' : 'el_pt > 25 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele23Leg1_TightID_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele23Leg1_TightID_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele12Leg2_TightID_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele12Leg2_TightID_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele27_TightID_Selective_QPlus' : 'el_pt > 25 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele27_TightID_Selective_QMinus' : 'el_pt > 25 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele23Leg1_TightID_Selective_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele23Leg1_TightID_Selective_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele12Leg2_TightID_Selective_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele12Leg2_TightID_Selective_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
}
flags = {
    'Ele27_MediumID_QPlus' : '(passHltEle27WPTightGsf == 1)',
    'Ele27_MediumID_QMinus' : '(passHltEle27WPTightGsf == 1)',
    'Ele23Leg1_MediumID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_MediumID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_MediumID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_MediumID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele27_TightID_QPlus' : '(passHltEle27WPTightGsf == 1)',
    'Ele27_TightID_QMinus' : '(passHltEle27WPTightGsf == 1)',
    'Ele23Leg1_TightID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_TightID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_TightID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_TightID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele27_TightID_Selective_QPlus' : '(passHltEle27WPTightGsf == 1)',
    'Ele27_TightID_Selective_QMinus' : '(passHltEle27WPTightGsf == 1)',
    'Ele23Leg1_TightID_Selective_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_TightID_Selective_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_TightID_Selective_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_TightID_Selective_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
}
