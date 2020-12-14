from flask import Flask, request, render_template
import pickle
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode
import re
import nltk
import string

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

app = Flask(__name__)

#model = pickle.load(open('model.pkl','rb'))


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


def lemmatize(sentence):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(sentence)

    out = " ".join([lemmatizer.lemmatize(w) for w in words])

    return out


def get_top_tweets(message):
    status = "fail"
    responce = ""
    emoji = ""
    message = lemmatize(pre_process(remove_noise(message)))
    responce = ""#add model

    if responce is not '':
        status = "success"


    return status, responce


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    status = 'fail'
    prediction = ''

    if request.method == 'POST':
        text = request.form
        # if text['message_user'] == 'analyze_message' and text['message'] is not '':
        #     status, prediction, emojis = get_top_tweets(text['message'])
        #
        #     if status is 'success':
        #         return render_template('result.html',
        #                                analysis_responce="The top 20 similar tweets are {}".format(prediction))
        #     else:
        #         return render_template('index.html', error="We didn't succeed to analyze your text, please try again.")
        #
        # else:
        #     return render_template('index.html', error="We can't analyze empty text.")
        return render_template('result.html', analysis_responce=text['message_user'])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
