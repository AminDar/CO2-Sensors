# -*- coding: utf-8 -*-
"""
@author: AminDar @Github
aathome@duck.com
For HRI
"""

""""
This zeroes sensor readings, applies calibration factors, evaluates accuracy, and plots results.
"""""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import json

# File path for variables.json
path = 'variables.json'

# Column names for the CSV file
columns = ['time', 'Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
           'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']

# Calibration Function
def calibrate_data(df):
    # Calibration after zeroing
    df['Concentration [ppm] at VYU'] = 1.153 * df['Concentration [ppm] at VYU'] + 34.763
    df['Concentration [ppm] at 21kv'] = 1.118 * df['Concentration [ppm] at 21kv'] + 41.575
    df['Concentration [ppm] at VZ2'] = 0.935 * df['Concentration [ppm] at VZ2'] + 0.59
    return df

# Data Processing Functions (Zeroing then Calibration)
def process_setup_data(df):
    # Convert time column to seconds
    first_timestamp = df['time'].dropna().iloc[0] if not df['time'].isnull().all() else None
    df['time'] = (df['time'] - first_timestamp).dt.total_seconds()
    df['time'] = df['time'].astype('float32')

    # Zeroing data individually for each column
    for col in ['Concentration [ppm] at VYU', 'Concentration [ppm] at VYV',
                'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']:
        df[col] = df[col] - df[col].iloc[0]  # Subtract the first value of each column

    # Calibration
    df = calibrate_data(df)
    return df

# Splitting Data into Step-Up
def split_up_data(path, column_names):
    with open(path, 'r') as json_file:
        metadata = json.load(json_file)

    # Read CSV data
    csv_file_path = metadata[0]
    df = pd.read_csv(csv_file_path, delimiter=';', skip_blank_lines=True)
    df.columns = column_names

    # Remove rows with invalid 'time'
    df = df.dropna(how='all').reset_index(drop=True)
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time']).reset_index(drop=True)

    # Find blank rows for splitting
    blank_rows = df.isnull().all(axis=1)
    blank_indices = blank_rows[blank_rows].index
    split_index = blank_indices[0] if len(blank_indices) > 0 else len(df)

    # Split data into a step-up portion
    df_up = df.iloc[:split_index].dropna(how='all')
    df_up = process_setup_data(df_up.copy())

    return df_up

# Evaluation Function
def evaluate_calibration(df):
    y_true = df['Concentration [ppm] at VYV']  # VYV as the true reference
    sensors = ['Concentration [ppm] at VYU', 'Concentration [ppm] at 21kv', 'Concentration [ppm] at VZ2']

    print("\nCalibration Results Compared to VYV (True Reference):\n")
    for sensor in sensors:
        y_pred = df[sensor]

        # Calculate error metrics
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        pearson_corr, _ = pearsonr(y_true, y_pred)
        spearman_corr, _ = spearmanr(y_true, y_pred)

        # Print results
        print(f"Calibrated {sensor} vs VYV:")
        print(f"  MAE (Mean Absolute Error): {mae:.3f}")
        print(f"  RMSE (Root Mean Squared Error): {rmse:.3f}")
        print(f"  Pearson Correlation (r): {pearson_corr:.3f}")
        print(f"  Spearman Rank Correlation (ρ): {spearman_corr:.3f}\n")

# Plot Data
def plot_data(df):
    plt.figure(figsize=(12, 6))

    # Plot all sensor data
    plt.plot(df['time'], df['Concentration [ppm] at VYU'], label='VYU (Calibrated)', color='blue')
    plt.plot(df['time'], df['Concentration [ppm] at VYV'], label='VYV (Reference)', color='orange')
    plt.plot(df['time'], df['Concentration [ppm] at 21kv'], label='21kv (Calibrated)', color='green')
    plt.plot(df['time'], df['Concentration [ppm] at VZ2'], label='VZ2 (Calibrated)', color='red')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Concentration [ppm]')
    plt.title('Sensor Calibration Comparison with VYV as Reference')
    plt.legend()
    plt.grid(False)
    plt.savefig('Calibration.jpg')
    plt.show()

# Main Function
def main():
    # Split Data into Step-Up
    df_stepUp = split_up_data(path, columns)

    # Evaluate Calibration
    evaluate_calibration(df_stepUp)

    # Plot Results
    plot_data(df_stepUp)

# Execute main function
if __name__ == "__main__":
    main()
