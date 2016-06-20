## TMVA Application

The purpose of this module is to generate a correspondance between a trained BDT and existing data. When using TMVA for training, an `.xml` file is created that contains the trained BDT parameters. We can use this `.xml` file to create an instance of a trained BDT, and then apply it to vectors that correspond to waveform variables. After this, we can create plots that show waveforms and their corresponding BDT scores. 

### Requirements

- ROOT
- TMVA 
- h5py
- numpy 

### Usage

See the examples/example.py file.
