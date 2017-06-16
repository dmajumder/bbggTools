from pullClass import *
from ROOT import *
import json, os
import shutil
from configsShapeSliceMassPlots import *
import resource

#SetMemoryPolicy( kMemoryStrict )

gStyle.SetOptStat(0)
dummyTFile = TFile("dummy.root", "RECREATE")

if not os.path.exists(dirName):
        print dirName, "doesn't exist, creating it..."
        os.makedirs(dirName)
        shutil.copy2(dirPrefix + "index.php", dirName+"/index.php")
        if os.path.exists(dirName):
                print dirName, "now exists!"

datasets = json.load(data_file)

Trees = {}

CutSignal = Cut
if doBlind == True:
	Cut += " && !((diphotonCandidate.M() > 115 && diphotonCandidate.M() < 135))"
if isPhoCR == True:
	Cut += " && (isPhotonCR == 1)"
	CutSignal += " && (isPhotonCR == 1)"
if isPhoCR == False:
	Cut += " && (isSignal == 1)"
	CutSignal += " && (isSignal == 1)"
if doSignalRegion == True:
	CutSignal += " && ( leadingJet_bDis > "+ str(BTAG) + " || subleadingJet_bDis > "+str(BTAG)+" ) "
	Cut += " && ( leadingJet_bDis > "+ str(BTAG) + " || subleadingJet_bDis > "+ str(BTAG) + " ) "
if doJetCR == True:
	Cut += " && leadingJet_bDis < "+ str(BTAG) + " && subleadingJet_bDis < "+ str(BTAG) + " "
weightedcut = ""
weightedcut += "( genTotalWeight *lumiFactor)*"
if (doPUweight):
	weightedcut += "( puweight )*("+Cut+")"
weightedCut = TCut(weightedcut)
cut_data = TCut(Cut)
cut_signal = TCut(weightedcut.replace("!((diphotonCandidate.M() > 115 && diphotonCandidate.M() < 135))", "(1>0)"))

colors = []
colors.append(kRed)
colors.append(kBlue)
colors.append(kMagenta)
colors.append(kViolet)
colors.append(kGreen)

kColor=0

for plot in plots:
    variable = plot[1]
    varName = plot[2]
    thisStack = 0
    thisHist = 0
    thisStack = myStack('test'+plot[0], varName, varName, dirName, lumi)
    if hideData == True:
        thisStack.hideData()
    if hideStat == True:
        thisStack.hideStat()
    if isPhoCR == 1:
        thisStack.makePhoCR()
    if doJetCR == 1:
        thisStack.makeJetCR()
    if doShape == True:
        thisStack.doShape()
    if useJsonWeighting == True:
        thisStack.useJsonWeighting()



    thisStack.setYear(year)

    modelHist = TH1F(plot[0]+"_hist", "", plot[3], plot[4], plot[5])

    backgroundHists = []
    for background in datasets["background"]:
        if not addbbH and 'bbH' in background: continue
	if not addHiggs and 'VH' in background: continue
	if not addHiggs and 'ttH' in background: continue
	if not addHiggs and 'ggH' in background: continue
	if not addHiggs and 'VBF' in background: continue
        if not dyjets and "DYJ" in background: continue
        if "QCD" in background: continue
        print background
        for i,fi in enumerate(datasets["background"][background]["files"]):
            print "file:"
            print fi
            thisTreeLoc = fi["file"]
	    skipEmptyFile = False
            if thisTreeLoc not in Trees:
                Trees[thisTreeLoc] = TChain("bbggSelectionTree")
                Trees[thisTreeLoc].AddFile(bkgLocation+thisTreeLoc)
                SetOwnership( Trees[thisTreeLoc], True )
            thisWeightedCut = weightedCut
            myCut = thisWeightedCut

            Histos = []
            Max = [] 
            #do plots in bins of mass
            for j in range(0,5):
                thisName = plot[0]+"_hist"+"_"+background
                thisHist = modelHist.Clone(thisName)
                thisHist.SetLineColor(colors[i]+j)
                locName = thisName+str(j)
                locHist = thisHist.Clone(locName)


                massCut = "diphotonCandidate.M()>"+str(100+j*20)+" && diphotonCandidate.M() <"+str(100+(j+1)*20)
                myCut += massCut
                Trees[thisTreeLoc].Draw(plot[1]+">>"+locName, myCut)

                myCut = TCut(myCut.GetTitle().replace("&&(diphotonCandidate.M()>"+str(100+j*20)+" && diphotonCandidate.M() <"+str(100+(j+1)*20)+")",""))
                Histos.append(locHist)
                if locHist.Integral()!=0:
                    Max.append(locHist.GetMaximum()/locHist.Integral())

            cs = TCanvas(plot[0]+"_"+background,plot[0]+"_"+background, 800, 600)
            cs.cd()
            histCount=0
            for histo in Histos:
                histo.Sumw2()
                if histo.Integral()!=0:
                    histo.Scale(1./histo.Integral())
                if histCount == 0: 
                    histo.GetYaxis().SetRangeUser(0,max(Max)*1.1)
                    histo.GetXaxis().SetTitle(plot[2])
                    histo.Draw("HistE")
                    histCount+=1
                else:
                    histo.Draw("sameHistE")
            
            cs.SaveAs(dirPrefix+dirSuffix+"/"+plot[0]+"_"+background+"_"+str(i)+".png")
            cs.SaveAs(dirPrefix+dirSuffix+"/"+plot[0]+"_"+background+"_"+str(i)+".pdf")
            cs.Clear()

