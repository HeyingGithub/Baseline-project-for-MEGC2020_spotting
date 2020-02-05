# Baseline project for MEGC2020_spotting

The project is the baseline method implementation for the Third Micro-Expression Grand Challenge (MEGC2020): New Learning Methods for Spotting and Recognition - spotting macro and micro expressions on long videos (workshop of FG2020 ). Link: <a href="http://megc2020.psych.ac.cn:81/">http://megc2020.psych.ac.cn:81/</a>

## Paper

Baseline paper on arXiv is available at <a href="https://arxiv.org/abs/1912.11985" >https://arxiv.org/abs/1912.11985</a>. Please cite:

He Y, Wang S J, Li J, et al. Spotting Macro-and Micro-expression Intervals in Long Video Sequences[J]. arXiv preprint arXiv:1912.11985, 2019.


## Method

For details, please refer to the above baseline paper. For your convenience, we briefly summarize the baseline method here. 

The original MDMD (Main Directional Maximal Difference Analysis)  method proposed in [1] is slightly modified for MEGC 2020 as follows.

(1) For preprocess, face regions are cropped according to the landmarks detected by the "Dlib" toolkit. More details can be gotten by reading the codes in the file "preprocess.py" in the folder "MEdatabase_processed".  

(2) For parameter settings: for the CAS(ME)^2 dataset, the "k" is set to 12 for micro-expressions, and 39 for macro-expressions; for the SAMM Long Videos dataset, the "k" is set to 80 for micro-expressions, and 260 for macro-expressions; the number of blocks is set to 6 x 6, and the number of directions is set to 4, and the "p" is set to 0.01. 

(3) The original MDMD only predicts whether a frame belongs to facial movements. To output target intervals,  the adjacent frames consistently predicted to be macro- or micro-expressions form an interval, and the intervals that are too long or too short are removed. The number of micro-expression frames is limited between 7 and 16 for the CAS(ME)^2 dataset, and between 47 and 105 for the SAMM Long Videos dataset. The number of macro-expression frames is defined as larger than 16 for the CAS(ME)^2 dataset, and larger than 105 for the SAMM Long Videos dataset.

[1] Wang S-J, Wu S, Qian X, Li J, Fu X. A main directional maximal difference analysis for spotting facial movements from long-term videos[J]. Neurocomputing, 2017,230: 382-389. 


## Results
Since the amount of TP is an important metric for the spotting result evaluation, we select the results under the condition of p=0.01 as the final baseline results. For CAS(ME)^2, the F1-scores are 0.1196 and 0.0082 for macro- and micro-expressions respectively, and 0.0376 for the overall result. For SAMM Long Videos, the F1-scores are 0.0629 and 0.0364 for macro- and micro-expressions respectively, and 0.0445 for the overall result. More details about the number of true labels, TP, FP, FN, precision, recall and F1-score for various situations are shown in the following table.

| Dataset      | CAS(ME)^2 | CAS(ME)^2 | CAS(ME)^2 | SAMM Long Videos | SAMM Long Videos |SAMM Long Videos |
|--------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|
| Expression   | macro\-expression                                              | micro\-expression                                           | overall | macro\-expression | micro\-expression | overall |
| Total number | 300                                                            | 57                                                          | 357     | 343               | 159               | 502     |
| TP           | 109                                                            | 21                                                          | 130     | 22                | 29                | 51      |
| FP           | 1414                                                           | 5014                                                        | 6428    | 334               | 1407              | 1741    |
| FN           | 191                                                            | 36                                                          | 227     | 321               | 130               | 451     |
| Precision    | 0\.0716                                                        | 0\.0042                                                     | 0\.0198 | 0\.0618           | 0\.0202           | 0\.0285 |
| Recall       | 0\.3633                                                        | 0\.3684                                                     | 0\.3641 | 0\.0641           | 0\.1824           | 0\.1016 |
| F1\-score    | 0\.1196                                                        | 0\.0082                                                     | 0\.0376 | 0\.0629           | 0\.0364           | 0\.0445 |


## How to reproduce the baseline results

The codes need to run in the environments: Python 3.5+ and Matlab.

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
