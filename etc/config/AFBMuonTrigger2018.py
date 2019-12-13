from AFBMuonCommon import *
from AFBMuon2018Common import *
baseOutDir = 'results/AFBMuonTrigger2018/'
tnpTreeDir = 'tpTree'
cutBase   = 'tag_IsoMu24==1 && tag_pt > 26 && tag_combRelIsoPF04dBeta < 0.15 && Loose'
additionalCutBase = {
    'MediumID_LooseTkIso_IsoMu24_QPlus' : 'charge > 0 && Medium == 1 && relTkIso < 0.10',
    'MediumID_LooseTkIso_IsoMu24_QMinus' : 'charge < 0 && Medium == 1 && relTkIso < 0.10',
}
flags = {
    'MediumID_LooseTkIso_IsoMu24_QPlus' : 'IsoMu24',
    'MediumID_LooseTkIso_IsoMu24_QMinus' : 'IsoMu24',
}
