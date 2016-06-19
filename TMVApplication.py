1#!/usr/bin/env python
# @(#)root/tmva $Id: TMVApplication.py,v 1.8 2008/03/19 21:54:39 andreas.hoecker Exp $
# ------------------------------------------------------------------------------ #
# Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #
# Package      : TMVA                                                            #
# Python script: TMVApplication.py                                               #
#                                                                                #
# This macro provides a simple example on how to use the trained classifiers     #
# within an analysis module                                                      #
#                                                                                #
# for help type "python TMVApplication.py --help"                                #
# ------------------------------------------------------------------------------ #

# --------------------------------------------
# Standard python imports
import sys              # exit
import time             # time accounting
import getopt           # command line parser
import math             # some math...
import numpy
import scipy
import tables

from array import array # used to reference variables in TMVA and TTrees
import os
import re
import traceback
from glob import glob
print sys.version

# --------------------------------------------

# Default settings for command line arguments
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
DEFAULT_METHODS  = "CutsGA,Likelihood,LikelihoodPCA,PDERS,KNN,HMatrix,Fisher,FDA_MT,MLP,SVM_Gauss,BDT,BDTD,RuleFit,Cuts, LD"
DEFAULT_DATA  = "/lustre/fs2/group/i3/lotfiben/2009/data_ic59/level3/0801/application"
# Print usage help
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
        % (DEFAULT_TREESIG, DEFAULT_TREEBKG)

    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print " "

# Main routine
def main():

    try:
        # Retrive command line options
        shortopts  = "m:i:o:d:vh?"
        longopts   = ["methods=", "inputfile=", "outputfile=","datatype=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )
        
    except getopt.GetoptError:
        # Print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    methods     = DEFAULT_METHODS
    directory   = DEFAULT_DATA
    verbose     = False
    
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-d", "--datatype"):
            directory = a
            
        elif o in ("-v", "--verbose"):
            verbose = True

    # Print methods
    #take leading and trailing white space out
    methods = methods.strip(" ")
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVApplication: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()

    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut, TH1F, TStopwatch
    print("ROOT classes successfully imported!\n") # DCS 17/06/2016 
    # check ROOT version, give alarm if 5.18
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
    
    # Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
    tmvadir = "/home/dean/software/tmva/TMVA-v4.2.0/test" 
    macro = os.path.join(tmvadir, "TMVAlogon.C")
    loadmacro = os.path.join(tmvadir, "TMVAGui.C")
    gROOT.SetMacroPath( tmvadir )
    gROOT.Macro       ( macro )
    gROOT.LoadMacro   ( loadmacro )
    print("ROOT macro path loaded correctly!\n")  

    # Import TMVA classes from ROOT
    from ROOT import TMVA

    # Create the Reader object
    reader = TMVA.Reader("!Color")
    var1 = array( 'f', [ 0 ] )
    var2 = array( 'f', [ 0 ] )
    var3 = array( 'f', [ 0 ] )
    var4 = array( 'f', [ 0 ] )
    var5 = array( 'f', [ 0 ] )
    var6 = array( 'f', [ 0 ] )
    var7 = array( 'f', [ 0 ] )
    var8 = array( 'f', [ 0 ] )
    var9 = array( 'f', [ 0 ] )
    var10 = array( 'f', [ 0 ] )
    variables = [var1, var2, var3,var4, var5, var6,var7, var8, var9, var10] 
    var_names = ['peaks','mean_peaks','integral','integral_over_peaks','max','mean','max_over_mean', 'std_dev_peaks', 'entropy','ps_integral']
    #variables = [var1, var2, var3, var4] 
    #var_names = ['var1', 'var2', 'var3', 'var4'] 
    for name, var in zip(var_names, variables):
        reader.AddVariable(name,var)   
    print("Variables successfully loaded!\n") 
    #reader.AddVariable("Nclusters.value", var1)
    #reader.AddVariable("(TMath::Log10(eventinfo_ALLOfflinePulseSeriesReco.tot_charge))*1000/eventinfo_ALLOfflinePulseSeriesReco.length" ,var2)
    #reader.AddVariable("MDCOGLaunches.value*1000./eventinfo_ALLOfflinePulseSeriesReco.length",var3)
    #reader.AddVariable("Nclusters.value*1000./eventinfo_ALLOfflinePulseSeriesReco.length" ,var4)
    #reader.AddVariable("NSMT8TRIGGER.value/eventinfo_ALLOfflinePulseSeriesReco.nstrings",var5)
    #reader.AddVariable("MedianCluster.value",var6)


    


    
    
    # book the MVA methods
    #dir    = "weights/"
    #prefix = "TMVAClassification_"
    #
    #for m in mlist:
    #    print( m + " method", dir + prefix + m + ".weights.xml") 
    #    reader.BookMVA( m + " method", dir + prefix + m + ".weights.xml" )
    
    weight_dir = "/home/dean/capstone/TMVA-classifier/weights/"
    weights = [f for f in os.listdir(weight_dir) if ".xml" in f] 
    for i,f in enumerate(weights):
        reader.BookMVA("BDT_{}".format(i),os.path.join(weight_dir,f)) #only care about BDT      
#    reader.BookMVA("BDT","weights/TMVAClassification_BDT.weights.xml") 


    #######################################################################
    # For an example how to apply your own plugin method, please see
    # TMVA/macros/TMVApplication.C
    #######################################################################

    # Book output histograms    
    nbin = 100

    histList = []
    for m in mlist:
        histList.append( TH1F( m, m, nbin, -3, 3 ) )
    
    for h in histList:
        h.Fill( reader.EvaluateMVA( h.GetName() + " method" ) )
    
    

    # Book example histogram for probability (the other methods would be done similarly)
    if "Fisher" in mlist:
        probHistFi   = TH1F( "PROBA_MVA_Fisher",  "PROBA_MVA_Fisher",  nbin, 0, 1 )
        rarityHistFi = TH1F( "RARITY_MVA_Fisher", "RARITY_MVA_Fisher", nbin, 0, 1 )

    
    
    filelist = glob(directory + "/" + "Level4b*.hdf")
    print 30*"#"
    print "the filelist, ", filelist
    print 30*"--"
    for file in filelist:

        try:
            startfile = tables.openFile(file,"a")
            #DELETE BDTs if they exist

            for var in startfile.root._v_children.keys():
                if re.match("BDT_", var):
                    startfile.removeNode("/", var)
                    startfile.removeNode("/__I3Index__", var)
            #NOW CLONE THE NODE

            for name in histList:  
                startfile.copyNode("/__I3Index__/StdDCOGLaunches", "/__I3Index__", str(name.GetName())) 
                startfile.copyNode("/StdDCOGLaunches", "/", str(name.GetName())) 
 
            startfile.close()
            
            h5 = tables.openFile(file,'r')
            mcog_over_t          = numpy.divide(h5.root.MDCOGLaunches.cols.value[:],\
                                                    h5.root.eventinfo_ALLOfflinePulseSeriesReco.cols.length[:]/1000.)
            q_over_t             = numpy.divide(numpy.log10(h5.root.eventinfo_ALLOfflinePulseSeriesReco.cols.tot_charge[:]),\
                                                    h5.root.eventinfo_ALLOfflinePulseSeriesReco.cols.length[:]/1000.)

            ncluster_over_t      = numpy.divide(h5.root.Nclusters.cols.value[:],\
                                             h5.root.eventinfo_ALLOfflinePulseSeriesReco.cols.length[:]/1000.)
            nsmt8_over_string    = numpy.divide(h5.root.NSMT8TRIGGER.cols.value[:],\
                                                    h5.root.eventinfo_ALLOfflinePulseSeriesReco.cols.nstrings[:])
            
            s1 = array('f' , h5.root.Nclusters.cols.value[:] )
            s2 = array('f' , q_over_t)
            s3 = array('f' , mcog_over_t[:] )
            s4 = array('f' , ncluster_over_t[:] )
            s5 = array('f' , nsmt8_over_string[:])
            s6 = array('f' , h5.root.MedianCluster.cols.value[:])
        
            h5.close()
            
            result = numpy.zeros((len(histList),len(s1)), numpy.dtype([('Classifier', numpy.double)]))

            
            
            for ievt in range(len(s1)):
                #if ievt%1000 == 0:
                #    print "--- ... Processing event: %i" % ievt 
                # Fill event in memory

                # Compute MVA input variables
                var1[0] = s1[ievt] 
                var2[0] = s2[ievt]
                var3[0] = s3[ievt] 
                var4[0] = s4[ievt]
                var5[0] = s5[ievt]
                var6[0] = s6[ievt]
                
                # Fill histograms with MVA outputs
                
                
                for j,h in enumerate(histList):
                    h.Fill( reader.EvaluateMVA( h.GetName() + " method" ) )
                    result[j][ievt]["Classifier"] = reader.EvaluateMVA( h.GetName() + " method" )                    
                    
                
                endfile = tables.openFile(file,'a')
                for k , name in enumerate(histList):
                    modifiedNode = endfile.getNode("/", str(name.GetName()) )
                    modifiedNode.cols.value[ievt] = result[k][ievt]["Classifier"]


                endfile.close()

            
            
            print time.strftime('Elapsed time - %H:%M:%S', time.gmtime(time.clock()))
                #sanity check of the mva values writen in the hdf files
    
                #ifile=tables.openFile(file,'r')
                 #   if len(ifile.root.BDT_400_20.cols.BDT) != len(ifile.root.MPEFit.cols.Zenith):
                 #       ifile.close()
                 #       print "Something wrong with file: ", k, j+1
                        #exit()
                        #os.system("rm "+"/data/icecube01/users/redlpete/IC59L2/TableIOL3/H5FilesIncludingScores/H5%0.2d%0.2d.hd5"%(k,j+1))
                  #  ifile.close()
        except ImportError as exce:
            print "file does not exist", k, j + 1
            print exce
            
    exit()
    ifile = tables.openFile("test.h5",mode='a')

    
    
    class Score(IsDescription):
        score = Float64Col()

    
    group = ifile.createGroup("/", 'Background', 'Scoreinfo')
    
    table = ifile.createTable(group, 'score' , Score, "Example")
    
    particle = table.row

    for n in range(len(result)):
        particle['score'] = result[n]
        particle.append()

    
    print "--- End of event loop: %s" % sw.Print()
    
    target  = TFile( "TMVApp1.root","RECREATE" )
    for h in histList:
        h.Write()

    target.Close()

    print "--- Created root file: \"TMVApp.root\" containing the MVA output histograms"   
    print "==> TMVApplication is done!"  
 
if __name__ == '__main__':
    main()
