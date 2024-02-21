import pandas as pd
import matplotlib.pyplot as plt
import spacy
import random


nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])

csvfilepath = "Dataset_new/Mouthwash_new/Colgate_mw_1.csv"

df = pd.read_csv(csvfilepath)

print(df)

positive = ""
positive_count = 0
negative = ""
negative_count = 0
neutral_count = 0
adjective_list = []

for index, row in df.iterrows():
    if row['Sentiment_label'] == 'positive':
        positive_count += 1
        if positive_count <= 20:
            positive += str(row['Review_text'])
    elif row['Sentiment_label'] == 'negative':
        negative_count += 1
        if negative_count <= 20:
            negative += str(row['Review_text'])
    else:
        neutral_count += 1
    # adjective
    doc = nlp(str(row['Review_text']))
    for token in doc:
        if token.pos_ == "ADJ" and [token.text.lower(), row['Sentiment_label']] not in adjective_list:
            adjective_list.append([token.text.lower(), row['Sentiment_label']])


sentiment_score = (positive_count + neutral_count - negative_count) / (positive_count + negative_count + neutral_count)
positivity_rate = (positive_count + neutral_count) / (positive_count + negative_count + neutral_count)
number_of_reviews = df.shape[0]

display_adjectives = []
for i in range(7):
    choice = random.choice(adjective_list)
    if choice not in display_adjectives:
        display_adjectives.append(choice)
# print(display_adjectives)
        
labels=["Postive","Negative","Neutral"] 
sizes=[positive_count, negative_count, neutral_count]
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
