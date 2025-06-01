import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("length.csv")

# Preview the data
print("First rows of the dataset:")
print(df.head())

# Group by year
yearly = df.groupby("year")["length"].agg(["sum", "mean"]).reset_index()
print("\nTotal and Average Article Length by Year:")
print(yearly)

# Group by year and month
monthly = df.groupby(["year", "month"])["length"].agg(["sum", "mean"]).reset_index()

# Add a new column "date" for monthly timeline
monthly["date"] = pd.to_datetime(monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2))


# 1. Total article length per year
fig1 = px.bar(yearly, x="year", y="sum",
              title="Total Article Length by Year – Reflecting Journalistic Focus",
              labels={"sum": "Total Words Published", "year": "Year"})
fig1.update_layout(yaxis_title="Total Words")
fig1.write_html("outputs/samrin-total-year.html")
fig1.show()


# 2. Average article length per year
fig2 = px.line(yearly, x="year", y="mean",
               title="Average Article Length by Year – Complexity of Coverage",
               markers=True,
               labels={"mean": "Average Words per Article", "year": "Year"})
fig2.update_layout(yaxis_title="Average Length (words)")
fig2.write_html("outputs/samrin-average-year.html")
fig2.show()


# 3. Total article length by month (timeline)
fig3 = px.line(monthly, x="date", y="sum",
               title="Monthly Total Article Length – Peaks in Conflict or Crisis",
               markers=True,
               labels={"sum": "Total Words", "date": "Month"})
fig3.update_layout(yaxis_title="Total Words per Month")
fig3.write_html("outputs/samrin-total-month.html")
fig3.show()


# 4. Average article length by month (timeline)
fig4 = px.line(monthly, x="date", y="mean",
               title="Monthly Average Article Length – Depth of Individual Reports",
               markers=True,
               labels={"mean": "Avg. Words per Article", "date": "Month"})
fig4.update_layout(yaxis_title="Average Words per Article")
fig4.write_html("outputs/samrin-average-month.html")
fig4.show()


