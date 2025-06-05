import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")
df.columns = df.columns.str.strip()

# Create datetime
df["date"] = pd.to_datetime({
    "year": df["year"],
    "month": df["month"],
    "day": df["day"]
})

# Define terms
peace_terms = ['ceasefire', 'resolution', 'peace']
conflict_terms = ['strike', 'invasion', 'military']
all_terms = peace_terms + conflict_terms

# Filter relevant terms
df2 = df[df["1-gram"].isin(all_terms)].copy()
df2["category"] = df2["1-gram"].apply(lambda x: "Peace" if x in peace_terms else "Conflict")

# Filter date range
df2 = df2[(df2["date"] >= "2023-10-01") & (df2["date"] <= "2024-05-30")]

# Create month column
df2["month"] = df2["date"].dt.to_period("M").dt.to_timestamp()

# Group by term and month
grouped = df2.groupby(["month", "1-gram", "category"])["count"].sum().reset_index()

# Split datasets
peace_df = grouped[grouped["category"] == "Peace"]
conflict_df = grouped[grouped["category"] == "Conflict"]

# Set up subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Peace Terms", "Conflict Terms"),
    shared_yaxes=True
)

# Add Peace bars
for term in peace_terms:
    sub_df = peace_df[peace_df["1-gram"] == term]
    fig.add_trace(
        go.Bar(x=sub_df["month"], y=sub_df["count"], name=term, text=sub_df["count"], textposition="outside"),
        row=1, col=1
    )

# Add Conflict bars
for term in conflict_terms:
    sub_df = conflict_df[conflict_df["1-gram"] == term]
    fig.add_trace(
        go.Bar(x=sub_df["month"], y=sub_df["count"], name=term, text=sub_df["count"], textposition="outside"),
        row=1, col=2
    )

# Update layout
fig.update_layout(
    title_text="Monthly Frequency of Peace & Conflict Terms (Oct 2023 – May 2024)",
    barmode="group",
    template="plotly_white",
    showlegend=True,
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

fig.update_xaxes(title_text="Month", tickangle=45, row=1, col=1)
fig.update_xaxes(title_text="Month", tickangle=45, row=1, col=2)
fig.update_yaxes(title_text="Frequency", row=1, col=1)

fig.show()






 







