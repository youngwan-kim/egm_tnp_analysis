from AFBMuonCommon import *
from AFBMuon2018Common import *
baseOutDir = 'results/AFBMuonIDISO2018_SSS/'
tnpTreeDir = 'tpTree'

if not samplesDef['data'  ] is None: samplesDef['data'].set_weight('(tag_charge*charge<0 ? 1. : -1.)')
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight('(tag_charge*charge<0 ? 1. : -1.)*'+weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight('(tag_charge*charge<0 ? 1. : -1.)*'+weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight('(tag_charge*charge<0 ? 1. : -1.)*'+weightName)

cutBase   = 'tag_IsoMu24==1 && tag_pt>26 && tag_combRelIsoPF04dBeta<0.15 && pair_BestZ==1'
additionalCutBase = {
    'MediumID_LooseTkIso_QPlus' : 'tag_charge<0',
    'MediumID_LooseTkIso_QMinus' : 'charge<0',
    'MediumID_LooseTkIso_ValidMatch_QPlus' : 'tag_charge<0 && numberOfMatches>-1',
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
