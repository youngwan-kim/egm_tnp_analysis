from libPython.tnpClassUtils import tnpSample

AFB={
    'data2016' : tnpSample('data2016','/gv0/Users/hsseo/EgammaTnP/2016/data/SingleElectron'),
    'mg2016' : tnpSample('mg2016','/gv0/Users/hsseo/EgammaTnP/2016/mc',isMC=True),
    'data2017' : tnpSample('data2017','/gv0/Users/hsseo/EgammaTnP/2017/data/SingleElectron'),
    'mg2017' : tnpSample('mg2017','/gv0/Users/hsseo/EgammaTnP/2017/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',isMC=True),
    'amc2017' : tnpSample('amc2017','/gv0/Users/hsseo/EgammaTnP/2017/mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',isMC=True),
    'data2018' : tnpSample('data2018','/gv0/Users/hsseo/EgammaTnP/2018/data/EGamma'),
    'mg2018' : tnpSample('mg2018','/gv0/Users/hsseo/EgammaTnP/2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',isMC=True),
    'amc2018' : tnpSample('amc2018','/gv0/Users/hsseo/EgammaTnP/2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',isMC=True),
}
AFBMuon={
    'data2018' : tnpSample('data2018','/gv0/Users/hsseo/MuonTnP/2018/data/SingleMuon',massName='mass'),
    'mg2018' : tnpSample('mg2018','/gv0/Users/hsseo/MuonTnP/2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',massName='mass',isMC=True),
    'amc2018' : tnpSample('amc2018','/gv0/Users/hsseo/MuonTnP/2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',massName='mass',isMC=True),
}

#Data2018_102X = {
#    ### MiniAOD TnP for IDs scale 
#    'DY_madgraph_100X_part012' : tnpSample('DY_madgraph_100X_part012', 
#                                       eos2018Data_102X + 'mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-AOD-100X_part012.root',
#                                       isMC = True, nEvts =  -1 ),
#
#    'DY_powheg_102X_part01' : tnpSample('DY_powheg_102X_part01', 
#                                       eos2018Data_102X + 'mc/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8-AOD-102X_part01.root',
#                                       isMC = True, nEvts =  -1 ),
#
#
#    'data_Run2018Av123' : tnpSample('data_Run2018Av123' , eos2018Data_102X + 'data/Prompt2018_RunA_v13.root' , lumi = 13.53),  # LIVIA: 22/9: for some reason do not manage to run on RunAv2
#
#    'data_Run2018Bv12' : tnpSample('data_Run2018Bv12' , eos2018Data_102X + 'data/Prompt2018_RunB_v12.root' , lumi = 6.78),
#
#    'data_Run2018Cv12' : tnpSample('data_Run2018Cv12' , eos2018Data_102X + 'data/Prompt2018_RunC_v12.root' , lumi = 6.61),
#
#    'data_Run2018Dv2' : tnpSample('data_Run2018Dv2' , eos2018Data_102X + 'data/Prompt2018_RunD_v2.root' , lumi = 12.78), # LIVIA: 22/9: lumi to be verified
#
#
#    }
#


##about lumi: thse ntuples are done with /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-321221_13TeV_PromptReco_Collisions18_JSON.txt = with recorded luminosity : 31.71 /fb but ~20% are crashed. Also we need to update the single runs lumi


 
