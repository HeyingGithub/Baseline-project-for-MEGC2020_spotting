% MEX_RLOF is a wrapper to the RLOF library that contains a set of sparse 
% motion estimation methods based on the local optical flow paradigm.  
%
% Usage:
%
% POINTLIST2 = mex_RLOF(IMAGE1, IMAGE1, POINTLIST1, PARAMSTRUCT);
%
% Arguments IMAGE1 and IMAGE1 could be gray scaled images (2-dimensional 
% arrays) or rgb images (3-dimensional arrays)
% They are required to have the same dimension and they must be doubles. 
%
% POINTLIST1 is the list of points to track (double 2xn array).
% With n the number of points in the point list.
%
% POINTLIST2 is the list of tracked points corresponding to "pointlist" 
% (double 2xn array).
%
% PARAMSTRUCT specifies one or more of the following name/value pairs. Only
% the 'method' is mandatory.
%
%       Name              Value
%       'method'          A string specifying the applied motion estimation
%                         method. The value can be one of the following:
%                         'PLK'       - Pyramidal Lucas Kanade provided by 
%                                       OpenCV.
%                         'BEPLK'     - Pyramidal Lucas Kanade using
%                                       bilinear equations, see 
%                                       Senst et al. 2013.
%                         'CB_PLK'    - Pyramidal Lucas Kanade with
%                                       adaptive support region, see
%                                       Senst et al. 2014.
%                         'CB_BEPLK'  - Pyramidal Lucas Kanade using
%                                       bilinear equations and an adaptive 
%                                       support region, see 
%                                       Senst et al. 2014.
%
%                         'RLOF'      - Robust Local Optical Flow, see  
%                                       Senst et al. 2011/2012.
%                         'BERLOF'    - Robust Local Optical Flow using
%                                       bilinear equations, see 
%                                       Senst et al. 2013.
%                         'CB_RLOF'   - Robust Local Optical Flow with
%                                       adaptive support region, see
%                                       Senst et al. 2014.
%                         'CB_BERLOF' - Robust Local Optical Flow using
%                                       bilinear equations and an adaptive 
%                                       support region, see 
%                                       Senst et al. 2014. Full paper 
%                                       references are given below.
% 
%       'noLevels'        A positive number specifying the number of 
%                         levels used for the gaussian image pyramid.
%
%       'noIterations'    A positive number specifying the number of 
%                         levels used for the gaussian image pyramid.  
%
%       'winSize'         A positive number specifying the size of the 
%                         support region. Using RLOF or CB derivates
%                         winSize specify the upper bound of the support
%                         region size. 
%
%       'smallWinSize'    Used only for RLOF and CB derivates. A positive
%                         number specifying the lower bound of the support  
%                         region. 
%
%       'CBThreshold'     Used only for CB derivates. A positive number
%                         specifying the pixel value threshold \tau, see
%                         Senst et al. 2014
%
%       'norm'            A vector [V1 V2] specifying the shrinked Hampel
%                         norm \sigma_1 and \sigma_2, see 
%                         Senst et al. 2014.
%
%       'options'         A string specifying the debug options. The value 
%                         can be one of the following:
%                         'PerformTest'    - A accuracy check with pre-
%                                            estimated motion vectors for 
%                                            the ErnstReuter image pair  
%                                            will be done.
%                         'PrintParameter' - Displays the parameter of the
%                                            respective algorithm.
% Tobias Senst
% TU-Berlin
% 17. Nov, 2014
%
% COPYRIGHT:                                                                 
% 
% This file is the property of the author and Communication Systems Group,   
% Technische Universität Berlin. All rights reserved.                        
%                                                                             
% It may not be publicly disclosed, distributed, used, copied or modified    
% without prior written authorization by a representative of                 
% Communication Systems Group, Technische Universität Berlin or the author.  
% Any modified version of this document needs to contain this header.        
% 
% THERMS IF USAGE:                                                           
% PERSONAL, NON-COMMERCIAL or ACADEMIC USAGE:                                
% You are free to use this software for whatever you like. If you use this 
% algorithm for a scientific publication, please cite the one of the       
% following paper:                                                         
%  																			  
% @INPROCEEDINGS{ICIPSenst2014,											  
% AUTHOR = {Tobias Senst and Thilo Borgmann and Ivo Keller and Thomas		  
% Sikora},																	  
% TITLE = {Cross based Robust Local Optical Flow},							  
% BOOKTITLE = {21th IEEE International Conference on Image Processing},	  
% YEAR = {2014},															  
% MONTH = okt,																  
% PAGES = {1967--1971},													  
% ADDRESS = {Paris, France},												  
% }																		  
%  																			  
% @INPROCEEDINGS{ICIPSenst2013,											  
% AUTHOR = {Tobias Senst and Jonas Geistert and Ivo Keller and Thomas		  
% Sikora},																	  
% TITLE = {Robust Local Optical Flow Estimation using Bilinear Equations  
% for Sparse Motion Estimation},												  
% BOOKTITLE = {20th IEEE International Conference on Image Processing},	  
% YEAR = {2013},															  
% MONTH = sep,																  
% PAGES = {2499--2503},													  
% ADDRESS = {Melbourne, Australia},										  
% DOI = {10.1109/ICIP.2013.6738515},										  
% }																		  
%                                                                              
% @ARTICLE{TCSVTSenst2012,                                                   
% AUTHOR = {Tobias Senst and Volker Eiselein and Thomas Sikora},             
% TITLE = {Robust Local Optical Flow for Feature Tracking},                  
% JOURNAL = {IEEE Transactions on Circuits and Systems for Video 
% Technology},
% YEAR = {2012},                                                             
% MONTH = sep,                                                               
% PAGES = {1377--1387},                                                      
% VOLUME = {22},                                                             
% NUMBER = {9},                                                              
% DOI = {10.1109/TCSVT.2012.2202070}                                         
% }                                                                          
%                                                                              
% @INPROCEEDINGS{WACVSenst2011,                                              
% AUTHOR = {Tobias Senst and Volker Eiselein and Rubén Heras Evangelio and   
% and Thomas Sikora},                                                            
% TITLE = {Robust Modified L2 Local Optical Flow Estimation and Feature      
% Tracking},                                                                 
% BOOKTITLE = {IEEE Workshop on Motion and Video Computing},                 
% YEAR = {2011},                                                             
% MONTH = jan,                                                               
% EDITOR = {Eric Mortensen},                                                 
% PAGES = {685--690},                                                        
% ADDRESS = {Kona, USA},                                                     
% DOI = {10.1109/WACV.2011.5711571},                                         
% }                                                                          
%                                                                              
% COMMERCIAL USAGE:                                                          
% It is not allowed to use any content of this package for any commercial  
% use or any advertisement for upcoming commercial products. If you want to
% use any content for such a purpose please contact:                       
% Prof. Dr.-Ing. Thomas Sikora <sikora@nue.tu-berlin.de>.                  
% 
% WARRANTIES:                                                                
%                                                                              
% Software provided by Technische Universität Berlin with this document is   
% provided "AS IS" and any express of implied warranties including, but      
% not limited to, the implied warranties of merchantability and fitness      
% for a particular purpose are disclaimed.                                   
% In no event shall the author or contributors be liable for any direct,     
% indirect, incidental, special, exemplary, or consequential damages         
% (including, but not limited to, procurement of substitute goods or         
% services, loss of use, data, or profits or business interruption) caused 
% in any way out of the use of this software, even if advised of the 
% possibility of such damage.                                                            
