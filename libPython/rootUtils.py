import ROOT as rt
import math
from fitUtils import *
#from fitSimultaneousUtils import *

def GetEffi( filename, binname ):
    rootfile = rt.TFile( filename, 'read' )
    canvas = rootfile.Get('%s_Canv'%binname)
    reports=canvas.GetPad(1).GetPrimitive("reportTPave").GetLine(1).GetTitle().split()
    rootfile.Close()
    return float(reports[3]), float(reports[5])

def GetChiPassFail(filename,binname):
    canvas=GetTObject(filename,binname+'_Canv')
    chiPass=canvas.GetPad(2).GetPrimitive('chiPass').GetTitle()
    chiFail=canvas.GetPad(3).GetPrimitive('chiFail').GetTitle()
    return float(chiPass.replace('chi/n=','')),float(chiFail.replace('chi/n=',''))

def GetScorePassFail(filename,binname):
    canvas=GetTObject(filename,binname+'_Canv')
    chiPass=canvas.GetPad(2).GetPrimitive('scorePass').GetTitle()
    chiFail=canvas.GetPad(3).GetPrimitive('scoreFail').GetTitle()
    return float(chiPass.replace('score=','')),float(chiFail.replace('score=',''))

def GetRooFitPar(filename,objname,parname):
    roofitresult=GetTObject(filename,objname)
    rooarglist=roofitresult.floatParsFinal()
    return rooarglist.at(rooarglist.index(parname)).getVal()

def GetTObject(filename,objname):
    rootfile=rt.TFile(filename,"read")
    obj=rootfile.Get(objname)
    rootfile.Close()
    return obj

def MoveTObject(filename1,filename2,objname):
    obj=GetTObject(filename1,objname)
    rootfile=rt.TFile(filename2,"update")
    if obj:
        obj.Write(objname)
    rootfile.Close()

def histPlotter( filename, tnpBin, plotDir ):
    print 'opening ', filename
    print '  get canvas: ' , '%s_Canv' % tnpBin['name']
    rootfile = rt.TFile(filename,"read")

    c = rootfile.Get( '%s_Canv' % tnpBin['name'] )
    c.Print( '%s/%s.png' % (plotDir,tnpBin['name']))


def computeEffi( n1,n2,e1,e2):
    eff   = n1/(n1+n2)
    e_eff = 1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
    if e_eff < 0.001 : e_eff = 0.001
    return eff,e_eff


import os.path
def getAllEffi( info, bindef ):
    effis = {}
    if not info['mcNominal'] is None and os.path.isfile(info['mcNominal']):
        rootfile = rt.TFile( info['mcNominal'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['mcNominal'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcNominal'] = [-1,-1]

    if not info['tagSel'] is None and os.path.isfile(info['tagSel']):
        rootfile = rt.TFile( info['tagSel'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['tagSel'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['tagSel'] = [-1,-1]
        
    if not info['mcAlt'] is None and os.path.isfile(info['mcAlt']):
        rootfile = rt.TFile( info['mcAlt'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['mcAlt'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcAlt'] = [-1,-1]

    if not info['dataNominal'] is None and os.path.isfile(info['dataNominal']) :
        rootfile = rt.TFile( info['dataNominal'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')
        
        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataNominal'] = computeEffi(nP,nF,eP,eF)
    else:
        effis['dataNominal'] = [-1,-1]
    if not info['dataAltSig'] is None and os.path.isfile(info['dataAltSig']) :
        rootfile = rt.TFile( info['dataAltSig'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataAltSig'] = computeEffi(nP,nF,eP,eF)

    else:
        effis['dataAltSig'] = [-1,-1]

    if not info['dataAltBkg'] is None and os.path.isfile(info['dataAltBkg']):
        rootfile = rt.TFile( info['dataAltBkg'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataAltBkg'] = computeEffi(nP,nF,eP,eF)
    else:
        effis['dataAltBkg'] = [-1,-1]
    return effis
