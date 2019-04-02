#############################################################
########## functions
#############################################################
voigtPlusExpo = [
    "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
    "Exponential::backgroundPass(mass, lp[0,-5,5])".replace("mass",mass_),
    "Exponential::backgroundFail(mass, lf[0,-5,5])".replace("mass",mass_),
    "efficiency[0.9,0,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusExpo = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
    "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
    "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
    "efficiency[0.9,0,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusExpoMin70 = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
    "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
    "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusCheb = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
    "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
    "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusCMS = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
    "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
    "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
"efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
voigtPlusCMS = [
    "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
    "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
    "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusCMS10_20 = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[1.5,1,2])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,7])".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
    "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
    "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
vpvPlusCMSbeta0p2 = [
    "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
    "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
    "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
    "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
    "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
voigtPlusCMSbeta0p2 = [
    "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
    "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
    "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
    "efficiency[0.9,0.7,1]",
    "signalFractionInPassing[0.9]"
]
#############################################################
########## General settings
#############################################################

numcut='DoubleMu17Mu8_IsoMu17leg==1'
DefaultDenCut='tag_IsoMu24==1 && tag_pt > 26 && mass > 50 && mass < 130 && tag_charge*charge < 0 && -0.2 < tag_dB && tag_dB < 0.2 && tag_combRelIsoPF04dBeta < 0.2 && -0.5 < tag_dzPV && tag_d\
zPV < 0.5 && pair_probeMultiplicity_Pt10_M60140==1 && pt > 10 && Medium > 0.5 && relTkIso < 0.10'
wonjuntnpdir='/data1/wonjun/public/TnPTreeZ_17Nov2017_SingleMuon_Run2017/'
flags = {
    'data_voigtPlusExpo'    : tnpFitting('data_voigtPlusExpo',[wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],DefaultDenCut,voigtPlusExpo)
    'data_vpvPlusExpo'    : tnpFitting('data_vpvPlusExpo',[wonjuntnpdir+'TnPTree_17Nov2017_SingleMuon_Run2017BCDEF_Full_GoldenJSON.root'],DefaultDenCut,vpvPlusExpo)
    'mc_voigtPlusExpo'    : tnpFitting('data_voigtPlusExpo',[wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],DefaultDenCut,voigtPlusExpo)
    'mc_vpvPlusExpo'    : tnpFitting('mc_vpvPlusExpo',[wonjuntnpdir+'TnPTree_94X_DYJetsToLL_M50_Madgraph_weighted_basicskim.root'],DefaultDenCut,vpvPlusExpo)
}

baseOutDir = 'results/Muon2017Leg1/'

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'pt' , 'type': 'float', 'bins': [10,20.0,30,40,50,200] },
]

#############################################################
########## Cuts definition for all samples
#############################################################

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
}

#### or remove any additional cut (default)
#additionalCuts = None
