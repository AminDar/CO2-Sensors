# CO2-Sensors

This repository provides scripts to record, calibrate and evaluate CO₂ concentration data using Tinkerforge CO2 Bricklet 2.0 sensors. The tools can help assess ventilation efficiency through step-up and step-down measurements and generate plots for further analysis. This repository was developed during a student project.

## Repository Layout

- **Co2-Record-Evaluate/Sensor.py** – Records CO₂ data from four sensors, stores measurements in `Raw/`, and visualizes readings live.
- **Co2-Record-Evaluate/SplitDataframe.py** – Splits a recorded CSV into step-up and step-down segments, applies calibration and plots the results.
- **Co2-Record-Evaluate/utils/** – Collection of utilities for calibration, regression analysis, integral calculations and air-change metrics (e.g. `Calibration.py`, `MFCstepupFunction.py`, `MFCstepDownFunction.py`).
- **Co2-Record-Evaluate/MFC.py** – Optional script to control a mass flow controller during experiments.
- **variables.json** – Generated metadata file containing the last recorded CSV file path and measurement interval.

## Usage

1. **Record data**
   ```bash
   python Co2-Record-Evaluate/Sensor.py
   ```
   Enter the desired measurement duration in minutes. A CSV file will be created inside `Co2-Record-Evaluate/Raw/`.

2. **Analyze the recording**
   ```bash
   python Co2-Record-Evaluate/SplitDataframe.py
   ```
   Follow the prompts to evaluate step-up/step-down sequences. Calibrated data and plots will be shown.

3. **Run individual utilities**
   For calibration assessment and plotting you can run:
   ```bash
   python Co2-Record-Evaluate/utils/Calibration.py
   ```
   Other scripts in `utils/` provide regression models and integral-based metrics.

## Requirements

The code relies on:
- Python 3
- `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `scipy`
- `colorama`
- `tinkerforge` (for communicating with the Bricklet sensors)

Install these packages with pip:
```bash
pip install pandas numpy matplotlib scikit-learn scipy colorama tinkerforge
```

## License

This project is available under the [MIT License](LICENSE).
