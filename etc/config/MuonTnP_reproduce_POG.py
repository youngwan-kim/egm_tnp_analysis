from libPython.tnpClassUtils import tnpSample
#############################################################
########## Setting
############################################################# 

#### Choose one of these ####################
#Period = {'2016BF', '2016GH', '2017', '2018' }
#Measure = {'IsoMu24' }
#Binnings = {'eta', 'phi', 'pt', 'nVertices', 'pteta'}

Period = '2018' 
Measure = 'IsoMu24'
Binnings = 'pt'

#############################################################
########## General Settings (default = '2017', 'Mu17', 'all')
#############################################################

baseOutDir = 'POG_reproduces_'+Period+'_'+Measure+'_'+Binnings+'/'

eventexp = 'tag_IsoMu27==1 && tag_pt > 29 && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.15 && Tight2012 && combRelIsoPF04dBeta < 0.15'
eventexpMC = '(tag_IsoMu27==1 && tag_pt > 29 && mcTrue && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.15 && Tight2012 && combRelIsoPF04dBeta < 0.15) * weight'

wonjuntnpdir = '/data9/Users/wonjun/public/CRABDIR/'
filename = 'TnPTreeZ_17Nov2017_SingleMuon_Run2017BCDEFv1_GoldenJSON.root'
filenameMC = 'TnPTreeZ_94X_DYJetsToLL_M50_Madgraph_WithWeights.root'

#### Measure Option ########################################################
passcondition = 'IsoMu27'
if Period == '2018' :
    passcondition = 'IsoMu24'
else :
    passcondition = 'IsoMu24 || IsoTkMu24'
if Measure == 'IDISO':
  passcondition = 'Tight2012 && combRelIsoPF04dBeta < 0.15'
  eventexp = eventexp.replace('Tight2012 && combRelIsoPF04dBeta < 0.15', 'TM')
  eventexpMC = eventexpMC.replace('Tight2012 && combRelIsoPF04dBeta < 0.15', 'TM')

#### Period Option ########################################################
if Period == "2016BF" :
  eventexp = eventexp.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  eventexpMC = eventexpMC.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  wonjuntnpdir = '/data9/Users/wonjun/public/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016/'
  filename = 'TnPTreeZ_LegacyRereco07Aug17_SingleMuon_BCDEF.root'
  filenameMC = 'DY_Summer16PremixMoriond_weighted_BCDEF.root'
elif Period == "2016GH" :
  eventexp = eventexp.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  eventexpMC = eventexpMC.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  wonjuntnpdir = '/data9/Users/wonjun/public/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016/'
  filename = 'TnPTreeZ_LegacyRereco07Aug17_SingleMuon_GH.root'
  filenameMC = 'DY_Summer16PremixMoriond_weighted_GH.root'
elif Period == "2018" :
  eventexp = eventexp.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  eventexpMC = eventexpMC.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  wonjuntnpdir = '/data9/Users/wonjun/public/TnPTreeZ_EarlyRereco_PromptReco_17Sep2018_SingleMuon_Run2018/'
  filename = 'TnPTreeZ_17Sep2018_SingleMuon_Run2018ABCD_GoldenJSON.root'
  filenameMC = 'TnPTreeZ_102XAutumn18_DYJetsToLL_M50_MadgraphMLM_weighted_ABCD.root'

#############################################################
########## Binning Definition  [can be nD bining]
#############################################################
ptmin = 26.
if Period == '2017':
  ptmin = 29.

## 'eta'
if Binnings == 'eta':
  biningDef = [
    { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4]  },
    { 'var' : 'pt' , 'type': 'float', 'bins': [ptmin, 1200.]  },
  ]
## 'pt'
elif Binnings == 'pt':
  biningDef = [
    { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, 2.4]  },
    { 'var' : 'pt' , 'type': 'float', 'bins': [2., 22., 25., 27., 29., 32., 40., 50., 60., 120., 200., 300., 500., 700., 1200.,]  },
  ]
  if Period != '2017':
    biningDef = [
      { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, 2.4]  },
      { 'var' : 'pt' , 'type': 'float', 'bins': [2., 18., 22., 24., 26., 30., 40., 50., 60., 120., 200., 300., 500., 700., 1200.,]  },
    ]
## 'phi'
elif Binnings == 'phi':
  pi = 3.141592
  degree15 = pi/12
  biningDef = [
    { 'var' : 'phi' , 'type': 'float', 'bins': [(-1)*degree15*12, (-1)*degree15*11, (-1)*degree15*9, (-1)*degree15*7, (-1)*degree15*5, (-1)*degree15*3, (-1)*degree15*1, degree15*1, degree15*3, degree15*5, degree15*7, degree15*9, degree15*11, degree15*12]  },
    { 'var' : 'pt' , 'type': 'float', 'bins': [ptmin, 1200.]  },
  ]
## 'nVertices'
elif Binnings == 'nVertices':
  biningDef = [
    { 'var' : 'tag_nVertices' , 'type': 'float', 'bins': [0.5, 2.5, 4.5, 6.5, 8.5, 10.5, 12.5, 14.5, 16.5, 18.5, 20.5, 22.5, 24.5, 26.5, 28.5, 30.5, 32.5, 34.5, 36.5, 38.5, 40.5, 42.5, 44.5, 46.5, 48.5, 50.5, 52.5, 54.5, 56.5, 58.5, 60.5]  },
    { 'var' : 'pt' , 'type': 'float', 'bins': [ptmin, 1200.]  },
  ]
## 'pteta'
else:
  biningDef = [
    { 'var' : 'abseta' , 'type': 'float', 'bins': [.0, 0.9, 1.2, 2.1, 2.4]  },
    { 'var' : 'pt' , 'type': 'float', 'bins': [26., 30., 40., 50., 60., 120., 200., 300., 1200.,]  },
  ]
  if Period != '2017':
    biningDef = [
      { 'var' : 'abseta' , 'type': 'float', 'bins': [.0, 0.9, 1.2, 2.1, 2.4]  },
      { 'var' : 'pt' , 'type': 'float', 'bins': [29., 32., 40., 50., 60., 120., 200., 300., 1200.,]  },
    ]

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanGaussP[0.0, -5.0,5.0]","sigmaGaussP[0.8, 0.5,2.5]",  ## [0.5, 0.4,5.0]
    "meanGaussF[0.0, -5.0,5.0]","sigmaGaussF[0.7, 0.5,2.5]", ## [0.5, 0.4,5.0]
    "aExpoP[-0.1, -1,0.1]",
    "aExpoF[-0.1, -1,0.1]",
    "Gaussian::sigResPass(mass,meanGaussP,sigmaGaussP)",
    "Gaussian::sigResFail(mass,meanGaussF,sigmaGaussF)",
    "Exponential::backgroundPass(mass, aExpoP)",
    "Exponential::backgroundFail(mass, aExpoF)",
    ]
tnpParNomFit2 = [
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.4,6.0]" ,"aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]',
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.4,15.0]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]',
    "aExpoP[-0.1, -1,0.1]",
    "aExpoF[-0.1, -1,0.1]",
    "RooCBShape::sigResPass(mass,meanCBP,sigmaCBP,aCBP,nCBP)",
    "RooCBShape::sigResFail(mass,meanCBF,sigmaCBF,aCBF,nCBF)",
    "Exponential::backgroundPass(mass, aExpoP)",
    "Exponential::backgroundFail(mass, aExpoF)",
    ]

tnpParAltBkgFit = [
    "meanGaussP[0.0, -5.0,5.0]","sigmaGaussP[0.8, 0.5,2.5]",
    "meanGaussF[0.0, -5.0,5.0]","sigmaGaussF[1.2, 0.55,2.5]",
    "aCMSP[60., 50.,80.]","bCMSP[0.05, 0.01,0.08]","cCMSP[0.1, 0, 1]","peakCMSP[90.0]",
    "aCMSF[60., 50.,80.]","bCMSF[0.05, 0.01,0.08]","cCMSF[0.1, 0, 1]","peakCMSF[90.0]",
    "Gaussian::sigResPass(mass,meanGaussP,sigmaGaussP)",
    "Gaussian::sigResFail(mass,meanGaussF,sigmaGaussF)",
    "RooCMSShape::backgroundPass(mass, aCMSP, bCMSP, cCMSP, peakCMSP)",
    "RooCMSShape::backgroundFail(mass, aCMSF, bCMSF, cCMSF, peakCMSF)",
    ]
     
tnpParAltSigFit = [
    #"meanP[0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",  ## These are used at CBExGaussShape funtion
    #"meanF[0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"aCMSP[60.,50.,75.]","bCMSP[0.04,0.01,0.06]","cCMSP[0.1, 0.005, 1]","peakCMSP[90.0]",                                     ## These are used at CMS function
    #"aCMSF[60.,50.,75.]","bCMSF[0.04,0.01,0.06]","cCMSF[0.1, 0.005, 1]","peakCMSF[90.0]",
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.4,6.0]" ,"aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]',
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.4,15.0]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]',
    "aExpoP[-0.1, -1,0.1]",
    "aExpoF[-0.1, -1,0.1]",
    "Exponential::backgroundPass(mass, aExpoP)",
    "Exponential::backgroundFail(mass, aExpoF)",
    ]
tnpParAltSigFit2 = [
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.4,6.0]" ,"aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]',
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.4,15.0]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]',
    "aCMSP[60., 50.,80.]","bCMSP[0.05, 0.01,0.08]","cCMSP[0.1, 0, 1]","peakCMSP[90.0]",
    "aCMSF[60., 50.,80.]","bCMSF[0.05, 0.01,0.08]","cCMSF[0.1, 0, 1]","peakCMSF[90.0]",
    "RooCMSShape::backgroundPass(mass, aCMSP, bCMSP, cCMSP, peakCMSP)",
    "RooCMSShape::backgroundFail(mass, aCMSF, bCMSF, cCMSF, peakCMSF)",
    ]

#############################################################
########## Setting Systematic
#############################################################

flags = {
    'data'              : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,40,70,130),
    'data_altsig'       : tnpSample([wonjuntnpdir+filename],eventexp,tnpParAltSigFit,40,70,130), ### This should be done after mc_altsig
    'data_mass60130'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,40,60,130),
    'data_mass70120'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,40,70,120),
    'data_massbin30'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,30,70,130),
    'data_massbin50'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,50,70,130),
    'data_tagiso010'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),tnpParNomFit,40,70,130),
    'data_tagiso020'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),tnpParNomFit,40,70,130),
    #'data_altbkd'       : tnpSample([wonjuntnpdir+filename],eventexp,tnpParAltBkgFit,40,70,130),

    'mc'                : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,130),  ## For MC, used tnpParAltBkgFit instead of tnpParNomFit 
    'mc_altsig'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltSigFit2,40,70,130), ## because CMS for background can be exactly zero, but Exponential can't be....?
    'mc_mass60130'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,60,130),
    'mc_mass70120'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,120),
    'mc_massbin30'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,30,70,130),
    'mc_massbin50'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,50,70,130),
    'mc_tagiso010'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),tnpParAltBkgFit,40,70,130),
    'mc_tagiso020'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),tnpParAltBkgFit,40,70,130),
    #'mc_altbkd'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,130),
}

systematicDef = {
    'data' : [['data_mass60130','data_mass70120'],['data_massbin30','data_massbin50'],['data_tagiso010','data_tagiso020'], ['data_altsig']], #['data_altbkd']
    'mc' :   [['mc_mass60130','mc_mass70120'],    ['mc_massbin30','mc_massbin50'],    ['mc_tagiso010','mc_tagiso020'],     ['mc_altsig']]    # ['mc_altbkd']
}

#############################################################
########## Cuts definition for all samples
#############################################################

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#### or remove any additional cut (default)
additionalCuts = None

