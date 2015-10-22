from flask import Flask
from celery import group
from twitter_task import twitter
import time

web_app = Flask(__name__)

WORDS = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']

TWEETS = dict()

def dict_add(a, b):
    for i in WORDS:
        a[i] += b[i]

def main():
    for word in WORDS:
        TWEETS[word] = 0;
    job = group(twitter.subtask(('tweets_' + str(i) + '.txt', WORDS)) for i in range(0,1))

    result = job.apply_async()
    time.sleep(30)
    while not result.ready():
        time.sleep(5)
    counts = result.join()
    for c in counts:
        dict_add(TWEETS, c)

    web_app.run(host='0.0.0.0',debug=True)

@web_app.route('/')
def index():
    #tweets = twitter('tweets_19.txt', WORDS)
    results = '<!DOCTYPE html><html><h1>Results</h1><table>'
    #print(tweets)
    for word in WORDS:
        results += '<tr><td>' + word + '</td><td>' + str(TWEETS[word]) + '</td></tr>'
    #for key, value in tweets:
    #    results += key + ' : ' + value
    #print(results)
    results += '</table></html>'
    return results

if __name__ == '__main__':
    main()
    #web_app.run(host='0.0.0.0',debug=True)
