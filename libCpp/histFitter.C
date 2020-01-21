#include "RooDataHist.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooAbsPdf.h"
#include "RooPlot.h"
#include "RooFitResult.h"
#include "TH1.h"
#include "TSystem.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TPaveText.h"

/// include pdfs
#include "RooCBExGaussShape.h"
#include "RooCMSShape.h"

#include <vector>
#include <string>
#ifdef __CINT__
#pragma link C++ class std::vector<std::string>+;
#endif

using namespace RooFit;
using namespace std;

class tnpFitter {
public:
  tnpFitter( TString filein, std::string histname,double xmin,double xmax);
  ~tnpFitter(void) {if( _work != 0 ) delete _work;}
  void setZLineShapes(TH1 *hZPass, TH1 *hZFail );
  void setWorkspace(std::vector<std::string>);
  void setOutputFile(TFile *fOut ) {_fOut = fOut;}
  TCanvas* fits(bool IsMCsample, std::string title = "",bool doCheck=false);
  void useMinos(bool minos = true) {_useMinos = minos;}
  void textParForCanvas(RooFitResult *resP, RooFitResult *resF, TPad *p);
  
  void fixSigmaFtoSigmaP(bool fix=true) { _fixSigmaFtoSigmaP= fix;}

  void setFitRange(double xMin,double xMax) { _xFitMin = xMin; _xFitMax = xMax; }
  RooWorkspace *_work;
private:
  std::string _histname_base;
  TFile *_fOut;
  double _nTotP, _nTotF;
  bool _useMinos;
  bool _fixSigmaFtoSigmaP;
  double _xFitMin,_xFitMax;
  int nBins;
};

tnpFitter::tnpFitter(TString filein, std::string histname,double xmin, double xmax) : _useMinos(false),_fixSigmaFtoSigmaP(false) {
  TFile f(filein);
  TH1 *hPass = (TH1*) f.Get(TString::Format("%s_Pass",histname.c_str()).Data());
  TH1 *hFail = (TH1*) f.Get(TString::Format("%s_Fail",histname.c_str()).Data());
  hPass->SetDirectory(0);
  hFail->SetDirectory(0);
  f.Close();
  nBins=hPass->GetNbinsX();

  RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);
  RooMsgService::instance().setSilentMode(true);
  _histname_base = histname;  

  _nTotP = hPass->Integral();
  _nTotF = hFail->Integral();
  cout<<_nTotP<<" "<<_nTotF<<endl;
  /// MC histos are done between 50-130 to do the convolution properly
  /// but when doing MC fit in 60-120, need to zero bins outside the range
  for( int ib = 0; ib <= hPass->GetXaxis()->GetNbins()+1; ib++ )
    if(  hPass->GetXaxis()->GetBinCenter(ib) <= xmin || hPass->GetXaxis()->GetBinCenter(ib) >= xmax ) {
      hPass->SetBinContent(ib,0);
      hFail->SetBinContent(ib,0);
    }
  
  _work = new RooWorkspace("w") ;
  _work->factory(Form("mass[%f,%f]",xmin,xmax));

  RooDataHist rooPass("hPass","hPass",*_work->var("mass"),hPass);
  RooDataHist rooFail("hFail","hFail",*_work->var("mass"),hFail);
  _work->import(rooPass) ;
  _work->import(rooFail) ;
  _xFitMin = xmin;
  _xFitMax = xmax;
}


void tnpFitter::setZLineShapes(TH1 *hZPass, TH1 *hZFail ) {
  RooDataHist rooPass("hGenZPass","hGenZPass",*_work->var("mass"),hZPass);
  RooDataHist rooFail("hGenZFail","hGenZFail",*_work->var("mass"),hZFail);
  _work->import(rooPass) ;
  _work->import(rooFail) ;  
}

void tnpFitter::setWorkspace(std::vector<std::string> workspace) {
  for( unsigned icom = 0 ; icom < workspace.size(); ++icom ) {
    cout<<workspace[icom].c_str()<<endl;
    _work->factory(workspace[icom].c_str());
  }
  _work->factory("HistPdf::sigPhysPass(mass,hGenZPass)");
  _work->factory("HistPdf::sigPhysFail(mass,hGenZFail)");
  _work->factory("FCONV::signalPass(mass, sigPhysPass , sigResPass)");
  _work->factory("FCONV::signalFail(mass, sigPhysFail , sigResFail)");
  _work->factory(TString::Format("nSigP[%f,10,%f]",_nTotP*0.9,_nTotP*1.55));
  _work->factory(TString::Format("nBkgP[%f,10,%f]",_nTotP*0.1,_nTotP*1.5));
  _work->factory(TString::Format("nSigF[%f,10,%f]",_nTotF*0.9,_nTotF*2.0));
  _work->factory(TString::Format("nBkgF[%f,10,%f]",_nTotF*0.1,_nTotF*1.5));
  _work->factory("SUM::pdfPass(nSigP*signalPass,nBkgP*backgroundPass)");
  _work->factory("SUM::pdfFail(nSigF*signalFail,nBkgF*backgroundFail)");

  _work->Print("t");
}

TCanvas* tnpFitter::fits(bool IsMCsample,string title,bool doCheck) {
  cout << " title : " << title << endl;

  RooAbsPdf *pdfPass = _work->pdf("pdfPass");
  RooAbsPdf *pdfFail = _work->pdf("pdfFail");

  if( IsMCsample ) {
    _work->var("nBkgP")->setVal(0); _work->var("nBkgP")->setConstant();
    _work->var("nBkgF")->setVal(0); _work->var("nBkgF")->setConstant();
    // Make Background into 0
    if( _work->var("peakCMSP") ) {_work->var("peakCMSP")->setVal(-90); _work->var("peakCMSP")->setConstant(); }
    if( _work->var("peakCMSF") ) {_work->var("peakCMSF")->setVal(-90); _work->var("peakCMSF")->setConstant(); }
    if( _work->var("cCMSP") )    {_work->var("cCMSP")->setVal(1);      _work->var("cCMSP")->setConstant();    }
    if( _work->var("cCMSF") )    {_work->var("cCMSF")->setVal(1);      _work->var("cCMSF")->setConstant();    }
    if( _work->var("aExpoP") )   {_work->var("aExpoP")->setVal(0);     _work->var("aExpoP")->setConstant();   }
    if( _work->var("aExpoF") )   {_work->var("aExpoF")->setVal(0);     _work->var("aExpoF")->setConstant();   }
    // MC fitting should be like an Cut&Count (Resolution function should be delta funtion-like.)
    if( _work->var("sigmaGaussP") )  _work->var("sigmaGaussP")->setRange(0, 0.1);
    if( _work->var("sigmaGaussF") )  _work->var("sigmaGaussF")->setRange(0, 0.1);
  }

  /// FC: seems to be better to change the actual range than using a fitRange in the fit itself (???)
  /// FC: I don't know why but the integral is done over the full range in the fit not on the reduced range
  _work->var("mass")->setRange(_xFitMin,_xFitMax);
  _work->var("mass")->setRange("fitMassRange",_xFitMin,_xFitMax);
  RooFitResult* resPass = pdfPass->fitTo(*_work->data("hPass"),Minos(_useMinos),SumW2Error(kTRUE),Save(),Range("fitMassRange"),PrintLevel(-1));
  //RooFitResult* resPass = pdfPass->fitTo(*_work->data("hPass"),Minos(_useMinos),SumW2Error(kTRUE),Save());
  if( _fixSigmaFtoSigmaP ) {
    //_work->var("sigmaF")->setVal( _work->var("sigmaP")->getVal() );
    //_work->var("sigmaF")->setConstant();
  }

  //_work->var("sigmaF")->setVal(_work->var("sigmaP")->getVal());
  //_work->var("sigmaF")->setRange(0.8* _work->var("sigmaP")->getVal(), 3.0* _work->var("sigmaP")->getVal());
  RooFitResult* resFail = pdfFail->fitTo(*_work->data("hFail"),Minos(_useMinos),SumW2Error(kTRUE),Save(),Range("fitMassRange"));
  //RooFitResult* resFail = pdfFail->fitTo(*_work->data("hFail"),Minos(_useMinos),SumW2Error(kTRUE),Save());

  RooPlot *pPass = _work->var("mass")->frame(_xFitMin,_xFitMax);
  RooPlot *pFail = _work->var("mass")->frame(_xFitMin,_xFitMax);
  pPass->SetTitle("passing probe");
  pFail->SetTitle("failing probe");

  _work->data("hPass") ->plotOn( pPass );
  _work->pdf("pdfPass")->plotOn( pPass, LineColor(kRed) );
  _work->pdf("pdfPass")->plotOn( pPass, Components("backgroundPass"),LineColor(kBlue),LineStyle(kDashed));
  _work->data("hPass") ->plotOn( pPass );
  
  _work->data("hFail") ->plotOn( pFail );
  _work->pdf("pdfFail")->plotOn( pFail, LineColor(kRed) );
  _work->pdf("pdfFail")->plotOn( pFail, Components("backgroundFail"),LineColor(kBlue),LineStyle(kDashed));
  _work->data("hFail") ->plotOn( pFail );

  TCanvas c("c","c",1100,450);
  c.Divide(3,1);
  TPad *padText = (TPad*)c.GetPad(1);
  textParForCanvas( resPass,resFail, padText );
  c.cd(2); pPass->Draw();
  double chiPassVal=pPass->chiSquare("pdfPass_Norm[mass]_Range[fit_nll_pdfPass_hPass]_NormRange[fit_nll_pdfPass_hPass]","h_hPass");
  TText chiPass(0.1,0.02,Form("chi^2/n=%f",chiPassVal)); chiPass.SetName("chiPass");chiPass.SetNDC();chiPass.Draw();
  c.cd(3); pFail->Draw();
  double chiFailVal=pFail->chiSquare("pdfFail_Norm[mass]_Range[fit_nll_pdfFail_hFail]_NormRange[fit_nll_pdfFail_hFail]","h_hFail");
  TText chiFail(0.1,0.02,Form("chi^2/n=%f",chiFailVal));chiFail.SetName("chiFail");chiFail.SetNDC();chiFail.Draw();
  _fOut->cd();
  c.Write(TString::Format("%s_Canv",_histname_base.c_str()),TObject::kWriteDelete);
  resPass->Write(TString::Format("%s_resP",_histname_base.c_str()),TObject::kWriteDelete);
  resFail->Write(TString::Format("%s_resF",_histname_base.c_str()),TObject::kWriteDelete);

  if(doCheck) return (TCanvas*)c.Clone();
  else return NULL;
}

/////// Stupid parameter dumper /////////
void tnpFitter::textParForCanvas(RooFitResult *resP, RooFitResult *resF,TPad *p) {

  double eff = -1;
  double e_eff = 0;

  RooRealVar *nSigP = _work->var("nSigP");
  RooRealVar *nSigF = _work->var("nSigF");
  
  double nP   = nSigP->getVal();
  double e_nP = nSigP->getError();
  double nF   = nSigF->getVal();
  double e_nF = nSigF->getError();
  double nTot = nP+nF;
  eff = nP / (nP+nF);
  e_eff = 1./(nTot*nTot) * sqrt( nP*nP* e_nF*e_nF + nF*nF * e_nP*e_nP );

  TPaveText *text1 = new TPaveText(0.05,0.75, 0.95,0.95); //original (0,0.8, 1,1)
  text1->SetFillColor(0);
  text1->SetBorderSize(0);
  text1->SetTextAlign(12);

  text1->AddText(TString::Format("* fit status pass: %d, fail : %d",resP->status(),resF->status()));
  text1->AddText(TString::Format("* eff = %1.4f #pm %1.4f",eff,e_eff));
  text1->SetName("reportTPave");
  //  text->SetTextSize(0.06);

  TPaveText *text = new TPaveText(0.05,0.05, 0.95,0.7); //original (0,0, 1,0.8)
  text->SetFillColor(0);
  text->SetBorderSize(0);
  text->SetTextAlign(12);
  text->AddText("    ---Floating Parameters--- " );
  RooArgList listParFinalP = resP->floatParsFinal();
  for( int ip = 0; ip < listParFinalP.getSize(); ip++ ) {
    TString vName = listParFinalP[ip].GetName();
    text->AddText(TString::Format("   - %s \t= %1.3f #pm %1.3f",
				  vName.Data(),
				  _work->var(vName)->getVal(),
				  _work->var(vName)->getError() ) );
  }

  RooArgList listParFinalF = resF->floatParsFinal();
  for( int ip = 0; ip < listParFinalF.getSize(); ip++ ) {
    TString vName = listParFinalF[ip].GetName();
    text->AddText(TString::Format("   - %s \t= %1.3f #pm %1.3f",
				  vName.Data(),
				  _work->var(vName)->getVal(),
				  _work->var(vName)->getError() ) );
  }

  p->cd();
  text1->Draw();
  text->Draw();
}
