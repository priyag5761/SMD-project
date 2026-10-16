# Auto MPG Statistical Analysis

## Project Overview
An interactive Streamlit application that studies the relationship between engine displacement and automobile fuel efficiency, measured in miles per gallon (MPG).

## Research Question
Is engine displacement significantly associated with automobile fuel efficiency (MPG)?

## Hypotheses
- **Null hypothesis (H₀):** There is no significant linear relationship between engine displacement and MPG.
- **Alternative hypothesis (H₁):** There is a significant linear relationship between engine displacement and MPG.

## Features
- **Overview:** Project purpose, research question, hypotheses, and dataset information.
- **Data Exploration:** Dataset preview, descriptive statistics, and histograms.
- **Relationship Analysis:** Scatter plot, Pearson correlation, p-value, hypothesis test, optional regression line, and engine-displacement range filter.
- **Regression Analysis:** Regression equation, slope, R², p-value, plot, and interpretation.
- **Project Conclusion:** Summary of the hypothesis decision and main findings.

## Dataset
The app reads `auto-mpg.csv`, containing 398 automobile records and 9 columns: MPG, cylinders, displacement, horsepower, weight, acceleration, model year, origin, and car name.

Keep `auto-mpg.csv` in the same folder as `app_final.py`.

## Statistical Methods
- Descriptive statistics
- Pearson correlation
- Hypothesis testing with significance level 0.05
- Ordinary Least Squares (OLS) simple linear regression

Regression model:

`MPG = intercept + slope × displacement`

## Technologies
Python, Streamlit, pandas, NumPy, Matplotlib, SciPy, and statsmodels.

## Setup and Run

Install dependencies using the project's `requirements.txt`:

```powershell
pip install -r requirements.txt
```

If necessary, install them directly:

```powershell
pip install streamlit pandas numpy matplotlib scipy statsmodels
```

Run the application from the folder containing `app_final.py` and `auto-mpg.csv`:

```powershell
python -m streamlit run app_final.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Main Findings
For the full dataset, the analysis previously produced approximately:
- **Pearson correlation:** -0.8042
- **Regression slope:** -0.0603
- **R²:** 0.647
- **Regression p-value:** 1.66 × 10⁻⁹¹

These results indicate a strong negative association between engine displacement and MPG. The fitted model explains approximately 64.7% of the observed variation in MPG.

## Limitations
- The simple regression model uses engine displacement as its only predictor.
- Association does not prove that engine displacement alone causes lower fuel efficiency.
- Other factors, such as vehicle weight, horsepower, and model year, are not included in the simple model.
- MPG predictions are estimates, not guaranteed real-world values.

## Application Entry Point
The main Streamlit application file is `app_final.py`.
