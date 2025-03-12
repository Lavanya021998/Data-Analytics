import pandas as pd
import numpy as np
import time  # To delay response
import warnings
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode
import plotly.express as px
matplotlib.use('Agg')
warnings.filterwarnings("ignore")  # To suppress warnings

import streamlit as st  # UI Module

################################# Dashboard ##########################################
st.subheader(":green[Data Analytics Project]", divider=True)
st.write(":blue[Data Taken For Analysis..]")

df = pd.read_excel("validatedata.xlsx")

st.dataframe(df.head())
st.divider()

st.subheader(":red[Uni-Variate Analytics (Single Column Data Study):]",divider=True)
cola, colb, colc = st.columns(3)
with colb:
    colname = st.selectbox("Select Column:", df.columns)

if df[colname].dtype == object:
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### [{colname}] Stats:")
        st.divider()
        st.write(df[colname].value_counts())
    with col2:
        st.write(f"### {colname} Bar Chart:")
        st.divider()
        st.bar_chart(df[colname].value_counts())

elif df[colname].dtype in [np.int64, np.float64]:
    # Drop NaN values for calculations
    numeric_data = df[colname].dropna()

    mean_value = np.mean(numeric_data)  # Mean
    median_value = np.median(numeric_data)  # Median
    mode_value = numeric_data.mode().values[0] if not numeric_data.mode().empty else "No mode"
    range_value = np.max(numeric_data) - np.min(numeric_data)
    variance_value = np.var(numeric_data)  # Sample variance
    std_dev_value = np.std(numeric_data)
    five_num_summary = numeric_data.describe()[["min", "25%", "50%", "75%", "max"]]
    # Measures of Symmetry
    skewness = numeric_data.skew()
    kurtosis = numeric_data.kurt()

    
    st.write("### Statistical Summary")
    st.write(f"**Mean:** {mean_value}")
    st.write(f"**Median:** {median_value}")
    st.write(f"**Mode:** {mode_value}")
    

    st.write(f"**Range:** {range_value:.2f}")
    st.write(f"**Variance:** {variance_value:.2f}")
    st.write(f"**Standard Deviation:** {std_dev_value:.2f}")
    st.write("### Five Number Summary:")
    st.write(five_num_summary)
    st.divider()
    st.write("### Measures of Symmetry")
    st.write(f"**Skewness:** {skewness:.2f}")
    st.write(f"**Kurtosis:** {kurtosis:.2f}")

    st.write("### Visual - Distplot (Histogram + Density Plot):",divider=True)
    fig, ax = plt.subplots()
    sns.histplot(numeric_data, bins=20, kde=True, ax=ax)
    st.pyplot(fig)
st.subheader(":violet[Bi-Variate Analytics  and Multivariate Analytics:]",divider=True)
st.dataframe(df.head(7))
st.write(":green[Pure numeric- To understand the data between number columns we can use correlation coeficient measure from descriptive stats.]")
# Select only numeric columns
numeric_cols = df.select_dtypes(include=[np.int64, np.float64]).columns.tolist()
numbcols=df.select_dtypes(include=[np.int64, np.float64]).columns.tolist()

col1, col2= st.columns(2)
with col1:
    st.subheader(":violet[select numeric columns:]",divider=True)
    numb1= st.selectbox("Choose a numeric column:", numeric_cols,index=0)
    st.write(f"You selected: {numb1}")
with col2:
    st.subheader(":violet[select numeric columns:]",divider=True)
    numb2= st.selectbox("Choose a numeric column:", numbcols,index=1)
    st.write(f"You selected: {numb2}")
    correlation = df[[numb1,numb2]].corr().iloc[0, 1]  # Get the correlation value
col1,col2,col3=st.columns(3)
    # Example: Show scatter plot
with col1:
    st.write(f"Correlation between **{numb1}** and **{numb2}**: `{correlation:.4f}`")
with col3:
    st.subheader("scatter plot b/w numeric columns:")
    st.scatter_chart(df[[numb1,numb2]])
st.subheader(":violet[categorical columns crosstab:]",divider=True)
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Allow user to select two or more categorical columns
selected_columns = st.multiselect("Select Two or More Categorical Columns:", categorical_columns, default=categorical_columns[:2])

if len(selected_columns) >= 2:
    # Compute cross-tab with multiple index columns
    crosstab_result = pd.crosstab(index=[df[col] for col in selected_columns[:-1]], columns=df[selected_columns[-1]], margins=True)
    # Display result
    st.subheader(f"Cross Tabulation of {', '.join(selected_columns)}")
    st.dataframe(crosstab_result)
st.divider()
if 'Institute name' in df.columns:
    classes = df['Institute name'].value_counts().sort_values(ascending=False)[0:10].index
    vals = df['Institute name'].value_counts().sort_values(ascending=False)[0:10].values
    
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(x=vals, labels=classes, autopct=lambda p: f'{p:.2f}%, ({p*sum(vals)/100 :.0f})')
    ax.set_title("Institute Comparison")
    ax.legend()
    
    st.pyplot(fig)
else:
    st.error("CSV file must contain an 'Institute name' column.")
st.divider()
if 'Training Methodology' in df.columns:
    classes = df['Training Methodology'].value_counts().sort_values(ascending=False)[0:3].index
    vals = df['Training Methodology'].value_counts().sort_values(ascending=False)[0:3].values
    
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.bar(classes, vals)
    ax.set_title("Comparison of Training Methodology")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    st.pyplot(fig)
else:
     st.error("CSV file must contain a 'Training Methodology' column.")
st.divider()
if 'Average Salary' in df.columns:
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.hist(df['Average Salary'], bins=20, edgecolor='black')
    ax.set_title("Distribution of Salary")
    ax.set_xlabel("Salary")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("CSV file must contain an 'Average Salary' column.")
st.divider()
if 'Faculty Expertise' in df.columns:
    plt.style.use("classic")
    fig, ax = plt.subplots(figsize=(8, 8))
    df['Faculty Expertise'].value_counts().sort_values(ascending=False)[0:10].plot(kind='pie', autopct="%.0f%%", ax=ax)
    ax.set_title("Faculty Expertise Distribution")
    ax.set_ylabel("")  # Hide y-label for better visualization
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("CSV file must contain a 'Faculty Expertise' column.")
st.divider()
cola, colb, colc = st.columns(3)
with cola:
    colname11 = st.selectbox("Select y column:", df.columns)
with colb:
    colname12=st.selectbox("select any course in columns for x:",df.columns)
with colc:
    colname21=st.selectbox("select column for hue:",df.columns)

st.subheader(":violet[Catplot Example: Faculty Expertise vs Data Science and AI]")

# Create the seaborn catplot
sns.set(style="whitegrid")
catplot = sns.catplot(data=df, y=colname11, x=colname12,hue=colname21, orient='h')
# Display the plot in Streamlit
st.pyplot(catplot.fig)
st.divider()
st.subheader(":violet[Correlation Heatmap]")
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='viridis', fmt='.2f', cbar=True)
# Display the plot in Streamlit
st.pyplot(plt)
st.divider()
st.subheader(":violet[Pairplot Example]")
# Create the seaborn pairplot with 'Target Audience' as the categorical column for hue
pairplot = sns.pairplot(df, hue='Target Audience')
st.pyplot(pairplot.fig)
