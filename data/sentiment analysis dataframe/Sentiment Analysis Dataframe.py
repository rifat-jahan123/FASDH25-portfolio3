#Import Libraries

import os

import pandas as pd

#Download the necessary language data for TextBlob to analyze text correctly
# It helps textblob break sentences into words and understand grammar

import nltk
nltk.download("punkt")

#Import TextBlob for sentiment analysis
from textblob import TextBlob


# Load the data
folder_path = "../articles"

#create empty lists to store data we extract from each article

filenames = []   # stores the name of each article file
texts = []     #stores the full text of each article
polarities = []      # stores sentiment polarity score (-1 to 1)
subjectivities = []    # stores sentiment subjectivity score (0 to 1)


# loop through every file in the folder

for filename in os.listdir(folder_path):

    #check if the file ends with ".txt" to ensure we only read text files
    if filename.endswith (".txt"):
        file_path = os.path.join(folder_path, filename)

        #Open the file in "read" mode with utf-8 encoding
        with open (file_path, "r", encoding = "utf-8") as f:

            # read the content of the file and store it as a string
            text = f.read()


            # create a textblob object from the text which lets us easily access sentiment features
            blob = TextBlob(text)


            #extract sentiment polarity: -1 is very negative, 0 is neutral and +1 is very positive
            polarity = blob.sentiment.polarity


            # Extract sentiment subjectivity: 0 is very factual, 1 is opinion based
            subjectivity = blob.sentiment.subjectivity


            # Now add these values to their respective lists
            filenames.append(filename)
            texts.append(text)
            polarities.append(polarity)
            subjectivities.append(subjectivity)


# Create a pandas DataFrame to organize all the data into a table
# Each row represents one article and its sentiment scores
df_sentiment = pd.DataFrame({
    "filename": filenames,
    "text": texts,
    "sentiment_polarity": polarities,
    "sentiment_subjectivity": subjectivities
})

#save the dataframe
df_sentiment.to_csv("sentiment_analysis_dataframe.csv", index= False)

print(df_sentiment.head())

        
