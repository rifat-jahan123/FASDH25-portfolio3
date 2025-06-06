import pandas as pd
import plotly.express as px
import os


# Load the dataset
df = pd.read_csv("../data/dataframes/length/length.csv")

# Group by year
yearly = df.groupby("year")["length"].agg(["sum", "mean", "count"]).reset_index()

# Group by year and month 
monthly = df.groupby(["year", "month"])["length"].agg(["sum", "mean", "count"]).reset_index()
monthly["date"] = pd.to_datetime(monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2))

# Total article length by year 
fig1 = px.bar(yearly, x="year", y="sum",
              title="Total Article Length by Year – Journalistic Focus",
              labels={"sum": "Total Words", "year": "Year"})
fig1.update_layout(yaxis_title="Total Words")
fig1.write_html("outputs/samrin-total-year.html")
fig1.show()

# Average article length by year 
fig2 = px.line(yearly, x="year", y="mean",
               title="Average Article Length by Year – Depth of Coverage",
               markers=True,
               labels={"mean": "Avg Words", "year": "Year"})
fig2.update_layout(yaxis_title="Average Words")
fig2.write_html("outputs/samrin-average-year.html")
fig2.show()

# Number of articles per month 
fig3 = px.line(monthly, x="date", y="count",
               title="Number of Articles Published per Month",
               markers=True,
               labels={"count": "Article Count", "date": "Month"})
fig3.update_layout(yaxis_title="Article Count")
fig3.write_html("outputs/samrin-article-count-month.html")
fig3.show()

# Total article length per month 
fig4 = px.line(monthly, x="date", y="sum",
               title="Monthly Total Article Length – Event-Driven Spikes",
               markers=True,
               labels={"sum": "Total Words", "date": "Month"})
fig4.update_layout(yaxis_title="Total Words")
fig4.write_html("outputs/samrin-total-month.html")
fig4.show()

# Average article length per month 
fig5 = px.line(monthly, x="date", y="mean",
               title="Monthly Average Article Length – Depth of Reporting",
               markers=True,
               labels={"mean": "Avg Words", "date": "Month"})
fig5.update_layout(yaxis_title="Average Words")
fig5.write_html("outputs/samrin-average-month.html")
fig5.show()

# first Faceted histogram grouped by month-year
# Categorize each article based on its length into Short, Medium, or Long
df["length_type"] = df["length"].apply(lambda x: "Short (<300)" if x < 300 else "Medium (300–800)" if x <= 800 else "Long (>800)")

# Create a new column 'year_month' by combining 'year' and 'month' into a datetime format
# got help from AI Entry 6
df["year_month"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2))

# Grouping the data by year_month and length_type, and counting the number of articles in each group
grouped = df.groupby(["year_month", "length_type"]).size().reset_index(name="count")

# Create a line plot showing how the number of articles in each length category changes over time
fig = px.line(grouped, x="year_month", y="count", color="length_type",
              title="Monthly Trends of Article Length Types",
              labels={"count": "Number of Articles", "year_month": "Month", "length_type": "Length Type"},
              markers=True)
fig.update_layout(xaxis_tickangle=45)
fig.write_html("outputs/samrin-monthly-length-type-lines.html")
fig.show()

# Second faceted histogram grouped by month-year
# Filter articles shorter than 2000 words
df_short = df[df["length"] <= 2000].copy()

# Create a "year-month" column in string format like "2023-06"
df_short["year_month"] = df_short["year"].astype(str) + "-" + df_short["month"].astype(str).str.zfill(2)

# Keep only months that have at least 10 articles
month_counts = df_short["year_month"].value_counts()
active_months = month_counts[month_counts >= 10].index  # Keep only those months where the number of articles is 10 or more

# Filter the dataset to include only those active months
df_short = df_short[df_short["year_month"].isin(active_months)] # got help from AI Entry 3  

# Create faceted histogram using the filtered data
# got help from AI Entry 3
fig7 = px.histogram(df_short,
                    x="length",
                    facet_col="year_month",  # Create one small chart for each one
                    facet_col_wrap=4,        # Wrap charts to show 4 per row
                    title="Faceted Histogram of Article Lengths by Month",
                    nbins=40,                # Number of bars (bins) in each histogram
                    
                    labels={"length": "Article Length", "year_month": "Month-Year"})

fig7.update_layout(showlegend=False, height=1000)
fig7.write_html("outputs/samrin-faceted-histogram.html")
fig7.show()

