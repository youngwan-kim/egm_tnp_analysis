#include"TH1D.h"
#include"TChain.h"
#include"TSystem.h"
#include"TTreeFormula.h"
#include"TFile.h"
#include<iostream>

map<TString,TH1D*> hists;
vector<TString> Split(TString s,TString del){
  TObjArray* array=s.Tokenize(del);
  vector<TString> out;
  for(const auto& obj:*array){
    out.push_back(((TObjString*)obj)->String());
  }
  array->Delete();
  return out;
}
void FillHist(TString histname, double value, double weight, int n_bin, double x_min, double x_max){
  auto it = hists.find(histname);
  TH1D* hist=NULL;
  if( it==hists.end() ){
    hist = new TH1D(histname, "", n_bin, x_min, x_max);
    hists[histname] = hist;
  }else hist=it->second;
  hist->Fill(value, weight);
}
void loop(TString dir,TString outfile,TString eventweight,int njob=1,int ijob=0){
  vector<TString> files=Split(gSystem->GetFromPipe("find "+dir+" -type f -name '*.root'|sort"),"\n");
  TChain *tree=new TChain("tpTree/fitter_tree");
  int stepsize=files.size()/njob+1;
  for(int i=stepsize*ijob;i<stepsize*(ijob+1);i++) 
    if(files[i].EndsWith(".root")) 
      tree->Add(files[i]);

  TTreeFormula* formula=new TTreeFormula("eventweight",eventweight,tree);
  tree->SetNotify(formula);
  
  float mass,;
  int PF,Glb,TM;
  tree->SetBranchAddress("mass",&mass);
  tree->SetBranchAddress("PF",&PF);
  
  int nevent=tree->GetEntries();
  for(int i=0;i<nevent;i++){
    if(i%50000==0) cout<<i<<"/"<<nevent<<endl;
    tree->GetEntry(i);
    if(formula->EvalInstance()){
      FillHist("mass",mass,formula->EvalInstance(),80,50,130);
    }
  }
    
  TFile fout(Form("%s.%d.%d",outfile.Data(),njob,ijob),"recreate");
  for(auto it=hists.begin();it!=hists.end();it++){
    TH1D* hist=it->second;
    hist->Write();
  }
  fout.Close();
}
void Loop(TString dir,TString outfile,TString eventweight,int njob=1){
  //system("echo -e \".L etc/scripts/loop.cc+\\n.q\"|root -l -b");
  TString cmd="export ROOT_HIST=0;";
  for(int i=0;i<njob;i++){
    cmd+="condor_run 'echo -e \".L etc/scripts/loop.cc+\\nloop(\\\""+dir+"\\\",\\\""+outfile+"\\\",\\\""+eventweight+Form("\\\",%d,%d",njob,i)+")\" |root -l -b' & ";
  }
  cmd+=" wait;";
  system(cmd);
  
  system("hadd -f "+outfile+" "+outfile+Form(".%d.*",njob));
  system("rm "+outfile+Form(".%d.*",njob));
}
void LoopAll(int njob=1){
  Loop("/gv0/Users/hsseo/MuonTnP/2018/data/SingleMuon/","data.root","tag_IsoMu24&&tag_pt>26&&tag_combRelIsoPF04dBeta<0.15&&pair_probeMultiplicity==1&&!Medium&&pt<20&&pt>10",njob);
  Loop("/gv0/Users/hsseo/MuonTnP/2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/","mg.root","tag_IsoMu24&&tag_pt>26&&tag_combRelIsoPF04dBeta<0.15&&pair_probeMultiplicity==1&&!Medium&&pt<20&&pt>10&&mcTrue",njob);
}
