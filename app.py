from flask import Flask, request, render_template
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode
import pandas as pd
import pickle
import re
import nltk
import string
import time
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram

REQUESTS = Counter('app_requests', 'How many times the application has been accessed')
SEARCH = Counter('app_search', 'How many search have been made')

INPROGRESS = Gauge('app_progress', 'In progress requests')
LAST = Gauge('app_last', 'Last application access')

LATENCY = Summary('app_latency', 'Time needed for a request')
LATENCY_HIS = Histogram('appl_hist_latency', 'Time needed for a request')

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

app = Flask(__name__)

model = pickle.load(open('model.pkl','rb'))


def remove_noise(a):
    if "pic" in a:
        a = a[:-26]
    a = re.sub(r'(\s)#\w+', r'\1', a)
    tokenizer = RegexpTokenizer(r'\w+')
    a = tokenizer.tokenize(a)
    a = " ".join(str(x) for x in a)
    a = re.sub('[0-9]+', '', a)

    return a


def pre_process(corpus):
    corpus = corpus.lower()
    stopset = stopwords.words('english') + list(string.punctuation)
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    corpus = unidecode(corpus)
    return corpus


def lemmatize(sentence):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(sentence)
    out = " ".join([lemmatizer.lemmatize(w) for w in words])
    return out


def get_similar(tweets,message):
    i = 0
    data = pd.DataFrame([], columns=['tweet_index', "similarity_score"])
    while i < len(tweets['text_proced']):
        a = {"tweet_index": i,
             "similarity_score": model.wv.n_similarity(message.lower().split(), tweets['text_proced'][i].lower().split())}
        data = data.append(a, ignore_index=True)
        i = i + 1
        top_20 = data.nlargest(20, ['similarity_score'])

    return top_20


def get_top_tweets(message):
    status = "fail"
    message = lemmatize(pre_process(remove_noise(message)))
    responce = []
    df = pd.read_csv('tweets_processed.csv')
    top_20 = get_similar(df, message)

    for i in top_20['tweet_index']:
        responce.append(df.loc[i, "text"])

    if responce is not '':
        status = "success"
    INPROGRESS.dec()
    return status, responce


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    status = 'fail'
    prediction = ''
    LAST.set(time.time())
    REQUESTS.inc()

    if request.method == 'POST':
        text = request.form

        start = time.time()
        if text['message_user'] is not '':
            INPROGRESS.inc()
            status, prediction = get_top_tweets(text['message_user'])

            if status is 'success':
                SEARCH.inc()
                LATENCY.observe(time.time() - start)
                LATENCY_HIS.observe(time.time() - start)
                return render_template('result.html',
                                       analysis_responce=prediction, message=text['message_user'])
            else:
                return render_template('index.html', error="We didn't succeed to analyze your text, please try again.")

        else:
            return render_template('index.html', error="We can't analyze empty text.")

    else:
        return render_template("index.html")


if __name__ == '__main__':
    start_http_server(8010)
    app.debug = True
    app.run(host='0.0.0.0')
