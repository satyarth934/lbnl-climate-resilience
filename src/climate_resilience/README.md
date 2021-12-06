Questions regarding the code:
1. What param tells us if the code is daily or monthly, etc.
    ANS: Input to the ee.ImageCollection function.
         Filtering based on dates and model.
         
2. What are the diff params in ee.ImageCollection? Why is it different for different functions?
    ANS: That is how it is supposed to be. Do not change these for the daily/monthly functions.
         TODO: We can have a different function though, for other datasets in 
               case someone wants to download a different dataset.
               CAUTION: Beware that the same query params might not apply for the other datasets.
               
3. Why are some functions filtering data on models and some not?
    ANS: That is how it is supposed to be. Only daily data can be filtered.
         Monthly data is already aggregated for model ensembles.

4. What do the variables mean?
    ANS: IDK. Doesn't matter.

5. How are the two extreme data analysis notebooks different? They seem to be doing the same thing.
    ANS: They are not. Only the variable values are different.

6. Where is the visualization code?
    ANS: Zexuan will share it. not yet shared.
         TODO: Create a github and share with him.

Things yet to implement:
1. Create parent functions to download different datasets - daily, monthly, avg, etc.
2. Run a single loop with all the permutations of all the 4 loops.
3. Parallelize this single loop. CAUTION: Might run into quota issues and will be hard to track progress in a parallel setting.











# Understanding the code.

We cannot directly download the data from the Google Earth Engine directly onto the local machine.
So the best option is to download to the drive and then download that data to the local drive.

The preprocessing functions will expect that the local data drive contains the downloaded data.
#TODO: Write clear instructions for each of these steps.

Ask the user if the data location is on google drive or local drive?
If on drive, then mount the google drive and access files from there for processing - IGNORE. 
If the data is on drive, the user needs to mount the drive.
Write tutorial about how to do this.






# Preprocessing Functions:
1. calculate_Nth_percentile()
2. calculate_pr_count_amount()
3. calculate_temporal_mean()
4. * get_climate_ensemble() 
    There are some flaws in the function. Calculating std is not possible.

# Following is the expected directory structure for functions 1, 2, and 3 in the preprocessing code:
datadir
├── scenario1_variable1_ensemble
│   ├── name1_state1_scenario1_variable1.csv
│   └── name2_state2_scenario1_variable1.csv
├── scenario1_variable2_ensemble
│   ├── name1_state1_scenario1_variable2.csv
│   └── name2_state2_scenario1_variable2.csv
├── scenario2_variable1_ensemble
│   ├── name1_state1_scenario2_variable1.csv
│   └── name2_state2_scenario2_variable1.csv
└── scenario2_variable2_ensemble
    ├── name1_state1_scenario2_variable2.csv
    └── name2_state2_scenario2_variable2.csv