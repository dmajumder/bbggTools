#####################################
## input: file with weights to one validation sample SM + 12 benchmarks + 72 outliers + 52 lambda-only scan
## output: validation plots
###################################
#!/usr/bin/env python
import os, sys, time,math
import ROOT
from ROOT import TH1D
from array import array
from ROOT import TLatex,TPad,TList,TH1,TH1F,TH2F,TH1D,TH2D,TFile,TTree,TCanvas,TLegend,SetOwnership,gDirectory,TObject,gStyle,gROOT,TLorentzVector,TGraph,TMultiGraph,TColor,TAttMarker,TLine,TDatime,TGaxis,TF1,THStack,TAxis,TStyle,TPaveText,TAttFill
import math
import bisect
from optparse import OptionParser
import numpy as np
from ROOT import TTree, TFile, AddressOf, gROOT, TChain, gPad

gStyle.SetOptStat(0000)

nclu=12
nout=6
Nlambda=52
input = "teste_weight.root"
File = ROOT.TFile.Open(input, 'read')

legend = TLegend(.9,.5,1.0,.95)


#########################
# draw all the weights
#########################

histoW = [None]*nclu 
histoMhh = [None]*nclu 
histoCost = [None]*nclu 
for cluster in range(0,nclu) : 
   histoW[cluster] = ROOT.TH1D('histoW'+str(cluster),'histoW'+str(cluster),500,0.,200.)
   histoW[cluster].SetLineColor(cluster+1)
   histoW[cluster].SetLineWidth(3)
   histoW[cluster].SetTitle(" Benchmarks from reweighting ")
   histoW[cluster].GetYaxis().SetTitle("shape normalized")
   histoW[cluster].GetXaxis().SetTitle("weights")
   histoMhh[cluster] = ROOT.TH1D('histoMhh'+str(cluster),'histoMhh'+str(cluster),90,200,1800.)
   histoMhh[cluster].SetLineColor(cluster+1)
   histoMhh[cluster].SetLineWidth(3)
   histoMhh[cluster].SetTitle(" Benchmarks from reweighting ")
   histoMhh[cluster].GetYaxis().SetTitle("shape normalized")
   histoMhh[cluster].GetXaxis().SetTitle("gen m_{HH}")
   histoCost[cluster] = ROOT.TH1D('histoCost'+str(cluster),'histoW'+str(cluster),10,-1.,1.)
   histoCost[cluster].SetLineColor(cluster+1)
   histoCost[cluster].SetLineWidth(3)
   histoCost[cluster].SetTitle(" Benchmarks from reweighting ")
   histoCost[cluster].GetYaxis().SetTitle("shape normalized")
   histoCost[cluster].GetXaxis().SetTitle("gen cos#theta *")

for event in File.TCVARS :
    #for cluster in range(0,nclu) :     
       #histoname = "bench"+str(cluster)
       # class User(object):
       # def __init__(self, username, password):
       # self.username = username
      weiclu = [None]*nclu
      weiclu[0] =  event.bench1
      weiclu[1] =  event.bench2
      weiclu[2] =  event.bench3
      weiclu[3] =  event.bench4
      weiclu[4] =  event.bench5
      weiclu[5] =  event.bench6
      weiclu[6] =  event.bench7
      weiclu[7] =  event.bench8
      weiclu[8] =  event.bench9
      weiclu[9] =  event.bench10
      weiclu[10] =  event.bench11
      weiclu[11] =  event.bench12
      Mtot = event.mHH 
      Cost = event.cosTheta 
      for cluster in range(0,nclu) : 
          histoW[cluster].Fill(weiclu[cluster])
          histoMhh[cluster].Fill(Mtot,weiclu[cluster])
          histoCost[cluster].Fill(Cost,weiclu[cluster])
      
c=ROOT.TCanvas()
for cluster in range(0,nclu) :     
    print "cluster "+str(cluster)+" have normalization "+ str(histoW[cluster].Integral())
    legend.AddEntry(histoW[cluster],str(cluster+1))
    if (cluster==0) : histoW[cluster].Draw()
    else : histoW[cluster].Draw("same")
c.SetLogx(1)
c.SetLogy(1)
legend.Draw()
c.Print("weights_bench.png")
c.Clear()
c.SetLogx(0)
c.SetLogy(0)
for cluster in range(0,nclu) : 
    histoMhh[cluster].Scale(1./histoMhh[cluster].Integral())
    if (cluster==0) : 
       histoMhh[0].SetMaximum(0.2)
       histoMhh[0].SetMinimum(0)
       histoMhh[cluster].Draw("hist")
    else : 
       histoMhh[cluster].Draw("hist,same")
legend.Draw()
c.Print("Mhh_bench.png")
c.Clear()
for cluster in range(0,nclu) :    
    print "cluster "+str(cluster)+" have normalization "+ str(histoCost[cluster].Integral())
    histoCost[cluster].Scale(1./histoCost[cluster].Integral())
    if (cluster==0) : 
       histoCost[0].SetMaximum(0.15)
       histoCost[0].SetMinimum(0)
       histoCost[cluster].Draw("hist")
    else : 
       histoCost[cluster].Draw("hist,same")
legend.Draw()
c.Print("Cost_bench.png")
c.Clear()


