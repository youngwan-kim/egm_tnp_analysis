#include "canvas_margin.h"

void plotter(TString DataPeriod = "2017", TString eff = "IsoMu24", TString Charge = "total"){

  bool DoDrawSF_pT = true;
  bool DoDrawSF_eta = true;
  bool DoDrawChargeAsym = true;
  bool DoSystematicStudy = true;

  if(eff == "IsoMu24" && DataPeriod == "2017") eff = "IsoMu27";
  vector<double> eta = { -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1.1, -1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4 };
  vector<double> pt = {10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 120 };
  if(eff == "Mu17") pt = { 20, 25, 30, 35, 40, 45, 50, 60, 120 };
  else if(eff == "IsoMu27") pt = {29, 32, 35, 40, 45, 50, 60, 120 };
  else if(eff == "IsoMu24") pt = {26, 30, 35, 40, 45, 50, 60, 120 };
  vector<TString> charge = {"+", "-"};
  if(Charge == "+") charge = {"+"};
  else if(Charge == "-") charge = {"-"};

  TString workingDir = DataPeriod+"_"+eff;

  for(unsigned int i_charge = 0; i_charge<charge.size(); i_charge++){
  
    TFile *result = new TFile(workingDir+"_"+charge.at(i_charge)+"/result.root");
    TFile *result_stat = new TFile(workingDir+"_"+charge.at(i_charge)+"/result_stat.root");
    TFile *result_syst = new TFile(workingDir+"_"+charge.at(i_charge)+"/result_syst.root");

    //############################################
    //### Draw the Eff vs pT plots of Data, MC ###
    //############################################
    cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies of "+charge.at(i_charge)+"muons as a function of pT\n\n";
    for(unsigned int i_eta = 0; i_eta<eta.size()-1; i_eta++){

      if(!DoDrawSF_pT) break;
    
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
      eff_data_syst->Draw("E2same");
      eff_mc_syst->Draw("E2same");

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

      TString plotDir = workingDir+"_"+charge.at(i_charge)+"/Plots/Eff_vs_pT/";
      gSystem->mkdir(plotDir,kTRUE);
      TString name = plotDir+"eta"+TString::Format("%d",i_eta)+"_"+TString::Format("%.2f",eta.at(i_eta))+"to"+TString::Format("%.2f",eta.at(i_eta+1));
      c_eff->SaveAs(name+".png");
      delete c_eff;
    }

    //#############################################
    //### Draw the Eff vs eta plots of Data, MC ###
    //#############################################
    cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies of "+charge.at(i_charge)+"muons as a function of eta\n\n";
    for(unsigned int i_pt = 0; i_pt<pt.size()-1; i_pt++){
    
      if(!DoDrawSF_eta) break;

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
      eff_data_syst->Draw("E2same");
      eff_mc_syst->Draw("E2same");

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
      
      TString plotDir = workingDir+"_"+charge.at(i_charge)+"/Plots/Eff_vs_eta/";
      gSystem->mkdir(plotDir,kTRUE);
      TString name = plotDir+"pt"+TString::Format("%d",i_pt)+"_"+TString::Format("%.2f",pt.at(i_pt))+"to"+TString::Format("%.2f",pt.at(i_pt+1));
      c_eff->SaveAs(name+".png");
      delete c_eff;
    }
  } //Charge loop ends here.

  //###################################
  //### Efficiency Charge Asymmetry ###
  //###################################
  //If Charge inclusive, compare the difference between -u and +u.
  if(Charge == "total"){

    vector<TString> data = {"data", "mc"};

    TFile *result_plus = new TFile(workingDir+"_+/result.root");
    TFile *result_minus = new TFile(workingDir+"_-/result.root");
    TFile *result_stat_plus = new TFile(workingDir+"_+/result_stat.root");
    TFile *result_stat_minus = new TFile(workingDir+"_-/result_stat.root");
    TFile *result_syst_plus = new TFile(workingDir+"_+/result_syst.root");
    TFile *result_syst_minus = new TFile(workingDir+"_-/result_syst.root");

    for(unsigned int i_data = 0; i_data<data.size(); i_data++){

      if(!DoDrawChargeAsym) break;
      cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Charge Asymmetry of efficiencies between +muons and -muons of "+data.at(i_data)+" as a function of eta\n\n";
      TString plotDir = workingDir+"_+/Plots/Eff_ChargeAsym/"+data.at(i_data)+"/";
      gSystem->mkdir(plotDir,kTRUE);

      // Charge Asym vs. eta
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
        eff_stat_minus->SetLineColor(kGreen+2);
        eff_stat_minus->SetMarkerColor(kGreen+2);
        eff_stat_minus->SetMarkerStyle(21);
        eff_stat_minus->SetMarkerSize(1);

        eff_syst_plus->SetFillColorAlpha(kRed, 0.35);
        eff_syst_plus->SetFillStyle(3244);
        eff_syst_minus->SetFillColorAlpha(kBlue, 0.5);
        eff_syst_minus->SetFillStyle(3244);

        eff_stat_plus->Draw("p");
        eff_stat_minus->Draw("psame");  
        eff_syst_plus->Draw("E2same");
        eff_syst_minus->Draw("E2same");

        TLegend *lg = new TLegend(0.6, 0.1, 0.9, 0.3);
        lg->SetFillStyle(0);
        lg->SetBorderSize(0);
        lg->AddEntry(eff_stat_plus, data.at(i_data)+" + #mu     ", "lp");
        lg->AddEntry(eff_stat_minus, data.at(i_data)+" - #mu     ", "lp");
        lg->Draw();

        eff_stat_plus->SetTitle("");
        eff_stat_plus->GetYaxis()->SetTitle("Efficiency");
        eff_stat_plus->GetYaxis()->SetRangeUser(0.5, 1.1);

        c1_down->cd();
    
        TH1D *ratio = (TH1D*)eff_stat_plus->Clone();
        ratio->Divide(eff_stat_minus);
        ratio->SetLineWidth(2);
        ratio->SetLineColor(kBlack);
        ratio->SetMarkerColor(kBlack);
        ratio->SetMarkerStyle(20);
        ratio->SetMarkerSize(1.6);
        ratio->Draw("p");
        ratio->GetXaxis()->SetTitle("#eta(#mu)");
        ratio->GetYaxis()->SetTitle("+/-");
        ratio->GetYaxis()->SetRangeUser(0.9, 1.1);

        hist_axis(eff_stat_plus, ratio);

        TLine line(-2.4, 1, 2.4, 1);
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

        TString name = plotDir+"pt"+TString::Format("%d",i_pt)+"_"+TString::Format("%.1f",pt.at(i_pt))+"to"+TString::Format("%.1f",pt.at(i_pt+1));
        c_eff->SaveAs(name+".png");
        delete c_eff;
      }

      // Charge Asym vs. pT
      for(unsigned int i_eta = 0; i_eta<eta.size()-1; i_eta++){
    
        TString data_name = data.at(i_data)+"_eta"+TString::Format("%.2f",eta.at(i_eta))+"to"+TString::Format("%.2f",eta.at(i_eta+1)); 

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
        eff_stat_minus->SetLineColor(kGreen+2);
        eff_stat_minus->SetMarkerColor(kGreen+2);
        eff_stat_minus->SetMarkerStyle(21);
        eff_stat_minus->SetMarkerSize(1);

        eff_syst_plus->SetFillColorAlpha(kRed, 0.35);
        eff_syst_plus->SetFillStyle(3244);
        eff_syst_minus->SetFillColorAlpha(kBlue, 0.5);
        eff_syst_minus->SetFillStyle(3244);

        eff_stat_plus->Draw("p");
        eff_stat_minus->Draw("psame");  
        eff_syst_plus->Draw("E2same");
        eff_syst_minus->Draw("E2same");

        TLegend *lg = new TLegend(0.6, 0.1, 0.9, 0.3);
        lg->SetFillStyle(0);
        lg->SetBorderSize(0);
        lg->AddEntry(eff_stat_plus, data.at(i_data)+" + #mu     ", "lp");
        lg->AddEntry(eff_stat_minus, data.at(i_data)+" - #mu     ", "lp");
        lg->Draw();

        eff_stat_plus->SetTitle("");
        eff_stat_plus->GetYaxis()->SetTitle("Efficiency");
        eff_stat_plus->GetYaxis()->SetRangeUser(0.5, 1.1);

        c1_down->cd();
    
        TH1D *ratio = (TH1D*)eff_stat_plus->Clone();
        ratio->Divide(eff_stat_minus);
        ratio->SetLineWidth(2);
        ratio->SetLineColor(kBlack);
        ratio->SetMarkerColor(kBlack);
        ratio->SetMarkerStyle(20);
        ratio->SetMarkerSize(1.6);
        ratio->Draw("p");
        ratio->GetXaxis()->SetTitle("p_{T}(#mu) [GeV]");
        ratio->GetYaxis()->SetTitle("+/-");
        ratio->GetYaxis()->SetRangeUser(0.9, 1.1);

        hist_axis(eff_stat_plus, ratio);

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
        latex_Lumi.DrawLatex(0.73, 0.965, "45.39 fb^{-1} (13 TeV)");
        latex_etacut.SetTextSize(0.03);
        latex_etacut.DrawLatex(0.73, 0.92, TString::Format("%.1f",eta.at(i_eta))+" < eta < "+TString::Format("%.1f",eta.at(i_eta+1)));
        latex_selection.SetTextSize(0.03);
        latex_selection.DrawLatex(0.125, 0.92, eff+" Efficiency");

        TString name = plotDir+"eta"+TString::Format("%d",i_eta)+"_"+TString::Format("%.1f",eta.at(i_eta))+"to"+TString::Format("%.1f",eta.at(i_eta+1));
        c_eff->SaveAs(name+".png");
        delete c_eff;
      }
    } // data, MC loop ends here.
    
    // 2D Charge Asym
    cout<<"\nInputs : DataPeriod = "+DataPeriod+", "+eff+" Efficiencies of muons\n\n";
    vector<TString> things = {"data", "mc", "SF" };
    TString plotDir = workingDir+"_+/Plots/Eff_ChargeAsym/";

    for(unsigned int i=0; i<things.size(); i++){

      if(!DoDrawChargeAsym) break;
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
      c_effplus->SaveAs(plotDir+"2D_"+things.at(i)+"_plus.png");
      delete c_effplus;

      TCanvas *c_effminus = new TCanvas("c_effminus", "", 1200, 800);
      gStyle->SetOptStat(0);
      c_effminus->cd();
      c_effminus->Draw();
      eff_minus->Draw("colz");
      c_effminus->SaveAs(plotDir+"2D_"+things.at(i)+"_minus.png");
      delete c_effminus;

      TCanvas *c_effAsym = new TCanvas("c_effAsym", "", 1200, 800);
      gStyle->SetOptStat(0);
      c_effAsym->cd();
      c_effAsym->Draw();

      eff_plus->Add(eff_minus, -1);
      eff_plus->Draw("colz");
      c_effAsym->SaveAs(plotDir+"2D_"+things.at(i)+"_Asym.png");
      delete c_effAsym;
    }

  }

  ///###############################################
  ///### Systematic study  (From JaeSung's code) ###
  ///###############################################

  if(!DoSystematicStudy) return;

  TGraphAsymmErrors* ValuesToError(TGraphAsymmErrors* a, bool rel);
  void AddSystematicToError(TGraphAsymmErrors *prev, TGraphAsymmErrors *newerror);
  void AddSystematicToCentralValue(TH2D *central, TH2D *a);
  void EmptyGraph(TGraphAsymmErrors* a);
  void EmptyHistError(TH2D *a);
  void PickLargestError(TGraphAsymmErrors *central, TGraphAsymmErrors *previous, TGraphAsymmErrors *now);
  void PickLargestError(TH2D *central, TH2D *previous, TH2D *now);
  TGraphAsymmErrors* hist_to_graph(TH1D* hist);
  TGraphAsymmErrors* GraphSubtract(TGraphAsymmErrors *a, TGraphAsymmErrors *b, bool Rel);
  void ScaleGraph(TGraphAsymmErrors *a, double c);
  double GetMaximum(TH1D* hist);
  double GetMaximum(TGraphAsymmErrors *a);

  vector< vector<TString> > vsysts = { {"Central"}, {"NMassBins_30", "NMassBins_50"}, {"MassRange_60to130", "MassRange_70to120"}, {"TagIso_0p10", "TagIso_0p20"},   { "SignalShape"  } };
  vector< vector<Color_t> > vcolors = {{ kBlack  }, {    kRed    ,       kOrange   }, {      kYellow,              kGreen      }, {    kViolet,      kGray     },   {     kBlue      } };
  vector< vector<TString> > vsystnames = {{  ""  }, { "_massbin30",   "_massbin50" }, {   "_mass60130",        "_mass70120"    }, { "_tagiso010",  "_tagiso020"},   {   "_altsig2"   } };

  for(unsigned int i_charge = 0; i_charge<charge.size(); i_charge++){
    vector<double> someerror_Data = {};
    vector<double> someerror_MC = {};
    TString plotDir = workingDir+"_"+charge.at(i_charge)+"/Plots/SystematicStudy/";
    gSystem->mkdir(plotDir,kTRUE);

    for(unsigned int i_pt = 0; i_pt<pt.size()-1; i_pt++){
      if(eff == "Turnon_Mu17") return;
      TString binname = "pt"+TString::Format("%.0f",pt.at(i_pt))+"to"+TString::Format("%.0f",pt.at(i_pt+1));

      // Canvas Setting
      TCanvas *c_Data = new TCanvas("c_Data", "", 800, 800);
      TPad *c_Data_up = new TPad("c_Data", "", 0, 0.25, 1, 1);
      TPad *c_Data_down = new TPad("c_Data_down", "", 0, 0, 1, 0.25);
      canvas_margin(c_Data, c_Data_up, c_Data_down);
      c_Data_down->SetGridx();
      c_Data_down->SetGridy();
      c_Data_up->Draw();
      c_Data_down->Draw();
      c_Data_up->cd();
      TCanvas *c_Data_err = new TCanvas("c_Data_err", "", 800, 800);
      canvas_margin(c_Data_err);

      TCanvas *c_MC = new TCanvas("c_MC", "", 800, 800);
      TPad *c_MC_up = new TPad("c_MC", "", 0, 0.25, 1, 1);
      TPad *c_MC_down = new TPad("c_MC_down", "", 0, 0, 1, 0.25);
      canvas_margin(c_MC, c_MC_up, c_MC_down);
      c_MC_down->SetGridx();
      c_MC_down->SetGridy();
      c_MC_up->Draw();
      c_MC_down->Draw();
      c_MC_up->cd();
      TCanvas *c_MC_err = new TCanvas("c_MC_err", "", 800, 800);
      canvas_margin(c_MC_err);

      // Save central values for calculating differences
      TGraphAsymmErrors *gr_Data_Central;
      TGraphAsymmErrors *gr_Data_TotSyst;
      TGraphAsymmErrors *gr_MC_Central;
      TGraphAsymmErrors *gr_MC_TotSyst;
      TGraphAsymmErrors *gr_error_Data;
      TGraphAsymmErrors *gr_error_MC;
      // Legend
      TLegend *lg = new TLegend(0.6, 0.1, 0.93, 0.5);
      lg->SetFillStyle(0);
      lg->SetBorderSize(0);
      for(unsigned int i_vsyst=0; i_vsyst<vsysts.size(); i_vsyst++){
	vector<TString> systs = vsysts.at(i_vsyst);
	vector<Color_t> colors = vcolors.at(i_vsyst);
	vector<TString> systnames = vsystnames.at(i_vsyst);
	TGraphAsymmErrors *gr_Data_ThisSourceLargest = NULL;
	TGraphAsymmErrors *gr_MC_ThisSourceLargest = NULL;

	for(unsigned int i_syst=0; i_syst<systs.size(); i_syst++){
	  TString syst = systs.at(i_syst);
	  TString systname = systnames.at(i_syst);
	  TFile *file_Data = new TFile(workingDir+"_"+charge.at(i_charge)+"/data"+systname+"/result_stat.root");
	  TFile *file_MC   = new TFile(workingDir+"_"+charge.at(i_charge)+"/mc"+systname+"/result_stat.root");
	  TH1D *hist_Data = (TH1D*)file_Data->Get("data"+systname+"_"+binname); TGraphAsymmErrors *gr_Data = hist_to_graph(hist_Data);
	  TH1D *hist_MC = (TH1D*)file_MC->Get("mc"+systname+"_"+binname); TGraphAsymmErrors *gr_MC = hist_to_graph(hist_MC);

	  if(syst=="Central"){
	    gr_Data_Central = (TGraphAsymmErrors*)gr_Data->Clone();
	    gr_MC_Central = (TGraphAsymmErrors*)gr_MC->Clone();
	  }

	  gr_Data->SetLineColor(colors.at(i_syst));
	  gr_Data->SetMarkerColor(colors.at(i_syst));
	  gr_Data->SetLineWidth(3);
	  gr_Data->SetMarkerSize(1.5);
	  gr_MC->SetLineColor(colors.at(i_syst));
	  gr_MC->SetMarkerColor(colors.at(i_syst));
	  gr_MC->SetLineWidth(3);
	  gr_MC->SetMarkerSize(1.5);

	  lg->AddEntry(gr_Data, syst, "lp");
	  TString DrawOption = "psame";
	  if(i_vsyst==0 && i_syst==0) DrawOption = "ap";

	  //##### Data #####
	  c_Data_up->cd();
	  gr_Data->Draw(DrawOption);
	  if(i_vsyst==0 && i_syst==0){
	    gr_Data->GetYaxis()->SetRangeUser(0., 1.0);
	    gr_Data->GetYaxis()->SetTitle("Efficiency");
	  }
	  c_Data->cd();
	  c_Data_down->cd();
	  //==== gr_diff_Data : Relative Difference
	  TGraphAsymmErrors *gr_diff_Data = GraphSubtract( gr_Data, gr_Data_Central, true );
	  ScaleGraph(gr_diff_Data, 100.);
	  hist_axis( gr_Data, gr_diff_Data );
	  gr_diff_Data->Draw(DrawOption);
	  gr_diff_Data->SetLineColor(colors.at(i_syst));
	  gr_diff_Data->SetMarkerColor(colors.at(i_syst));
	  /////gr_diff_Data->SetMarkerStyle(21);
	  if(i_vsyst==0 && i_syst==0){
	    gr_diff_Data->GetXaxis()->SetTitle("#eta(#mu)");
	    gr_diff_Data->GetYaxis()->SetRangeUser(-3, 3);
	    gr_diff_Data->GetYaxis()->SetTitle("Rel. Diff. [%]");
	  }
	  //==== Error only plot
	  //==== If Central, Draw Fit Uncertainty
	  if(syst=="Central"){
	    c_Data_err->cd();
	    //==== now graph value is rel error
	    gr_error_Data = ValuesToError(gr_Data, true);
	    ScaleGraph(gr_error_Data, 100.);
	    gr_error_Data->SetLineColor(kBlue);
	    gr_error_Data->SetMarkerColor(kBlue);
	    gr_error_Data->SetLineWidth(3);
	    gr_error_Data->Draw("ap");
	    hist_axis(gr_error_Data);
	    gr_error_Data->GetXaxis()->SetTitle("#eta(#mu)");
	    if(eff=="Mu17") gr_error_Data->GetXaxis()->SetRangeUser(19., 100.);
	    gr_error_Data->GetYaxis()->SetTitle("Rel. Diff. [%]");
	    gr_error_Data->GetYaxis()->SetRangeUser(0., 4.);

	    gr_Data_TotSyst = (TGraphAsymmErrors*)gr_Data->Clone();
	    EmptyGraph(gr_Data_TotSyst);
	  }
	  //==== If systematic, add up errors
	  else{
	    if(!gr_Data_ThisSourceLargest){
	      gr_Data_ThisSourceLargest = (TGraphAsymmErrors*)gr_Data_Central->Clone();
	      EmptyGraph(gr_Data_ThisSourceLargest);
	    }
	    PickLargestError(gr_Data_Central, gr_Data_ThisSourceLargest, gr_Data);
	  }

	  //##### MC #####
	  c_MC_up->cd();
	  gr_MC->Draw(DrawOption);
	  if(i_vsyst==0 && i_syst==0){
	    gr_MC->GetYaxis()->SetRangeUser(0., 1.0);
	    gr_MC->GetYaxis()->SetTitle("Efficiency");
	  }
	  c_MC->cd();
	  c_MC_down->cd();
	  //==== gr_diff_MC : Relative Difference
	  TGraphAsymmErrors *gr_diff_MC = GraphSubtract( gr_MC, gr_MC_Central, true );
	  ScaleGraph(gr_diff_MC, 100.);
	  hist_axis( gr_MC, gr_diff_MC );
	  gr_diff_MC->Draw(DrawOption);
	  gr_diff_MC->SetLineColor(colors.at(i_syst));
	  gr_diff_MC->SetMarkerColor(colors.at(i_syst));
	  ////gr_diff_MC->SetMarkerStyle(21);
	  if(i_vsyst==0 && i_syst==0){
	    gr_diff_MC->GetXaxis()->SetTitle("#eta(#mu)");
	    gr_diff_MC->GetYaxis()->SetRangeUser(-3, 3);
	    gr_diff_MC->GetYaxis()->SetTitle("Rel. Diff. [%]");
	  }
	  //==== Error only plot
	  //==== If Central, Draw Fit Uncertainty
	  if(syst=="Central"){
	    c_MC_err->cd();
	    //==== now graph value is rel error
	    gr_error_MC = ValuesToError(gr_MC, true);
	    ScaleGraph(gr_error_MC, 100.);
	    gr_error_MC->SetLineColor(kBlue);
	    gr_error_MC->SetMarkerColor(kBlue);
	    gr_error_MC->SetLineWidth(3);
	    gr_error_MC->Draw("ap");
	    hist_axis(gr_error_MC);
	    gr_error_MC->GetXaxis()->SetTitle("#eta(#mu)");
	    if(eff=="Mu17") gr_error_MC->GetXaxis()->SetRangeUser(19., 100.);
	    gr_error_MC->GetYaxis()->SetTitle("Rel. Diff. [%]");
	    gr_error_MC->GetYaxis()->SetRangeUser(0., 4.);

	    gr_MC_TotSyst = (TGraphAsymmErrors*)gr_MC->Clone();
	    EmptyGraph(gr_MC_TotSyst);
	  }
	  //==== If systematic, add up errors
	  else{
	    if(!gr_MC_ThisSourceLargest){
	      gr_MC_ThisSourceLargest = (TGraphAsymmErrors*)gr_MC_Central->Clone();
	      EmptyGraph(gr_MC_ThisSourceLargest);
	    }
	    PickLargestError(gr_MC_Central, gr_MC_ThisSourceLargest, gr_MC);
	  }
	}
	if(gr_Data_ThisSourceLargest && gr_MC_ThisSourceLargest){
	  AddSystematicToError(gr_Data_TotSyst, gr_Data_ThisSourceLargest);
	  AddSystematicToError(gr_MC_TotSyst, gr_MC_ThisSourceLargest);
	}
      }

      c_Data_up->cd();
      gr_Data_Central->Draw("psame");
      lg->Draw();
      c_Data->SaveAs(plotDir+"Data_"+binname+".png");
      //==== Error
      c_Data_err->cd();
      ScaleGraph(gr_Data_TotSyst, 100.);
      gr_Data_TotSyst->SetLineColor(kRed);
      gr_Data_TotSyst->SetMarkerColor(kRed);
      gr_Data_TotSyst->SetLineWidth(3);
      gr_Data_TotSyst->Draw("psame");
      double y_error_max_Data = 1.2;
      gr_error_Data->GetYaxis()->SetRangeUser(0., y_error_max_Data);
      //==== Sum
      TGraphAsymmErrors *gr_Data_AllError = (TGraphAsymmErrors *)gr_error_Data->Clone();
      for(int aaa=0; aaa<gr_Data_AllError->GetN(); aaa++){

	double x_fit, y_fit;
	double x_syst, y_syst;

	gr_Data_AllError->GetPoint(aaa, x_fit, y_fit);
	gr_Data_TotSyst->GetPoint(aaa, x_syst, y_syst);

	double err = sqrt(y_fit*y_fit+y_syst*y_syst);
	someerror_Data.push_back(err);
	gr_Data_AllError->SetPoint(aaa, x_fit, err);
      }
      gr_Data_AllError->SetLineColor(kBlack);
      gr_Data_AllError->SetMarkerColor(kBlack);
      gr_Data_AllError->SetLineWidth(3);
      gr_Data_AllError->Draw("psame");

      TLegend *lg_error = new TLegend(0.6, 0.7, 0.93, 0.9);
      lg_error->SetFillStyle(0);
      lg_error->SetBorderSize(0);
      lg_error->AddEntry(gr_Data_AllError, "Total Uncert.", "lp");
      lg_error->AddEntry(gr_Data_TotSyst, "Syst. Uncert.", "lp");
      lg_error->AddEntry(gr_error_Data, "Fit Uncert.", "lp");
      lg_error->Draw();

      c_Data_err->SaveAs(plotDir+"DataDiff_"+binname+".png");
      c_Data_err->Close();

      c_MC_up->cd();
      gr_MC_Central->Draw("psame");
      lg->Draw();
      c_MC->SaveAs(plotDir+"MC_"+binname+".png");
      //==== Error
      c_MC_err->cd();
      ScaleGraph(gr_MC_TotSyst, 100.);
      gr_MC_TotSyst->SetLineColor(kRed);
      gr_MC_TotSyst->SetMarkerColor(kRed);
      gr_MC_TotSyst->SetLineWidth(3);
      gr_MC_TotSyst->Draw("psame");
      double y_error_max_MC = 1.2;
      gr_error_MC->GetYaxis()->SetRangeUser(0., y_error_max_MC);
      //==== Sum
      TGraphAsymmErrors *gr_MC_AllError = (TGraphAsymmErrors *)gr_error_MC->Clone();
      for(int aaa=0; aaa<gr_MC_AllError->GetN(); aaa++){

	double x_fit, y_fit;
	double x_syst, y_syst;

	gr_MC_AllError->GetPoint(aaa, x_fit, y_fit);
	gr_MC_TotSyst->GetPoint(aaa, x_syst, y_syst);

	double err = sqrt(y_fit*y_fit+y_syst*y_syst);
	someerror_MC.push_back(err);
	gr_MC_AllError->SetPoint(aaa, x_fit, err);
      }
      gr_MC_AllError->SetLineColor(kBlack);
      gr_MC_AllError->SetMarkerColor(kBlack);
      gr_MC_AllError->SetLineWidth(3);
      gr_MC_AllError->Draw("psame");
      lg_error->Draw();
      c_MC_err->SaveAs(plotDir+"MCDiff_"+binname+".png");
      c_MC_err->Close();

      c_Data->Close();
      c_MC->Close();
    }

    //#######################################
    //##### Draw 1D systematic Monster Plot of Data, MC
    //#######################################

    TCanvas *c_hoi = new TCanvas("c_MC", "", 1600, 800);
    TH1D *hoi_Data = new TH1D("hoi_Data", "" ,someerror_Data.size(),0,someerror_Data.size()-1);
    TH1D *hoi_MC = new TH1D("hoi_MC", "" ,someerror_MC.size(),0,someerror_Data.size()-1);

    double YMax = 5.2;
    hoi_Data->GetYaxis()->SetRangeUser(0., YMax);
    hoi_MC->GetYaxis()->SetRangeUser(0., YMax);
    for (int i=0;i<someerror_Data.size();i++){
      hoi_Data->SetBinContent(i+1,someerror_Data.at(i));
      hoi_Data->GetYaxis()->SetTitle("Stat. + Syst. Uncertainty (%)");
      hoi_MC->SetBinContent(i+1,someerror_MC.at(i));
      hoi_Data->GetYaxis()->SetTitle("Stat. + Syst. Uncertainty (%)");
    }
    canvas_margin(c_hoi);
    hist_axis(hoi_Data);
    hoi_Data->SetLineColor(kBlack);
    hoi_Data->SetLineWidth(2);
    hoi_MC->SetLineColor(kRed);
    hoi_MC->SetLineWidth(2);
    c_hoi->cd();
    hoi_Data->Draw("hist");
    hoi_MC->Draw("same");

    TLegend *hoi = new TLegend(0.9, 0.55, 0.99, 0.75);
    hoi->SetFillStyle(0);
    hoi->SetBorderSize(0);
    hoi->AddEntry(hoi_Data, "Data", "lp");
    hoi->AddEntry(hoi_MC, "MC", "lp");
    hoi->Draw();

    TLine line1(0,0.5,someerror_Data.size(),0.5);
    line1.SetLineWidth(1);
    line1.SetLineColor(kBlue);
    line1.DrawLine(0,1,someerror_Data.size(),1);
    line1.SetLineColor(kBlack);
    line1.DrawLine(0,2,someerror_Data.size(),2);
    line1.SetLineColor(kGreen+2);
    line1.DrawClone("SAME");
    TLine line2(someerror_Data.size()-1,0,someerror_Data.size()-1,YMax);
    line2.SetLineWidth(1);
    line2.SetLineStyle(7);
    line2.DrawLine(48-1,0,48-1,YMax);
    line2.DrawLine(48*2-1,0,48*2-1,YMax);
    line2.DrawLine(48*3-1,0,48*3-1,YMax);
    line2.DrawLine(48*4-1,0,48*4-1,YMax);
    line2.DrawLine(48*5-1,0,48*5-1,YMax);
    line2.DrawLine(48*6-1,0,48*6-1,YMax);
    line2.DrawLine(48*7-1,0,48*7-1,YMax);
    line2.DrawLine(48*8-1,0,48*8-1,YMax);
    line2.DrawLine(48*9-1,0,48*9-1,YMax);
    line2.DrawClone("SAME");

    TLatex latex_pt, latex_legend;
    latex_pt.SetNDC();
    latex_legend.SetNDC();
    latex_pt.SetTextSize(0.03);
    if(eff == "Mu8" || eff == "IDISO"){
      latex_pt.DrawLatex(0.13, 0.9, "10 - 15");
      latex_pt.DrawLatex(0.13+0.08777, 0.9, "15 - 20");
      latex_pt.DrawLatex(0.13+0.08777*2, 0.9, "20 - 25");
      latex_pt.DrawLatex(0.13+0.08777*3, 0.9, "25 - 30");
      latex_pt.DrawLatex(0.13+0.08777*4, 0.9, "30 - 35");
      latex_pt.DrawLatex(0.13+0.08777*5, 0.9, "35 - 40");
      latex_pt.DrawLatex(0.13+0.08777*6, 0.9, "40 - 45");
      latex_pt.DrawLatex(0.13+0.08777*7, 0.9, "45 - 50");
      latex_pt.DrawLatex(0.13+0.08777*8, 0.9, "50 - 60");
      latex_pt.DrawLatex(0.92, 0.9, "60 -120");
    }
    else if(eff == "Mu17"){
      latex_pt.DrawLatex(0.145, 0.9, "20 - 25");
      latex_pt.DrawLatex(0.14+0.10857, 0.9, "25 - 30");
      latex_pt.DrawLatex(0.14+0.10857*2, 0.9, "30 - 35");
      latex_pt.DrawLatex(0.14+0.10857*3, 0.9, "35 - 40");
      latex_pt.DrawLatex(0.14+0.10857*4, 0.9, "40 - 45");
      latex_pt.DrawLatex(0.14+0.10857*5, 0.9, "45 - 50");
      latex_pt.DrawLatex(0.14+0.10857*6, 0.9, "50 - 60");
      latex_pt.DrawLatex(0.905, 0.9, "60 -120");
    }
    else{
      if(DataPeriod == "2017"){
	latex_pt.DrawLatex(0.15, 0.9, "29 - 32");
	latex_pt.DrawLatex(0.15+0.125, 0.9, "32 - 35");
      }
      else{
	latex_pt.DrawLatex(0.15, 0.9, "26 - 30");
	latex_pt.DrawLatex(0.15+0.125, 0.9, "30 - 35");
      }
      latex_pt.DrawLatex(0.15+0.125*2, 0.9, "35 - 40");
      latex_pt.DrawLatex(0.15+0.125*3, 0.9, "40 - 45");
      latex_pt.DrawLatex(0.15+0.125*4, 0.9, "45 - 50");
      latex_pt.DrawLatex(0.15+0.125*5, 0.9, "50 - 60");
      latex_pt.DrawLatex(0.9, 0.9, "60 -120");
    }
    latex_pt.DrawLatex(0.9, 0.84, "#scale[1.3]{ P_{T} [GeV]}");
    latex_legend.SetTextSize(0.04);
    latex_legend.DrawLatex(0.95, 0.01, "Bin #");

    c_hoi->SaveAs(plotDir+"1D_Diff.png");
    c_hoi->Close();
  }// charge loop ends here.
}

// Jaesung's functions
TGraphAsymmErrors* ValuesToError(TGraphAsymmErrors* a, bool rel){

  TGraphAsymmErrors *out = (TGraphAsymmErrors*)a->Clone();
  int NX = a->GetN();

  for(int i=0; i<NX; i++){

    double x, y, xerr_low, xerr_high, yerr_low, yerr_high;

    a->GetPoint(i, x, y);
    xerr_low  = a->GetErrorXlow(i);
    xerr_high = a->GetErrorXhigh(i);
    yerr_low  = a->GetErrorYlow(i);
    yerr_high = a->GetErrorYhigh(i);

    double newval = sqrt((yerr_low*yerr_low+yerr_high*yerr_high)/2.);
    if(rel) newval = newval/y;

    out->SetPoint(i, x, newval);
    out->SetPointError(i, xerr_low, xerr_high, 0., 0.);
  }
  return out;
}

void AddSystematicToError(TGraphAsymmErrors *prev, TGraphAsymmErrors *newerror){

  //==== a : Total Syst
  //==== b : New Syst

  int NX = prev->GetN();
  for(int i=0; i<NX; i++){
    double x_prev, y_prev;
    prev->GetPoint(i, x_prev, y_prev);
    double x_new, y_new;
    newerror->GetPoint(i, x_new, y_new);

    double y_added = sqrt(y_prev*y_prev+y_new*y_new);
    prev->SetPoint(i, x_prev, y_added);
  }
}

void AddSystematicToCentralValue(TH2D *central, TH2D *a){

  for(int i=1; i<=central->GetXaxis()->GetNbins(); i++){
    for(int j=1; j<=central->GetYaxis()->GetNbins(); j++){

      double value_central = central->GetBinContent(i,j);
      double err_original = central->GetBinError(i,j);
      double this_syst = a->GetBinError(i,j);

      double new_err = sqrt(err_original*err_original+this_syst*this_syst);
      central->SetBinError(i,j, new_err);
    }
  }
}

void EmptyGraph(TGraphAsymmErrors* a){

  int NX = a->GetN();
  for(int i=0; i<NX; i++){
    double x, y, xerr_low, xerr_high;
    a->GetPoint(i, x, y);
    xerr_low  = a->GetErrorXlow(i);
    xerr_high = a->GetErrorXhigh(i);
    a->SetPoint(i, x, 0.);
    a->SetPointError(i, xerr_low, xerr_high, 0., 0.);
  }
}

void PickLargestError(TGraphAsymmErrors *central, TGraphAsymmErrors *previous, TGraphAsymmErrors *now){

  //==== Central : Eff
  //==== Previous : Error
  //==== now : Eff

  int NX = central->GetN();
  for(int i=0; i<NX; i++){
    double x_central, y_central;
    double x_prev, y_prev;
    double x_now, y_now;

    central->GetPoint(i, x_central, y_central);
    previous->GetPoint(i, x_prev, y_prev);
    now->GetPoint(i, x_now, y_now);
    double this_y = max( y_prev, fabs(y_now-y_central)/y_central );
    previous->SetPoint(i, x_prev, this_y);
  }
}

void PickLargestError(TH2D *central, TH2D *previous, TH2D *now){

  //==== Central : Eff
  //==== Previous : Error
  //==== now : Eff

  for(int ix=1; ix<=central->GetXaxis()->GetNbins(); ix++){
    for(int iy=1; iy<=central->GetYaxis()->GetNbins(); iy++){

      double y_central = central->GetBinContent(ix, iy);
      double y_now = now->GetBinContent(ix, iy);
      double yerr_now = fabs(y_central-y_now);
      double yerr_previous = previous->GetBinError(ix, iy);

      double newerr = max(yerr_now, yerr_previous);
      previous->SetBinError(ix, iy, newerr);
    }
  }
}

void EmptyHistError(TH2D *a){
  for(int ix=1; ix<=a->GetXaxis()->GetNbins(); ix++){
    for(int iy=1; iy<=a->GetYaxis()->GetNbins(); iy++){
      a->SetBinError(ix, iy, 0);
    }
  }
}

//##### From mylib.h of Jaesung ################
TGraphAsymmErrors* hist_to_graph(TH1D* hist){

  TH1::SetDefaultSumw2(true);

  int Nbins = hist->GetXaxis()->GetNbins();
  double x[Nbins], y[Nbins], xlow[Nbins], xup[Nbins], ylow[Nbins], yup[Nbins];
  TAxis *xaxis = hist->GetXaxis();
  for(Int_t i=0; i<Nbins; i++){
    x[i] = xaxis->GetBinCenter(i+1);
    y[i] = hist->GetBinContent(i+1);
    xlow[i] = xaxis->GetBinCenter(i+1)-xaxis->GetBinLowEdge(i+1);
    xup[i] = xaxis->GetBinUpEdge(i+1)-xaxis->GetBinCenter(i+1);
    ylow[i] = hist->GetBinError(i+1);
    yup[i] = hist->GetBinError(i+1);
    //ylow[i] = 0;
    //yup[i] = 0;
    //cout << "x = " << x[i] << ", y = " << y[i] << ", x_low = " << xlow[i] << ", xup = " << xup[i] << ", ylow = " << ylow[i] << ", yup = " << yup[i] << endl;
  }
  TGraphAsymmErrors *out = new TGraphAsymmErrors(Nbins, x, y, xlow, xup, ylow, yup);
  out->SetTitle("");
  return out;
}

TGraphAsymmErrors* GraphSubtract(TGraphAsymmErrors *a, TGraphAsymmErrors *b, bool Rel){

  //==== do a-b

  int NX = a->GetN();
  TGraphAsymmErrors* gr_out = (TGraphAsymmErrors*)a->Clone();
  for(int i=0; i<NX; i++){

    double a_x, a_y, b_x, b_y;
    a->GetPoint(i, a_x, a_y);
    b->GetPoint(i, b_x, b_y);
    if(Rel==true){
      gr_out->SetPoint( i, a_x, (a_y-b_y)/b_y );
    }
    else{
      gr_out->SetPoint( i, a_x, a_y-b_y );
    }
  }
  return gr_out;
}

void ScaleGraph(TGraphAsymmErrors *a, double c){

  int NX = a->GetN();

  for(int i=0; i<NX; i++){

    double x, y, yerr_low, yerr_high;

    a->GetPoint(i, x, y);
    yerr_low  = a->GetErrorYlow(i);
    yerr_high = a->GetErrorYhigh(i);

    a->SetPoint(i, x, c*y);
    a->SetPointEYlow(i, c*yerr_low);
    a->SetPointEYhigh(i, c*yerr_high);
  }
}

double GetMaximum(TH1D* hist){

  TAxis *xaxis = hist->GetXaxis();

  double maxval(-1.);
  for(int i=1; i<=xaxis->GetNbins(); i++){
    if( hist->GetBinContent(i) + hist->GetBinError(i) > maxval ){
      maxval = hist->GetBinContent(i) + hist->GetBinError(i);
    }
  }
  return maxval;
}

double GetMaximum(TGraphAsymmErrors *a){

  int NX = a->GetN();

  double maxval(-9999.);
  for(int i=0; i<NX; i++){

    double x, y, yerr_low, yerr_high;

    a->GetPoint(i, x, y);
    yerr_low  = a->GetErrorYlow(i);
    yerr_high = a->GetErrorYhigh(i);

    if( y+yerr_high > maxval ){
      maxval = y+yerr_high;
    }
  }
  return maxval;
}
