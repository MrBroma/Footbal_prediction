# Footbal Match Prediction - Belgian Jupiler Pro-League

## Introduction 
This is a teamwork project, aiming to develop a comprehensive system capable of accurately predicting the outcomes of football matches in the Belgian Jupiler Pro League. By combining **data scraping**, **machine learning**, and **data visualization** techniques, we will create a robust tool for analyzing historical match data, extracting relevant features, and building predictive models.

### Key Objectives:

**Data Acquisition:** Efficiently scrape data from football websites, including date, time, match statistics and real-time odds.  
**Data Processing:** Clean and preprocess the scraped data to ensure its quality and suitability for analysis.   
**Feature Engineering:** Create meaningful features that capture the essential aspects of football matches, such as season, head-to-head records, and match performance.  
**Model Development:** Train and evaluate various machine learning models to predict match outcomes, considering factors like home advantage, team strength and goal-scoring trends.  
**Visualization:** Develop a user-friendly interface using Streamlit to visualize predictions, real-time data, and model performance.  
**Automation:** Implement Airflow to automate the data pipeline, ensuring timely updates and efficient execution of tasks.


## Data Acquisition
### Data Scriping

### Data Base



## Data Preprocessing
The entire DataFrame consists of 92 columns, which are structured but require significant cleaning, including the handling of null values.
### Data Cleaning
The dataset uses abbreviated column names for efficiency. For example, "FTHG" stands for "Full Time Home Goals" and "FTAG" represents "Full Time Away Goals." A detailed explanation of all column names can be found in the official documentation at [this link](https://www.football-data.co.uk/notes.txt).  
Additionally, the dataset contained missing values for certain features, such as 'WHH', 'WHD', and 'WHA,' representing the William Hill bookmaker odds for Home Win, Draw, and Away Win, respectively. These features had over 300 missing values. Since our primary goal is to predict future match outcomes, for 'odds' part, we only focus on the 'AvgH', 'AvgD', and 'AvgA' columns, which represent the average odds from all bookmakers. These columns provide a more comprehensive and reliable representation of the odds landscape.  
Regarding the 'match stats' features, only a handful of rows contained missing data. Given the minimal number of affected rows (less than 10), it was no problem to drop them.

## Machine Learning
![Image Alt Text](/Figures/FTR.png)

### Feature Selection

### Feature Engineering

### Model Selection and Training


## Streamlit Visualization


## Airflow Automation 


## Project Structure


## Team Members
**Data Engineer:** [MrBroma (Loic Rouaud)](https://github.com/MrBroma), [mehmetbatar35(Mehmet Batar)](https://github.com/mehmetbatar35)  
**Data Analyst:** [EmmaSHANG0625 (Hui Shang)](https://github.com/EmmaSHANG0625), [appiKaL(Kyllian Culot)](https://github.com/appiKaL)

## Project Timeline
### Phase 1: Data Collection 
  * Data scraping from multiple sources (05/09/2024-16/09/2024)
  * Data cleaning and preprocessing (05/09/2024-09/09/2024)

### Phase 2: Model Development 
  * Feature engineering (09/09/2024-10/09/2024)
  * Model selection and training (10/09/2024-11/09/2024)
  * Model evaluation (11/09/2024-12/09/2024)

### Phase 3: Deployment
  * Deployment of Strreamit (12/09/2024-16/09/2024)
  * Monitoring and maintenance (16/09/2024)






