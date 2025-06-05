
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("length.csv")

# Preview the data
print("First few rows:")
print(df.head())

# Group by year
yearly = df.groupby("year")["length"].agg(["sum", "mean", "count"]).reset_index()
print("\nYearly summary (total, average, and count):")
print(yearly)

# Group by year and month 
monthly = df.groupby(["year", "month"])["length"].agg(["sum", "mean", "count"]).reset_index()

# Create "date" column for monthly timeline
monthly["date"] = pd.to_datetime(monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)) # I got help from chatgpt

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

# Faceted histogram of article lengths per month 
df["month"] = df["month"].astype(int)
fig6 = px.histogram(df, x="length", facet_col="month", facet_col_wrap=4, color="year",  # I got help from chatgpt
                    title="Faceted Histogram of Article Lengths by Month",
                    labels={"length": "Article Length", "month": "Month"})
fig6.update_layout(showlegend=False)
fig6.write_html("outputs/samrin-faceted-lengths.html")
fig6.show()

