# Importing required libraries such as pandas used to work with DataFrames
import pandas as pd

# importing plotly which is used to make interactive graphs 
import plotly.express as px


# Load the dataset 
df = pd.read_csv("../data/dataframes/topic-model/topic-model.csv")

#Exploration
#View first 5 articles in the dataframe
print("First 5 rows of the dataset:")
print(df.head())


#View all the column names in the dataset
print("\nColumn names in the dataset:")
print(df.columns)


#View the number of rows and columns in the dataset
print("\nShape of the dataset (rows, columns):")
print(df.shape)



# Create a new column called date from year, month and day columns 
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Count how many articles belong to each topic
# It counts how many times a topic appears, then sorts them by topic number and converts the result into a new table
topic_counts = df["Topic"].value_counts().sort_index().reset_index()


# Renames the columns of the table to Topic and Article count to make them clearer
topic_counts.columns = ["Topic", "Article Count"]

#Sort the table so that the topic with the most documents appear first
topic_counts = topic_counts.sort_values("Article Count", ascending=False)

# Create a bar chart to show that how many articles are present in each topic 
fig_topic_distribution = px.bar(
    topic_counts,
    x = "Topic",   # x-axis shows the topic number 
    y = "Article Count",   #y-axis shows how many articles are in each topic 
    title = "Article Count per Topic",  # This is the title of the graph 
    text_auto = True,  # This shows the numbers directly on the bars to make it easier
    height = 400   # It sets the height of the graph

)

fig_topic_distribution.write_html("article_count_per_topic.html")
fig_topic_distribution.show()  # Show the graph 


#filter out unassigned topics (Topic = -1)
# It keeps only those rows where a topic is assigned and creates a new copy of the filtered data
df = df[df["Topic"] != -1].copy()

# Remove Stop Words as they don't add much meaning
# Copied from NLTK website
stop_words = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

# Go through each of the 4 topic keyword columns in the DataFrame and remove stop words 
for col in ["topic_1", "topic_2", "topic_3", "topic_4"]:
    def remove_stop_words(word):
        if word in stop_words:  # it checks if the word is in stop words list 
            return ""   # if it's present it removes it 
        return word   # otherwise it keeps the word as it is

    # Applying the stop word removal function to every word in each of the topic columns
    
    df[col] = df[col].apply(remove_stop_words)
    

# Combine the 4 topic keywords into a single label per topic
# It adds all the words in the 4 separate columns into one column and names it Topic Label
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)


# Get the top 5 most common topics by the total number of articles they appear in
# It counts the articles for each topic and selects the 5 with the highest count
top_topics = df["Topic"].value_counts().nlargest(5).index

# Creates a new table that only includes rows from the 5 topics 
df_top_topics = df[df["Topic"].isin(top_topics)].copy()

#Find the Daily topic trends by counting the number of times articles are written per day for each topic label
daily_trend = df_top_topics.groupby(["date", "Topic_Label"]).size().reset_index(name="Article Count")

# Create a line chart to show how article counts changed on daily basis for each top topic
fig_daily_facet = px.line(
    daily_trend,
    x = "date",
    y = "Article Count",
    color = "Topic_Label",  # Different color for each topic
    facet_col = "Topic_Label",   # Separate chart for each topic
    facet_col_wrap = 2,    # Wrap the chart into 2 columns
    title = "Daily Topic Trend Over Time for Top 5 Topics"
)

fig_daily_facet.write_html("daily_topic_trend_over_time_for_top_5_topics.html")
fig_daily_facet.show()

# Create a column with year and month to help while we group them as month later
# It converts the year and month to strings, adds a dash and makes sure that month is of two digits
df["year_month"] = df ["year"].astype(str) + "-" + df ["month"].astype(str).str.zfill(2)

# Filters the data to only include rows with the top 5 topics
df_monthly_top = df[df["Topic"].isin(top_topics)].copy()

# Counts how many articles exist of each topic label for each year and month 
monthly_trend = df_monthly_top.groupby(["year_month", "Topic_Label"]).size().reset_index(name="Article Count")


# Make a bar graph to show topic trends by month
fig_monthly = px.bar(
    monthly_trend,
    x ="year_month",
    y = "Article Count",
    color = "Topic_Label",
    barmode = "group",    # Bars are grouped side by side for each topic per month
    facet_col = "Topic_Label",
    facet_col_wrap = 2,
    title = "Monthly Topic Trends for Top 5 Topics",
    text_auto = True,
    height = 600
)

fig_monthly.update_layout(xaxis_tickangle=45) # Rotates the x-axis labels to make them easier to read
fig_monthly.write_html("monthly_topic_trends_for_top_5_topics.html")
fig_monthly.show()


# Finding the most used words per topic
# This selects the five columns, Topic label - the human readable name and the four topic columns associated with the articles 
# It uses melt function so that each has only one keyword and the topic label is repeated for each word

keyword_df = df[["Topic_Label", "topic_1", "topic_2", "topic_3", "topic_4"]].melt(
    id_vars="Topic_Label",  # Keeps the topic label the same
    value_name="Keyword"   # creates one column for all keywords from the four keyword columns
)


# Count how often each keyword appears in each topic
# Groups both topic and keywords and counts how many times each keyword appears 
top_words_by_topic = keyword_df.groupby(["Topic_Label", "Keyword"]).size().reset_index(name='Frequency')

# Sorts keywords by topic and within each topic in order of how frequent they are
top_words_by_topic = top_words_by_topic.sort_values(["Topic_Label", "Frequency"], ascending=[True, False])

# Get top 5 most used keyword for each topic

# Create an empty list 
top_keywords_list = []

# Go through each unique label one by one 
for topic in top_words_by_topic["Topic_Label"].unique():

    #From the sorted data above take the top 5 keywords for the particular topic
    top5 = top_words_by_topic[top_words_by_topic["Topic_Label"] == topic].head(5)

    #Add these top 5 rows to the list 
    top_keywords_list.append(top5)


# Combine the top 5 keywords from all the topics into a single table 
top5_keywords_df = pd.concat(top_keywords_list)


# Limit to top 5 topics for visualization

# Get a list of Topic Label names that are part of the most discussed topics 
top_topic_labels = df[df["Topic"].isin(top_topics)]["Topic_Label"].unique()

# Filter the top 5 keyowrd data to keep only keywords from those top topics 
filtered_keywords_df = top5_keywords_df[top5_keywords_df["Topic_Label"].isin(top_topic_labels)]

# Create a horizontal bar chart for top 5 keywords for each top topic 
fig_top_words = px.bar(
    filtered_keywords_df,  # Uses the filtered keyword data
    x="Frequency",      # shows how often the keywords appear 
    y="Keyword",
    color="Keyword",
    facet_col="Topic_Label",
    facet_col_wrap=2,   # arrange small charts into rows of two
    orientation="h",    # make the bars horizontal 
    height=800,         
    title="Top 5 Keywords per Topic (Horizontal View)"
)
fig_top_words.write_html("top_5_keywords_per_topic.html")
fig_top_words.show()


# Calculate the average word count per article for each topic

# Group the data by topic and calculate the average number of words used in articles under each topic
average_count = df.groupby("Topic_Label")["Count"].mean().reset_index(name="Average_Word_Count")

# Create a bar graph showing average word count per topic
fig_average_count = px.bar(
    average_count,          # Use the table with average word counts
    x="Topic_Label",
    y="Average_Word_Count",
    title="Average Word Count per Topic",
    text_auto = True,
    height = 600
)
fig_average_count.write_html("average_word_count_per_topic.html")
fig_average_count.show()


# Count the number of articles written per topic each year 
# Group the DataFrame by Topic_Label and year and count the number of articles in each group
# and rename it to get a new DataFramae with a column called "Article Count"
grouped = df.groupby(["Topic_Label", "year"]).size().reset_index(name="Article_Count")

# Find the top 10 topics that have the highest total article counts across all years
top_ten_topics = grouped.groupby("Topic_Label")["Article_Count"].sum().nlargest(10).index

# Filter the DataFrame to get the toop 10 topics only 
grouped = grouped[grouped["Topic_Label"].isin(top_ten_topics)]


#Create the Bar chart 
fig = px.bar(
    grouped,
    x='year',
    y='Article_Count',
    color='Topic_Label',
    barmode='group',
    title='Article Counts by Topic and Year',
    labels={'Topic_Label': 'Topic', 'Article_Count': 'Number of Articles', 'year': 'Year'},
    text_auto = True,
    height = 500
)
fig.write_html("article_counts_by_topic_and_year.html")
fig.show()

# Count how many times war is mentioned in the article titles 

# Filter the dataset to only keep the articles that beling to the top 10 topics 
filtered_df = df[df["Topic_Label"].isin(top_ten_topics)].copy()

# Check if the word war appears in each article title
war_occurrences = filtered_df ["title"].str.contains("war", case =False, na=False)

# Convert the True or False result into 1 (war mentioned) or 0 (not mentioned) and add a new column
filtered_df["war_mention"] = war_occurrences.astype(int)

# Group by year and sum the war_mention column to count how many articles mentioned war each year
war_counts_per_year = filtered_df.groupby("year")["war_mention"].sum().reset_index()

# Sort the results by year so the line chart appear in the right order 
war_counts_per_year = war_counts_per_year.sort_values("year")

# Create line chart
fig_war_trend = px.line(
    war_counts_per_year,
    x="year",
    y="war_mention",
    markers=True,
    title="Number of Articles Mentioning 'War' by Year (Top Topics)",
    labels={"war_mention": "Count of 'war' mentions", "year": "Year"}
)

# update x-axis to show every single year 
fig_war_trend.update_layout(xaxis=dict(dtick=1))
fig_war_trend.write_html("number_of_articles_mentioning_war_by_year.html")
fig_war_trend.show()
