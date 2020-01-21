#include "canvas_margin.h"

void check_chargeAsym(TString DataPeriod = "2016BF", TString eff = "Mu17"){

  TFile *result_plus  = new TFile("won_results_"+DataPeriod+"_"+eff+"_+/result.root");
  TFile *result_minus = new TFile("won_results_"+DataPeriod+"_"+eff+"_-/result.root");
    
  cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies of muons\n\n";
    
  vector<TString> things = {"data", "mc", "SF" };

  for(unsigned int i=0; i<things.size(); i++){

    TString histname = "";
    if(things.at(i) == "SF") histname = "SF_eta_pt"; 
    else histname = "muonEffi_"+things.at(i)+"_eta_pt";

    TH2D *eff_plus = (TH2D*)result_plus->Get(histname);
    TH2D *eff_minus = (TH2D*)result_minus->Get(histname);
    TString name = DataPeriod+"_"+eff+"_"+things.at(i);

    TCanvas *c_effplus = new TCanvas("c_effplus", "", 1200, 800);
    gStyle->SetOptStat(0);
    c_effplus->Draw();
    eff_plus->Draw("colz");
    c_effplus->SaveAs(name+"_plus.png");
    delete c_effplus;

    TCanvas *c_effminus = new TCanvas("c_effminus", "", 1200, 800);
    gStyle->SetOptStat(0);
    c_effminus->cd();
    c_effminus->Draw();
    eff_minus->Draw("colz");
    c_effminus->SaveAs(name+"_minus.png");
    delete c_effminus;

    TCanvas *c_effAsym = new TCanvas("c_effAsym", "", 1200, 800);
    gStyle->SetOptStat(0);
    c_effAsym->cd();
    c_effAsym->Draw();

    eff_plus->Add(eff_minus, -1);
    eff_plus->Draw("colz");
    c_effAsym->SaveAs(name+"_Asym.png");
    delete c_effAsym;
  }
}
