#include "canvas_margin.h"

void plotter(TString DataPeriod = "2017", TString eff = "IDISO_factorize", TString Charge = "total"){

  vector<double> eta = { -2.4, -2.1, -1.85, -1.6, -1.4, -1.2, -0.9, -0.6, -0.3, -0.2, 0., 0.2, 0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 1.85, 2.1, 2.4 };
  vector<double> pt = {10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 120 };
  if(eff == "Mu17") pt = { 10, 15, 16, 17, 18, 19, 20, 25, 30, 35, 40, 45, 50, 60, 120 };
  else if(eff == "IsoMu24" && DataPeriod == "2017") pt = {10, 15, 20, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50, 60, 120 };
  else if(eff == "IsoMu24" && DataPeriod != "2017") pt = {10, 15, 20, 22, 23, 24, 25, 26, 27, 30, 35, 40, 45, 50, 60, 120 };
  vector<TString> charge = {"+", "-"};
  if(Charge == "+") charge = {"+"};
  else if(Charge == "-") charge = {"-"};

  for(unsigned int i_charge = 0; i_charge<charge.size(); i_charge++){
  
    TFile *result = new TFile("won_results_"+DataPeriod+"_"+eff+"_"+charge.at(i_charge)+"/result.root");
    TFile *result_stat = new TFile("won_results_"+DataPeriod+"_"+eff+"_"+charge.at(i_charge)+"/result_stat.root");
    TFile *result_syst = new TFile("won_results_"+DataPeriod+"_"+eff+"_"+charge.at(i_charge)+"/result_syst.root");
    
    //### Draw the Eff vs pT plots of Data, MC #######################
    cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies of "+charge.at(i_charge)+"muons\n\n";
    for(unsigned int i_eta = 0; i_eta<eta.size()-1; i_eta++){
    
      TString data_name = "data_eta"+TString::Format("%.2f",eta.at(i_eta))+"to"+TString::Format("%.2f",eta.at(i_eta+1)); 
      TString mc_name = "mc_eta"+TString::Format("%.2f",eta.at(i_eta))+"to"+TString::Format("%.2f",eta.at(i_eta+1));

      TH1D *eff_data = (TH1D*)result->Get(data_name);
      TH1D *eff_mc = (TH1D*)result->Get(mc_name);
      TH1D *eff_data_stat = (TH1D*)result_stat->Get(data_name);
      TH1D *eff_mc_stat = (TH1D*)result_stat->Get(mc_name);
      TH1D *eff_data_syst = (TH1D*)result_syst->Get(data_name);
      TH1D *eff_mc_syst = (TH1D*)result_syst->Get(mc_name);

      TCanvas *c_eff = new TCanvas("c_eff", "", 800, 800);
      c_eff->Draw();
      TPad *c1_up = new TPad("c1_up", "", 0, 0.25, 1, 1);
      TPad *c1_down = new TPad("c1_down", "", 0, 0, 1, 0.25);
      canvas_margin(c_eff,c1_up,c1_down);
      c1_down->SetGridx();
      c1_down->SetGridy();
      c1_up->Draw();
      c1_down->Draw();

      c1_up->cd();
      eff_data_stat->SetLineColor(kBlack);
      eff_data_stat->SetMarkerColor(kBlack);
      eff_data_stat->SetMarkerStyle(21);
      eff_data_stat->SetMarkerSize(1);
      eff_mc_stat->SetLineColor(kBlue);
      eff_mc_stat->SetMarkerColor(kBlue);
      eff_mc_stat->SetMarkerStyle(21);
      eff_mc_stat->SetMarkerSize(1);

      eff_data_syst->SetFillColorAlpha(kRed, 0.35);
      eff_data_syst->SetFillStyle(3244);
      eff_mc_syst->SetFillColorAlpha(kGreen+2, 0.5);
      eff_mc_syst->SetFillStyle(3244);

      eff_data_stat->Draw("p");
      eff_mc_stat->Draw("psame");  
      //eff_data_syst->Draw("E2same");
      //eff_mc_syst->Draw("E2same");

      TLegend *lg = new TLegend(0.6, 0.1, 0.9, 0.3);
      lg->SetFillStyle(0);
      lg->SetBorderSize(0);
      lg->AddEntry(eff_data_stat, "Run "+DataPeriod, "lp");
      lg->AddEntry(eff_mc_stat, "MC", "lp");
      lg->Draw();

      eff_data_stat->SetTitle("");
      eff_data_stat->GetYaxis()->SetTitle("Efficiency");
      eff_data_stat->GetYaxis()->SetRangeUser(0.0, 1.1);

      c1_down->cd();
    
      TH1D *ratio = (TH1D*)eff_data_stat->Clone();
      ratio->Divide(eff_mc_stat);
      ratio->SetLineWidth(2);
      ratio->SetLineColor(kBlack);
      ratio->SetMarkerColor(kBlack);
      ratio->SetMarkerStyle(20);
      ratio->SetMarkerSize(1.6);
      ratio->Draw("p");
      ratio->GetXaxis()->SetTitle("p_{T}(#mu^{"+charge.at(i_charge)+"}) [GeV]");
      ratio->GetYaxis()->SetTitle("Data/MC");
      ratio->GetYaxis()->SetRangeUser(0.9, 1.1);

      hist_axis(eff_data_stat, ratio);

      TLine line(pt.at(0), 1, 120, 1);
      line.SetLineWidth(1);
      line.SetLineColor(kRed);
      line.DrawClone("SAME");

      c_eff->cd();
      TLatex latex_CMSPriliminary, latex_Lumi, latex_etacut, latex_selection;
      latex_CMSPriliminary.SetNDC();
      latex_Lumi.SetNDC();
      latex_etacut.SetNDC();
      latex_selection.SetNDC();

      latex_CMSPriliminary.SetTextSize(0.045);
      latex_CMSPriliminary.DrawLatex(0.09, 0.965, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}");
      latex_Lumi.SetTextSize(0.03);
      //latex_Lumi.DrawLatex(0.73, 0.965, "45.39 fb^{-1} (13 TeV)");
      latex_Lumi.DrawLatex(0.73, 0.965, "Run "+DataPeriod+" (13 TeV)");
      latex_etacut.SetTextSize(0.03);
      latex_etacut.DrawLatex(0.73, 0.92, TString::Format("%0.2f",eta.at(i_eta))+" < eta < "+TString::Format("%.2f",eta.at(i_eta+1)));
      latex_selection.SetTextSize(0.05); //original size 0.03 and position (0.125,0.92)
      latex_selection.DrawLatex(0.14, 0.90, eff+" Efficiency");
      //latex_selection.DrawLatex(0.14, 0.90, "IDISO Efficiency");

      TString name = "Plots/"+DataPeriod+"_"+eff+"_"+charge.at(i_charge)+"_eta"+TString::Format("%d",i_eta)+"_"+TString::Format("%.2f",eta.at(i_eta))+"to"+TString::Format("%.2f",eta.at(i_eta+1));
      c_eff->SaveAs(name+".pdf");
      delete c_eff;
    }

    //### Draw the Eff vs eta plots of Data, MC #######################
    for(unsigned int i_pt = 0; i_pt<pt.size()-1; i_pt++){
    
      TString data_name = "data_pt"+TString::Format("%.0f",pt.at(i_pt))+"to"+TString::Format("%.0f",pt.at(i_pt+1)); 
      TString mc_name = "mc_pt"+TString::Format("%.0f",pt.at(i_pt))+"to"+TString::Format("%.0f",pt.at(i_pt+1));

      TH1D *eff_data = (TH1D*)result->Get(data_name);
      TH1D *eff_mc = (TH1D*)result->Get(mc_name);
      TH1D *eff_data_stat = (TH1D*)result_stat->Get(data_name);
      TH1D *eff_mc_stat = (TH1D*)result_stat->Get(mc_name);
      TH1D *eff_data_syst = (TH1D*)result_syst->Get(data_name);
      TH1D *eff_mc_syst = (TH1D*)result_syst->Get(mc_name);

      TCanvas *c_eff = new TCanvas("c_eff", "", 800, 800);
      c_eff->Draw();
      TPad *c1_up = new TPad("c1_up", "", 0, 0.25, 1, 1);
      TPad *c1_down = new TPad("c1_down", "", 0, 0, 1, 0.25);
      canvas_margin(c_eff,c1_up,c1_down);
      c1_down->SetGridx();
      c1_down->SetGridy();
      c1_up->Draw();
      c1_down->Draw();

      c1_up->cd();
      eff_data_stat->SetLineColor(kBlack);
      eff_data_stat->SetMarkerColor(kBlack);
      eff_data_stat->SetMarkerStyle(21);
      eff_data_stat->SetMarkerSize(1);
      eff_mc_stat->SetLineColor(kBlue);
      eff_mc_stat->SetMarkerColor(kBlue);
      eff_mc_stat->SetMarkerStyle(21);
      eff_mc_stat->SetMarkerSize(1);

      eff_data_syst->SetFillColorAlpha(kRed, 0.35);
      eff_data_syst->SetFillStyle(3244);
      eff_mc_syst->SetFillColorAlpha(kGreen+2, 0.5);
      eff_mc_syst->SetFillStyle(3244);

      eff_data_stat->GetXaxis()->SetRangeUser(-3.0, 3.0);
      eff_data_stat->Draw("p");
      eff_mc_stat->Draw("psame");  
      //eff_data_syst->Draw("E2same");
      //eff_mc_syst->Draw("E2same");

      TLegend *lg = new TLegend(0.6, 0.1, 0.9, 0.3);
      lg->SetFillStyle(0);
      lg->SetBorderSize(0);
      lg->AddEntry(eff_data_stat, "Run "+DataPeriod, "lp");
      lg->AddEntry(eff_mc_stat, "MC", "lp");
      lg->Draw();

      eff_data_stat->SetTitle("");
      eff_data_stat->GetYaxis()->SetTitle("Efficiency");
      eff_data_stat->GetYaxis()->SetRangeUser(0.6, 1.1);
      c1_down->cd();
    
      TH1D *ratio = (TH1D*)eff_data_stat->Clone();
      ratio->Divide(eff_mc_stat);
      ratio->SetLineWidth(2);
      ratio->SetLineColor(kBlack);
      ratio->SetMarkerColor(kBlack);
      ratio->SetMarkerStyle(20);
      ratio->SetMarkerSize(1.6);
      ratio->GetXaxis()->SetRangeUser(-3.0, 3.0);
      ratio->Draw("p");
      ratio->GetXaxis()->SetTitle("#eta(#mu^{"+charge.at(i_charge)+"})");
      ratio->GetYaxis()->SetTitle("Data/MC");
      ratio->GetYaxis()->SetRangeUser(0.9, 1.1);

      hist_axis(eff_data_stat, ratio);

      TLine line(-2.65, 1, 2.7, 1);
      line.SetLineWidth(1);
      line.SetLineColor(kRed);
      line.DrawClone("SAME");

      c_eff->cd();
      TLatex latex_CMSPriliminary, latex_Lumi, latex_ptcut, latex_selection;
      latex_CMSPriliminary.SetNDC();
      latex_Lumi.SetNDC();
      latex_ptcut.SetNDC();
      latex_selection.SetNDC();

      latex_CMSPriliminary.SetTextSize(0.045);
      latex_CMSPriliminary.DrawLatex(0.09, 0.965, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}");
      latex_Lumi.SetTextSize(0.03);
      //latex_Lumi.DrawLatex(0.73, 0.965, "45.39 fb^{-1} (13 TeV)");
      latex_Lumi.DrawLatex(0.73, 0.965, "Run "+DataPeriod+" (13 TeV)");
      latex_ptcut.SetTextSize(0.03);
      latex_ptcut.DrawLatex(0.73, 0.92, TString::Format("%.0f",pt.at(i_pt))+" < p_{T} < "+TString::Format("%.0f",pt.at(i_pt+1))+" [GeV]");
      latex_selection.SetTextSize(0.05); //original size 0.03 and position (0.125,0.92)
      latex_selection.DrawLatex(0.14, 0.90, eff+" Efficiency");
      //latex_selection.DrawLatex(0.14, 0.90, "IDISO Efficiency");
      
      TString name = "Plots/"+DataPeriod+"_"+eff+"_"+charge.at(i_charge)+"_pt"+TString::Format("%d",i_pt)+"_"+TString::Format("%.2f",pt.at(i_pt))+"to"+TString::Format("%.2f",pt.at(i_pt+1));
      c_eff->SaveAs(name+".pdf");
      delete c_eff;
    }
  } //Charge loop ends here.

  //If Charge inclusive, compare the difference between -u and +u. (Eff vs eTa)
  if(Charge == "total"){

    vector<TString> data = {"data", "mc"};

    TFile *result_plus = new TFile("won_results_"+DataPeriod+"_"+eff+"_+/result.root");
    TFile *result_minus = new TFile("won_results_"+DataPeriod+"_"+eff+"_-/result.root");
    TFile *result_stat_plus = new TFile("won_results_"+DataPeriod+"_"+eff+"_+/result_stat.root");
    TFile *result_stat_minus = new TFile("won_results_"+DataPeriod+"_"+eff+"_-/result_stat.root");
    TFile *result_syst_plus = new TFile("won_results_"+DataPeriod+"_"+eff+"_+/result_syst.root");
    TFile *result_syst_minus = new TFile("won_results_"+DataPeriod+"_"+eff+"_-/result_syst.root");

    for(unsigned int i_data = 0; i_data<data.size(); i_data++){
      cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies between +muons and -muons of "+data.at(i_data)+"\n\n";
      for(unsigned int i_pt = 0; i_pt<pt.size()-1; i_pt++){
    
        TString data_name = data.at(i_data)+"_pt"+TString::Format("%.0f",pt.at(i_pt))+"to"+TString::Format("%.0f",pt.at(i_pt+1)); 

        TH1D *eff_plus = (TH1D*)result_plus->Get(data_name);
        TH1D *eff_minus = (TH1D*)result_minus->Get(data_name);
        TH1D *eff_stat_plus = (TH1D*)result_stat_plus->Get(data_name);
        TH1D *eff_stat_minus = (TH1D*)result_stat_minus->Get(data_name);
        TH1D *eff_syst_plus = (TH1D*)result_syst_plus->Get(data_name);
        TH1D *eff_syst_minus = (TH1D*)result_syst_minus->Get(data_name);

        TCanvas *c_eff = new TCanvas("c_eff", "", 800, 800);
        c_eff->Draw();
        TPad *c1_up = new TPad("c1_up", "", 0, 0.25, 1, 1);
        TPad *c1_down = new TPad("c1_down", "", 0, 0, 1, 0.25);
        canvas_margin(c_eff,c1_up,c1_down);
        c1_down->SetGridx();
        c1_down->SetGridy();
        c1_up->Draw();
        c1_down->Draw();

        c1_up->cd();
        eff_stat_plus->SetLineColor(kBlack);
        eff_stat_plus->SetMarkerColor(kBlack);
        eff_stat_plus->SetMarkerStyle(21);
        eff_stat_plus->SetMarkerSize(1);
        eff_stat_minus->SetLineColor(kBlue);
        eff_stat_minus->SetMarkerColor(kBlue);
        eff_stat_minus->SetMarkerStyle(21);
        eff_stat_minus->SetMarkerSize(1);

        eff_syst_plus->SetFillColorAlpha(kRed, 0.35);
        eff_syst_plus->SetFillStyle(3244);
        eff_syst_minus->SetFillColorAlpha(kGreen+2, 0.5);
        eff_syst_minus->SetFillStyle(3244);

        eff_stat_plus->GetXaxis()->SetRangeUser(-3.0, 3.0);
        eff_stat_plus->Draw("p");
        eff_stat_minus->Draw("psame");  
        //eff_syst_plus->Draw("E2same");
        //eff_syst_minus->Draw("E2same");

        TLegend *lg = new TLegend(0.6, 0.1, 0.9, 0.3);
        lg->SetFillStyle(0);
        lg->SetBorderSize(0);
        lg->AddEntry(eff_stat_plus, data.at(i_data)+" + #mu     ", "lp");
        lg->AddEntry(eff_stat_minus, data.at(i_data)+" - #mu     ", "lp");
        lg->Draw();

        eff_stat_plus->SetTitle("");
        eff_stat_plus->GetYaxis()->SetTitle("Efficiency");
        eff_stat_plus->GetYaxis()->SetRangeUser(0.6, 1.1);

        c1_down->cd();
    
        TH1D *ratio = (TH1D*)eff_stat_plus->Clone();
        ratio->Divide(eff_stat_minus);
        ratio->SetLineWidth(2);
        ratio->SetLineColor(kBlack);
        ratio->SetMarkerColor(kBlack);
        ratio->SetMarkerStyle(20);
        ratio->SetMarkerSize(1.6);
        ratio->GetXaxis()->SetRangeUser(-3.0, 3.0);
        ratio->Draw("p");
        ratio->GetXaxis()->SetTitle("#eta(#mu)");
        ratio->GetYaxis()->SetTitle("+/-");
        ratio->GetYaxis()->SetRangeUser(0.95, 1.05);

        hist_axis(eff_stat_plus, ratio);

        TLine line(-2.65, 1, 2.7, 1);
        line.SetLineWidth(1);
        line.SetLineColor(kRed);
        line.DrawClone("SAME");

        c_eff->cd();
        TLatex latex_CMSPriliminary, latex_Lumi, latex_ptcut, latex_selection;
        latex_CMSPriliminary.SetNDC();
        latex_Lumi.SetNDC();
        latex_ptcut.SetNDC();
        latex_selection.SetNDC();

        latex_CMSPriliminary.SetTextSize(0.045);
        latex_CMSPriliminary.DrawLatex(0.09, 0.965, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}");
        latex_Lumi.SetTextSize(0.03);
        latex_Lumi.DrawLatex(0.73, 0.965, "45.39 fb^{-1} (13 TeV)");
        latex_ptcut.SetTextSize(0.03);
        latex_ptcut.DrawLatex(0.73, 0.92, TString::Format("%.0f",pt.at(i_pt))+" < p_{T} < "+TString::Format("%.0f",pt.at(i_pt+1))+" [GeV]");
        latex_selection.SetTextSize(0.03);
        latex_selection.DrawLatex(0.125, 0.92, eff+" Efficiency");

        TString name = "Plots/"+DataPeriod+"_"+eff+"_chargedep_"+data.at(i_data)+"_pt"+TString::Format("%d",i_pt)+"_"+TString::Format("%.2f",pt.at(i_pt))+"to"+TString::Format("%.2f",pt.at(i_pt+1));
        c_eff->SaveAs(name+".png");
        delete c_eff;
      }
    }
  } // data, MC loop ends here.
}    
    
