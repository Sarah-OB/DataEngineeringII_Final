# Required libraries

#pip install unidecode
#pip install gensim
#pip install nltk==3.4

# Importing libraries

import pandas as pd
import nltk
import re
import pickle
# from nltk.tokenize import RegexpTokenize
from nltk.tokenize import TweetTokenizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
import string
import gensim
from gensim.models import Word2Vec
from nltk.tokenize import RegexpTokenizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Load data

df = pd.read_csv('tweets.csv')


# Preprocessing

# Removing noise
def remove_noise(a):
    if "pic" in a:
        a = a[:-26]
    a = re.sub(r'(\s)#\w+', r'\1', a)
    tokenizer = RegexpTokenizer(r'\w+')
    a = tokenizer.tokenize(a)
    a = " ".join(str(x) for x in a)
    a = re.sub('[0-9]+', '', a)

    return a


# Stop words and tokenization
def pre_process(corpus):
    # convert input corpus to lower case.
    corpus = corpus.lower()
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens.
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    # remove non-ascii characters
    corpus = unidecode(corpus)
    return corpus


# Lemmatization
from nltk.stem import WordNetLemmatizer


def lemmatize(sentence):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(sentence)

    out = " ".join([lemmatizer.lemmatize(w) for w in words])

    return (out)


df['text_proced'] = df['text'].apply(remove_noise)
df['text_proced'] = df['text_proced'].apply(pre_process)
df['text_proced'] = df['text_proced'].apply(lemmatize)

# Transfer learning : updation the model from GoogleNews

tokenizer = RegexpTokenizer(r'\w+')
sentences = [tokenizer.tokenize(df['text_proced'][i]) for i in range(len(df['text_proced']))]
# size option needs to be set to 300 to be the same as Google's pre-trained model
model = Word2Vec(size=300, window=5,
                 min_count=1, workers=2)
model.build_vocab(sentences)
# assign the vectors to the vocabs that are in Google's pre-trained model and your sentences defined above.
# lockf needs to be set to 1.0 to allow continued training.
model.intersect_word2vec_format('GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)
# continue training with you own data
model.train(sentences, total_examples=3, epochs=5)

# Top 20 tweets

text = " time for a Royal Celebration!"
text = lemmatize(pre_process(remove_noise(text)))
i = 0
data = pd.DataFrame([], columns=['tweet_index', "similarity_score"])
while i < len(df['text_proced']):
    a = {"tweet_index": i,
         "similarity_score": model.wv.n_similarity(text.lower().split(), df['text_proced'][i].lower().split())}
    data = data.append(a, ignore_index=True)
    i = i + 1
    top_20 = data.nlargest(20, ['similarity_score'])

print(" In order, this tweet is similar ")
for i in top_20['tweet_index']:
    print("at " + "{:.0%}".format(top_20["similarity_score"][i]) + " to the tweet of " + df.loc[
        i, "author"] + " posted the " + df.loc[i, "date"] + " And the text is " + df.loc[i, "text"])

#Serialize the model
pickle.dump(model, open('model.pkl', 'wb'))
analysis_model = pickle.load(open('model.pkl','rb'))
