import ROOT as rt
rt.gROOT.LoadMacro('./libCpp/histFitter.C+')
rt.gROOT.LoadMacro('./libCpp/RooCBExGaussShape.cc+')
rt.gROOT.LoadMacro('./libCpp/RooCMSShape.cc+')
rt.gROOT.SetBatch(1)

from ROOT import tnpFitter

import re
import math
import sys
import time

minPtForSwitch = 120

def ptMin( tnpBin ):
    ptmin = 1
    if tnpBin['name'].find('pt_') >= 0:
        ptmin = float(tnpBin['name'].split('pt_')[1].split('p')[0])
    elif tnpBin['name'].find('et_') >= 0:
        ptmin = float(tnpBin['name'].split('et_')[1].split('p')[0])
    return ptmin

def histFitter(histfile,fitfile,tnpBin,xmin,xmax,fitparameters,doDraw):
    if doDraw: rt.gROOT.SetBatch(0)
    tnpWorkspace = []
    tnpWorkspace.extend(fitparameters)
    
    fitter = tnpFitter( histfile, tnpBin['name'],xmin,xmax )

    ## setup
    fitter.useMinos()
    rootfile = rt.TFile(fitfile,'update')
    fitter.setOutputFile( rootfile )
    
    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)

    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    print title
    fit=fitter.fits(title,doDraw)
    if doDraw: 
        fit.Draw()
        time.sleep(10)
        rt.gROOT.SetBatch(1)

    rootfile.Close()

#######################################
### By Won (For Muon TnP)
#######################################

def createWorkspaceForAltSig(fitfile, tnpBin, fitparameters, IsMC ):

    if IsMC:
        return fitparameters

    FitOfMC = fitfile.replace('data', 'mc')
    filemc  = rt.TFile(FitOfMC,'read')

    from ROOT import RooFit,RooFitResult
    fitresP = filemc.Get( '%s_resP' % tnpBin['name']  )
    fitresF = filemc.Get( '%s_resF' % tnpBin['name'] )

    listOfParam = ['meanCBP','meanCBF', 'sigmaCBP','sigmaCBF','nCBP','nCBF','aCBP','aCBF'] # These parameter values from MC fitting results are used at Data fitting -Won
    freedomOfParam = 1 # Originally, these parameters from MC were fixed. However I'm gonna give them some freedom as many as their error. -Won
    
    fitPar = fitresF.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, fitparameters)
                for ir in listToRM :
                    fitparameters.remove(ir)
                #fitparameters.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )
                fitparameters.append('%s[%2.3f, %2.3f,%2.3f]'%(pName, fitPar[ipar].getVal(), max(0.5,fitPar[ipar].getVal()-freedomOfParam*fitPar[ipar].getError()), fitPar[ipar].getVal()+freedomOfParam*fitPar[ipar].getError()))
  
    fitPar = fitresP.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, fitparameters)
                for ir in listToRM :
                    fitparameters.remove(ir)
                #fitparameters.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )
                fitparameters.append('%s[%2.3f, %2.3f,%2.3f]'%(pName, fitPar[ipar].getVal(), max(0.5,fitPar[ipar].getVal()-freedomOfParam*fitPar[ipar].getError()), fitPar[ipar].getVal()+freedomOfParam*fitPar[ipar].getError()))

    filemc.Close()

    return fitparameters

def histFitter_Norminal(histfile,fitfile,tnpBin,xmin,xmax,fitparameters,doDraw):
    if doDraw: rt.gROOT.SetBatch(0)

    tnpWorkspace = []
    tnpWorkspace.extend(fitparameters)

    fitter = tnpFitter( histfile, tnpBin['name'],xmin,xmax )

    ## setup
    fitter.useMinos()
    rootfile = rt.TFile(fitfile,'update')
    fitter.setOutputFile( rootfile )

    ## generated Z LineShape
    ## for high pT change the failing spectra to any probe to get statistics
    MChist = ''
    IsMC = False
    if 'data' in histfile:
        MChist = histfile.replace('data', 'mc')
    else:
        MChist = histfile
        IsMC = True 
    fileMC  = rt.TFile(MChist,'read')
    histZLineShapeP = fileMC.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileMC.Get('%s_Fail'%tnpBin['name'])

    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)
    fileMC.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)

    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    print title

    fit=fitter.fits(IsMC, title,doDraw)

    if doDraw:
        fit.Draw()
        time.sleep(10)
        rt.gROOT.SetBatch(1)

    rootfile.Close()

def histFitter_AltSig(histfile,fitfile,tnpBin,xmin,xmax,fitparameters,doDraw):
    if doDraw: rt.gROOT.SetBatch(0)

    IsMC = False
    if 'data' not in histfile:
        IsMC = True 
    tnpWorkspacePar = createWorkspaceForAltSig(fitfile, tnpBin, fitparameters, IsMC )
    tnpWorkspaceFunc = [
        #"tailLeft[1]",
        #"RooCBExGaussShape::sigResPass(x,meanP,expr('sqrt(sigmaP*sigmaP+sosP*sosP)',{sigmaP,sosP}),alphaP,nP, expr('sqrt(sigmaP_2*sigmaP_2+sosP*sosP)',{sigmaP_2,sosP}),tailLeft)",
        #"RooCBExGaussShape::sigResFail(x,meanF,expr('sqrt(sigmaF*sigmaF+sosF*sosF)',{sigmaF,sosF}),alphaF,nF, expr('sqrt(sigmaF_2*sigmaF_2+sosF*sosF)',{sigmaF_2,sosF}),tailLeft)",
        "RooCBShape::sigResPass(mass,meanCBP,sigmaCBP,aCBP,nCBP)",
        "RooCBShape::sigResFail(mass,meanCBF,sigmaCBF,aCBF,nCBF)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspacePar)
    tnpWorkspace.extend(tnpWorkspaceFunc)

    fitter = tnpFitter( histfile, tnpBin['name'],xmin,xmax )

    ## setup
    fitter.useMinos()
    rootfile = rt.TFile(fitfile,'update')
    fitter.setOutputFile( rootfile )

    ## generated Z LineShape
    fileMC  = rt.TFile('etc/inputs/ZeeGenLevel.root','read')
    histZLineShape = fileMC.Get('Mass')
    fitter.setZLineShapes(histZLineShape,histZLineShape)
    fileMC.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)

    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    print title

    fit=fitter.fits(IsMC, title,doDraw)

    if doDraw:
        fit.Draw()
        time.sleep(10)
        rt.gROOT.SetBatch(1)

    rootfile.Close()

