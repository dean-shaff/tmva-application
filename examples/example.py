import sys
sys.path.append('/home/dean/capstone/TMVA-classifier') 
from deanTMVApplication import BDT_Application

def main():
    
    weights = ['path/to/weight/file'] #I've set up a weight directory to place weight files
    var_file = 'path/to/var/file' #this is the file containing waveform labels, and calculated waveforms
    wf_file = 'path/to/wf/file' # this the file containing waveform labels and actual waveforms  
    applier = BDT_Application() 
    applier.load_methods(weights)   
    applier.sample_BDT(var_file) # this will create a file called BDTresults.hdf5
    #Now, once we have this results file, we can apply it to waveforms!
    #the view_waveform static method will creat png files that can be used to make a    #movie. 
    BDT_Application.view_waveforms('BDTresults.hdf5',wf_file,max_wf=100)
     
