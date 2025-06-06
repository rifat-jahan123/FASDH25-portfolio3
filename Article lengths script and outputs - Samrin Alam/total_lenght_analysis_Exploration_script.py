import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("../data/dataframes/length/length.csv")
print("Data loaded successfully.")

# Group by year
yearly = df.groupby("year")["length"].agg(["sum", "mean", "count"]).reset_index()
print("Yearly summary (total, average, and count):")
print(yearly)

# Group by year and month 
# First, combine 'year' and 'month' into a new column called 'date_string'

# Group the data by year and month and calculate total, average, and count of article lengths
monthly = df.groupby(["year", "month"])["length"].agg(["sum", "mean", "count"]).reset_index()

# Create a new column combining year and month in "YYYY-MM" format
# got help from AI Entry 6
monthly["date"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)

# Convert the "date" column into datetime format for better handling in graphs
monthly["date"] = pd.to_datetime(monthly["date"])

# Print the first few rows to check if it worked
print("Monthly summary preview:")
print(monthly.head())

# Total article length by year 
fig1 = px.bar(yearly, x="year", y="sum",
              title="Total Article Length by Year – Journalistic Focus",
              labels={"sum": "Total Words", "year": "Year"})
fig1.update_layout(yaxis_title="Total Words")
fig1.write_html("outputs/samrin-total-year.html")
print("Graph saved: samrin-total-year.html")


# Count articles per month
df["year_month"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2))
article_count_by_month = df["year_month"].value_counts().sort_index()
print("Number of articles published per month:")
print(article_count_by_month)

# Average article length by year 
fig2 = px.line(yearly, x="year", y="mean",
               title="Average Article Length by Year – Depth of Coverage",
               markers=True,
               labels={"mean": "Avg Words", "year": "Year"})
fig2.update_layout(yaxis_title="Average Words")
fig2.write_html("outputs/samrin-average-year.html")
print("Graph saved: samrin-average-year.html")


# Number of articles per month 
fig3 = px.line(monthly, x="date", y="count",
               title="Number of Articles Published per Month",
               markers=True,
               labels={"count": "Article Count", "date": "Month"})
fig3.update_layout(yaxis_title="Article Count")
fig3.write_html("outputs/samrin-article-count-month.html")
print("Graph saved: samrin-article-count-month.html")


# Total article length per month 
fig4 = px.line(monthly, x="date", y="sum",
               title="Monthly Total Article Length – Event-Driven Spikes",
               markers=True,
               labels={"sum": "Total Words", "date": "Month"})
fig4.update_layout(yaxis_title="Total Words")
fig4.write_html("outputs/samrin-total-month.html")
print("Graph saved: samrin-total-month.html")


# Average article length per month 
fig5 = px.line(monthly, x="date", y="mean",
               title="Monthly Average Article Length – Depth of Reporting",
               markers=True,
               labels={"mean": "Avg Words", "date": "Month"})
fig5.update_layout(yaxis_title="Average Words")
fig5.write_html("outputs/samrin-average-month.html")
print("Graph saved: samrin-average-month.html")


# Create year_month and length_type columns
df["year_month"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2))

def label_length(length):  # got help from AI Entry 2
    if length < 300:
        return "Short (<300)"
    elif length <= 800:
        return "Medium (300–800)"
    else:
        return "Long (>800)"

df["length_type"] = df["length"].apply(label_length)

# Group by month and length type
grouped = df.groupby(["year_month", "length_type"]).size().reset_index(name="count")

# Multi-line graph
fig6 = px.line(grouped, x="year_month", y="count", color="length_type",
              title="Monthly Trends of Article Length Types",
              labels={"count": "Number of Articles", "year_month": "Month", "length_type": "Length Type"},
              markers=True)
fig6.update_layout(xaxis_tickangle=45)
fig6.write_html("outputs/samrin-monthly-length-type-lines.html")
print("Graph saved: samrin-monthly-length-type-lines.html")

