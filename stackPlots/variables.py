nbin = 40
dr = "sqrt( (leadingPhoton.Eta() - subleadingPhoton.Eta())*(leadingPhoton.Eta() - subleadingPhoton.Eta()) + (leadingPhoton.Phi() - subleadingPhoton.Phi())*(leadingPhoton.Phi() - subleadingPhoton.Phi()) )"

plots = []
plots.append(["j1ratio_dijet", "leadingJet.Pt()/dijetCandidate.M()", "p_{T}(j_{1})/M(jj)", nbin, 0.1, 1.5])
plots.append(["dijet_deta", "fabs(leadingJet.Eta() - subleadingJet.Eta())", "#Delta#eta between jets", nbin, 0, 5])
plots.append(["diPho_Mass", "diphotonCandidate.M()", "DiPhoton Candidate Mass (GeV)", nbin, 100, 180])
#plots.append(["costhetastar", "fabs(CosThetaStar)", "|cos#theta*|", nbin, 0, 1])
plots.append(["leadingPhoton_pt", "leadingPhoton.pt()", "Leading Photon Pt (GeV)", nbin, 30, 300])
plots.append(["nvtx", "nvtx", "Number of vertices", 30, 0, 30])
plots.append(["diPho_Mass", "diphotonCandidate.M()", "DiPhoton Candidate Mass (GeV)", nbin, 100, 180])
plots.append(["diPho_Mass_HM", "diphotonCandidate.M()", "DiPhoton Candidate Mass (GeV)", nbin, 80, 2000])
plots.append(["diJet_Mass", "dijetCandidate.M()", "DiJet Candidate Mass (GeV)", nbin, 60, 180])
plots.append(["diJet_Mass_Limit", "dijetCandidate.M()", "DiJet Candidate Mass (GeV)", nbin, 60, 180])
plots.append(["diJet_Mass_HM", "dijetCandidate.M()", "DiJet Candidate Mass (GeV)", nbin, 80, 2000])
plots.append(["leadingJet_pt", "leadingJet.pt()", "Leading Jet Pt (GeV)", nbin, 15, 200] )
plots.append(["subleadingJet_pt", "subleadingJet.pt()", "Subleading Jet Pt (GeV)", nbin, 15, 80] )
plots.append(["leadingJet_eta", "leadingJet.Eta()", "Leading Jet Eta", nbin, -3, 3] )
plots.append(["leadingPhoton_eta", "leadingPhoton.Eta()", "Leading Photon Eta", nbin, -3, 3] )
plots.append(["dicandidate_Mass", "diHiggsCandidate.M()", "DiHiggs Candidate Mass (GeV)", nbin, 100, 1000])
plots.append(["MX", "diHiggsCandidate.M() - dijetCandidate.M() + 125.", "M_{X} (GeV)", nbin, 100, 1000])
plots.append(["MKF", "diHiggsCandidate_KF.M()", "M_{KinFit}(bb#gamma#gamma) (GeV)", nbin, 100, 1000])
plots.append(["dicandidate_Mass_Limit", "diHiggsCandidate.M()", "DiHiggs Candidate Mass (GeV)", nbin, 225, 350])
plots.append(["dicandidate_Mass_HM", "diHiggsCandidate.M()", "DiHiggs Candidate Mass (GeV)", nbin, 250, 5000])
plots.append(["btagSum", "leadingJet_bDis+subleadingJet_bDis", "Sum of b-tag of jet pair", nbin, 0, 2])
plots.append(["subleadingPhoton_pt", "subleadingPhoton.pt()", "Subleading Photon Pt (GeV)", nbin, 30, 150])
plots.append(["subleadingPhoton_eta", "subleadingPhoton.eta()", "Subleading Photon Eta)", nbin, -3, 3])
plots.append(["dr_photons", dr, "#DeltaR between photons", nbin, 0, 10])
plots.append(["leadingPho_MVA", "leadingPhotonIDMVA", "Leading Photon #gammaMVA discriminant", nbin, 0, 1])
plots.append(["subleadingPho_MVA", "subleadingPhotonIDMVA", "SubLeading Photon #gammaMVA discriminant", nbin, 0, 1])
