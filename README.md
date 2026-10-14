# Auto MPG Statistical Analysis

An interactive Streamlit mini-project that investigates the relationship between engine displacement and fuel efficiency (MPG) using descriptive statistics, Pearson correlation, hypothesis testing, and simple linear regression.

## Research Question

Is engine displacement significantly associated with automobile fuel efficiency?

## Hypotheses

- **Null hypothesis (H₀):** There is no significant linear relationship between engine displacement and MPG.
- **Alternative hypothesis (H₁):** There is a significant linear relationship between engine displacement and MPG.

## Features

- **Overview:** Introduces the research question, hypotheses, and dataset.
- **Data Exploration:** Displays a dataset preview, descriptive statistics, and histograms.
- **Relationship Analysis:** Shows a scatter plot, Pearson correlation, p-value, and an optional regression line. A displacement-range slider lets users analyze a subset of vehicles.
- **Regression Analysis:** Displays the regression equation, slope, R², p-value, visualization, and interpretation.
- **Project Conclusion:** Summarizes the hypothesis decision and the main findings.

## Dataset

The project uses `auto-mpg.csv`, containing 398 vehicle records and 9 columns:

`mpg`, `cylinders`, `displacement`, `horsepower`, `weight`, `acceleration`, `model year`, `origin`, and `car name`.

The dataset file must be in the same folder as the Streamlit application.

## Statistical Methods

- Descriptive statistics
- Pearson correlation
- p-value-based hypothesis testing using a significance level of 0.05
- Ordinary Least Squares (OLS) simple linear regression

The fitted model has the form:

`MPG = intercept + slope × displacement`

## Requirements

- Python 3.10 or newer recommended
- Streamlit
- pandas
- NumPy
- Matplotlib
- SciPy
- statsmodels

## Installation and Setup

1. Open a terminal in the project folder.
2. (Optional but recommended) Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required packages:

   ```powershell
   pip install -r requirements.txt
   ```

   If `requirements.txt` is incomplete, install the packages directly:

   ```powershell
   pip install streamlit pandas numpy matplotlib scipy statsmodels
   ```

4. Make sure `auto-mpg.csv` is in the same folder as the app.
5. Run the app (replace `app_fixed.py` with `app.py` if that is the filename you chose):

   ```powershell
   python -m streamlit run app_fixed.py
   ```

6. Open the local URL printed in the terminal, usually `http://localhost:8501`.

## Project Structure

```text
smd-pro/
├── app_fixed.py       # Streamlit application (or app.py, depending on your filename)
├── auto-mpg.csv       # Dataset
├── requirements.txt   # Python dependencies
├── analysis.py        # Standalone statistical analysis, if retained
├── test.py            # Development/testing script, if retained
└── README.md          # Project documentation
```

## Interpreting the Results

For the full dataset, the analysis previously produced approximately:

- Pearson correlation: **-0.8042**
- Regression R²: **0.647**
- Regression slope: **-0.0603**
- Regression p-value: **1.66 × 10⁻⁹¹**

These results indicate a strong negative association in this dataset: vehicles with larger engine displacement tend to have lower MPG. The regression model explains about 64.7% of the observed variation in MPG.

These are associations in the dataset, not proof that engine displacement alone causes lower fuel efficiency. The model uses one predictor and does not account for other factors such as vehicle weight, horsepower, model year, or cylinder count.

## Limitations

- The analysis examines a linear relationship between displacement and MPG.
- The simple regression model uses engine displacement as its only predictor.
- Results may differ for selected subsets of vehicles.
- Predictions are estimates and should not be treated as exact vehicle-specific fuel-efficiency values.

## Author

SMD Mini Project
