import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from scipy.stats import pearsonr

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Auto MPG Statistical Analysis",
    page_icon="🚗",
    layout="wide"
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv("auto-mpg.csv")

# --------------------------------------------------
# Global statistical model
# --------------------------------------------------
# Calculated once so the values are available to every page.
X_global = sm.add_constant(df["displacement"])
y_global = df["mpg"]
model_global = sm.OLS(y_global, X_global).fit()

intercept_global = model_global.params["const"]
slope_global = model_global.params["displacement"]
r_squared_global = model_global.rsquared
p_value_global = model_global.pvalues["displacement"]
r_global, correlation_p_global = pearsonr(
    df["displacement"],
    df["mpg"]
)


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Data Exploration",
        "Relationship Analysis",
        "Regression Analysis",
        "MPG Prediction",
        "Statistical Summary",
        "Project Conclusion"
    ]
)


# ==================================================
# PAGE 1 — OVERVIEW
# ==================================================

if page == "Overview":

    st.title("🚗 Auto MPG Statistical Analysis")

    st.write(
        "An interactive statistical analysis of the relationship "
        "between engine displacement and fuel efficiency."
    )

    st.header("Project Overview")

    st.write(
        "This project investigates whether engine displacement "
        "is significantly associated with automobile fuel efficiency."
    )

    st.subheader("Research Question")

    st.info(
        "Is engine displacement significantly associated with "
        "fuel efficiency (MPG)?"
    )

    st.subheader("Hypotheses")

    st.markdown("""
    **Null Hypothesis (H₀):**  
    There is no significant linear relationship between engine
    displacement and MPG.

    **Alternative Hypothesis (H₁):**  
    There is a significant linear relationship between engine
    displacement and MPG.
    """)

    st.subheader("Dataset")

    st.write(
        "The dataset contains information about 398 automobiles."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Vehicles", "398")

    with col2:
        st.metric("Average MPG", "23.51")

    with col3:
        st.metric("Average Displacement", "193.43")


# ==================================================
# PAGE 2 — DATA EXPLORATION
# ==================================================

elif page == "Data Exploration":

    st.title("📊 Data Exploration")

    st.write(
        "Explore the automobile dataset and examine the basic "
        "characteristics of MPG and engine displacement."
    )

    # Dataset information
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Number of Vehicles", len(df))

    with col2:
        st.metric("Number of Variables", len(df.columns))

    st.divider()

    # Data preview
    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    # Descriptive statistics
    st.subheader("Descriptive Statistics")

    stats = df[["mpg", "displacement"]].describe().T

    stats = stats.rename(
        columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Std. Dev.",
            "min": "Minimum",
            "25%": "25%",
            "50%": "Median",
            "75%": "75%",
            "max": "Maximum"
        }
    )

    st.dataframe(
        stats.round(2),
        use_container_width=True
    )

    st.divider()

    # Histogram
    st.subheader("Distribution")

    variable = st.selectbox(
        "Select a variable:",
        ["mpg", "displacement"]
    )

    labels = {
        "mpg": "Fuel Efficiency (MPG)",
        "displacement": "Engine Displacement"
    }

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        df[variable],
        bins=20,
        edgecolor="black"
    )

    ax.set_xlabel(labels[variable])
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of {labels[variable]}")

    st.pyplot(fig)




# ==================================================
# PAGE 3 — RELATIONSHIP ANALYSIS
# ==================================================

elif page == "Relationship Analysis":

    st.title("📈 Relationship Analysis")

    st.write(
        "Analyze the relationship between engine displacement "
        "and fuel efficiency using correlation and visualization."
    )

    # --------------------------------------------------
    # Engine displacement filter
    # --------------------------------------------------

    st.subheader("Filter Vehicles")

    min_displacement = float(df["displacement"].min())
    max_displacement = float(df["displacement"].max())

    displacement_range = st.slider(
        "Select engine displacement range:",
        min_value=min_displacement,
        max_value=max_displacement,
        value=(min_displacement, max_displacement)
    )

    # Filter dataset
    filtered_df = df[
        (df["displacement"] >= displacement_range[0]) &
        (df["displacement"] <= displacement_range[1])
    ]

    # --------------------------------------------------
    # Basic information
    # --------------------------------------------------

    st.write(
        f"Showing **{len(filtered_df)}** vehicles "
        f"within the selected displacement range."
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data",
        data=csv_data,
        file_name="filtered_auto_mpg.csv",
        mime="text/csv"
    )

    if len(filtered_df) < 3:

        st.warning(
            "Please select a wider range. At least 3 vehicles "
            "are required for correlation analysis."
        )

    else:

        # --------------------------------------------------
        # Pearson correlation
        # --------------------------------------------------

        r, p_value = pearsonr(
            filtered_df["displacement"],
            filtered_df["mpg"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Vehicles",
                len(filtered_df)
            )

        with col2:
            st.metric(
                "Pearson Correlation",
                f"{r:.4f}"
            )

        with col3:
            st.metric(
                "p-value",
                f"{p_value:.2e}"
            )

        st.divider()

        # --------------------------------------------------
        # Scatter plot
        # --------------------------------------------------

        st.subheader(
            "Engine Displacement vs Fuel Efficiency"
        )

        show_line = st.checkbox(
            "Show regression line",
            value=True
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.scatter(
            filtered_df["displacement"],
            filtered_df["mpg"],
            alpha=0.7,
            label="Observed data"
        )

        if show_line:

            slope, intercept = np.polyfit(
                filtered_df["displacement"],
                filtered_df["mpg"],
                1
            )

            x_values = np.linspace(
                filtered_df["displacement"].min(),
                filtered_df["displacement"].max(),
                100
            )

            y_values = intercept + slope * x_values

            ax.plot(
                x_values,
                y_values,
                color="red",
                label="Regression line"
            )

        ax.set_xlabel("Engine Displacement")
        ax.set_ylabel("Fuel Efficiency (MPG)")
        ax.set_title(
            "Engine Displacement vs Fuel Efficiency"
        )

        ax.legend()

        st.pyplot(fig)

        st.divider()

        # --------------------------------------------------
        # Hypothesis test
        # --------------------------------------------------

        st.subheader("Hypothesis Test")

        st.markdown("""
        **H₀:** There is no significant linear relationship
        between engine displacement and MPG.

        **H₁:** There is a significant linear relationship
        between engine displacement and MPG.
        """)

        if p_value_global < 0.05:

            st.success(
                "Reject H₀: There is a statistically significant "
                "relationship between engine displacement and MPG."
            )

        else:

            st.warning(
                "Fail to reject H₀: There is not enough evidence "
                "of a statistically significant relationship."
            )





# ==================================================
# PAGE 4 — REGRESSION ANALYSIS
# ==================================================

elif page == "Regression Analysis":

    st.title("📉 Regression Analysis")

    st.write(
        "A simple linear regression model is used to examine "
        "whether engine displacement can predict fuel efficiency."
    )

    # --------------------------------------------------
    # Regression model
    # --------------------------------------------------

    X = sm.add_constant(df["displacement"])
    y = df["mpg"]

    model = sm.OLS(y, X).fit()

    intercept = model.params["const"]
    slope = model.params["displacement"]
    r_squared = model.rsquared
    p_value = model.pvalues["displacement"]


    r, correlation_p = pearsonr(
    df["displacement"],
    df["mpg"]
    )


    # --------------------------------------------------
    # Regression equation
    # --------------------------------------------------

    st.subheader("Regression Equation")

    st.latex(
        f"MPG = {intercept:.2f} "
        f"{slope:+.4f} \\times Displacement"
    )

    # --------------------------------------------------
    # Key results
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "R²",
            f"{r_squared:.3f}"
        )

    with col2:
        st.metric(
            "Slope",
            f"{slope:.4f}"
        )

    with col3:
        st.metric(
            "p-value",
            f"{p_value:.2e}"
        )

    st.divider()

    # --------------------------------------------------
    # Regression plot
    # --------------------------------------------------

    st.subheader("Regression Plot")

    predicted = model.predict(X)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.scatter(
        df["displacement"],
        df["mpg"],
        alpha=0.7,
        label="Observed data"
    )

    ax.plot(
        df["displacement"],
        predicted,
        color="red",
        linewidth=2,
        label="Regression line"
    )

    ax.set_xlabel("Engine Displacement")
    ax.set_ylabel("Fuel Efficiency (MPG)")
    ax.set_title(
        "Linear Regression: Displacement vs MPG"
    )

    ax.legend()

    st.pyplot(fig)

    st.divider()

    # --------------------------------------------------
    # Interpretation
    # --------------------------------------------------

    st.subheader("Interpretation")

    st.write(
        f"The regression model has an R² value of "
        f"**{r_squared:.3f}**, meaning that approximately "
        f"**{r_squared * 100:.1f}%** of the variation in MPG "
        f"is explained by engine displacement."
    )

    if p_value < 0.05:

        st.success(
            "The p-value is less than 0.05. Therefore, "
            "engine displacement has a statistically significant "
            "linear relationship with MPG."
        )

    else:

        st.warning(
            "The p-value is greater than 0.05. Therefore, "
            "there is insufficient evidence of a significant "
            "linear relationship."
        )

    if slope < 0:

        st.info(
            "The negative regression coefficient indicates that "
            "vehicles with larger engine displacement tend to "
            "have lower fuel efficiency."
        )

    else:

        st.info(
            "The positive regression coefficient indicates that "
            "vehicles with larger engine displacement tend to "
            "have higher fuel efficiency."
        )




# ==================================================
# PAGE 5 — MPG PREDICTION
# ==================================================

elif page == "MPG Prediction":

    st.title("🚗 MPG Prediction")

    st.write(
        "Use the fitted linear regression model to estimate fuel "
        "efficiency for a selected engine displacement."
    )

    st.subheader("Enter Engine Displacement")

    min_disp = float(df["displacement"].min())
    max_disp = float(df["displacement"].max())
    mean_disp = float(df["displacement"].mean())

    displacement_input = st.slider(
        "Engine displacement:",
        min_value=min_disp,
        max_value=max_disp,
        value=mean_disp,
        step=1.0
    )

    predicted_mpg = intercept_global + slope_global * displacement_input

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Engine Displacement", f"{displacement_input:.1f}")

    with col2:
        st.metric("Predicted MPG", f"{predicted_mpg:.2f}")

    with col3:
        st.metric("Model R²", f"{r_squared_global:.3f}")

    st.divider()

    st.subheader("Prediction Result")

    if predicted_mpg >= df["mpg"].mean():
        st.success(
            f"A vehicle with a displacement of **{displacement_input:.1f}** "
            f"is predicted to achieve approximately **{predicted_mpg:.2f} MPG**."
        )
    else:
        st.info(
            f"A vehicle with a displacement of **{displacement_input:.1f}** "
            f"is predicted to achieve approximately **{predicted_mpg:.2f} MPG**."
        )

    st.subheader("Prediction Equation")

    st.latex(
        f"MPG = {intercept_global:.2f} "
        f"{slope_global:+.4f} \\times Displacement"
    )

    st.caption(
        "This is an estimate from the simple linear regression model; "
        "it should not be interpreted as an exact vehicle-specific MPG value."
    )

    st.divider()

    # Visualize the selected prediction against the fitted model.
    x_values = np.linspace(min_disp, max_disp, 100)
    y_values = intercept_global + slope_global * x_values

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(
        df["displacement"],
        df["mpg"],
        alpha=0.55,
        label="Observed data"
    )
    ax.plot(
        x_values,
        y_values,
        color="red",
        linewidth=2,
        label="Regression line"
    )
    ax.scatter(
        [displacement_input],
        [predicted_mpg],
        color="black",
        s=90,
        zorder=5,
        label="Selected prediction"
    )

    ax.set_xlabel("Engine Displacement")
    ax.set_ylabel("Fuel Efficiency (MPG)")
    ax.set_title("MPG Prediction from Engine Displacement")
    ax.legend()

    st.pyplot(fig)


# ==================================================
# PAGE 6 — STATISTICAL SUMMARY
# ==================================================

elif page == "Statistical Summary":

    st.title("📋 Statistical Summary")

    st.write(
        "A compact summary of the main descriptive and inferential "
        "statistics used in this project."
    )

    st.subheader("Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Vehicles", f"{len(df)}")

    with col2:
        st.metric("Average MPG", f"{df['mpg'].mean():.2f}")

    with col3:
        st.metric("Average Displacement", f"{df['displacement'].mean():.2f}")

    with col4:
        st.metric("Variables", f"{len(df.columns)}")

    st.divider()

    st.subheader("Key Statistical Results")

    summary = pd.DataFrame({
        "Measure": [
            "Pearson correlation (r)",
            "Correlation p-value",
            "Regression intercept",
            "Regression slope",
            "R²",
            "Regression p-value",
            "Significance level"
        ],
        "Value": [
            f"{r_global:.4f}",
            f"{correlation_p_global:.2e}",
            f"{intercept_global:.4f}",
            f"{slope_global:.4f}",
            f"{r_squared_global:.4f}",
            f"{p_value_global:.2e}",
            "0.05"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Interpretation")

    if p_value_global < 0.05:
        st.success(
            "The regression p-value is below 0.05, so the null hypothesis "
            "is rejected. There is statistically significant evidence of "
            "a linear relationship between engine displacement and MPG."
        )
    else:
        st.warning(
            "The regression p-value is above 0.05, so there is not enough "
            "evidence to reject the null hypothesis."
        )

    if r_global < 0:
        st.info(
            f"The Pearson correlation is **{r_global:.4f}**, indicating a "
            "negative association: larger engine displacement generally "
            "corresponds to lower MPG in this dataset."
        )

    st.subheader("Model Equation")

    st.latex(
        f"MPG = {intercept_global:.2f} "
        f"{slope_global:+.4f} \\times Displacement"
    )


# --------------------------------------------------
# Final Conclusion
# --------------------------------------------------

# st.divider()

# st.subheader("🎯 Project Conclusion")

# st.markdown("""
# ### Hypothesis Decision

# **Null Hypothesis (H₀):**  
# There is no significant linear relationship between engine
# displacement and fuel efficiency.

# **Alternative Hypothesis (H₁):**  
# There is a significant linear relationship between engine
# displacement and fuel efficiency.
# """)

# if p_value_global < 0.05:

#     st.success(
#         "### H₀ is Rejected"
#     )

#     st.write(
#         "The analysis provides strong statistical evidence "
#         "of a significant relationship between engine "
#         "displacement and fuel efficiency."
#     )

#     st.write(
#         f"The Pearson correlation is **{r_global:.4f}**, indicating "
#         "a strong negative relationship. The regression model "
#         f"has an R² of **{r_squared_global:.3f}**, meaning that engine "
#         f"displacement explains approximately "
#         f"**{r_squared_global * 100:.1f}%** of the variation in MPG."
#     )

#     st.write(
#         "Therefore, vehicles with larger engine displacement "
#         "generally tend to have lower fuel efficiency."
#     )

# else:

#     st.warning(
#         "### H₀ is Not Rejected"
#     )

#     st.write(
#         "The analysis does not provide sufficient statistical "
#         "evidence of a significant linear relationship."
#     )

# st.sidebar.divider()
# st.sidebar.caption("Auto MPG Statistical Analysis • SMD Mini Project")










# ==================================================
# PAGE 7 — PROJECT CONCLUSION
# ==================================================

elif page == "Project Conclusion":

    st.title("🎯 Project Conclusion")

    st.subheader("Hypothesis Decision")

    st.markdown("""
    **Null Hypothesis (H₀):**  
    There is no significant linear relationship between engine
    displacement and fuel efficiency.

    **Alternative Hypothesis (H₁):**  
    There is a significant linear relationship between engine
    displacement and fuel efficiency.
    """)

    if p_value_global < 0.05:

        st.success("### H₀ is Rejected")

        st.write(
            "The analysis provides strong statistical evidence "
            "of a significant relationship between engine "
            "displacement and fuel efficiency."
        )

        st.write(
            f"The Pearson correlation is **{r_global:.4f}**, indicating "
            f"a {'negative' if r_global < 0 else 'positive'} relationship. "
            f"The regression model has an R² of **{r_squared_global:.3f}**, "
            f"meaning that engine displacement explains approximately "
            f"**{r_squared_global * 100:.1f}%** of the variation in MPG."
        )

        if slope_global < 0:
            st.info(
                "Therefore, vehicles with larger engine displacement "
                "generally tend to have lower fuel efficiency."
            )
        else:
            st.info(
                "Therefore, vehicles with larger engine displacement "
                "generally tend to have higher fuel efficiency."
            )

    else:
        st.warning("### H₀ is Not Rejected")
        st.write(
            "The analysis does not provide sufficient statistical "
            "evidence of a significant linear relationship between "
            "engine displacement and fuel efficiency."
        )


st.sidebar.divider()
st.sidebar.caption("Auto MPG Statistical Analysis • SMD Mini Project")
