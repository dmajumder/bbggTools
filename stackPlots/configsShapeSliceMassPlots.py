
##################################################
##################################################
## Configuration parameters to run MakeShape.py ##
##################################################
##################################################

doBlind = False
doShape = True
doSignalRegion = True
doJetCR = False


useJsonWeighting=False

isPhoCR = False
addHiggs = False
hideData = True
addbbH = False
dyjets = False

#do pile up reweighting
doPUweight = True

year = ""

doSignal = True

hideStat = True

#btagging working poing
# 0.46 - loose
# 0.80 - medium
# 0.935 - tight
BTAG = 0.

#Luminosity to normalize backgrounds
lumi = 35870#pb
MCSF = 1.0
#List of datasets to be used (cross section information defined there)
data_file = open("datasets/datasets80X_Moriond_onlyNRSM.json")

#number of bins in histograms
nbin = 30
dr_photons = "sqrt( (leadingPhoton.Eta() - subleadingPhoton.Eta())*(leadingPhoton.Eta() - subleadingPhoton.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingPhoton.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingPhoton.Phi()) )"
dr_jets = "sqrt( (leadingJet.Eta() - subleadingJet.Eta())*(leadingJet.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingJet.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(leadingJet.Phi() - subleadingJet.Phi()) )"
dr_leadPhoLeadJet ="sqrt( (leadingPhoton.Eta() - leadingJet.Eta())*(leadingPhoton.Eta() - leadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - leadingJet.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - leadingJet.Phi()) )"
dr_leadPhoSubleadJet ="sqrt( (leadingPhoton.Eta() - subleadingJet.Eta())*(leadingPhoton.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingJet.Phi()) )"
dr_subleadPhoLeadJet ="sqrt( (subleadingPhoton.Eta() - leadingJet.Eta())*(subleadingPhoton.Eta() - leadingJet.Eta()) + TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - leadingJet.Phi())*TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - leadingJet.Phi()) )"
dr_subleadPhoSubleadJet ="sqrt( (subleadingPhoton.Eta() - subleadingJet.Eta())*(subleadingPhoton.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - subleadingJet.Phi()) )"
dphi_hh="TVector2::Phi_mpi_pi(diphotonCandidate.Phi()-dijetCandidate.Phi())"
dr_hh="sqrt( (diphotonCandidate.Eta() - dijetCandidate.Eta())*(diphotonCandidate.Eta() - dijetCandidate.Eta()) + TVector2::Phi_mpi_pi(diphotonCandidate.Phi() - dijetCandidate.Phi())*TVector2::Phi_mpi_pi(diphotonCandidate.Phi() - dijetCandidate.Phi()) )"
n_bGen = "(subleadingJet_genFlavourb==5)+(leadingJet_genFlavourb==5)"

#plots will be saved in dirName
prefix = ""
dirSuffix = "20170616_slice"
dirPrefix = "/afs/cern.ch/user/m/micheli/www/plots/HHBBGG/"
dirName = dirPrefix + dirSuffix

#Location of root files for each invidivual samples. Name of the root files is defined in datasets/datasets(76).json
higgsoLocation="/afs/cern.ch/user/m/micheli/scratch1/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/test/RunJobs/Background_20170606_2/"
bkgLocation="/afs/cern.ch/user/m/micheli/scratch1/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/test/RunJobs/Background_20170606_2/"
dataLocation="/afs/cern.ch/user/m/micheli/scratch1/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/test/RunJobs/HHbbggSignal_20170606_2/"
signalLocation="/afs/cern.ch/user/m/micheli/scratch1/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/test/RunJobs/HHbbggSignal_20170606_2/"

#plots to be made
plots = []

#plots.append(["HHTagger", "HHTagger", "Categorization MVA", 50, -1, 1])
#plots.append(["HHTagger_LM", "HHTagger_LM", "Categorization MVA (Low Mass Training)", 50, -1, 1])
#plots.append(["HHTagger_HM", "HHTagger_HM", "Categorization MVA (High Mass Training)", 50, -1, 1])


plots.append(["diPho_Mass", "diphotonCandidate.M()", "M(#gamma#gamma) [GeV]", 80, 100, 180])
plots.append(["diJet_Mass", "dijetCandidate.M()", "M(jj) [GeV]", 40, 60, 180])

plots.append(["PhotonIDMVA2", "(customSubLeadingPhotonIDMVA)", "SubLeading Photon Id MVA", nbin, -1, 1])
plots.append(["PhotonIDMVA1", "(customLeadingPhotonIDMVA)", "Leading Photon Id MVA ", nbin, -1, 1])

plots.append(["costhetastar_cs", "fabs(CosThetaStar_CS)", "|cos#theta*|_{CS}", nbin, 0, 1])

plots.append(["CosTheta_gg", "fabs(CosTheta_gg)", "|Cos(#theta_{#gamma#gamma})|", nbin, 0, 1])
plots.append(["CosTheta_bb", "fabs(CosTheta_bb)", "|Cos(#theta_{bb})|", nbin, 0, 1])

plots.append(["diPhoton_pt_overM", "diphotonCandidate.Pt()/diHiggsCandidate.M()", "p_{T}(#gamma#gamma)/M_{jj#gamma#gamma}", nbin, 0, 1] )
plots.append(["diJet_pt_overM", "dijetCandidate.Pt()/diHiggsCandidate.M()", "p_{T}(jj)/M_{jj#gamma#gamma}", nbin, 0, 1] )

plots.append(["dphi_hh", dphi_hh, "#Delta#Phi (hh)", nbin, 0, 8])
plots.append(["leadingJet_btag", "leadingJet_bDis", "b-tag leading jet", nbin, 0, 1])
plots.append(["subleadingJet_btag", "subleadingJet_bDis", "b-tag subleading jet", nbin, 0, 1])

plots.append(["dr_hh", dr_hh, "#DeltaR (hh)", nbin, 0, 8])

plots.append(["leadingPhotonSigOverE", "leadingPhotonSigOverE", "Leading Photon #sigma_{E}/E", nbin, 0, 0.1])
plots.append(["subleadingPhotonSigOverE", "subleadingPhotonSigOverE", "Subleading Photon #sigma_{E}/E", nbin, 0, 0.1])
plots.append(["sigmaMOverMDecorr", "sigmaMOverMDecorr", "#sigma_{M_{decorr}}/M", nbin, 0, 0.1])



#cuts to be used to make plots
Cut = " isSignal && diphotonCandidate.M() > 100 && diphotonCandidate.M() < 180"
Cut += " && dijetCandidate.M() > 60 && dijetCandidate.M() < 180"
#Cut += " && (((leadingJet_bDis > 0.8 && subleadingJet_bDis > 0.8) && (leadingJet_bDis < 0.92))+((leadingJet_bDis > 0.8 && subleadingJet_bDis > 0.8) && (subleadingJet_bDis < 0.92)))"
#Cut += " && (diHiggsCandidate.M() - dijetCandidate.M() + 125) < 400"
#Cut += " && (diHiggsCandidate.M() - dijetCandidate.M() + 125.) > 280 && (diHiggsCandidate.M() - dijetCandidate.M() + 125.) < 320"
#Cut += " && diHiggsCandidate.M() > 280 && diHiggsCandidate.M() < 320"
#Cut += " && (leadingJet.pt()/dijetCandidate.M()) > 0.3333"
#Cut += " && (subleadingJet.pt()/dijetCandidate.M()) > 0.25"
#Cut += " && leadingPhoton.pt() > 35 && subleadingPhoton.pt() > 35 "
#Cut += " && leadingJet.pt() > 35 && subleadingJet.pt() > 35 "
#Cut += " && leadingJet.Eta() < 2. && leadingJet.Eta() > -2"
#Cut += " && leadingPhotonID[1] == 1 "
#Cut += " && subleadingPhotonID[1] == 1 "
#Cut += " && leadingPhotonISO[1] == 1 "
#Cut += " && subleadingPhotonISO[1] == 1 "
#Cut += " && leadingPhotonEVeto == 0 "
#Cut += " && subleadingPhotonEVeto == 0 "
#Cut += " && leadingPhotonEVeto == 1 "
#Cut += " && subleadingPhotonEVeto == 1 "
#Cut += " && leadingPhotonISO[0] == 1 "
#Cut += " && subleadingPhotonISO[0] == 1 "
#Cut += " && leadingJet.pt() > 45 && subleadingJet.pt() > 45 "
#Cut += " && leadingJet_bDis > 0.9 && subleadingJet_bDis > 0.9"
