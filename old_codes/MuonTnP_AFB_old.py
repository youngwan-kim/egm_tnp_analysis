from libPython.tnpClassUtils import tnpSample
#############################################################
########## Setting
############################################################# 

#### Choose one of these ####################
#Period = {'2016BF', '2016GH', '2017', '2018' }
#Measure = {'IDISO', 'Mu17', 'Mu8', 'IsoMu24' }
#Charge = {'+', '-', 'all' }

Period = '2016BF' 
Measure = 'Mu17'
Charge = '+'

#############################################################
########## functions
#############################################################
vpv1TEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",        ## From Won standard Expo
           "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[4,2,10])",
           "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1aTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[0.8,0.4,1.3])", ## From Won Expo3
            "Voigtian::signal2TEMP(x, mean2TEMP[89,85,95], widthTEMP,        sigma2TEMP[2,1,5])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1bTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[1,  0.5,1.5])", ## From Won Expo4
            "Voigtian::signal2TEMP(x, mean2TEMP[93,85,95], widthTEMP,        sigma2TEMP[2,1,5])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1cTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[1.1,0.7,1.7])", ## From Won Expo5a
            "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[2,1,5])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1dTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[1.5,0.6,2  ])", ## From Won Expo6 
            "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[2,1,5])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1eTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91,84,98], widthTEMP[2.495], sigma1TEMP[2.5,1,6])",       ## From KP Expo3 pass
            "Voigtian::signal2TEMP(x, mean2TEMP[91,81,101], widthTEMP,        sigma2TEMP[5,1,10])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1fTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91,86,96], widthTEMP[2.495], sigma1TEMP[2.5,1,5])",       ## From KP Expo4 pass
            "Voigtian::signal2TEMP(x, mean2TEMP[91,78,104], widthTEMP,        sigma2TEMP[5,1,8])",
            "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]

Expo1=["Exponential::backgroundPass(x, lp[-0.1,-1,0.1])",
       "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
Expo1a=["Exponential::backgroundPass(x, lp[-0.5,-1,0.1])",
        "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
Expo1b=["Exponential::backgroundPass(x, lp[-0.0,-1,0.1])",
        "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
CMS1=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
      "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)",]
CMS1a=["RooCMSShape::backgroundPass(x, alphaPass[80.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[80.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)",]
CMS1b=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.015, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.015, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)",]
CMS1c=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.05, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.05, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)",]
CMS1d=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.03, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.03, 0.,0.1], peakPass)",]
CMS1e=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.03, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.1, 0.05,0.15], gammaFail[0.03, 0.,0.1], peakPass)",]
CMS1f=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.03, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.02, 0.00,0.2], gammaFail[0.06, 0.,0.1], peakPass)",]
CMS1g=["RooCMSShape::backgroundPass(x, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.03, 0.,0.1], peakPass[90.0])",
       "RooCMSShape::backgroundFail(x, alphaFail[60.,50.,90.], betaFail[0.01, 0.00,0.3], gammaFail[0.06, 0.,0.1], peakPass)",]
Cubic1=["Chebychev::backgroundPass(x, {cPass1[0.25,0,0.5], cPass2[-0.25,-1,0.1], cPass3[0,-0.25,0.25]})",
        "Chebychev::backgroundFail(x, {cFail1[0.25,0,0.5], cFail2[-0.25,-1,0.1], cFail3[0,-0.25,0.25]})",]
Cubic1a=["Chebychev::backgroundPass(x, {cPass1[0.4,0,0.5], cPass2[-0.25,-1,0.1], cPass3[0,-0.25,0.25]})",
         "Chebychev::backgroundFail(x, {cFail1[0.4,0,0.5], cFail2[-0.25,-1,0.1], cFail3[0,-0.25,0.25]})",]
Cubic1b=["Chebychev::backgroundPass(x, {cPass1[0.1,0,0.5], cPass2[-0.25,-1,0.1], cPass3[0,-0.25,0.25]})",
         "Chebychev::backgroundFail(x, {cFail1[0.1,0,0.5], cFail2[-0.25,-1,0.1], cFail3[0,-0.25,0.25]})",]

Cubic1c=["Chebychev::backgroundPass(x, {cPass1[0,-10,10], cPass2[0,-10,10], cPass3[0,-10,10]})",
         "Chebychev::backgroundFail(x, {cFail1[0.25,0,0.5], cFail2[-0.7,-1,0.1], cFail3[0,-0.25,0.25]})",]
Cubic1d=["Chebychev::backgroundPass(x, {cPass1[0,-5, 5 ], cPass2[0,-5, 5 ], cPass3[0,-5, 5 ]})",
         "Chebychev::backgroundFail(x, {cFail1[0.25,0,0.5], cFail2[-0.25,-1,0.1], cFail3[0.1,-0.25,0.25]})",]
#### NEW Addition
Quart=["Chebychev::backgroundPass(x, {cPass1[0,-10,10], cPass2[0,-10,10], cPass3[0,-10,10], cPass4[0,-10,10]})",
       "Chebychev::backgroundFail(x, {cFail1[0,-10,10], cFail2[0,-10,10], cFail3[0,-10,10], cFail4[0,-10,10]})",]
Quart2=["Chebychev::backgroundPass(x, {cPass1[0,-10,10], cPass2[0,-10,10], cPass3[0,-10,10], cPass4[0,-10,10]})",
        "Chebychev::backgroundFail(x, {cFail1[0,-5, 5 ], cFail2[0,-5, 5 ], cFail3[0,-5, 5 ], cFail4[0,-5, 5 ]})",]
Quint=["Chebychev::backgroundPass(x, {cPass1[0,-5, 5 ], cPass2[0,-5, 5 ], cPass3[0,-5, 5 ], cPass4[0,-5, 5 ], cPass5[0,-5, 5 ]})",
       "Chebychev::backgroundFail(x, {cFail1[0,-5, 5 ], cFail2[0,-5, 5 ], cFail3[0,-5, 5 ], cFail4[0,-5, 5 ], cFail5[0,-5, 5 ]})",]
CMSpCubic=["Chebychev::backgroundPass(x, {cPass1[0,-2, 2 ], cPass2[0,-2, 2 ], cPass3[0.1,-2, 2 ]})",
           "Chebychev::backgroundFail1(x, {cFail1[0,-2, 2 ], cFail2[0,-2, 2 ], cFail3[0.1,-2, 2 ]})",
           "RooCMSShape::backgroundFail2(x, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass[90.0])",
           "SUM::backgroundFail(bFrac[0.5, 0, 1]*backgroundFail1,backgroundFail2)",]
CMSpQuart=["Chebychev::backgroundPass(x, {cPass1[0,-2, 2 ], cPass2[0,-2, 2 ], cPass3[0,-2, 2 ], cPass4[0,-2, 2 ]})",
           "Chebychev::backgroundFail1(x, {cFail1[0,-2, 2 ], cFail2[0,-2, 2 ], cFail3[0,-2, 2 ], cFail4[0,-2, 2 ]})",
           "RooCMSShape::backgroundFail2(x, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass[90.0])",
           "SUM::backgroundFail(bFrac[0.5, 0, 1]*backgroundFail1,backgroundFail2)",]

vpv1 = [w.replace('TEMP','Pass') for w in vpv1TEMP]+[w.replace('TEMP','Fail') for w in vpv1TEMP]
vpv1a = [w.replace('TEMP','Pass') for w in vpv1aTEMP]+[w.replace('TEMP','Fail') for w in vpv1aTEMP]
vpv1b = [w.replace('TEMP','Pass') for w in vpv1bTEMP]+[w.replace('TEMP','Fail') for w in vpv1bTEMP]
vpv1c = [w.replace('TEMP','Pass') for w in vpv1cTEMP]+[w.replace('TEMP','Fail') for w in vpv1cTEMP]
vpv1d = [w.replace('TEMP','Pass') for w in vpv1dTEMP]+[w.replace('TEMP','Fail') for w in vpv1dTEMP]
vpv1e = [w.replace('TEMP','Pass') for w in vpv1eTEMP]+[w.replace('TEMP','Fail') for w in vpv1eTEMP]
vpv1f = [w.replace('TEMP','Pass') for w in vpv1fTEMP]+[w.replace('TEMP','Fail') for w in vpv1fTEMP]

voigt = ["Voigtian::signalPass(x, meanPass[90,80,100], widthPass[2.495], sigmaPass[3,0.7,20])",
       "Voigtian::signalFail(x, meanFail[90,80,100], widthFail[2.495], sigmaFail[3,1,20])",]
voigt2 = ["Voigtian::signalPass(x, meanPass[90,80,100], widthPass[2.495], sigmaPass[2,0.7,6])",
        "Voigtian::signalFail(x, meanFail[90,80,100], widthFail[2.495], sigmaFail[2,1,7])",]
#### NEW Addition
voigt3 = ["Voigtian::signalPass(x, meanPass[90,80,100], widthPass[2.495], sigmaPass[4.5,3,7])",
          "Voigtian::signalFail(x, meanFail[90,80,100], widthFail[2.495], sigmaFail[4.5,3,7])",]
voigt4 = ["Voigtian::signalPass(x, meanPass[90,80,100], widthPass[2.495], sigmaPass[1.5,0.7,2.5])",
          "Voigtian::signalFail(x, meanFail[90,80,100], widthFail[2.495], sigmaFail[1.5,0.7,2.5])",]


#############################################################
########## General Settings (default = '2017', 'Mu17', 'all')
#############################################################

baseOutDir = 'won_results_'+Period+'_'+Measure+'_'+Charge+'/'

passcondition = 'DoubleIsoMu17Mu8_IsoMu17leg || DoubleIsoMu17TkMu8_IsoMu17leg'
eventexp = 'tag_IsoMu27==1 && tag_pt > 29 && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.15 && Medium && relTkIso < 0.10'
eventexpMC = '(tag_IsoMu27==1 && tag_pt > 29 && mcTrue && mass > 60 && mass < 130 && tag_charge*charge < 0 && tag_combRelIsoPF04dBeta < 0.15 && Medium && relTkIso < 0.10) * weight'

wonjuntnpdir = '/data9/Users/wonjun/public/CRABDIR/'
filename = 'TnPTreeZ_17Nov2017_SingleMuon_Run2017BCDEFv1_GoldenJSON.root'
filenameMC = 'TnPTreeZ_94X_DYJetsToLL_M50_Madgraph_WithWeights.root'

#### Measure Option ########################################################
if Measure == 'Mu8' :
  passcondition = 'DoubleIsoMu17Mu8_IsoMu8leg || DoubleIsoMu17TkMu8_IsoMu8leg'
elif Measure == 'IsoMu24' :
  if Period == '2017' :
    passcondition = 'IsoMu27'
  elif Period == '2018' :
    passcondition = 'IsoMu24'
  else :
    passcondition = 'IsoMu24 || IsoTkMu24'
elif Measure == 'IDISO':
  passcondition = 'Medium && relTkIso < 0.10'
  eventexp = eventexp.replace('Medium && relTkIso < 0.10', 'TM')
  eventexpMC = eventexpMC.replace('Medium && relTkIso < 0.10', 'TM')

#### Charge Option ########################################################
if Charge == "+" :
  eventexp = eventexp.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge > 0')
  eventexpMC = eventexpMC.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge > 0')
elif Charge == "-" :
  eventexp = eventexp.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge < 0')
  eventexpMC = eventexpMC.replace('tag_charge*charge < 0','tag_charge*charge < 0 && charge < 0')

#### Period Option ########################################################
if Period == "2016BF" :
  eventexp = eventexp.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  eventexpMC = eventexpMC.replace('tag_IsoMu27==1 && tag_pt > 29','tag_IsoMu24==1 && tag_pt > 26')
  wonjuntnpdir = '/data9/Users/wonjun/public/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016/'
  filename = 'TnPTreeZ_LegacyRereco07Aug17_SingleMuon_BCDEF.root'
  filenameMC = 'DY_Summer16PremixMoriond_weighted_BCDEF.root'
  if Measure == 'IDISO':
    passcondition = passcondition.replace('Medium','Medium2016') #From Simranjit's presentation
  else :
    eventexp = eventexp.replace('Medium','Medium2016')
    eventexpMC = eventexpMC.replace('Medium','Medium2016')
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


fitfunctions={
    'vpv1PlusExpo1':vpv1+Expo1,
    'vpv1aPlusExpo1':vpv1a+Expo1,
    'vpv1bPlusExpo1':vpv1b+Expo1,
    'vpv1cPlusExpo1':vpv1c+Expo1,
    'vpv1dPlusExpo1':vpv1d+Expo1,
    'vpv1ePlusExpo1':vpv1e+Expo1,
    'vpv1fPlusExpo1':vpv1f+Expo1,
    'vpv1PlusExpo1a':vpv1+Expo1a,
    'vpv1PlusExpo1b':vpv1+Expo1b,

    'vpv1PlusCMS1':vpv1+CMS1,    
    'vpv1aPlusCMS1':vpv1a+CMS1,  
    'vpv1bPlusCMS1':vpv1b+CMS1,  
    'vpv1cPlusCMS1':vpv1c+CMS1,  
    'vpv1dPlusCMS1':vpv1d+CMS1,  
    'vpv1ePlusCMS1':vpv1e+CMS1,  
    'vpv1fPlusCMS1':vpv1f+CMS1,  

    'vpv1cPlusCMS1a':vpv1c+CMS1a,
    'vpv1cPlusCMS1b':vpv1c+CMS1b,
    'vpv1cPlusCMS1c':vpv1c+CMS1c,
    'vpv1cPlusCMS1d':vpv1c+CMS1d,
    'vpv1cPlusCMS1e':vpv1c+CMS1e,
}
fitfunctions_altsig={
    'voigtPlusExpo1':voigt+Expo1,
    'voigtPlusExpo1b':voigt+Expo1b,
    'voigtPlusCMS1':voigt+CMS1,    
    'voigtPlusCMS1b':voigt+CMS1b,  
    'voigtPlusCMS1d':voigt+CMS1d,  
    'voigt2PlusExpo1':voigt2+Expo1,
    'voigt2PlusExpo1a':voigt2+Expo1a,
    'voigt2PlusCMS1':voigt2+CMS1,  
    'voigt2PlusCMS1a':voigt2+CMS1a,
    'voigt2PlusCMS1c':voigt2+CMS1c,
    'voigt2PlusCMS1e':voigt2+CMS1e,
    'voigt3PlusExpo1':voigt3+Expo1,
    'voigt3PlusCMS1b':voigt3+CMS1b,
    'voigt4PlusExpo1b':voigt4+Expo1b,
    'voigt4PlusCMS1':voigt4+CMS1,
}
'''
if Measure == "IDISO" :
  fitfunctions={
    'vpv1PlusExpo1':vpv1+Expo1,   #31 Is it conserved ordering?
    'vpv1aPlusExpo1':vpv1a+Expo1, #22
    'vpv1bPlusExpo1':vpv1b+Expo1, #30
    'vpv1cPlusExpo1':vpv1c+Expo1, #25
    'vpv1dPlusExpo1':vpv1d+Expo1, #23
    'vpv1ePlusExpo1':vpv1e+Expo1, #8
    'vpv1fPlusExpo1':vpv1f+Expo1, #0
    #'vpv1gPlusExpo1':vpv1g+Expo1,
    #'vpv1hPlusExpo1':vpv1h+Expo1,
    #'vpv1PlusExpo1a':vpv1+Expo1a,
    #'vpv1PlusExpo1b':vpv1+Expo1b,

    #'vpv1PlusCMS1':vpv1+CMS1,
    #'vpv1aPlusCMS1':vpv1a+CMS1,
    'vpv1bPlusCMS1':vpv1b+CMS1,   #17
    'vpv1cPlusCMS1':vpv1c+CMS1,   #1
    'vpv1dPlusCMS1':vpv1d+CMS1,   #28
    'vpv1ePlusCMS1':vpv1e+CMS1,   #19
    'vpv1fPlusCMS1':vpv1f+CMS1,   #26
    #'vpv1gPlusCMS1':vpv1g+CMS1,
    #'vpv1hPlusCMS1':vpv1h+CMS1,

    'vpv1cPlusCMS1a':vpv1c+CMS1a, #7
    'vpv1cPlusCMS1b':vpv1c+CMS1b, #5
    'vpv1cPlusCMS1c':vpv1c+CMS1c, #6
    'vpv1cPlusCMS1d':vpv1c+CMS1d, #9
    'vpv1cPlusCMS1e':vpv1c+CMS1e, #10
    'vpv1PlusCMS1f':vpv1+CMS1f,
    'vpv1gPlusCMS1f':vpv1b+CMS1f,

    'vpv1PlusCubic1':vpv1+Cubic1,    #18
    'vpv1aPlusCubic1':vpv1a+Cubic1,
    'vpv1bPlusCubic1':vpv1b+Cubic1,  #27
    'vpv1cPlusCubic1':vpv1c+Cubic1,  #29
    'vpv1dPlusCubic1':vpv1d+Cubic1,  #24
    'vpv1ePlusCubic1':vpv1e+Cubic1,  #12
    'vpv1fPlusCubic1':vpv1f+Cubic1,  #20
    #'vpv1gPlusCubic1':vpv1g+Cubic1,
    #'vpv1hPlusCubic1':vpv1h+Cubic1,
    'vpv1cPlusCubic1a':vpv1c+Cubic1a,#13
    'vpv1cPlusCubic1b':vpv1c+Cubic1b,#15
    'vpv1cPlusCubic1c':vpv1c+Cubic1c,#14
    'vpv1cPlusCubic1d':vpv1c+Cubic1d,#11
  }
  fitfunctions_altsig={
    'voigtPlusExpo1':voigt+Expo1,      #1
    'voigtPlusExpo1b':voigt+Expo1b,    #4
    'voigtPlusCMS1':voigt+CMS1,        #17
    'voigtPlusCMS1b':voigt+CMS1b,      #16
    'voigtPlusCMS1d':voigt+CMS1d,      #18
    'voigtPlusCMS1f':voigt+CMS1f,   
    'voigtPlusCubic1':voigt+Cubic1,    #7
    'voigtPlusCubic1b':voigt+Cubic1b,  #11
    'voigtPlusCubic1d':voigt+Cubic1d,  #13
    'voigt2PlusExpo1':voigt2+Expo1,    #21
    'voigt2PlusExpo1b':voigt2+Expo1a,  #3
    'voigt2PlusCMS1':voigt2+CMS1,      #5
    'voigt2PlusCMS1a':voigt2+CMS1a,    #12
    'voigt2PlusCMS1c':voigt2+CMS1c,    #10
    'voigt2PlusCMS1e':voigt2+CMS1e,    #14
    'voigt2PlusCubic1':voigt2+Cubic1,  #15
    'voigt2PlusCubic1a':voigt2+Cubic1a,#2
    'voigt2PlusCubic1c':voigt2+Cubic1c,#9
    'voigt2PlusQuart':voigt2+Quart,    #0
    'voigt2PlusQuart2':voigt2+Quart2,  #19   
    'voigt2PlusQuint':voigt2+Quint,    #6
    'voigt2PlusCMSpCubic':voigt2+CMSpCubic,#20
    'voigt2PlusCMSpQuart':voigt2+CMSpQuart,#8
  }
'''

#############################################################
########## Binning Definition  [can be nD bining]
#############################################################
biningDef = [              ### For IDISO or Mu8 
    { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0.0, 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4] },
    { 'var' : 'pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 120] },
]
if Measure == 'Mu17' :
  biningDef = [            ### For Mu17
    { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0.0, 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4] },
    { 'var' : 'pt' , 'type': 'float', 'bins': [20, 25, 30, 35, 40, 45, 50, 60, 120] },            ## For turn-on curve, add [10,15,16,17,18,19,20,...]
  ]
elif Measure == 'IsoMu24' :
  if Period == '2017' :
    biningDef = [          ### For IsoMu27
      { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0.0, 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4] },
      { 'var' : 'pt' , 'type': 'float', 'bins': [29, 32, 35, 40, 45, 50, 60, 120] },         ## For turn-on curve, add [...,25,26,27,28,29,30,...]
    ]
  else :
    biningDef = [          ### For IsoMu24
      { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0.0, 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4] },
      { 'var' : 'pt' , 'type': 'float', 'bins': [26, 30, 35, 40, 45, 50, 60, 120] },       ## For turn-on curve, add [...,20,22,23,24,25,26,27,30,...]
    ]

#############################################################
########## Setting Systematic
#############################################################

flags = {
    'data'              : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions,40,70,130),
    'data_altsig'       : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions_altsig,40,70,130),
    'data_mass60130'    : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions,40,60,130),
    'data_mass70120'    : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions,40,70,120),
    'data_massbin30'    : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions,30,70,130),
    'data_massbin50'    : tnpSample([wonjuntnpdir+filename],eventexp,fitfunctions,50,70,130),
    'data_tagiso010'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),fitfunctions,40,70,130),
    'data_tagiso020'    : tnpSample([wonjuntnpdir+filename],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),fitfunctions,40,70,130),

    'mc'                : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions,40,70,130),
    'mc_altsig'         : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions_altsig,40,70,130),
    'mc_mass60130'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions,40,60,130),
    'mc_mass70120'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions,40,70,120),
    'mc_massbin30'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions,30,70,130),
    'mc_massbin50'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC,fitfunctions,50,70,130),
    'mc_tagiso010'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),fitfunctions,40,70,130),
    'mc_tagiso020'      : tnpSample([wonjuntnpdir+filenameMC],eventexpMC.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),fitfunctions,40,70,130),
}

systematicDef = {
    'data' : [['data_mass60130','data_mass70120'],['data_massbin30','data_massbin50'],['data_tagiso010','data_tagiso020'], ['data_altsig']],
    'mc' : [['mc_mass60130','mc_mass70120'],['mc_massbin30','mc_massbin50'],['mc_tagiso010','mc_tagiso020'], ['mc_altsig']]
}

#############################################################
########## Cuts definition for all samples
#############################################################

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#### or remove any additional cut (default)
additionalCuts = None
