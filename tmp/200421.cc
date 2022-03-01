TCanvas* GetSig(TString path="results/AFBElectronID2016_v2/MediumID_Q"){
  gStyle->SetPaintTextFormat(".1f");
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadRightMargin(0.15);
  gStyle->SetPadBottomMargin(0.15);

  TString fname_plus=path+"Plus/egammaEffi.txt_EGM2D.root";
  TString fname_minus=path+"Minus/egammaEffi.txt_EGM2D.root";
  TFile f_plus(fname_plus);
  TH2F* h_plus=(TH2F*)f_plus.Get("EGamma_SF2D");
  TFile f_minus(fname_minus);
  TH2F* h_minus=(TH2F*)f_minus.Get("EGamma_SF2D");
  
  TH2F* h_sig=(TH2F*)h_plus->Clone("sig");
  h_sig->Reset();
  h_sig->SetMaximum(3);
  h_sig->SetMinimum(-3);
  h_sig->SetDirectory(0);
  for(int i=1;i<=h_sig->GetNbinsX();i++){
    for(int j=1;j<=h_sig->GetNbinsY();j++){
      double v1=h_plus->GetBinContent(i,j);
      double e1=h_plus->GetBinError(i,j);
      double v2=h_minus->GetBinContent(i,j);
      double e2=h_minus->GetBinError(i,j);
      //cout<<i<<" "<<j<<" "<<v1<<" "<<e1<<" "<<v2<<" "<<e2<<" "<<(v1-v2)/sqrt(pow(e1,2)+pow(e2,2))<<endl;
      h_sig->SetBinContent(i,j,(v1-v2)/sqrt(pow(e1,2)+pow(e2,2)));
    }
  }
   
  TCanvas* c=new TCanvas;
  h_sig->SetTitle(path);
  h_sig->SetStats(0);
  h_sig->Draw("text colz");
  gPad->SetLogy();
  h_sig->GetYaxis()->SetMoreLogLabels();
  
  return c;
}
TCanvas* GetDiff(TString path="results/AFBElectronID2016_v2/MediumID_Q"){
  gStyle->SetPaintTextFormat(".2f");
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadRightMargin(0.15);
  gStyle->SetPadBottomMargin(0.15);

  TString fname_plus=path+"Plus/egammaEffi.txt_EGM2D.root";
  TString fname_minus=path+"Minus/egammaEffi.txt_EGM2D.root";
  TFile f_plus(fname_plus);
  TH2F* h_plus=(TH2F*)f_plus.Get("EGamma_SF2D");
  TFile f_minus(fname_minus);
  TH2F* h_minus=(TH2F*)f_minus.Get("EGamma_SF2D");
  
  TH2F* h_sig=(TH2F*)h_plus->Clone("diff");
  h_sig->Reset();
  h_sig->SetMaximum(0.1);
  h_sig->SetMinimum(-0.1);
  h_sig->SetDirectory(0);
  for(int i=1;i<=h_sig->GetNbinsX();i++){
    for(int j=1;j<=h_sig->GetNbinsY();j++){
      double v1=h_plus->GetBinContent(i,j);
      double e1=h_plus->GetBinError(i,j);
      double v2=h_minus->GetBinContent(i,j);
      double e2=h_minus->GetBinError(i,j);
      //cout<<i<<" "<<j<<" "<<v1<<" "<<e1<<" "<<v2<<" "<<e2<<" "<<(v1-v2)/sqrt(pow(e1,2)+pow(e2,2))<<endl;
      h_sig->SetBinContent(i,j,(v1-v2));
    }
  }
   
  TCanvas* c=new TCanvas;
  h_sig->SetTitle(path);
  h_sig->SetStats(0);
  h_sig->Draw("text colz");
  gPad->SetLogy();
  h_sig->GetYaxis()->SetMoreLogLabels();
  
  return c;
}
void SaveSigAll(){
  vector<TString> paths={
    "results/AFBElectronID2016_v2/MediumID_Q",
    "results/AFBElectronID2017_v2/MediumID_Q",
    "results/AFBElectronID2018_v2/MediumID_Q",
    "results/AFBElectronID2016_v2/TightID_Selective_Q",
    "results/AFBElectronID2017_v2/TightID_Selective_Q",
    "results/AFBElectronID2018_v2/TightID_Selective_Q",
    "results/AFBElectronTrigger2016_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele27_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele32_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele32_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele27_TightID_Selective_Q",
    "results/AFBElectronTrigger2017_v2/Ele32_TightID_Selective_Q",
    "results/AFBElectronTrigger2018_v2/Ele32_TightID_Selective_Q",
  };
  for(auto path:paths){
    TCanvas *c=GetSig(path);
    c->SaveAs("plot/sig_"+path.ReplaceAll("/","_")+".png");
    delete c;
  }
}
    
void SaveDiffAll(){
  vector<TString> paths={
    "results/AFBElectronID2016_v2/MediumID_Q",
    "results/AFBElectronID2017_v2/MediumID_Q",
    "results/AFBElectronID2018_v2/MediumID_Q",
    "results/AFBElectronID2016_v2/TightID_Selective_Q",
    "results/AFBElectronID2017_v2/TightID_Selective_Q",
    "results/AFBElectronID2018_v2/TightID_Selective_Q",
    "results/AFBElectronTrigger2016_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele23Leg1_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele12Leg2_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele27_MediumID_Q",
    "results/AFBElectronTrigger2017_v2/Ele32_MediumID_Q",
    "results/AFBElectronTrigger2018_v2/Ele32_MediumID_Q",
    "results/AFBElectronTrigger2016_v2/Ele27_TightID_Selective_Q",
    "results/AFBElectronTrigger2017_v2/Ele32_TightID_Selective_Q",
    "results/AFBElectronTrigger2018_v2/Ele32_TightID_Selective_Q",
  };
  for(auto path:paths){
    TCanvas *c=GetDiff(path);
    c->SaveAs("plot/diff_"+path.ReplaceAll("/","_")+".png");
    delete c;
  }
}
    
TH1D* sigma(){
  TString fpipe=gSystem->GetFromPipe("find results/*v2 -maxdepth 3 -type f -name 'data*nominalFit.root'");
  TObjArray* list=fpipe.Tokenize("\n");
  TH1D* h=new TH1D("sigma","sigma",120,-1,5);
  int total=0;
  int p1=0;
  h->SetDirectory(0);
  for(auto l:*list){
    TString filename=((TObjString*)l)->GetString();
    TFile f(filename);
    for(auto key:*f.GetListOfKeys()){
      TString name=key->GetName();
      if(name.Contains("_res")){
	TString PF=name[name.Length()-1];
	RooFitResult* result=(RooFitResult*)f.Get(name);
	RooRealVar* sigma=(RooRealVar*)result->floatParsFinal().find("sigma"+PF);
	double val=sigma->getVal();
	if(fabs(val-0.5)<0.000001) continue; // below trigger threshold
	if(fabs(val-sigma->getMin())<0.001){
	  cout<<filename<<" "<<name<<" "<<val<<" "<<sigma->getMin()<<" "<<sigma->getMax()<<endl;
	  p1++;
	}
	total++;
	h->Fill(val);
      }
    }
  }
  h->Draw();
  cout<<p1<<"/"<<total<<endl;
  return h;
}
TH1D* mean(){
  TString fpipe=gSystem->GetFromPipe("find results/*v2 -maxdepth 3 -type f -name 'data*nominalFit.root'");
  TObjArray* list=fpipe.Tokenize("\n");
  TH1D* h=new TH1D("mean","mean",150,-3,3);
  int total=0;
  int p1=0;
  h->SetDirectory(0);
  for(auto l:*list){
    TString filename=((TObjString*)l)->GetString();
    TFile f(filename);
    for(auto key:*f.GetListOfKeys()){
      TString name=key->GetName();
      if(name.Contains("_res")){
	TString PF=name[name.Length()-1];
	RooFitResult* result=(RooFitResult*)f.Get(name);
	RooRealVar* sigma=(RooRealVar*)result->floatParsFinal().find("mean"+PF);
	double val=sigma->getVal();
	if(fabs(val)<0.000001) continue; // below trigger threshold
	if(fabs(val-sigma->getMin())<0.001){
	  cout<<filename<<" "<<name<<" "<<val<<" "<<sigma->getMin()<<" "<<sigma->getMax()<<endl;
	  p1++;
	}
	total++;
	h->Fill(val);
      }
    }
  }
  h->Draw();
  return h;
}
void MakeLink(){
  TString fpipe=gSystem->GetFromPipe("find results/*v2 -maxdepth 1 -mindepth 1 -type d|sed 's@results/@@'|sort -V");
  TObjArray* list=fpipe.Tokenize("\n");
  TString prefix="https://hyseo.web.cern.ch/hyseo/tnp/";
  for(auto l:*list){
    TString path=((TObjString*)l)->GetString();
    cout<<path<<endl;
    cout<<"<a href=\""+prefix+path+"/egammaEffi.txt_egammaPlots.pdf\">pdf</a> ";
    cout<<"<a href=\""+prefix+path+"/egammaEffi.txt_EGM2D.root\">root</a> ";
    cout<<"<a href=\""+prefix+path+"/plots\">plots</a> ";
    cout<<" <br> "<<endl;
  }
}
