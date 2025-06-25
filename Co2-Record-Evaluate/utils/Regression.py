# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import json
import os

# Load the path from variables.json
with open('../variables.json', 'r') as file:
    metadata = json.load(file)
csv_file_path = os.path.join('..',metadata[0])  # Extract the CSV file path from the JSON file

# Load your data
df = pd.read_csv(csv_file_path, delimiter=';', skip_blank_lines=True)

# Ensure the first column is time and not used in regression
time_column = 'time'  # The first column is assumed to be time
sensor_columns = ['Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
                  'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']

# Function to zero data by subtracting the first value in each column
def zero_data(df, sensor_columns):
    for col in sensor_columns:
        df[col] = df[col] - df[col].iloc[0]
    return df

# Apply zeroing to the dataset
df_zeroed = zero_data(df, sensor_columns)

# Remove rows with NaN values after zeroing
df_zeroed_clean = df_zeroed.dropna(subset=sensor_columns)

# Perform linear regression: VYV as dependent variable (y)
y = df_zeroed_clean['Concentration [ppm] at VYV'].values  # Dependent variable
results_zeroed_clean = {}

# Perform linear regression for each independent sensor
for sensor in ['Concentration [ppm] at VYU', 'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']:
    x = df_zeroed_clean[sensor].values.reshape(-1, 1)  # Independent variable
    model = LinearRegression()
    model.fit(x, y)  # Fit the model
    slope = model.coef_[0]  # Slope of the line
    intercept = model.intercept_  # Intercept of the line
    r_squared = model.score(x, y)  # Coefficient of determination (R²)

    # Store the regression results
    results_zeroed_clean[sensor] = {
        'Slope': slope,
        'Intercept': intercept,
        'R²': r_squared
    }
    plt.rcParams.update({
        'font.size': 22,  
        'axes.titlesize': 20,  
        'axes.labelsize': 20,  
        'xtick.labelsize': 20,  
        'ytick.labelsize': 20,  
        'legend.fontsize': 16   
    })
    # Plot the scatter plot and regression line
    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, label=f'{sensor} vs VYV (data)', alpha=0.6)
    plt.plot(x, model.predict(x), color='red', label='Fitted Line')

    # Annotate the regression formula on the plot
    x_pos = x.min() + 0.1 * (x.max() - x.min())
    y_pos = y.min() + 0.7 * (y.max() - y.min())
    formula = f"y = {slope:.3f}x + {intercept:.3f}\nR² = {r_squared:.3f}"
    plt.text(x_pos, y_pos, formula, fontsize=18, color='red',
             bbox=dict(facecolor='white', alpha=0.5))

    # Set labels, title, and legend
    plt.xlabel(sensor)
    plt.ylabel('Concentration [ppm] at VYV')
    plt.title(f'Linear Regression: {sensor} vs VYV')
    plt.legend()
    plt.grid(True)
    plt.show()

# Convert results to a DataFrame for better visualization
results_zeroed_clean_df = pd.DataFrame(results_zeroed_clean).T
results_zeroed_clean_df.rename(columns={'Slope': 'Slope (m)', 'Intercept': 'Intercept (b)', 'R²': 'R-squared'},
                               inplace=True)

# Display the results
print("\nLinear Relationship Results (VYV as Dependent Variable):")
print(results_zeroed_clean_df)
