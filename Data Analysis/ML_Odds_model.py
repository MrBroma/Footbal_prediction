import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error

# Load the data
df = pd.read_csv('ML_data.csv')

# Encode 'HomeTeam' and 'AwayTeam'
from sklearn.preprocessing import LabelEncoder
le_home = LabelEncoder()
le_away = LabelEncoder()
df['HomeTeam_encoded'] = le_home.fit_transform(df['HomeTeam'])
df['AwayTeam_encoded'] = le_away.fit_transform(df['AwayTeam'])

le_season = LabelEncoder()
df['season_encoded'] = le_season.fit_transform(df['season'])

# Prepare the feature set for regression
features = ['season_encoded', 'HomeTeam_encoded', 'AwayTeam_encoded', 'HomeTeamStrength', 'AwayTeamStrength', 
            'avgHG', 'avgAG', 'avgHHG', 'avgHAG', 'avgHST', 'avgAST']

# Include the odds columns for regression target
df_ML = df[features + ['AvgH', 'AvgD', 'AvgA']]  # Assuming BWH, BWA, BWD are HomeOdds, AwayOdds, and DrawOdds

# Remove any rows with missing values
df_ML.dropna(inplace=True)

# Define features (X) and target variables (y)
X = df_ML[features]
y = df_ML[['AvgH', 'AvgD', 'AvgA']]  # Odds to predict

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the regression model (using Ridge regression with MultiOutput)
ridge = Ridge(alpha=0.1)  # Ridge regression with alpha=0.1
model_regression = MultiOutputRegressor(ridge)
model_regression.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model_regression.predict(X_test)

# Calculate Mean Squared Error for each odds type
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
print(f"Mean Squared Error for HomeOdds: {mse[0]}, AwayOdds: {mse[1]}, DrawOdds: {mse[2]}")

# Example prediction with new inputs
def get_team_stats(df, season, home_team, away_team):
    home_team_stats = df[(df['season'] == season) & (df['HomeTeam'] == home_team)].iloc[0]
    away_team_stats = df[(df['season'] == season) & (df['AwayTeam'] == away_team)].iloc[0]
    return {
        'HomeTeamStrength': home_team_stats['HomeTeamStrength'],
        'AwayTeamStrength': away_team_stats['AwayTeamStrength'],
        'avgHG': home_team_stats['avgHG'],
        'avgAG': away_team_stats['avgAG'],
        'avgHHG': home_team_stats['avgHHG'],
        'avgHAG': away_team_stats['avgHAG'],
        'avgHST': home_team_stats['avgHST'],
        'avgAST': away_team_stats['avgAST'],
    }

# Example input parameters for a new match
input_season = 'S2024/2025'
input_home_team = 'Cercle Brugge'
input_away_team = 'Genk'

# Dynamically retrieve stats for both teams
team_stats = get_team_stats(df, input_season, input_home_team, input_away_team)

# Encode the input values
input_season_encoded = le_season.transform([input_season])[0]
input_home_team_encoded = le_home.transform([input_home_team])[0]
input_away_team_encoded = le_away.transform([input_away_team])[0]

# Create the new input DataFrame for the model
new_input = pd.DataFrame({
    'season_encoded': [input_season_encoded],
    'HomeTeam_encoded': [input_home_team_encoded],
    'AwayTeam_encoded': [input_away_team_encoded],
    'HomeTeamStrength': [team_stats['HomeTeamStrength']],
    'AwayTeamStrength': [team_stats['AwayTeamStrength']],
    'avgHG': [team_stats['avgHG']],
    'avgAG': [team_stats['avgAG']],
    'avgHHG': [team_stats['avgHHG']],
    'avgHAG': [team_stats['avgHAG']],
    'avgHST': [team_stats['avgHST']],
    'avgAST': [team_stats['avgAST']],
})

# Use the model to predict odds
prediction_reg = model_regression.predict(new_input)
home_odds, away_odds, draw_odds = [round(x, 2) for x in prediction_reg[0]]
print(f"Predicted HomeOdds: {home_odds}, AwayOdds: {away_odds}, DrawOdds: {draw_odds}")

