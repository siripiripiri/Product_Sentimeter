import spacy
from transformers import pipeline
pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

nlp = spacy.load("en_core_web_sm")

def extract_aspect_sentiment_triplets(review_text):
    doc = nlp(review_text)
    aspect_sentiment_triplets = []
    for sentence in doc.sents:
        for token in sentence:
            if token.pos_ == 'NOUN':  # Consider only nouns as potential aspects
                aspect = token.text
                aspect_span = sentence.text
                # sentiment = analyze_sentiment(aspect_span)  # Analyze sentiment of the aspect span
                aspect_sentiment_triplets.append((aspect, aspect_span,""))
    return aspect_sentiment_triplets


aspect_freq = {}

csvfilepath = "Dataset_new/Mouthwash_new/Colgate_mw_1.csv"
with open(csvfilepath, "r") as csvfile:
    for line in csvfile:
        line = line.split(',')[-1]

        senti = extract_aspect_sentiment_triplets(line)
        for aspect_triplet in senti:
            # print("Aspect:", aspect_triplet[0])
            # print("Aspect Span:", aspect_triplet[1])
            # print("Sentiment:", aspect_triplet[2])
            # print()
            try:
                output = pipe(aspect_triplet[1])
                senti_label = output[0]['label']


                if aspect_triplet[0] not in aspect_freq:
                    aspect_freq[aspect_triplet[0]] = [1, 0, 0]
                else:
                    aspect_freq[aspect_triplet[0]][0] += 1
                    
                if senti_label == 'positive':
                    aspect_freq[aspect_triplet[0]][1] += 1
                elif senti_label == 'negative':
                    aspect_freq[aspect_triplet[0]][2] += 1
            except:
                pass


print(aspect_freq)
