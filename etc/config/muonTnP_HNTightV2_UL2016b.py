from libPython.tnpClassUtils import tnpSample
#############################################################
########## Setting
############################################################# 

#### Choose one of these ####################
#Period = {'2016BF', '2016GH', '2017', '2018' , 'UL2016a', 'UL2016b', 'UL2017', 'UL2018' }
#Measure = {'IDISO', 'Mu17', 'Mu8', 'IsoMu24' }
#Charge = {'+', '-', 'all' }

Period = 'UL2016b'
Measure = 'Mu17'
Charge = ''
IDname = 'HNTightV2'

#############################################################
########## General Settings (default = (default = 'UL2018', 'Mu17', 'all')
#############################################################
baseOutDir = 'HNTightV2/'+Period+'_'+Measure+'/'
passcondition = 'DoubleIsoMu17Mu8_IsoMu17leg || DoubleIsoMu17TkMu8_IsoMu17leg'
eventexp = 'tag_IsoMu27==1 && tag_pt > 29 && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.07 && tag_dB < 0.05 && tag_dzPV > -0.1 && tag_dzPV < 0.1 && tag_SIP < 3 && pair_deltaR > 0.4 && TM'
eventexpMC = '(tag_IsoMu27==1 && tag_pt > 29 && mcTrue && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.07 && tag_dB < 0.05 && tag_dzPV > -0.1 && tag_dzPV < 0.1 && tag_SIP < 3 && pair_deltaR > 0.4 && TM) * weight'

wonjuntnpdir = '/data9/Users/wonjun/public/TnP_Trees/'
filename = 'TnPTreeZ_21Feb2020_UL2016_SingleMuon_Run2016FGHv1.root'
filenameMC = 'TnPTreeZ_106XSummer19_UL16RECO_DYJetsToLL_M50_MadgraphMLM_WithWeights.root'

#### Measure Option ########################################################
if Measure == 'Mu8' :
  passcondition = 'DoubleIsoMu17Mu8_IsoMu8leg || DoubleIsoMu17TkMu8_IsoMu8leg'
elif Measure == 'IsoMu27' :
  passcondition = 'IsoMu27'
elif Measure == 'IsoMu24' :
  if Period == '2018' :
    passcondition = 'IsoMu24'
  else :
    passcondition = 'IsoMu24 || IsoTkMu24'
elif Measure == 'IDISO':
  eventexp = eventexp.replace('pair_deltaR > 0.4 && TM', 'TM')
  eventexpMC = eventexpMC.replace('pair_deltaR > 0.4 && TM', 'TM')
  passcondition = 'Tight2012 && combRelIsoPF04dBeta < 0.07 && dB < 0.05 && dzPV > -0.1 && dzPV < 0.1 && SIP < 3'

#### Charge Option ########################################################
if Charge == "+" :
  eventexp = eventexp.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge > 0')
  eventexpMC = eventexpMC.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge > 0')
elif Charge == "-" :
  eventexp = eventexp.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge < 0')
  eventexpMC = eventexpMC.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge < 0')

############################################################################

if Measure != 'IsoMu24' :
  eventexp = eventexp.replace('tag_IsoMu24==1 && tag_pt > 26', 'tag_IsoMu27==1 && tag_pt > 29')

#############################################################
########## Binning Definition  [can be nD bining]
#############################################################
### For HNtypeI

biningDef = [
    { 'var' : 'abseta', 'type': 'float', 'bins': [0.0, 0.9, 1.2, 2.1, 2.4] },
    ## Official bins : [10, 15, 20, 25, 30, 40, 50, 60, 120, 200, 500]
    { 'var' : 'pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 40, 50, 60, 120, 500] },
]
if Measure == 'Mu8' :
  biningDef = [
      { 'var' : 'abseta', 'type': 'float', 'bins': [0.0, 0.9, 1.2, 2.1, 2.4] },
      { 'var' : 'pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 40, 50, 60, 120, 500] },
  ]
elif Measure == 'Mu17' :
  biningDef = [
      { 'var' : 'abseta', 'type': 'float', 'bins': [0.0, 0.9, 1.2, 2.1, 2.4] },
      { 'var' : 'pt' , 'type': 'float', 'bins': [20, 25, 30, 40, 50, 60, 120, 500] },
  ]

    #{ 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0.0, 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4] },
#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
## Convolution with Gaussian, and Exponential for Bkg
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
## Convolution with CBShape, and Exponential for Bkg
tnpParNomFit2 = [
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.5,2.5]","aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]',
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.5,2.5]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]',
    "aExpoP[-0.1, -1,0.1]",
    "aExpoF[-0.1, -1,0.1]",
    "RooCBShape::sigResPass(mass,meanCBP,sigmaCBP,aCBP,nCBP)",
    "RooCBShape::sigResFail(mass,meanCBF,sigmaCBF,aCBF,nCBF)",
    "Exponential::backgroundPass(mass, aExpoP)",
    "Exponential::backgroundFail(mass, aExpoF)",
    ]
## Convolution with Gaussian, and RooCMS for Bkg
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
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.5,2.5]","aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]', #Sigma 1, 0.4,6
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.5,2.5]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]', #Sigma 2, 0.4,15
    "aExpoP[-0.1, -1,0.1]",
    "aExpoF[-0.1, -1,0.1]",
    "Exponential::backgroundPass(mass, aExpoP)",
    "Exponential::backgroundFail(mass, aExpoF)",
    ]
tnpParAltSigFit2 = [
    "meanCBP[0.0, -5.0,5.0]","sigmaCBP[1, 0.4,2.5]","aCBP[2.0, 1.2,3.5]",'nCBP[3, 0.1,5]', #Sigma 1, 0.4,6
    "meanCBF[0.0, -5.0,5.0]","sigmaCBF[2, 0.4,2.5]","aCBF[2.0, 1.2,3.5]",'nCBF[3, 0.1,5]', #Sigma 2, 0.4,15
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
    #'data_altsig'       : tnpSample([wonjuntnpdir+filename],eventexp,tnpParAltSigFit,40,70,130), ### This should be done after mc_altsig
    'data_mass60130'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,40,60,130),
    'data_mass70120'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,40,70,120),
    'data_massbin30'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,30,70,130),
    'data_massbin50'    : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit,50,70,130),
    #'data_tagiso010'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),tnpParNomFit,40,70,130),
    'data_tagiso005'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.07','tag_combRelIsoPF04dBeta < 0.05'),tnpParNomFit,40,70,130),
    'data_tagiso010'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.07','tag_combRelIsoPF04dBeta < 0.1'),tnpParNomFit,40,70,130),
    #'data_altbkd'       : tnpSample([wonjuntnpdir+filename],eventexp,tnpParAltBkgFit,40,70,130),
    'data_altsig2'       : tnpSample([wonjuntnpdir+filename],eventexp,tnpParNomFit2,40,70,130),

    'mc'                : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,130),  ## For MC, used tnpParAltBkgFit instead of tnpParNomFit 
    #'mc_altsig'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltSigFit2,40,70,130), ## because CMS for background can be exactly zero, but Exponential can't be....?
    'mc_mass60130'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,60,130),
    'mc_mass70120'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,120),
    'mc_massbin30'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,30,70,130),
    'mc_massbin50'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,50,70,130),
    #'mc_tagiso010'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),tnpParAltBkgFit,40,70,130),
    'mc_tagiso005'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.07','tag_combRelIsoPF04dBeta < 0.05'),tnpParAltBkgFit,40,70,130),
    'mc_tagiso010'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.07','tag_combRelIsoPF04dBeta < 0.1'),tnpParAltBkgFit,40,70,130),
    #'mc_altbkd'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,130),
    'mc_altsig2'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,tnpParAltBkgFit,40,70,130),
}

systematicDef = {
    #'data' : [['data_mass60130','data_mass70120'],['data_massbin30','data_massbin50'],['data_tagiso010','data_tagiso020'], ['data_altsig2']], #['data_altbkd']
    #'mc' :   [['mc_mass60130','mc_mass70120'],    ['mc_massbin30','mc_massbin50'],    ['mc_tagiso010','mc_tagiso020'],     ['mc_altsig2']]    # ['mc_altbkd']
    'data' : [['data_mass60130','data_mass70120'],['data_massbin30','data_massbin50'],['data_tagiso005', 'data_tagiso010'], ['data_altsig2']], #['data_altbkd']
    'mc' :   [['mc_mass60130','mc_mass70120'],    ['mc_massbin30','mc_massbin50'],    ['mc_tagiso005', 'mc_tagiso010'],     ['mc_altsig2']]    # ['mc_altbkd']
}

#############################################################
########## Cuts definition for all samples
#############################################################

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#### or remove any additional cut (default)
additionalCuts = None

