from AFBMuonCommon import *
from AFBMuon2018Common import *
baseOutDir = 'results/AFBMuonIDISO2018/'
tnpTreeDir = 'tpTree'
cutBase   = 'tag_IsoMu24==1 && tag_pt>26 && tag_combRelIsoPF04dBeta<0.15 && pair_BestZ==1 && tag_charge*charge<0'
additionalCutBase = {
    'MediumID_LooseTkIso_QPlus' : 'charge>0',
    'MediumID_LooseTkIso_QMinus' : 'charge<0',
    'MediumID_LooseTkIso_ValidMatch_QPlus' : 'charge>0 && numberOfMatches>-1',
    'MediumID_LooseTkIso_ValidMatch_QMinus' : 'charge<0 && numberOfMatches>-1',
    'MediumID_LooseTkIso_ValidMatch' : 'numberOfMatches>-1',
}
flags = {
    'MediumID_LooseTkIso_QPlus' : '(Medium && relTkIso<0.10)',
    'MediumID_LooseTkIso_QMinus' : '(Medium && relTkIso<0.10)',
    'MediumID_LooseTkIso' : '(Medium && relTkIso<0.10)',
    'MediumID_LooseTkIso_ValidMatch_QPlus' : '(Medium && relTkIso<0.10)',
    'MediumID_LooseTkIso_ValidMatch_QMinus' : '(Medium && relTkIso<0.10)',
    'MediumID_LooseTkIso_ValidMatch' : '(Medium && relTkIso<0.10)',
    'LooseID': 'Loose',
    'Glb': 'Glb',
    'TM': 'TM',
    'GlbOrTM': '( TM || Glb )'
}
