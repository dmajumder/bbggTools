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
inputtovalidationFullSim = "output_GluGluToHHTo2B2G_node_0_13TeV-madgraph.root"
benchmarksV1fromLHE = "Distros_benchmarks_5p_500000ev_12sam_13TeV_JHEPv3.root" #

#color ={1 , 2, 3 ,4 , 5, }


legend = TLegend(.5,.8,1.0,.95)

#########################
# declare the histograms
#########################
# bechmarks
histoW = [None]*nclu 
histoMhh = [None]*nclu 
histoCost = [None]*nclu 
for cluster in range(0,nclu) : 
   histoW[cluster] = ROOT.TH1D('histoW'+str(cluster),'histoW'+str(cluster),500,0.,200.)
   histoW[cluster].SetLineColor(cluster+1)
   histoW[cluster].SetLineWidth(1)
   histoW[cluster].SetTitle(" Benchmarks from reweighting ")
   histoW[cluster].GetYaxis().SetTitle("shape normalized")
   histoW[cluster].GetXaxis().SetTitle("weights")
   histoMhh[cluster] = ROOT.TH1D('histoMhh'+str(cluster),'histoMhh'+str(cluster),60,0.,1800.)
   histoMhh[cluster].SetLineColor(1)
   histoMhh[cluster].SetLineWidth(1)
   histoMhh[cluster].SetTitle(" Benchmarks from reweighting ")
   histoMhh[cluster].GetYaxis().SetTitle("shape normalized")
   histoMhh[cluster].GetXaxis().SetTitle("gen m_{HH}")
   histoCost[cluster] = ROOT.TH1D('histoCost'+str(cluster),'histoW'+str(cluster),11,-1.,1.)
   histoCost[cluster].SetLineColor(1)
   histoCost[cluster].SetLineWidth(1)
   histoCost[cluster].SetTitle(" Benchmarks from reweighting ")
   histoCost[cluster].GetYaxis().SetTitle("shape normalized")
   histoCost[cluster].GetXaxis().SetTitle("gen cos#theta *")

#############################
# the parton level, for checking
Filebenchmarks = ROOT.TFile.Open(benchmarksV1fromLHE, 'read')
histoLHEMhh = [None]*nclu 
histoLHECost = [None]*nclu
for cluster in range(0,nclu) : 
    histoname = str(cluster)+"_mhh"
    histoLHEMhh[cluster] = Filebenchmarks.Get(histoname)
    histoLHEMhh[cluster].SetLineColor(3)
    histoLHEMhh[cluster].SetLineWidth(3)
    histoLHEMhh[cluster].SetLineStyle(4)
    histoLHEMhh[cluster].SetTitle(" Benchmarks from reweighting ")
    histoLHEMhh[cluster].GetYaxis().SetTitle("shape normalized")
    histoLHEMhh[cluster].GetXaxis().SetTitle("gen m_{HH}")
    histoname = str(cluster)+"_hths"
    histoLHECost[cluster] = Filebenchmarks.Get(histoname)
    histoLHECost[cluster].SetLineColor(3)
    histoLHECost[cluster].SetLineWidth(3)
    histoLHECost[cluster].SetLineStyle(4)
    histoLHECost[cluster].SetTitle(" Benchmarks from reweighting ")
    histoLHECost[cluster].GetYaxis().SetTitle("shape normalized")
    histoLHECost[cluster].GetXaxis().SetTitle("gen cos#theta *")

#########################
# retrieve the weights
#########################
File = ROOT.TFile.Open(input, 'read')
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
      
#########################
# Closure 1: Draw histograms for benchmars and see the matching at parton level (dumb)
#########################
print "Closure 1: Draw histograms for benchmars and see the matching at parton level (dumb)"

close1 ="closure1_benchmarks/"
c=ROOT.TCanvas()
for cluster in range(0,nclu) :     
    print "cluster "+str(cluster)+" have normalization "+ str(histoW[cluster].Integral())
    legend.AddEntry(histoW[cluster],str(cluster+1))
    if (cluster==0) : histoW[cluster].Draw()
    else : histoW[cluster].Draw("same")
c.SetLogx(1)
c.SetLogy(1)
legend.Draw()
legend.Clear()
c.Print(close1+"weights_bench.png")
c.Clear()
c.Close()
c.cd()
c.SetLogx(0)
c.SetLogy(0)
####
for cluster in range(0,nclu) :     
    c1=ROOT.TCanvas()
    print "cluster "+str(cluster)+" have nevents = "+ str(histoW[cluster].Integral())+" and after reweighting normalization ="+str(histoMhh[cluster].Integral())
    norm = histoMhh[cluster].Integral() #/ histoW[cluster].Integral() #
    histoMhh[cluster].Scale(1./norm)
    histoLHEMhh[cluster].Scale(1./histoLHEMhh[cluster].Integral())
    print "after scale cluster "+str(cluster)+" have nevents = "+ str(histoW[cluster].Integral())+" and after reweighting normalization ="+str(norm)
    if (cluster==0) : 
        histoMhh[cluster].Draw("hist")
        legend.AddEntry(histoMhh[cluster],"from reweighting")
        histoLHEMhh[cluster].Draw("same")
        legend.AddEntry(histoLHEMhh[cluster],"from lhe")    
    else : 
        histoMhh[cluster].Draw("same,hist")
        histoLHEMhh[cluster].Draw("same,hist")
    legend.Draw()
    c1.SetLogx(0)
    c1.SetLogy(0)
    c1.Print(close1+"Mhh_bench_"+str(cluster)+".png")
####
for cluster in range(0,nclu) :  
    c1=ROOT.TCanvas()
    histoCost[cluster].Scale(1./histoCost[cluster].Integral())
    histoLHECost[cluster].Scale(1./histoLHECost[cluster].Integral())
    if (cluster==0) : 
        histoCost[cluster].SetMinimum(0)
        histoCost[cluster].SetMaximum(1.5)
        histoCost[cluster].Draw("hist")
        #    legend.AddEntry(histoCost[cluster],"from reweighting")
        histoLHECost[cluster].Draw("same")
        #legend.AddEntry(histoLHECost[cluster],"from lhe")    
    else : 
        histoCost[cluster].Draw("same,hist")
        histoLHECost[cluster].Draw("same")
    histoCost[cluster].SetMinimum(0)
    histoCost[cluster].SetMaximum(0.2)
    legend.Draw()
    c1.SetLogx(0)
    c1.SetLogy(0)
    c1.Print(close1+"Cost_bench_"+str(cluster)+".png")


'''
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
'''


#########################
# Closure 2: Draw histograms for the box-only and see the matching at parton level
#########################


#########################
# Plots for fun: Draw histograms outliers 
#########################


