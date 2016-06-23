#####################################
## input: aabb minitrees to 13 benchmarks
## output: one validation sample SM + 12 benchmarks + 72 outliers + 52 lambda-only scan
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
from ROOT import TTree, TFile, AddressOf, gROOT, TChain

input = "noCuts/"
os.system('mkdir V3benchmarks')
os.system('mkdir V3outliers')
os.system('mkdir lambdaonly')

file = "output_GluGluToHHTo2B2G_node_"
fileEnd="_13TeV-madgraph.root"
#fileL="_13TeV-madgraph_LOWMASS.root"


nclu=12
nout=6
Nlambda=52

#Nvarbinmass=91 
Nvarbinmass=91 
Nvarbincosth=11
#a = np.ones((3,2))        # a 2D array with 3 rows, 2 columns, filled with ones
#Matrix1 = [[[None]*Nvarbincosth]*Nvarbinmass]*nclu # of the benchmark
#Matrix2high = [[None]*Nvarbincosth]*Nvarbinmass # of the fullsim set
#Matrix2low = [[None]*Nvarbincosth]*Nvarbinmass # of the fullsim set

Matrix1 = np.zeros((nclu,Nvarbinmass,Nvarbincosth))  # of the benchmark
Matrix1out = np.zeros((nclu,nout,Nvarbinmass,Nvarbincosth))  # of the ouliers
Matrix2out = np.zeros((Nlambda,Nvarbinmass,Nvarbincosth))  # of the lambda-only

Matrix2high = np.zeros((Nvarbinmass,Nvarbincosth)) # of the fullsim set
Matrix1validationhigh = np.zeros((Nvarbinmass,Nvarbincosth))# of the fullsim set
      
######################################
### read the reweiting maps to the benchmarks
lambdaonly = "Distros_lambdaOnly_5p_50000ev_52sam_13TeV_JHEP_50K.root"
envelope = "Distros_envelope_5p_20000ev_6sam_13TeV.root"
benchmarks = "Distros_benchmarks_5p_500000ev_12sam_13TeV_JHEPv3.root" # "Distros_5p_500000ev_12sam_13TeV_JHEP_500K.root"

######################################
# benchmarks
######################################
Filebenchmarks = ROOT.TFile.Open(benchmarks, 'read')
histo2D = [None]*nclu 
counter=0
# the file already contains the 2D histos
for cluster in range(0,nclu) :
    # just take the histo
    # bin1.SetBins(90,0.,1800.,10,-1,1.);
    #Filebenchmarks->cd("clu"+str(cluster))
    histoname = str(cluster)+"_bin1"
    histo2D[cluster] =  Filebenchmarks.Get(histoname)
    #c=ROOT.TCanvas()
    #histo2D[cluster].Draw()
    #c.Print("teste.png")
    #print histo2D[cluster].GetSize()
    Xaxis = histo2D[cluster].GetXaxis()
    Yaxis = histo2D[cluster].GetYaxis()
    for ibin in range(0,int(Nvarbinmass)) :
       for ibin2 in range(0,int(Nvarbincosth)) :
           mass = float(1801- 20*(ibin)) 
           cost = 1.01- 0.2*(ibin2)
           #print str(mass) + " " + str(cost)
           binspot= histo2D[cluster].FindBin(mass,cost)
           nevBin = histo2D[cluster].GetBinContent(int(binspot))
           Matrix1[cluster][ibin][ibin2] =  nevBin
           counter = counter + histo2D[cluster].GetBinContent(int(binspot))
           #print (ibin,ibin2,Matrix1[cluster][ibin][ibin2],histo2D[cluster].GetBinContent(int(binspot)))
    print str(cluster) + " " +str(counter) + " events to reweinght to benchmark"
    counter=0
Filebenchmarks.Close()
print "read benchmarks"
######################################
# envelope - the sample 0 is the benchmarks
######################################
Fileenvelope = ROOT.TFile.Open(envelope, 'read')
histo2Dout = [[None]*nout]*nclu 
counter=0 
for cluster in range(0,nclu) :
  histoPath= "clu"+str(cluster+1)
  gDirectory.cd(histoPath)
  for out in range(0,nout) :
    histoname = str(out)+"_bin1"
    histo2Dout[cluster][out] =  gDirectory.Get(histoname)
    Xaxis = histo2Dout[cluster][out].GetXaxis()
    Yaxis = histo2Dout[cluster][out].GetYaxis()
    for ibin in range(0,int(Nvarbinmass)) :
        for ibin2 in range(0,int(Nvarbincosth)) :
            mass = float(1810- 20*(ibin)) 
            cost = 1.1- 0.2*(ibin2)
            #print str(mass) + " " + str(cost)
            binspot= histo2Dout[cluster][out].FindBin(mass,cost)
            nevBin = histo2Dout[cluster][out].GetBinContent(int(binspot))
            Matrix1out[cluster][out][ibin][ibin2] =  nevBin
            counter = counter + histo2Dout[cluster][out].GetBinContent(int(binspot))
    #print (ibin,ibin2,Matrix1[cluster][ibin][ibin2],histo2D[cluster].GetBinContent(int(binspot)))
    #print str(cluster+1) +" "+ str(out) +" "+str(counter) + " events to reweinght to benchmark"
    print str(cluster) + " "+ str(out) + " " +str(counter) + " events to reweinght to benchmark"
    counter=0
    #print histoPath + " " + histoname 
  gDirectory.Close()
Fileenvelope.Close()
print "read outliers"

######################################
# lambda-only
######################################
Filelambdaonly = ROOT.TFile.Open(lambdaonly, 'read')
histo2Dlam = [None]*Nlambda
counter=0
print lambdaonly
# the file already contains the 2D histos
gDirectory.cd("lamdaOnly")
for cluster in range(0,Nlambda) :
    histoname = str(cluster)+"_bin1"
    histo2Dlam[cluster] =  gDirectory.Get(histoname)
    #c=ROOT.TCanvas()
    #histo2Dlam[cluster].Draw()
    #c.Print("teste_lam.png")
    Xaxis = histo2Dlam[cluster].GetXaxis()
    Yaxis = histo2Dlam[cluster].GetYaxis()
    for ibin in range(0,int(Nvarbinmass)) :
        for ibin2 in range(0,int(Nvarbincosth)) :
            mass = float(1810- 20*(ibin)) 
            cost = 1.1- 0.2*(ibin2)
            #print str(mass) + " " + str(cost)
            binspot= histo2Dlam[cluster].FindBin(mass,cost)
            nevBin = histo2Dlam[cluster].GetBinContent(int(binspot))
            Matrix2out[cluster][ibin][ibin2] =  nevBin
            counter = counter + histo2Dlam[cluster].GetBinContent(int(binspot))
    #print (ibin,ibin2,Matrix1[cluster][ibin][ibin2],histo2D[cluster].GetBinContent(int(binspot)))
    print str(cluster) + " " +str(counter) + " events to reweinght to benchmark"
    counter=0
gDirectory.Close()
Filelambdaonly.Close()
print "read lambda only" 
######################################


'''
for cluster in range(0,1) :
   for ibin in range(0,int(Nvarbinmass)) :
      for ibin2 in range(0,int(Nvarbincosth)) :
          print (ibin,ibin2,Matrix1[cluster][ibin][ibin2])
'''          


######################################
## pass over all the events, make a matrix  weights
Sum2D = ROOT.TH2D("Sum2D","Sum2D",90,0.,1800.,10,-1,1.)
countereventHs=0
countereventLs=0
countereventHa=0
countereventLa=0
onebin=0
for files in range(0,13) :
   fileRead = input + file + str(files) + fileEnd 
   print fileRead 
   FileHigh = ROOT.TFile.Open(fileRead, 'read')
   tree= FileHigh.Get('fsDir/GenTree')
   numEntries = tree.GetEntries()
   countereventHs = countereventHs+ numEntries
   for event in tree:
       Mtot =  event.mHH # change to the gen mtot
       Cost = event.cosTheta # change to the gen cost
       #print Cost
       Sum2D.Fill(Mtot,Cost)
       # find the bin
       imass=-1 
       icosth=-1
       for ibin in range(0,int(Nvarbinmass)) :
           #print (float(1800- 20*(ibin)),Mtot)
           if (Mtot > float(1800- 20*(ibin)) and imass < 0): 
               #print "bingo"
              imass=ibin
              continue
       for ibin in range(0,int(Nvarbincosth)) :
           #print (float(1.0- 0.2*(ibin)),Cost)
           if (Cost >= float(1.0- 0.2*(ibin)) and icosth < 0 ): 
               #print "bingo"
              icosth = ibin
              continue
       #print str(imass) + " " + str(icosth)
       if (imass < 0 or icosth < 0): print "no bin found - making fullsimed events matrix" 
       elif (imass > 0 and icosth > 0) :
           #old = Matrix2high[imass][icosth]
           Matrix2high[imass][icosth] +=  1
           countereventHa += 1
       if(files==0) : Matrix1validationhigh[imass][icosth] +=  1
   print "this file had "+str(numEntries)+" entries"
   FileHigh.Close()
print " "
print "we have "+str(countereventHs)+" events before selection"
#######################################################
c=ROOT.TCanvas()
Sum2D.Draw()
c.Print("Sum2D_new.png")

#######################################
#print onebin
#print Matrix2high[69][1]
'''
countereventH=0
countereventL=0
countereventbench=0
for ibin in range(0,int(Nvarbinmass)) :
    for ibin2 in range(0,int(Nvarbincosth)) :
        #print Matrix2[ibin][ibin2]
        #print str(ibin) + " , " +str(ibin2)+" , "+ str(Matrix1[0][ibin][ibin2]) + " " + str(Matrix2low[ibin][ibin2]) + " " + str(Matrix2high[ibin][ibin2])
        countereventH +=  Matrix2high[ibin][ibin2]
        countereventL += Matrix2low[ibin][ibin2]
        countereventbench = countereventbench + Matrix1[0][ibin][ibin2]
print "we have "+str(countereventL)+" events to reweight in the low mass category ("+str(countereventLs)+", "+str(countereventLa)+"), and"
print "we have "+str(countereventH)+" events to reweight in the high mass category ("+str(countereventHs)+", "+str(countereventHa)+"), and"
print "we have "+str(countereventbench)+" events to reweight in each benchmark"
'''
#######################################
# make the minitrees 
# Create a struct
gROOT.ProcessLine(\
                  "struct MyStruct{\
                  Int_t evt;\
                  Int_t file;\
                  Double_t mHH;\
                  Double_t cosTheta;\
                  Double_t wBox;\
                  Double_t wFlat;\
                  Double_t bench1;\
                  Double_t bench1_out1;\
                  Double_t bench1_out2;\
                  Double_t bench1_out3;\
                  Double_t bench1_out4;\
                  Double_t bench1_out5;\
                  Double_t bench1_out6;\
                  Double_t bench2;\
                  Double_t bench2_out1;\
                  Double_t bench2_out2;\
                  Double_t bench2_out3;\
                  Double_t bench2_out4;\
                  Double_t bench2_out5;\
                  Double_t bench2_out6;\
                  Double_t bench3;\
                  Double_t bench3_out1;\
                  Double_t bench3_out2;\
                  Double_t bench3_out3;\
                  Double_t bench3_out4;\
                  Double_t bench3_out5;\
                  Double_t bench3_out6;\
                  Double_t bench4;\
                  Double_t bench4_out1;\
                  Double_t bench4_out2;\
                  Double_t bench4_out3;\
                  Double_t bench4_out4;\
                  Double_t bench4_out5;\
                  Double_t bench4_out6;\
                  Double_t bench5;\
                  Double_t bench5_out1;\
                  Double_t bench5_out2;\
                  Double_t bench5_out3;\
                  Double_t bench5_out4;\
                  Double_t bench5_out5;\
                  Double_t bench5_out6;\
                  Double_t bench6;\
                  Double_t bench6_out1;\
                  Double_t bench6_out2;\
                  Double_t bench6_out3;\
                  Double_t bench6_out4;\
                  Double_t bench6_out5;\
                  Double_t bench6_out6;\
                  Double_t bench7;\
                  Double_t bench7_out1;\
                  Double_t bench7_out2;\
                  Double_t bench7_out3;\
                  Double_t bench7_out4;\
                  Double_t bench7_out5;\
                  Double_t bench7_out6;\
                  Double_t bench8;\
                  Double_t bench8_out1;\
                  Double_t bench8_out2;\
                  Double_t bench8_out3;\
                  Double_t bench8_out4;\
                  Double_t bench8_out5;\
                  Double_t bench8_out6;\
                  Double_t bench9;\
                  Double_t bench9_out1;\
                  Double_t bench9_out2;\
                  Double_t bench9_out3;\
                  Double_t bench9_out4;\
                  Double_t bench9_out5;\
                  Double_t bench9_out6;\
                  Double_t bench10;\
                  Double_t bench10_out1;\
                  Double_t bench10_out2;\
                  Double_t bench10_out3;\
                  Double_t bench10_out4;\
                  Double_t bench10_out5;\
                  Double_t bench10_out6;\
                  Double_t bench11;\
                  Double_t bench11_out1;\
                  Double_t bench11_out2;\
                  Double_t bench11_out3;\
                  Double_t bench11_out4;\
                  Double_t bench11_out5;\
                  Double_t bench11_out6;\
                  Double_t bench12;\
                  Double_t bench12_out1;\
                  Double_t bench12_out2;\
                  Double_t bench12_out3;\
                  Double_t bench12_out4;\
                  Double_t bench12_out5;\
                  Double_t bench12_out6;\
                  Double_t lam1;\
                  Double_t lam2;\
                  Double_t lam3;\
                  Double_t lam4;\
                  Double_t lam5;\
                  Double_t lam6;\
                  Double_t lam7;\
                  Double_t lam8;\
                  Double_t lam9;\
                  Double_t lam10;\
                  Double_t lam11;\
                  Double_t lam12;\
                  Double_t lam13;\
                  Double_t lam14;\
                  Double_t lam15;\
                  Double_t lam16;\
                  Double_t lam17;\
                  Double_t lam18;\
                  Double_t lam19;\
                  Double_t lam20;\
                  Double_t lam21;\
                  Double_t lam22;\
                  Double_t lam23;\
                  Double_t lam24;\
                  Double_t lam25;\
                  Double_t lam26;\
                  Double_t lam27;\
                  Double_t lam28;\
                  Double_t lam29;\
                  Double_t lam30;\
                  Double_t lam31;\
                  Double_t lam32;\
                  Double_t lam33;\
                  Double_t lam34;\
                  Double_t lam35;\
                  Double_t lam36;\
                  Double_t lam37;\
                  Double_t lam38;\
                  Double_t lam39;\
                  Double_t lam40;\
                  Double_t lam41;\
                  Double_t lam42;\
                  Double_t lam43;\
                  Double_t lam44;\
                  Double_t lam45;\
                  Double_t lam46;\
                  Double_t lam47;\
                  Double_t lam48;\
                  Double_t lam49;\
                  Double_t lam50;\
                  Double_t lam51;\
                  Double_t lam52;\
                  };")
from ROOT import MyStruct
################################
# benchmarks
benchmarksV3 = "V3benchmarks/V3_LT_output_GluGluToHHTo2B2G_"
fcluH = [None]*int(nclu+1) 
fcluL = [None]*int(nclu+1) 
################################
'''
for cluster in range(0,nclu+1) : # cluster = -1 (file =0) is for the validation sample (0 of V1)
    name = None
    if (cluster ==0) : name = "box_validation"
    elif (cluster <13): name = "JHEPv3_benchmark_" # benchmarks
    '''
fweights = ROOT.TFile("teste_weight.root","RECREATE")   
t = TTree('TCVARS','My test tree')
s = MyStruct()
t.Branch('evt',AddressOf(s,'evt'),'evt/I')
t.Branch('file',AddressOf(s,'file'),'file/I')
t.Branch('mHH',AddressOf(s,'mHH'),'mHH/D')
t.Branch('cosTheta',AddressOf(s,'cosTheta'),'cosTheta/D')
t.Branch('wBox',AddressOf(s,'wBox'),'wBox/D')
#t.Branch('mHHgen',AddressOf(s,'mHHgen'),'mHHgen/D')
#t.Branch('cosThetagen',AddressOf(s,'cosThetagen'),'cosThetagen/D')
for ii in range(1,nclu+1) : t.Branch('bench'+str(ii),AddressOf(s,'bench'+str(ii)),'bench'+str(ii)+'/D')
for ii in range(1,nclu+1) :
    for jj in range(1,nout+1) : t.Branch('bench'+str(ii)+'_out'+str(jj),AddressOf(s,'bench'+str(ii)+'_out'+str(jj)),'bench'+str(ii)+'_out'+str(jj)+'/D')
for ii in range(1,Nlambda+1) : t.Branch('lam'+str(ii),AddressOf(s,'lam'+str(ii)),'lam'+str(ii)+'/D')  
#
for files in range(0,13) :
    fileRead = input + file + str(files) + fileEnd 
    print fileRead 
    FileHigh = ROOT.TFile.Open(fileRead, 'read')
    tree= FileHigh.Get('fsDir/GenTree')
    numEntries = tree.GetEntries()
    countereventHs = countereventHs+ numEntries
    for event in tree:
           ###
           iEv =event.evt
           Mtotgen =  event.mHH # change to the gen mtot
           Costgen = event.cosTheta # change to the gen cost
           # I calculate weight by event and save to a tree
           weightclu = np.zeros((nclu))
           weightLam = np.zeros((Nlambda))
           weighout = [[0]*nout]*nclu
           weightvalidation=0
           weightFlat=0
           ###############
           # find the bin
           imass=-1 
           icosth=-1
           for ibin in range(0,int(Nvarbinmass)) :
               #print (float(1500)- 30*(ibin),massV[i][S1],float(imass))
               if (Mtotgen > float(1800- 20*(ibin)) and float(imass) < 0): 
                   imass=ibin
                   continue
           for ibin in range(0,int(Nvarbincosth)) :
               if (Costgen > 1.0- 0.2*(ibin) and icosth < 0 ): 
                   icosth = ibin
                   continue
               if (Costgen ==-1.0 and icosth < 0 ): icosth = 10
           #print str(Mtotgen)+" "+str(Costgen)+" "+ str(imass)+" "+str(icosth) 
           #print "matrices: "+str(Matrix1[0][imass][icosth])+" "+str(Matrix1validationhigh[imass][icosth]) + " " + str(Matrix2high[imass][icosth])
           if (imass < 0 or icosth < 0): print "no bin found - weight event by event " +str(Mtotgen)+" "+str(Costgen)
           elif (Matrix2high[imass][icosth] > 0 ) :
              weightFlat = float(1/Matrix2high[imass][icosth])
              weightvalidation = float(Matrix1validationhigh[imass][icosth]/Matrix2high[imass][icosth])
              for ii in range(0,nclu) : weightclu[ii] = float(Matrix1[ii][imass][icosth]/Matrix2high[imass][icosth])
              for ii in range(0,nclu) : 
                  for jj in range(0,nout) : weighout[ii][jj] = float(Matrix1out[ii][jj][imass][icosth]/Matrix2high[imass][icosth])
              for ii in range(0,Nlambda) : weightLam[ii] = float(Matrix2out[ii][imass][icosth]/Matrix2high[imass][icosth])
           else :
               #print "too many bins? The corresponding on validation "+str(Matrix1validationhigh[imass][icosth])
              weightvalidation = float(0)
              if (Matrix1validationhigh[imass][icosth] > 3) : print "too many bins? The corresponding on validation "+str(Matrix1validationhigh[imass][icosth])
              for ii in range(0,nclu) : 
                  weightclu[ii] = float(0)
                  if (Matrix1[ii][imass][icosth] > 3) : print "too many bins? The corresponding on validation "+str(Matrix1[ii][imass][icosth])
              for ii in range(0,nclu) : 
                  for jj in range(0,nout) : 
                      weighout[ii][jj] = float(0)
                      if (Matrix1out[ii][jj][imass][icosth] > 3) : print "too many bins? The corresponding on validation "+str(Matrix1out[ii][jj][imass][icosth])
              for ii in range(0,Nlambda) : 
                  weightLam[ii] = float(0)
                  if (Matrix2out[ii][imass][icosth] > 3) : print "too many bins? The corresponding on validation "+str(Matrix2out[ii][imass][icosth])
              #print weightvalidation
              #elif (cluster <13): weight = float(Matrix1[cluster-1][imass][icosth]/Matrix2high[imass][icosth]) # benchmarks
           
           s.file = int(files)
           s.evt = int(iEv)
           s.mHH = float(Mtotgen)
           s.cosTheta = float(Costgen)
           s.wBox = float(weightvalidation)
           s.wFlat = float(weightFlat)
               #for ii in range(0,nclu) : 
               #name = 'bench'+str(ii+1)
           s.bench1 = float(weightclu[0])
           s.bench2 = float(weightclu[1])
           s.bench3 = float(weightclu[2])
           s.bench4 = float(weightclu[3])
           s.bench5 = float(weightclu[4])
           s.bench6 = float(weightclu[5])
           s.bench7 = float(weightclu[6])
           s.bench8 = float(weightclu[7])
           s.bench9 = float(weightclu[8])
           s.bench10 = float(weightclu[9])
           s.bench11 = float(weightclu[10])
           s.bench12 = float(weightclu[11])
           #
           s.bench1_out1 = float(weighout[0][0])
           s.bench2_out1 = float(weighout[1][0])
           s.bench3_out1 = float(weighout[2][0])
           s.bench4_out1 = float(weighout[3][0])
           s.bench5_out1 = float(weighout[4][0])
           s.bench6_out1 = float(weighout[5][0])
           s.bench7_out1 = float(weighout[6][0])
           s.bench8_out1 = float(weighout[7][0])
           s.bench9_out1 = float(weighout[8][0])
           s.bench10_out1 = float(weighout[9][0])
           s.bench11_out1 = float(weighout[10][0])
           s.bench12_out1 = float(weighout[11][0])
           #
           s.bench1_out2 = float(weighout[0][1])
           s.bench2_out2 = float(weighout[1][1])
           s.bench3_out2 = float(weighout[2][1])
           s.bench4_out2 = float(weighout[3][1])
           s.bench5_out2 = float(weighout[4][1])
           s.bench6_out2 = float(weighout[5][1])
           s.bench7_out2 = float(weighout[6][1])
           s.bench8_out2 = float(weighout[7][1])
           s.bench9_out2 = float(weighout[8][1])
           s.bench10_out2 = float(weighout[9][1])
           s.bench11_out2 = float(weighout[10][1])
           s.bench12_out2 = float(weighout[11][1])
           #
           s.bench1_out3 = float(weighout[0][2])
           s.bench2_out3 = float(weighout[1][2])
           s.bench3_out3 = float(weighout[2][2])
           s.bench4_out3 = float(weighout[3][2])
           s.bench5_out3 = float(weighout[4][2])
           s.bench6_out3 = float(weighout[5][2])
           s.bench7_out3 = float(weighout[6][2])
           s.bench8_out3 = float(weighout[7][2])
           s.bench9_out3 = float(weighout[8][2])
           s.bench10_out3 = float(weighout[9][2])
           s.bench11_out3 = float(weighout[10][2])
           s.bench12_out3 = float(weighout[11][2])
           #
           s.bench1_out4 = float(weighout[0][3])
           s.bench2_out4 = float(weighout[1][3])
           s.bench3_out4 = float(weighout[2][3])
           s.bench4_out4 = float(weighout[3][3])
           s.bench5_out4 = float(weighout[4][3])
           s.bench6_out4 = float(weighout[5][3])
           s.bench7_out4 = float(weighout[6][3])
           s.bench8_out4 = float(weighout[7][3])
           s.bench9_out4 = float(weighout[8][3])
           s.bench10_out4 = float(weighout[9][3])
           s.bench11_out4 = float(weighout[10][3])
           s.bench12_out4 = float(weighout[11][3])    
           #
           s.bench1_out5 = float(weighout[0][4])
           s.bench2_out5 = float(weighout[1][4])
           s.bench3_out5 = float(weighout[2][4])
           s.bench4_out5 = float(weighout[3][4])
           s.bench5_out5 = float(weighout[4][4])
           s.bench6_out5 = float(weighout[5][4])
           s.bench7_out5 = float(weighout[6][4])
           s.bench8_out5 = float(weighout[7][4])
           s.bench9_out5 = float(weighout[8][4])
           s.bench10_out5 = float(weighout[9][4])
           s.bench11_out5 = float(weighout[10][4])
           s.bench12_out5 = float(weighout[11][4])
           #
           s.bench1_out6 = float(weighout[0][5])
           s.bench2_out6 = float(weighout[1][5])
           s.bench3_out6 = float(weighout[2][5])
           s.bench4_out6 = float(weighout[3][5])
           s.bench5_out6 = float(weighout[4][5])
           s.bench6_out6 = float(weighout[5][5])
           s.bench7_out6 = float(weighout[6][5])
           s.bench8_out6 = float(weighout[7][5])
           s.bench9_out6 = float(weighout[8][5])
           s.bench10_out6 = float(weighout[9][5])
           s.bench11_out6 = float(weighout[10][5])
           s.bench12_out6 = float(weighout[11][5]) 
           #
           s.lam1 = float(weightLam[0])
           s.lam2 = float(weightLam[1])
           s.lam3 = float(weightLam[2])
           s.lam4 = float(weightLam[3])
           s.lam5 = float(weightLam[4])
           s.lam6 = float(weightLam[5])
           s.lam7 = float(weightLam[6])
           s.lam8 = float(weightLam[7])
           s.lam9 = float(weightLam[8])
           s.lam10 = float(weightLam[9])
           s.lam11 = float(weightLam[10])
           s.lam12 = float(weightLam[11])
           s.lam13 = float(weightLam[12])
           s.lam14 = float(weightLam[13])
           s.lam15 = float(weightLam[14])
           s.lam16 = float(weightLam[15])
           s.lam17 = float(weightLam[16])
           s.lam18 = float(weightLam[17])
           s.lam19 = float(weightLam[18])
           s.lam20 = float(weightLam[19])
           s.lam21 = float(weightLam[20])
           s.lam22 = float(weightLam[21])
           s.lam23 = float(weightLam[22])
           s.lam24 = float(weightLam[23])
           s.lam25 = float(weightLam[24])
           s.lam26 = float(weightLam[25])
           s.lam27 = float(weightLam[26])
           s.lam28 = float(weightLam[27])
           s.lam29 = float(weightLam[28])
           s.lam30 = float(weightLam[29])
           s.lam31 = float(weightLam[30])
           s.lam32 = float(weightLam[31])
           s.lam33 = float(weightLam[32])
           s.lam34 = float(weightLam[33])
           s.lam35 = float(weightLam[34])
           s.lam36 = float(weightLam[35])
           s.lam37 = float(weightLam[36])
           s.lam38 = float(weightLam[37])
           s.lam39 = float(weightLam[38])
           s.lam40 = float(weightLam[39])
           s.lam41 = float(weightLam[40])
           s.lam42 = float(weightLam[41])
           s.lam43 = float(weightLam[42])
           s.lam44 = float(weightLam[43])
           s.lam45 = float(weightLam[44])
           s.lam46 = float(weightLam[45])
           s.lam47 = float(weightLam[46])
           s.lam48 = float(weightLam[47])
           s.lam49 = float(weightLam[48])
           s.lam50 = float(weightLam[49])
           s.lam51 = float(weightLam[50])
           s.lam52 = float(weightLam[51])

           '''
           s.mjj = float(Mjj)
           s.evWeight = float(evWei)
           s.evWeightTh = float(weight)
           s.evWeightTot = float(weight*evWei)
           '''
           t.Fill()
    FileHigh.Close()
fweights.Write()
fweights.Close()
print "saved "+"teste_weight.root"

'''
###################################################
# lambda only
##################################################
lambdaonlyFolder = "lambdaonly/V3_LT_output_GluGluToHHTo2B2G_"
fcluH = [None]*Nlambda
fcluL = [None]*Nlambda 
name = "lambda_only"
for cluster in range(0,52) : 
    fcluL[cluster] = ROOT.TFile(lambdaonlyFolder+name+str(cluster+1)+fileL,"RECREATE")   
    t = TTree('TCVARS','My test tree')
    s = MyStruct()
    t.Branch('cut_based_ct',AddressOf(s,'cut_based_ct'),'cut_based_ct/I')
    t.Branch('mtotgen',AddressOf(s,'mtotgen'),'mtotgen/D')
    t.Branch('costgen',AddressOf(s,'costgen'),'costgen/D')
    t.Branch('mtot',AddressOf(s,'mtot'),'mtot/D')
    t.Branch('mgg',AddressOf(s,'mgg'),'mgg/D')
    t.Branch('mjj',AddressOf(s,'mjj'),'mjj/D')
    t.Branch('evWeight',AddressOf(s,'evWeight'),'evWeight/D')
    t.Branch('evWeightTh',AddressOf(s,'evWeightTh'),'evWeightTh/D')
    t.Branch('evWeightTot',AddressOf(s,'evWeightTot'),'evWeightTot/D')
    #
    for files in range(0,13) :
       fileLow = inputLM + file + str(files) + fileL 
       FileLow = ROOT.TFile.Open(fileLow, 'read')
       ################################
       # low
       for event in FileLow.TCVARS:
           #
           ###
           Mtotgen =  event.mtot # change to the gen mtot
           Costgen = event.cut_based_ct # change to the gen cost
           Mtot =  event.mtot 
           Mgg =  event.mgg 
           Cat = event.cut_based_ct 
           Mjj =  event.mjj 
           evWei = event.evWeight
           # I calculate weight by event and save to a tree
           weight = 0 #np.zeros((nclu))
           weightvalidation=0
           ###############
           # find the bin
           imass=-1 
           icosth=-1
           for ibin in range(0,int(Nvarbinmass)) :
               #print (float(1500)- 30*(ibin),massV[i][S1],float(imass))
               if (Mtotgen > float(1800- 20*(ibin)) and float(imass) < 0): 
                  imass=ibin
                  continue
           for ibin in range(0,int(Nvarbincosth)) :
               if (Costgen > 1.0- 0.2*(ibin) and icosth < 0 ): 
                  icosth = ibin
                  continue
               if (Costgen ==-1.0 and icosth < 0 ): icosth = 10
           #print str(Matrix1[imass][icosth]) + " " + str(Matrix2low[imass][icosth])
           if (imass < 0 or icosth < 0): print "no bin found - weight event by event " +str(Mtotgen)+" "+str(Costgen)
           elif (Matrix2low[imass][icosth] > 0 ) :
               weight = float(Matrix2out[cluster][imass][icosth]/Matrix2low[imass][icosth])                
           s.cut_based_ct = int(Cat)
           s.mtotgen = float(Mtotgen)
           s.costgen = float(Costgen)
           s.mtot = float(Mtot)
           s.mgg = float(Mgg)
           s.mjj = float(Mjj)
           s.evWeight = float(evWei)
           s.evWeightTh = float(weight)
           s.evWeightTot = float(weight*evWei)
           t.Fill()
    fcluL[cluster].Write()
    fcluL[cluster].Close()
    print "saved "+str(lambdaonlyFolder+name+str(cluster+1)+fileL)
    ################################
    #
    ###############################
    fcluH[cluster] = ROOT.TFile(lambdaonlyFolder+str(cluster+1)+fileH,"RECREATE")   
    tH = TTree('TCVARS','My test tree')
    tH.Branch('cut_based_ct',AddressOf(s,'cut_based_ct'),'cut_based_ct/I')
    tH.Branch('mtotgen',AddressOf(s,'mtotgen'),'mtotgen/D')
    tH.Branch('costgen',AddressOf(s,'costgen'),'costgen/D')
    tH.Branch('mtot',AddressOf(s,'mtot'),'mtot/D')
    tH.Branch('mgg',AddressOf(s,'mgg'),'mgg/D')
    tH.Branch('mjj',AddressOf(s,'mjj'),'mjj/D')
    tH.Branch('evWeight',AddressOf(s,'evWeight'),'evWeight/D')
    tH.Branch('evWeightTh',AddressOf(s,'evWeightTh'),'evWeightTh/D')
    tH.Branch('evWeightTot',AddressOf(s,'evWeightTot'),'evWeightTot/D')
    for files in range(0,13) :
       #################################
       # high
       fileHigh = inputHM + file + str(files) + fileH        
       FileHigh = ROOT.TFile.Open(fileHigh, 'read') 
       for event in FileHigh.TCVARS:
           #
           ###
           Mtotgen =  event.mtot # change to the gen mtot
           Costgen = event.cut_based_ct # change to the gen cost
           Mtot =  event.mtot 
           Mgg =  event.mgg 
           Cat = event.cut_based_ct 
           Mjj =  event.mjj 
           evWei = event.evWeight
           # I calculate weight by event and save to a tree
           weight = 0 #np.zeros((nclu))
           weightvalidation=0
           ###############
           # find the bin
           imass=-1 
           icosth=-1
           for ibin in range(0,int(Nvarbinmass)) :
               #print (float(1500)- 30*(ibin),massV[i][S1],float(imass))
               if (Mtotgen > float(1800- 20*(ibin)) and float(imass) < 0): 
                   imass=ibin
                   continue
           for ibin in range(0,int(Nvarbincosth)) :
               if (Costgen > 1.0- 0.2*(ibin) and icosth < 0 ): 
                   icosth = ibin
                   continue
               if (Costgen ==-1.0 and icosth < 0 ): icosth = 10
           #print str(Matrix1[imass][icosth]) + " " + str(Matrix2low[imass][icosth])
           if (imass < 0 or icosth < 0): print "no bin found - weight event by event " +str(Mtotgen)+" "+str(Costgen)
           elif (Matrix2low[imass][icosth] > 0 ) :
              weight = float(Matrix2out[cluster][imass][icosth]/Matrix2high[imass][icosth]) # benchmarks
           s.cut_based_ct = int(Cat)
           s.mtotgen = float(Mtotgen)
           s.costgen = float(Costgen)
           s.mtot = float(Mtot)
           s.mgg = float(Mgg)
           s.mjj = float(Mjj)
           s.evWeight = float(evWei)
           s.evWeightTh = float(weight)
           s.evWeightTot = float(weight*evWei)
           tH.Fill()
    fcluH[cluster].Write()
    fcluH[cluster].Close()
    print "saved "+ lambdaonlyFolder+name+str(cluster+1)+fileH
###################################################
# outliers
##################################################
outliersV3 = "V3outliers/V3_LT_output_GluGluToHHTo2B2G_"
fcluH = [[None]*nout]*nclu 
fcluL = [[None]*nout]*nclu 
name = "JHEPv3_cluster_"
name2="_outlier_"
# low mass
for cluster in range(0,nclu) : 
  for out in range(0,nout) :
    fcluL[cluster][out] = ROOT.TFile(outliersV3+name+str(cluster+1)+name2+ str(out) +fileL,"RECREATE")   
    t = TTree('TCVARS','My test tree')
    s = MyStruct()
    t.Branch('cut_based_ct',AddressOf(s,'cut_based_ct'),'cut_based_ct/I')
    t.Branch('mtotgen',AddressOf(s,'mtotgen'),'mtotgen/D')
    t.Branch('costgen',AddressOf(s,'costgen'),'costgen/D')
    t.Branch('mtot',AddressOf(s,'mtot'),'mtot/D')
    t.Branch('mgg',AddressOf(s,'mgg'),'mgg/D')
    t.Branch('mjj',AddressOf(s,'mjj'),'mjj/D')
    t.Branch('evWeight',AddressOf(s,'evWeight'),'evWeight/D')
    t.Branch('evWeightTh',AddressOf(s,'evWeightTh'),'evWeightTh/D')
    t.Branch('evWeightTot',AddressOf(s,'evWeightTot'),'evWeightTot/D')
    #t.Branch('mtotTHweighted',AddressOf(s,'mtotTHweighted'),'mtotTHweighted/D')
    for files in range(0,13) :
       fileLow = inputLM + file + str(files) + fileL 
       FileLow = ROOT.TFile.Open(fileLow, 'read')
       ################################
       # low
       for event in FileLow.TCVARS:
           #
           ###
           Mtotgen =  event.mtot # change to the gen mtot
           Costgen = event.cut_based_ct # change to the gen cost
           Mtot =  event.mtot 
           Mgg =  event.mgg 
           Cat = event.cut_based_ct 
           Mjj =  event.mjj 
           evWei = event.evWeight
           # I calculate weight by event and save to a tree
           weight = 0 #np.zeros((nclu))
           weightvalidation=0
           ###############
           # find the bin
           imass=-1 
           icosth=-1
           for ibin in range(0,int(Nvarbinmass)) :
               #print (float(1500)- 30*(ibin),massV[i][S1],float(imass))
               if (Mtotgen > float(1800- 20*(ibin)) and float(imass) < 0): 
                  imass=ibin
                  continue
           for ibin in range(0,int(Nvarbincosth)) :
               if (Costgen > 1.0- 0.2*(ibin) and icosth < 0 ): 
                  icosth = ibin
                  continue
               if (Costgen ==-1.0 and icosth < 0 ): icosth = 10
           #print str(Matrix1[imass][icosth]) + " " + str(Matrix2low[imass][icosth])
           if (imass < 0 or icosth < 0): print "no bin found - weight event by event " +str(Mtotgen)+" "+str(Costgen)
           elif (Matrix2low[imass][icosth] > 0 ) :
               weight = float(Matrix1out[cluster][out][imass][icosth]/Matrix2low[imass][icosth])                
           s.cut_based_ct = int(Cat)
           s.mtotgen = float(Mtotgen)
           s.costgen = float(Costgen)
           s.mtot = float(Mtot)
           s.mgg = float(Mgg)
           s.mjj = float(Mjj)
           s.evWeight = float(evWei)
           s.evWeightTh = float(weight)
           s.evWeightTot = float(weight*evWei)
           #s.mtotTHweighted= float(Mtot)
           t.Fill()
    fcluL[cluster][out].Write()
    fcluL[cluster][out].Close()
    print "saved "+str(outliersV3+name+str(cluster+1)+name2+ str(out) +fileL)
    ################################
    #
    ###############################
# high mass
for cluster in range(0,nclu) : 
    for out in range(0,nout) :    
      fcluH[cluster][out] = ROOT.TFile(outliersV3+name+str(cluster+1)+name2+ str(out) +fileH,"RECREATE")   
      tHH = TTree('TCVARS','My test tree')
      s = MyStruct()
      tHH.Branch('cut_based_ct',AddressOf(s,'cut_based_ct'),'cut_based_ct/I')
      tHH.Branch('mtotgen',AddressOf(s,'mtotgen'),'mtotgen/D')
      tHH.Branch('costgen',AddressOf(s,'costgen'),'costgen/D')
      tHH.Branch('mtot',AddressOf(s,'mtot'),'mtot/D')
      tHH.Branch('mgg',AddressOf(s,'mgg'),'mgg/D')
      tHH.Branch('mjj',AddressOf(s,'mjj'),'mjj/D')
      tHH.Branch('evWeight',AddressOf(s,'evWeight'),'evWeight/D')
      tHH.Branch('evWeightTh',AddressOf(s,'evWeightTh'),'evWeightTh/D')
      tHH.Branch('evWeightTot',AddressOf(s,'evWeightTot'),'evWeightTot/D')
      for files in range(0,13) :
         #################################
         # high
         fileHigh = inputHM + file + str(files) + fileH        
         FileHigh = ROOT.TFile.Open(fileHigh, 'read') 
         for event in FileHigh.TCVARS:
             ###
             Mtotgen =  event.mtot # change to the gen mtot
             Costgen = event.cut_based_ct # change to the gen cost
             Mtot =  event.mtot 
             Mgg =  event.mgg 
             Cat = event.cut_based_ct 
             Mjj =  event.mjj 
             evWei = event.evWeight
             # I calculate weight by event and save to a tree
             weight = 0 #np.zeros((nclu))
             weightvalidation=0
             ###############
             # find the bin
             imass=-1 
             icosth=-1
             for ibin in range(0,int(Nvarbinmass)) :
                 #print (float(1500)- 30*(ibin),massV[i][S1],float(imass))
                 if (Mtotgen > float(1800- 20*(ibin)) and float(imass) < 0): 
                     imass=ibin
                     continue
             for ibin in range(0,int(Nvarbincosth)) :
                 if (Costgen > 1.0- 0.2*(ibin) and icosth < 0 ): 
                     icosth = ibin
                     continue
                 if (Costgen ==-1.0 and icosth < 0 ): icosth = 10
             #print str(Matrix1[imass][icosth]) + " " + str(Matrix2low[imass][icosth])
             if (imass < 0 or icosth < 0): print "no bin found - weight event by event " +str(Mtotgen)+" "+str(Costgen)
             elif (Matrix2low[imass][icosth] > 0 ) : weight = float(Matrix1out[cluster][out][imass][icosth]/Matrix2high[imass][icosth]) # benchmarks
             s.cut_based_ct = int(Cat)
             s.mtotgen = float(Mtotgen)
             s.costgen = float(Costgen)
             s.mtot = float(Mtot)
             s.mgg = float(Mgg)
             s.mjj = float(Mjj)
             s.evWeight = float(evWei)
             #s.evWeightTh = float(weight)
             s.evWeightTot = float(weight*evWei)
             tHH.Fill()
      fcluH[cluster][out].Write()
      fcluH[cluster][out].Close()
      print "saved "+str(outliersV3+name+str(cluster+1)+name2+ str(out) +fileH)
       '''


