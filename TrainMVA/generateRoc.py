from ROOT import *
from array import array

gROOT.SetBatch(True)

import argparse
parser =  argparse.ArgumentParser(description='Add Classification BDT weights')
parser.add_argument('-f', '--file', dest='inputFile', required=True, type=str)


opt = parser.parse_args()


#TMVA.TMVAGui(opt.sig)
TMVA.efficiencies(opt.inputFile)
h= c.GetPrimitive("MVA_BDT_rejBvsS")

nameOutput = opt.inputFile.replace(".root","")
outfile = TFile("plots/"+nameOutput+".root", "RECREATE")
h.Write("roc")
outfile.Close()
