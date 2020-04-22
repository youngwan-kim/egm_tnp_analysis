from AFBElectronCommon import *
import etc.inputs.tnpSampleDef as tnpSamples
samplesDef = {
    'data'   : tnpSamples.AFB['data2017_official_L1matched'].clone(),
    'mcNom'  : tnpSamples.AFB['mg2017_official_L1matched'].clone(),
    'mcAlt'  : tnpSamples.AFB['amc2017_official_L1matched'].clone(),
    'tagSel' : tnpSamples.AFB['mg2017_official_L1matched'].clone(),
}
samplesDef['tagSel'].rename('mcAltSel_'+samplesDef['tagSel'].name)
samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

baseOutDir = 'results/AFBElectronTrigger2017_v1_3/'
tnpTreeDir = 'tnpEleTrig'
cutBase   = 'tag_Ele_pt > 34 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0'
additionalCutBase = {
    'Ele35_MediumID_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele35_MediumID_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele32_MediumID_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele32_MediumID_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele23Leg1_MediumID_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele23Leg1_MediumID_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele12Leg2_MediumID_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedMedium94XV2 == 1',
    'Ele12Leg2_MediumID_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedMedium94XV2 == 1',
    'Ele35_TightID_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele35_TightID_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele32_TightID_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele32_TightID_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele23Leg1_TightID_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele23Leg1_TightID_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele12Leg2_TightID_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedTight94XV2 == 1',
    'Ele12Leg2_TightID_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedTight94XV2 == 1',
    'Ele35_TightID_Selective_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele35_TightID_Selective_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele32_TightID_Selective_QPlus' : 'el_pt > 30 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele32_TightID_Selective_QMinus' : 'el_pt > 30 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele23Leg1_TightID_Selective_QPlus' : 'el_pt > 20 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele23Leg1_TightID_Selective_QMinus' : 'el_pt > 20 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele12Leg2_TightID_Selective_QPlus' : 'el_pt > 10 && el_q > 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
    'Ele12Leg2_TightID_Selective_QMinus' : 'el_pt > 10 && el_q < 0 && passingCutBasedTight94XV2 == 1 && el_3charge',
}
flags = {
#    'Ele35_MediumID_QPlus' : '(passingHLT35 == 1)',
#    'Ele35_MediumID_QMinus' : '(passingHLT35 == 1)',
    'Ele32_MediumID_QPlus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele32_MediumID_QMinus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele23Leg1_MediumID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_MediumID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_MediumID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_MediumID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
#    'Ele35_TightID_QPlus' : '(passingHLT35 == 1)',
#    'Ele35_TightID_QMinus' : '(passingHLT35 == 1)',
    'Ele32_TightID_QPlus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele32_TightID_QMinus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele23Leg1_TightID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_TightID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_TightID_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_TightID_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
#    'Ele35_TightID_Selective_QPlus' : '(passingHLT35 == 1)',
#    'Ele35_TightID_Selective_QMinus' : '(passingHLT35 == 1)',
    'Ele32_TightID_Selective_QPlus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele32_TightID_Selective_QMinus' : '(passHltEle32DoubleEGWPTightGsf == 1)',
    'Ele23Leg1_TightID_Selective_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele23Leg1_TightID_Selective_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)',
    'Ele12Leg2_TightID_Selective_QPlus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
    'Ele12Leg2_TightID_Selective_QMinus' : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2 == 1)',
}
