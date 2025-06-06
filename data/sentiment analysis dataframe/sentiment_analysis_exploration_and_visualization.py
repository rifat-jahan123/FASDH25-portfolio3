#Import libraries
import pandas as pd
import plotly.express as px


#Load the dataset
df = pd.read_csv("sentiment_analysis_dataframe.csv")

#Exploration

#show first few rows 
print(df.head())

#show basic information about the columns
print(df.describe())


#Making sure that the year column exists therefore we extract it from the filename
df["year"] = df ["filename"].str[:4]

#Group by year and then calculate the average sentiment polarity
average_polarity_by_year = df.groupby("year")["sentiment_polarity"].mean().reset_index()

#Visualize through a bar chart
fig1 = px.bar(average_polarity_by_year,
              x = "year",
              y = "sentiment_polarity",
              title = "Average Sentiment Polarity by Year",
              labels = {"sentiment_polarity": "Average Polarity"})

fig1.write_html ("average_sentiment_polarity_by_year.html")
fig1.show()


#Group by year and find the average subjectivity
average_subjectivity = df.groupby("year")["sentiment_subjectivity"].mean().reset_index()


#Make a line graoh to show the average subjectivity over time
fig2 = px.line(average_subjectivity,
               x = "year",
               y = "sentiment_subjectivity",
               title = "Average Subjectivity Over Time")

fig2.write_html("average_subjectivity_over_time.html")
fig2.show()


# Create a new column for sentiment type
sentiment_labels = []

#Loop through sentiment_polarity column
for polarity in df["sentiment_polarity"]:
    if polarity >= 0:
        sentiment_labels.append("Positive")  #Mark as positive if polarity is greater than or equal to 0
    else:
        sentiment_labels.append("Negative")  #Mark as negative if polarity is less than 0

#Add new list as a column to the DataFrame
df["sentiment_type"] = sentiment_labels



#Make a scatter plot to show how polarity and subjectivity are related
fig3 = px.scatter (df,
                   x= "sentiment_polarity",  #Polarity values
                   y = "sentiment_subjectivity",  #subjectivity values 
                   color = "sentiment_type",  #use color to distinguish sentiment type
                   hover_name = "filename",   #show filename on hover 
                   title = "Polarity vs Subjectivity",  
                   labels = {
                       "sentiment_polarity": "Sentiment Polarity",
                       "sentiment_subjectivity": "Sentiment Subjectivity"
                   },
                   color_discrete_map ={
                       "Positive": "lightblue",  #light blue for positive sentiments
                       "Negative": "tomato"   #tomato red for negative sentiments 
                   }
)

fig3.write_html("polarity_vs_subjectivity.html")
fig3.show()
               

#Sort by polairty to find the most positive and negative articles
print("Most Positive Articles:")
print(df.sort_values(by="sentiment_polarity", ascending=False).head(5))

print("Most Negative Articles:")
print(df.sort_values(by="sentiment_polarity", ascending=True).head(5))


