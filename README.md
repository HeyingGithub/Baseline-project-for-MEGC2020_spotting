# Baseline project for MEGC2020_spotting

The project is the baseline method implementation for the Third Micro-Expression Grand Challenge (MEGC2020): New Learning Methods for Spotting and Recognition - spotting part (workshop og FG2020 ). 


## Method

The method is Main Directional Maximal Difference Analysis (MDMD). For details, please refer to the flowing paper. 

[1] Wang S-J, Wu S, Qian X, Li J, Fu X. A main directional maximal difference analysis for spotting facial movements from long-term videos[J]. Neurocomputing, 2017,230: 382-389. 

There are some additional instructions for slight modification here: 

(1) For preprocess, face regions are cropped according to the landmarks detected by the "Dlib" toolkit. More details can be gotten by reading the codes in the file "preprocess.py" in the folder "MEdatabase_processed".  

(2) For parameter settings: for the CAS(ME)^2 dataset, the "k" is set to 12 for micro-expressions, and 39 for macro-expressions; for the SAMM Long Videos dataset, the "k" is set to 80 for micro-expressions, and 260 for macro-expressions; the number of blocks is set to 6 x 6, and the number of directions is set to 4, and the "p" is set to 1. 

(3) The original MDMD only predicts whether a frame blongs to facial movements. To output target intervals,  the adjacent frames consistently predicted to be macro- or micro-expressions form an interval, and the intervals that are too long or too short are removed. (The number of micro-expression frames is limited between 7 and 16 for the CAS(ME)^2 dataset, and between 47 and 105 for the SAMM Long Videos dataset. The number of macro-expression frames is limited larger than 16 for the CAS(ME)^2 dataset, and larger than 105 for the SAMM Long Videos dataset.)


## How to reproduce the baseline results

Firstly, put the datasets or their soft links into the two "dataset_new" folders respectively in "MDMD_results" and "MEdatabase_processed". Structure the two "dataset_new" folders as follows: 

 dataset_new <br>
>└─data <br>
>>├─CAS(ME)^2 <br>
>>>├─CAS(ME)^2code_final.xlsx <br>
>>>├─cropped <br>
>>>├─rawpic <br>
>>>├─rawvideo <br>
>>>└─selectedpic <br>

>>├─SAMM_MEGC <br>
>>>├─SAMM_longvideos <br>
>>>└─SAMM_LongVideos_V1_Release.xlsx <br>

Secondly, run the following codes: 

(1) Preprocess data 

In the folder "MEdatabase_processed", run the Python script: 
```Python
python preprocess.py # crop faces
python RGBtoGray.py # get gray images
python generate_dt_txt.py # generate dataset infomation
```

(2) Run "MDMD" codes 

In the folder "MDMD_codes", run the Matlab script: 
```Matlab
cmd.m % Note that: the "dataset" should be set to "ME2" or "SAMM_MEGC", and the "cls" should be set to "micro" or "macro".
```

(3) Process results

In the folder "MDMD_results", run the Matlab and Python scripts: 
```Matlab
MDMDmat_to_txt.m % generate predicted intervals (without removing too short or too long ones)
```
```Python
python evaluation_all_p.py # generate evaluation results of all "p" parameters (remove too short or too long intervals)
python gen_MEGC2020_log_file.py # generate the FG-MEGC2020 log file
```
