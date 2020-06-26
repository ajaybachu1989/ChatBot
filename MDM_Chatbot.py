 #This is a basic chatbot which can be used to interact with a file and answer simple queries
#Author: Avik Mukherjee
#Date: October 2019
#Version: 1.0
#------------------------------------------------------------------------------------------
#Change History:
#January 2020 - Added server side functionality through Flask
#May 2020 - Hardcoded values to workaround tfidf anomalies temporarily
#------------------------------------------------------------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string
import os
import requests
import random
#from os import getcwd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def sessions():
    return render_template('homepage.html')

@app.route("/get")
def response():
    #url = "https://raw.github.com/getavik/My-SourceFiles/master/Metric%20Definition%20List%20Text.txt"
    url = "https://raw.githubusercontent.com/bijayinidash/chatbot/master/TextCustomer"
    response = requests.get(url,verify = False)
# =============================================================================
#     directory = getcwd()
#     filename = directory + '\\Metric Definition List Text.txt'
#     f = open(filename,'w')
# =============================================================================
    raw = response.text
    raw=raw.lower()# converts to lowercase
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find(os.path.join('corpora', 'wordnet'))
    except LookupError:
        nltk.download('punkt')
        nltk.download('wordnet')  
    sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
    #word_tokens = nltk.word_tokenize(raw)# converts to list of words
    lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    GREETING_INPUTS = ("hello", "hello!", "hi", "hi!", "greetings", "greetings!", "sup","hey")
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "how can I help you today?"]

    def greeting(sentence):
        #return chatbot.get_response(sentence)
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)
        
    flag=True
    while(flag==True):
        user_response=request.args.get('msg')
        user_response=user_response.lower()
        robo_response=''
        user_response=user_response.strip()
        sent_tokens.append(user_response)
        #return(str(sent_tokens))
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        #sdf = pd.SparseDataFrame(tfidf)
        #return(str(tfidf[-1]))
        vals = cosine_similarity(tfidf[-1], tfidf)
        #return(str(vals))
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        sent_tokens.remove(user_response)

        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='ok thanks' or user_response=='thank you'):
                flag=False
                robo_response="You are welcome!"
                return str(robo_response)
            else:
                if(greeting(user_response)!=None):
                    return str(greeting(user_response))
                else:
                    if(req_tfidf==0):
                        robo_response=robo_response+"I am sorry! I didn't understand you"
                        return str(robo_response)
                    else:
                        if(user_response=='person' or user_response=='total person'):
                            robo_response = robo_response+"Total Person 654"
                            return str(robo_response)
                        else:
                            if(user_response=='organization' or user_response=='total organization'):
                                robo_response = robo_response+"Total Organizations 68"
                                return str(robo_response)
                            else:
                                if(user_response=='customer compliance'):
                                    robo_response = robo_response+"Customer Compliance is the term for the action taken to ensure a benefit customer gives the correct information and reports all relevant changes at the right time during the life of the benefit claim"
                                    return str(robo_response)
                                else:
                                    if(user_response=='PII' or user_response=='personal data'):
                                        robo_response = robo_response+"Personal data, also known as personal information or personally identifiable information is any information relating to an identifiable person" 
                                        return str(robo_response)
                                    else:
                                        if(user_response=='tax' or user_response=='tax number'):
                                            robo_response = robo_response+"Tax number should be unique" 
                                            return str(robo_response)
                                        else:
                                            robo_response = robo_response+sent_tokens[idx]
                                            return str(robo_response)
        else:
            flag=False
            return str("Bye! take care...")
    
if __name__ == '__main__':
    app.run()
