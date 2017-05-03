from ROOT import *
from array import array

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gROOT.ProcessLine(".L ~/setTDRStyle.C")
setTDRStyle()

import argparse
parser =  argparse.ArgumentParser(description='Add Classification BDT weights')
parser.add_argument('-m', '--moreVar', dest='moreVar', required=True, type=str)
parser.add_argument('-s', '--stdVar', dest='std', required=True, type=str)

opt = parser.parse_args()

inputMore = TFile(opt.moreVar)
inputStd = TFile(opt.std)

h_moreVar = inputMore.Get("roc")
h_std = inputStd.Get("roc")

c1 = TCanvas()
#h_moreVar.SetLineWidth(2)
h_moreVar.SetLineColor(kRed)
leg = TLegend(0.2, 0.6, 0.3, 0.7)
leg.SetLineWidth(0)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.AddEntry(h_moreVar,"New","l")
leg.AddEntry(h_std,"Std","l")

h_moreVar.GetXaxis().SetRangeUser(0.3, 1)
h_moreVar.GetYaxis().SetRangeUser(0.3, 1.1)
h_moreVar.Draw()
h_std.Draw("same")
leg.Draw("same") 
c1.SaveAs("plots/RocComparison.png")
c1.SaveAs("plots/RocComparison.pdf")

moreVarOutput = opt.moreVar.replace(".root","")
stdOutput = opt.std.replace(".root","")
stdOutput = opt.std.replace("plots/","")
outfile = TFile(moreVarOutput+"_"+stdOutput+".root", "RECREATE")
h_moreVar.Write("roc_moreVar")
h_std.Write("roc_std")
c1.Write("roc_comparison")
outfile.Close()
