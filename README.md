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
Last season data: The data of the 5 last seasons CSV on https://www.football-data.co.uk/belgiumm.php were used.  
Ongoing stats: Scraping of the ongoing day including future matches and odds.

### Data Base
Creation of different stat tables in a database created with PostgresSQL.

## Data Preprocessing
The entire DataFrame consists of 92 columns, which are structured but require significant cleaning, including the handling of null values.
### Data Cleaning
The dataset uses abbreviated column names for efficiency. For example, "FTHG" stands for "Full Time Home Goals" and "FTAG" represents "Full Time Away Goals." A detailed explanation of all column names can be found in the official documentation at [this link](https://www.football-data.co.uk/notes.txt).  

Additionally, the dataset contained missing values for certain features, such as 'WHH', 'WHD', and 'WHA,' representing the William Hill bookmaker odds for Home Win, Draw, and Away Win, respectively. These features had over 300 missing values. Since our primary goal is to predict future match outcomes, for 'odds' part, we only focus on the 'AvgH', 'AvgD', and 'AvgA' columns, which represent the average odds from all bookmakers. These columns provide a more comprehensive and reliable representation of the odds landscape.  

Regarding the 'match stats' features, only a handful of rows contained missing data. Given the minimal number of affected rows (less than 10), it was no problem to drop them.

## Machine Learning
![Image Alt Text](/Figures/FTR.png)
We first briefly analyzed the distribution of the target column 'FTR'. As depicted in the figure above, the data clearly indicates a strong bias towards home team victories.
### Feature Selection
Next, to select the most informative features for our machine learning model, I conducted statistical tests to assess their relevance to the target variable.This is a common challenge in applied machine learning where identifying truly relevant input features is crucial.

For classification problems with categorical input variables, statistical tests can help determine if the output variable is dependent or independent of these inputs. Independent variables might be less relevant to the problem and could potentially be excluded from the dataset.

To identify statistically significant relationships between features and the target variable 'FTR,' we employed [Pearson's Chi-Squared statistical hypothesis](https://machinelearningmastery.com/chi-squared-test-for-machine-learning/) test. We selected features with a Chi-squared score greater than 10 and a p-value less than 0.05 to ensure a strong association and statistical significance. The selected features are presented in the following table:
| Feature | Chi2 Score | P-value |
|---|---|---|
| HomeTeam | 87.749075 | 8.821258e-205 |
| AwayTeam | 35.859735 | 1.633644e-086 |
| HTHG | 307.557766 | 1.639380e-677 |
| HTAG | 255.304096 | 3.642670e-568 |
| HS | 108.406514 | 2.882867e-249 |
| AS | 155.586110 | 1.640233e-3410 |
| HST | 335.394968 | 1.478795e-7311 |
| AST | 294.840229 | 9.467988e-6516 |
| HY | 45.949982 | 1.052176e-1018 |
| HR | 33.063638 | 6.611839e-0819 |
| AR | 13.971808 | 9.248270e-04 |

Collinearity arises when two or more independent variables are highly correlated, providing redundant information about the variance within the dataset. Adding additional features that exhibit collinearity can exacerbate this issue, leading to multicollinearity.

To identify multicollinear variables, we can calculate the Variance Inflation Factor (VIF). A high VIF value indicates that a particular independent variable is strongly correlated with other variables in the model, suggesting potential collinearity. The VIF value of the tested features are around 1, which means they are not strongly correlated with each other. 

| Variable | VIF |
|---|---|
| const | 24.3111061 |
| HomeTeam | 1.0428732 |
| AwayTeam | 1.0155113 |
| HTHG | 1.2185434 |
| HTAG | 1.1792135 |
| HS | 1.7976556 |
| AS | 1.8809357 |
| HST | 2.0350868 |
| AST | 2.0279009 |
| HY | 1.08659110 |
| HR | 1.07204711 |
| AR | 1.033538 |

### Feature Engineering
To predict the 'FTR' outcome of future matches, our model relies solely on the 'Time,' 'HomeTeam,' and 'AwayTeam' information. Therefore, we created new features based on these factors.

Considering the potential variability in team performance across seasons, we introduced a 'season_encoded' feature. To account for home advantage and team-specific strengths, we calculated 'HomeTeamStrength' and 'AwayTeamStrength' features. Additionally, we derived average historical performance metrics, such as 'avgHG' (average home goals), 'avgAG' (average away goals), 'avgHHG' (average home goals against), 'avgHAG' (average away goals against), 'avgHST' (average home shots on target), and 'avgAST' (average away shots on target), for both home and away teams.

These features, organized as matrices for HomeTeam and AwayTeam, form the input to our prediction model.

### Model Selection and Training
Given that I'm working with Python, it's straightforward to experiment with and compare various machine learning models. For this project, I selected the following three models:

**Random Forest:** A popular ensemble method that combines multiple decision trees to make predictions. Each decision tree generates its own prediction, and the final prediction is determined by the majority vote.  
**Logistic Regression:** A statistical model used for binary classification. While it's inherently binary, techniques like one-vs-rest can extend it to handle multi-class problems, as in our case where the target variable has three possible outcomes (H, D, A).  
**XGBoost:** A gradient boosting algorithm known for its efficiency and performance. It builds a model incrementally, adding new decision trees to correct the errors of previous ones.

Here are the results:  

**Random Forest:**
| precision | recall | f1-score | support |
|---|---|---|---|
| 0 | 0.55 | 0.65 | 0.60 | 112 |
| 1 | 0.31 | 0.15 | 0.21 | 65 |
| 2 | 0.53 | 0.60 | 0.56 | 95 |
| accuracy | | | 0.51 | 272 |
| macro avg | 0.46 | 0.47 | 0.46 | 272 |
| weighted avg | 0.49 | 0.51 | 0.49 | 272 |

**Logistic Regression:**
| precision | recall | f1-score | support |
|---|---|---|---|
| 0 | 0.67 | 0.63 | 0.65 | 221 |
| 1 | 0.38 | 0.32 | 0.34 | 126 |
| 2 | 0.56 | 0.66 | 0.60 | 181 |
| accuracy | | | 0.57 | 528 |
| macro avg | 0.54 | 0.54 | 0.53 | 528 |
| weighted avg | 0.56 | 0.57 | 0.56 | 528 |

**XGBoost:**
| precision | recall | f1-score | support |
|---|---|---|---|
| 0 | 0.48 | 0.57 | 0.52 | 151 |
| 1 | 0.31 | 0.18 | 0.22 | 97 |
| 2 | 0.48 | 0.52 | 0.50 | 129 |
| accuracy | | | 0.45 | 377 |
| macro avg | 0.42 | 0.42 | 0.41 | 377 |
| weighted avg | 0.43 | 0.45 | 0.43 | 377 |

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






