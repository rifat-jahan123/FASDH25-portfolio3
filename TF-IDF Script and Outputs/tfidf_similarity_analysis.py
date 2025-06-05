# Importing the necessary libraries
import pandas as pd
import plotly.express as px
import os

# Defining the base folder path
base_path = r"..\data\dataframes\tfidf"
# Defining the filenames
files = [
    "tfidf-over-0.3.csv",
    "tfidf-over-0.3-len100.csv",
    "tfidf-over-0.3-len200.csv"
]

# Loading all datasets into a list of DataFrames
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(base_path, file))
    # Renaming the relevant columns for clarity and consistency
    df.columns = [
        'article1', 'article2', 'cosine_similarity',
        'title1', 'year1', 'month1', 'day1',
        'title2', 'year2', 'month2', 'day2'
    ]

    # Adding source file column
    df['source_file'] = file
    # Combining year, month, day into datetime for both articles
    df['date1'] = pd.to_datetime(dict(year=df['year1'], month=df['month1'], day=df['day1']), errors='coerce')
    df['date2'] = pd.to_datetime(dict(year=df['year2'], month=df['month2'], day=df['day2']), errors='coerce')

    # Assigning the earlier date in the pair for temporal analysis
    df['pair_date'] = df[['date1', 'date2']].min(axis=1)

    # Appending to list
    dfs.append(df)

# Combining all dataframes into one
combined_df = pd.concat(dfs, ignore_index=True)

# Dropping rows with missing similarity or date values
combined_df.dropna(subset=['cosine_similarity', 'pair_date'], inplace=True)

# Extracting 'month' from 'pair_date' for monthly analysis
combined_df['month'] = combined_df['pair_date'].dt.to_period('M')

# Basic statistics
print("Summary statistics:\n", combined_df['cosine_similarity'].describe())

# Exploring via Gephi
# Creating Edges CSV (Gephi format)
edges = combined_df[['article1', 'article2', 'cosine_similarity']].copy()
edges.columns = ['Source', 'Target', 'Weight']

# Filtering out weak connections to simplify the graph
edges = edges[edges['Source'] != edges['Target']]  # remove self-loops
edges = edges[edges['Weight'] >= 0.4]  # you can adjust this threshold

# Exporting edges
edges.to_csv("edges.csv", index=False)
print("edges.csv created")

# Creating Nodes CSV (Gephi format)
# Getting all unique article IDs from both columns
unique_articles = pd.unique(edges[['Source', 'Target']].values.ravel())

# Creating DataFrame with optional labels (can use title1/title2 later)
nodes = pd.DataFrame({'Id': unique_articles, 'Label': unique_articles})

# Exporting nodes
nodes.to_csv("nodes.csv", index=False)
print("nodes.csv created")

# Top 10 most similar article pairs 
top_similar = combined_df[combined_df['article1'] != combined_df['article2']]
top_similar = top_similar.sort_values(by='cosine_similarity', ascending=False).head(10)
print("Top 10 most similar article pairs:\n", top_similar[['title1', 'title2', 'cosine_similarity']])

# Histogram of cosine similarity scores by source file
fig = px.histogram(
    combined_df,
    x="cosine_similarity",
    color="source_file",
    nbins=50,
    title="TF-IDF Cosine Similarity Distribution (All Files)",
    labels={"cosine_similarity": "Cosine Similarity Score", "source_file": "Source File"},
    barmode='overlay'
)
fig.update_layout(
    xaxis_title="Cosine Similarity",
    yaxis_title="Frequency",
    bargap=0.2
)
fig.write_html("tfidf_all_similarity_distribution.html")
fig.show()

# Time-based analysis: average similarity by month and file
monthly_similarity = combined_df.groupby(['month', 'source_file'])['cosine_similarity'].mean().reset_index()

# Converting 'month' from Period to string (or datetime)
monthly_similarity['month'] = monthly_similarity['month'].astype(str)

# Plotting average monthly similarity trends through line graph
fig2 = px.line(
    monthly_similarity,
    x='month',
    y='cosine_similarity',
    color='source_file',
    title='Average TF-IDF Cosine Similarity Over Time',
    labels={'cosine_similarity': 'Average Similarity', 'month': 'Publication Month', 'source_file': 'Dataset'}
)
fig2.update_layout(
    xaxis_title='Month',
    yaxis_title='Average Cosine Similarity'
)
fig2.write_html("monthly_similarity_trend.html")
fig2.show()
