import pandas as pd

csvfilepath = "Dataset_new/Mouthwash_new/Colgate_mw_1.csv"

df = pd.read_csv(csvfilepath)

print(df)

positive = ""
positive_count = 0
negative = ""
negative_count = 0
neutral_count = 0

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

print(positive_count, negative_count, neutral_count)

print((positive_count + neutral_count - negative_count) / (positive_count + negative_count + neutral_count))


