import sys 
import time 
import numpy as np 
import tables 
import os 
import h5py
import matplotlib.pyplot as plt 
try:
    import seaborn as sns 
except ImportError:
    print("Looks like you don't have seaborn intalled!") 
from array import array 

from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut, TH1F, TStopwatch
from ROOT import TMVA 

class BDT_Application(object):

    def __init__(self,**kwargs):
        """
        This initialization function sets up the TMVA macro path, and
        sets up variables for the TMVA reader. These variables are defined as 
        single entry Python arrays. One has to use these arrays as TMVA/ROOT works  
        by reference. This means that adding variables to the TMVA reader amounts 
        to adding pointers to the TMVA reader. We have to then iterate
        (not very numpy) through our variable arrays, setting the reader variable           arrays (and evaluating as we go). 
        kwargs:
            - var_names: the names of the variables used in the BDT application 
                (default 10 variables) 
            - tmva_dir: the installation location of TMVA macros (/home/dean/software/tmva/TMVA-v4.2.0/test) 
            
        """
        var_names = kwargs.get('var_names', ['peaks','mean_peaks','integral','integral_over_peaks','max','mean','max_over_mean', 'std_dev_peaks', 'entropy','ps_integral'])
        tmvadir = kwargs.get("tmva_dir", "/home/dean/software/tmva/TMVA-v4.2.0/test") 
        
        #setting up TMVA macro path
        try:    
            macro = os.path.join(tmvadir, "TMVAlogon.C")
            loadmacro = os.path.join(tmvadir, "TMVAGui.C")
            gROOT.SetMacroPath( tmvadir )
            gROOT.Macro       ( macro )
            gROOT.LoadMacro   ( loadmacro )
        except:
            print("Couldn't successfully establish TMVA macro path") 
            sys.exit() 

        self.reader = TMVA.Reader("!Color")
        variables = [] 
        for i in xrange(len(var_names)):
            variables.append(array('f',[0]))
        
        for name, var in zip(var_names, variables):
            self.reader.AddVariable(name, var)
        self.variables = variables  
    def load_methods(self, weight_files):
        """
        Once the variables are loaded then we can add methods that we want to apply.
        args:
            - weight_files: A list of weight files we wish to apply.  
        """
    

        #weights_dir = "/home/dean/capstone/TMVA-classifier/weights/" 
        #weights = [os.path.join(weights_dir,f) for f in os.listdir(weights_dir) if ".xml" in f] 
        
        for i, weight_file in enumerate(weight_files):
            self.reader.BookMVA("BDT_{}".format(i),weight_file)  
        
        print("Weight files successfully booked!")
        
        # now be book output histograms 
        nbin = 100 
        
        hist_list = [] 
        
        for i in xrange(len(weights)):
            method_name = "BDT_{}".format(i) 
            hist_list.append( (TH1F ( method_name, method_name, nbin, -3, 3)))
        
        for h in hist_list:
            h.Fill(self.reader.EvaluateMVA(h.GetName()))
        self.hist_list = hist_list 
        print("Histograms set up") 

    def sample_BDT(self, var_file):
        """
        The meat and potatoes. This is where we actually sample from the 
        TMVA whose weights are loaded into the TMVA reader. We do this by iteratively
        setting the readers variable 'arrays' with the variable values from our variable 
        files. Once set, we evaluate the method on that given set of variables. 
        args:
            -var_file: the file containing the variable values from waveforms 
        """
        #hdf_var = "var_files/varHL_12000_17-06_no_norm_by-wf_all.hdf5"
        f = h5py.File(var_file, 'r') 
        dat = f['var+labels'][...]
        print(dat.shape) 
        #test_var = [] 
        #for i in xrange(dat.shape[1] - 4 ):
        #    test_var.append(array('f', dat[:,4+i]))
        f.close()
        result = np.zeros((len(weights), dat.shape[0]))
        print("Loaded up variables, now evaluating methods")  
        for ievt in xrange(dat.shape[0]):
            for j in xrange(dat.shape[1] - 4):
                #self.variables[j][0] = test_var[j][ievt] # we have to do this because TMVA works by reference 
                self.variables[j][0] = dat[ievt,j+4] # this sets the variables in the tmva reader  
            for i,h in enumerate(self.hist_list):
                h.Fill(self.reader.EvaluateMVA( h.GetName()))
                result[i,ievt] = self.reader.EvaluateMVA(h.GetName())
            if (ievt % 1000 == 0):
                print("{} waveforms done, {} left to go!".format(ievt, dat.shape[0] - ievt)) 
        labels = dat[:,:3]
        result_labels = np.hstack((labels, result.T))
        print("Finished up creating BDT scores. Saving now...")
        f = h5py.File("BDTresults.hdf5","w") 
        f.create_dataset("scores", data=result_labels) 
        f.close() 
        print("Finished saving")  
          
    @staticmethod
    def view_waveforms(results_file, wf_file, max_wf = 100 ):
        """
        Takes a results file and generates plots with BDT score correspondance.
        args:
            results_file: The file with labels and BDT scores
            wf_file: The file with labels and waveforms 
        """            
        fres = h5py.File(results_file,'r') 
        fwf = h5py.File(wf_file, 'r') 
        res = fres['scores'][...]
        labels = res[:,:3]
        scores = res[:,3] 
        fig = plt.figure() 
        ax = fig.add_subplot(111) 
        num_wf = 0
        for lab, score in zip(labels, scores):
            str_lab = "{}/{}/{}".format(int(lab[0]), int(lab[1]), int(lab[2]))
            wf = fwf[str_lab][...]
            ax.plot(wf,drawstyle='steps-mid')
            
            ax.set_xlim([0, wf.shape[0]]) 
            ax.set_ylabel("ADC counts above baseline") 
            ax.set_xlabel("Time, 10 ns")  
            ax.set_title("BDT score: {:.2f}\nEvent {}, Channel {}, Waveform {}".format(score,int(lab[0]), int(lab[1]), int(lab[2])))
            num = '{:04}'.format(num_wf)
            fig.savefig("./plots/wf{}.png".format(num))         
            if num_wf >= max_wf:
                break
            num_wf += 1
            ax.clear()  
        fres.close()
        fwf.close() 
        
if __name__ == '__main__':
    weights_dir = "/home/dean/capstone/TMVA-classifier/weights/" 
    weights = [os.path.join(weights_dir,f) for f in os.listdir(weights_dir) if ".xml" in f] 
    weights = ["/home/dean/capstone/TMVA-classifier/weights/TMVAClassification_BDT_ntrees200_maxdepth10_ncuts3_top.weights.xml"]
    hdf_var = "var_files/varHL_12000_19-06_no_norm_by-wf_top.hdf5"
    hdf_wf = "var_files/wfsHL_12000_19-06_no_norm_by-wf_top.hdf5"
    #applier = BDT_Application()
    #applier.load_methods(weights) 
    #applier.sample_BDT(hdf_var) 
    BDT_Application.view_waveforms('BDTresults_top.hdf5',hdf_wf,max_wf=100)
