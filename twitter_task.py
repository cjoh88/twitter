from celery import Celery
import os
import re
import json
import urllib2

app = Celery('twitter_task', backend='amqp', broker='amqp://')



def count_word(word, input_string):
    count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), input_string))
    return count

def count(input_string):
    result = dict()
    for word in WORDS:
        data = json.loads(input_string)
        result[word] = count_word(word, data['text'])
    return result

@app.task
def twitter(file_name, words):
    result = dict()
    for word in words:
        result[word] = 0
    #conn = swiftclient.client.Connection(auth_version=2, **config)
    #tweets = conn.get_object(CONTAINER, filename)
    #conn.close()
    #f = open(file_name, 'r')
    f = urllib2.urlopen('http://smog.uppmax.uu.se:8080/swift/v1/tweets/' + file_name)
    for line in f:
        for word in words:
            result[word] += count_word(word, line)
    f.close()
    return result
