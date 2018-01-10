import ROOT

# Get the data from the ROOT file
root_bkg = ROOT.TChain('bbggSelectionTree')
root_bkg.AddFile('/afs/cern.ch/work/m/micheli/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/test/RunJobs/Background_20170620/output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa.root')
print 'Background events:',root_bkg.GetEntries()
root_sig = ROOT.TChain('bbggSelectionTree')
root_sig.AddFile(' /afs/cern.ch/user/m/micheli/scratch1/CMSSW_8_0_26_patch1/src/flashgg/bbggTools/TrainMVA/AllNonResSig_20170620.root')
#root_sig.AddFile('res_lowmass.root')
print 'Signal events:',root_sig.GetEntries()

# Useful output information will be stored in a new root file:
outfileName = "StdVariables_DiphoJets.root"
f_out = ROOT.TFile(outfileName,"RECREATE")

# Create the TMVA factory
ROOT.TMVA.Tools.Instance()
factory = ROOT.TMVA.Factory("TMVAClassification", f_out,"AnalysisType=Classification")

# Add the six variables to the TMVA factory as floats
dr_leadPhoLeadJet ="sqrt( (leadingPhoton.Eta() - leadingJet.Eta())*(leadingPhoton.Eta() - leadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - leadingJet.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - leadingJet.Phi()) )"
dr_leadPhoSubleadJet ="sqrt( (leadingPhoton.Eta() - subleadingJet.Eta())*(leadingPhoton.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingJet.Phi()) )"
dr_subleadPhoLeadJet ="sqrt( (subleadingPhoton.Eta() - leadingJet.Eta())*(subleadingPhoton.Eta() - leadingJet.Eta()) + TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - leadingJet.Phi())*TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - leadingJet.Phi()) )"
dr_subleadPhoSubleadJet ="sqrt( (subleadingPhoton.Eta() - subleadingJet.Eta())*(subleadingPhoton.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(subleadingPhoton.Phi() - subleadingJet.Phi()) )"
mvaVars = [
##Main: 
'leadingJet_bDis',
'subleadingJet_bDis',
'diphotonCandidate.Pt()/(diHiggsCandidate.M())',
'fabs(CosThetaStar_CS)',
'fabs(CosTheta_bb)',
'fabs(CosTheta_gg)',
'dijetCandidate.Pt()/(diHiggsCandidate.M())'
##########new vars:
#    'diHiggsCandidate.Pt()/(diHiggsCandidate.M())',
#dr photons:
#    'sqrt( (leadingPhoton.Eta() - subleadingPhoton.Eta())*(leadingPhoton.Eta() - subleadingPhoton.Eta()) + TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingPhoton.Phi())*TVector2::Phi_mpi_pi(leadingPhoton.Phi() - subleadingPhoton.Phi()) )',
#dr jets:
#    'sqrt( (leadingJet.Eta() - subleadingJet.Eta())*(leadingJet.Eta() - subleadingJet.Eta()) + TVector2::Phi_mpi_pi(leadingJet.Phi() - subleadingJet.Phi())*TVector2::Phi_mpi_pi(leadingJet.Phi() - subleadingJet.Phi()) )',
#dphi (hh):
#    'TVector2::Phi_mpi_pi(diphotonCandidate.Phi()-dijetCandidate.Phi())',
#dr (gamma-jet):
#    dr_leadPhoLeadJet,
#dr_leadPhoSubleadJet,
#dr_subleadPhoLeadJet,
#dr_subleadPhoSubleadJet
           ]

for x in mvaVars:
    factory.AddVariable(x,"F")



# Link the signal and background to the root_data ntuple
factory.AddSignalTree(root_sig)
factory.AddBackgroundTree(root_bkg)

# cuts defining the signal and background sample
###high mass cut
#sigCut = ROOT.TCut("(isSignal == 1 && (diHiggsCandidate.M() - dijetCandidate.M() -diphotonCandidate.M() + 250) > 400) && leadingJet_bDis > -1 && subleadingJet_bDis > -1")
#bkgCut = ROOT.TCut("(isSignal == 0 && (diHiggsCandidate.M() - dijetCandidate.M() -diphotonCandidate.M() + 250) > 400) && leadingJet_bDis > -1 && subleadingJet_bDis > -1")
###no cut on mass
sigCut = ROOT.TCut("(isSignal == 1 &&  leadingJet_bDis > -1 && subleadingJet_bDis > -1)")
bkgCut = ROOT.TCut("(isSignal == 0 &&  leadingJet_bDis > -1 && subleadingJet_bDis > -1)")

#sigCut = ROOT.TCut("(isSignal == 1 && (diHiggsCandidate.M() - dijetCandidate.M() + 125) > 350) ")
#bkgCut = ROOT.TCut("(isSignal == 0 && (diHiggsCandidate.M() - dijetCandidate.M() + 125) > 350) ")



# Prepare the training/testing signal/background
factory.PrepareTrainingAndTestTree(sigCut,bkgCut,"SplitMode=Random:NormMode=NumEvents:!V")

# Book the SVM method and train/test
#method = factory.BookMethod( ROOT.TMVA.Types.kSVM, "SVM", "C=1.0:Gamma=0.005:Tol=0.001:VarTransform=None" )
#method = factory.BookMethod( ROOT.TMVA.Types.kBDT, "BDT", "UseRandomisedTrees=1:NTrees=1000:BoostType=Grad:NegWeightTreatment=IgnoreNegWeightsInTraining")
#method = factory.BookMethod( ROOT.TMVA.Types.kBDT, "BDT", "NTrees=2000:BoostType=AdaBoost:AdaBoostBeta=0.6:UseRandomisedTrees=True:UseNVars=6:nCuts=2000:PruneMethod=CostComplexity:PruneStrength=-1")
#gradient boosting
method = factory.BookMethod( ROOT.TMVA.Types.kBDT, "BDTG", "UseRandomisedTrees=1:NTrees=1000:BoostType=Grad:MaxDepth=10:Shrinkage=0.2:NegWeightTreatment=IgnoreNegWeightsInTraining")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# Launch the GUI for the root macros
#ROOT.TMVA.TMVAGui( outfileName )
