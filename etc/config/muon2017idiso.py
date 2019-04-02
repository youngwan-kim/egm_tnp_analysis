from libPython.tnpClassUtils import tnpSample
#############################################################
########## functions
#############################################################
vpv1TEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[4,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1aTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[89,85,95], widthTEMP,        sigma2TEMP[4,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1bTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[93,85,95], widthTEMP,        sigma2TEMP[4,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1cTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[1.2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[4,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1dTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2.5,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[4,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1eTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[2.5,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1fTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[2,1,3])",
          "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[6,2,7])",
          "SUM::signalTEMP(vFracTEMP[0.8,0,1]*signal1TEMP, signal2TEMP)",]
vpv1gTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[2.495,0.1,3], sigma1TEMP[1.5,1,2])",
            "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[2.5,2,4])",
            "SUM::signalTEMP(vFracTEMP[0.95,0,1]*signal1TEMP, signal2TEMP)",]
vpv1hTEMP= ["Voigtian::signal1TEMP(x, mean1TEMP[91.5,85,95], widthTEMP[0.1,0.01,2], sigma1TEMP[1.5,1,2])",
            "Voigtian::signal2TEMP(x, mean2TEMP[91.5,85,95], widthTEMP,        sigma2TEMP[2.5,2,5])",
            "SUM::signalTEMP(vFracTEMP[0.99,0,1]*signal1TEMP, signal2TEMP)",]
Expo1=["Exponential::backgroundPass(x, lp[-0.1,-1,0.1])",
       "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
Expo1a=["Exponential::backgroundPass(x, lp[-0.5,-1,0.1])",
        "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
Expo1b=["Exponential::backgroundPass(x, lp[-0.0,-1,0.1])",
       "Exponential::backgroundFail(x, lf[-0.1,-1,0.1])",]
Expo1c=["Exponential::backgroundPass(x, lp[-0.1,-1,0.1])",
       "Exponential::backgroundFail(x, lf[-0.5,-1,0.1])",]
Expo1d=["Exponential::backgroundPass(x, lp[-0.1,-1,0.1])",
       "Exponential::backgroundFail(x, lf[-0.0,-1,0.1])",]
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
       "RooCMSShape::backgroundFail(x, alphaFail[70.,60.,90.], betaFail[0.1, 0.05,0.2], gammaFail[0.03, 0.,0.1], peakPass)",]
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
Cubic1c=["Chebychev::backgroundPass(x, {cPass1[0.25,0,0.5], cPass2[-0.7,-1,0.1], cPass3[0,-0.25,0.25]})",
       "Chebychev::backgroundFail(x, {cFail1[0.25,0,0.5], cFail2[-0.7,-1,0.1], cFail3[0,-0.25,0.25]})",]
Cubic1d=["Chebychev::backgroundPass(x, {cPass1[0.25,0,0.5], cPass2[-0.25,-1,0.1], cPass3[0.1,-0.25,0.25]})",
       "Chebychev::backgroundFail(x, {cFail1[0.25,0,0.5], cFail2[-0.25,-1,0.1], cFail3[0.1,-0.25,0.25]})",]

vpv1 = [w.replace('TEMP','Pass') for w in vpv1TEMP]+[w.replace('TEMP','Fail') for w in vpv1TEMP]
vpv1a = [w.replace('TEMP','Pass') for w in vpv1aTEMP]+[w.replace('TEMP','Fail') for w in vpv1aTEMP]
vpv1b = [w.replace('TEMP','Pass') for w in vpv1bTEMP]+[w.replace('TEMP','Fail') for w in vpv1bTEMP]
vpv1c = [w.replace('TEMP','Pass') for w in vpv1cTEMP]+[w.replace('TEMP','Fail') for w in vpv1cTEMP]
vpv1d = [w.replace('TEMP','Pass') for w in vpv1dTEMP]+[w.replace('TEMP','Fail') for w in vpv1dTEMP]
vpv1e = [w.replace('TEMP','Pass') for w in vpv1eTEMP]+[w.replace('TEMP','Fail') for w in vpv1eTEMP]
vpv1f = [w.replace('TEMP','Pass') for w in vpv1fTEMP]+[w.replace('TEMP','Fail') for w in vpv1fTEMP]
vpv1g = [w.replace('TEMP','Pass') for w in vpv1gTEMP]+[w.replace('TEMP','Fail') for w in vpv1gTEMP]
vpv1h = [w.replace('TEMP','Pass') for w in vpv1hTEMP]+[w.replace('TEMP','Fail') for w in vpv1hTEMP]


voigt=["Voigtian::signalPass(x, meanPass[90,80,100], widthPass[2.495], sigmaPass[3,1,20])",
       "Voigtian::signalFail(x, meanFail[90,80,100], widthFail[2.495], sigmaFail[3,1,20])",]

#############################################################
########## General settings
#############################################################
fitfunctions={
    'vpv1PlusExpo1':vpv1+Expo1,
    'vpv1aPlusExpo1':vpv1a+Expo1,
    'vpv1bPlusExpo1':vpv1b+Expo1,
    'vpv1cPlusExpo1':vpv1c+Expo1,
    'vpv1dPlusExpo1':vpv1d+Expo1,
    'vpv1ePlusExpo1':vpv1e+Expo1,
    'vpv1fPlusExpo1':vpv1f+Expo1,
    'vpv1gPlusExpo1':vpv1g+Expo1,
    'vpv1hPlusExpo1':vpv1h+Expo1,
    'vpv1PlusExpo1a':vpv1+Expo1a,
    'vpv1PlusExpo1b':vpv1+Expo1b,
    'vpv1PlusExpo1c':vpv1+Expo1c,
    'vpv1PlusExpo1d':vpv1+Expo1d,

    'vpv1PlusCMS1':vpv1+CMS1,
    'vpv1aPlusCMS1':vpv1a+CMS1,
    'vpv1bPlusCMS1':vpv1b+CMS1,
    'vpv1cPlusCMS1':vpv1c+CMS1,
    'vpv1dPlusCMS1':vpv1d+CMS1,
    'vpv1ePlusCMS1':vpv1e+CMS1,
    'vpv1fPlusCMS1':vpv1f+CMS1,
    'vpv1gPlusCMS1':vpv1g+CMS1,
    'vpv1hPlusCMS1':vpv1h+CMS1,

    'vpv1PlusCMS1a':vpv1+CMS1a,
    'vpv1PlusCMS1b':vpv1+CMS1b,
    'vpv1PlusCMS1c':vpv1+CMS1c,
    'vpv1PlusCMS1d':vpv1+CMS1d,
    'vpv1PlusCMS1e':vpv1+CMS1e,
    'vpv1PlusCMS1f':vpv1+CMS1f,
    'vpv1gPlusCMS1f':vpv1g+CMS1f,

    'vpv1PlusCubic1':vpv1+Cubic1,
    'vpv1aPlusCubic1':vpv1a+Cubic1,
    'vpv1bPlusCubic1':vpv1b+Cubic1,
    'vpv1cPlusCubic1':vpv1c+Cubic1,
    'vpv1dPlusCubic1':vpv1d+Cubic1,
    'vpv1ePlusCubic1':vpv1e+Cubic1,
    'vpv1fPlusCubic1':vpv1f+Cubic1,
    'vpv1gPlusCubic1':vpv1g+Cubic1,
    'vpv1hPlusCubic1':vpv1h+Cubic1,
    'vpv1PlusCubic1a':vpv1+Cubic1a,
    'vpv1PlusCubic1b':vpv1+Cubic1b,
    'vpv1PlusCubic1c':vpv1+Cubic1c,
    'vpv1PlusCubic1d':vpv1+Cubic1d,
}
fitfunctions_altsig={
    'voigtPlusExpo1':voigt+Expo1,
    'voigtPlusCMS1':voigt+CMS1,
}

baseOutDir = 'results/muon2017idiso/'
passcondition='Medium > 0.5 && relTkIso < 0.10'
eventexp='tag_IsoMu24==1 && tag_pt > 26 && mass > 60 && mass < 130 && tag_charge*charge < 0 && -0.2 < tag_dB && tag_dB < 0.2 && tag_combRelIsoPF04dBeta < 0.15 && -0.5 < tag_dzPV && tag_dzPV < 0.5 && pair_probeMultiplicity_Pt10_M60140==1 '
wonjuntnpdir='/data1/wonjun/public/TnPTreeZ_17Nov2017_SingleMuon_Run2017/'

flags = {
    'data'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions,40,70,130),
#    'data_altsig'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions_altsig,40,70,130),
    'data_mass60130'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions,40,60,130),
    'data_mass70120'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions,40,70,120),
    'data_massbin30'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions,30,70,130),
    'data_massbin50'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp,fitfunctions,50,70,130),
    'data_tagiso010'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),fitfunctions,40,70,130),
    'data_tagiso020'    : tnpSample([wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),fitfunctions,40,70,130),
    'mc'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions,40,70,130),
#    'mc_altsig'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions_altsig,40,70,130),
    'mc_mass60130'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions,40,60,130),
    'mc_mass70120'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions,40,70,120),
    'mc_massbin30'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions,30,70,130),
    'mc_massbin50'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp,fitfunctions,50,70,130),
    'mc_tagiso010'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.1'),fitfunctions,40,70,130),
    'mc_tagiso020'    : tnpSample([wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],eventexp.replace('tag_combRelIsoPF04dBeta < 0.15','tag_combRelIsoPF04dBeta < 0.2'),fitfunctions,40,70,130),
}


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
    { 'var' : 'eta' , 'type': 'float', 'bins': [-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4] },
    { 'var' : 'pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 40, 50, 60, 120] },
]

#############################################################
########## Cuts definition for all samples
#############################################################

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#### or remove any additional cut (default)
additionalCuts = None
