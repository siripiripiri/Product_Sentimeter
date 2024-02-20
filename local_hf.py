from transformers import pipeline

pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

res = pipe(
    '''
I must say after a long time got a good brush. The bristles are very soft on the gums and yet do the job well. The head is big enough to fit in all corners of the mouth covers the entire mouth properly. Great product
'''
)

print(res[0]['label'])