
# Import necessary libraries 
import pandas as pd

import plotly.graph_objects as go   # for creating bar graphs and other visual plots

from plotly.subplots import make_subplots   # for creating multiple subplots in a single figure

# Load data
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

#Remove any kind of whitespace from column names to avoid errors
df.columns = df.columns.str.strip()

# Create single date column by combining year, month and day columns 
df["date"] = pd.to_datetime({
    "year": df["year"],
    "month": df["month"],
    "day": df["day"]
})

# Define lists of specific 1-gram words related to peace and conflict 
peace_terms = ['ceasefire', 'resolution', 'peace']
conflict_terms = ['strike', 'invasion', 'military']

#combine all of the terms into one list for filtering 
all_terms = peace_terms + conflict_terms

# Filter relevant terms
# Keep only rows where hte 1-gram word is in our list of interest
df2 = df[df["1-gram"].isin(all_terms)].copy()

#create a new column called category to label each word as either peace or conflict
df2["category"] = df2["1-gram"].apply(lambda x: "Peace" if x in peace_terms else "Conflict")


# Filter data to only include rows within the speciifed date range (Oct 2023 to May 2024)
df2 = df2[(df2["date"] >= "2023-10-01") & (df2["date"] <= "2024-05-30")]

# Create month column by converting the date to the first day of each month 
df2["month"] = df2["date"].dt.to_period("M").dt.to_timestamp()

# Group the data by month, term and category and sum the counts to get total monthly frequency 
grouped = df2.groupby(["month", "1-gram", "category"])["count"].sum().reset_index()

# Split datasets by creating separate DataFrames for peace and conflict terms
peace_df = grouped[grouped["category"] == "Peace"]
conflict_df = grouped[grouped["category"] == "Conflict"]

# Set up subplots with 1 row and 2 columns (side by side bar graphs)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Peace Terms", "Conflict Terms"), #titles for subplots
    shared_yaxes=True  # share the same y-axis scale for better comparison 
)

# Add bar plots for each peace-related term for the first subplot
for term in peace_terms:
    sub_df = peace_df[peace_df["1-gram"] == term]  #filter data for this specific term 
    fig.add_trace(
        go.Bar(
            x=sub_df["month"],   #x-axis - months
            y=sub_df["count"],   #y-axis - frequency counts 
            name=term, 
            text=sub_df["count"],   #show count values on bars 
            textposition="outside"),  # position count text outside the bar 
        row=1, col=1    # Add to first subplot 
    )

# Add bar plots for each conflict related term to the second subplot (right side)
for term in conflict_terms:
    sub_df = conflict_df[conflict_df["1-gram"] == term] #filter data for the specific term 
    fig.add_trace(
        go.Bar(x=sub_df["month"], y=sub_df["count"], name=term, text=sub_df["count"], textposition="outside"),
        row=1, col=2    #Add to second subplot
    )

# Update layout of the graph 
fig.update_layout(
    title_text="Monthly Frequency of Peace & Conflict Terms (Oct 2023 – May 2024)",  #Main title
    barmode="group",  # group bars side by side 
    template="plotly_white", #use a clean white background 
    showlegend=True,      # show legend to identify terms 
    uniformtext_minsize=8,  # minimum text size for bar labels 
    uniformtext_mode='hide'   # hide text if it doesn't fit correctly 
)

#Add x-axis label and rotate for better readability 
fig.update_xaxes(title_text="Month", tickangle=45, row=1, col=1)
fig.update_xaxes(title_text="Month", tickangle=45, row=1, col=2)

#add y-axis label on the left subplot 
fig.update_yaxes(title_text="Frequency", row=1, col=1)

#save as html
fig.write_html("monthly_frequency_of_peace_and_conflict_terms.html")

#display the final graph 
fig.show()





 







