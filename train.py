import pandas as pd
from metrics import metrics
import praw
import logging
import config


def Login():
    try:
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = "some_bot_checker test bot v0.1")
    except:
        logging.error('Login Failed')

    return r



training_df = pd.DataFrame(columns = ['author', 'similarity', 'replyTime', 'commentRate'])
r = Login()
authors = pd.read_csv('sampleAuthors.csv')
authors = authors['author'].tolist()
met = metrics()

for auth in authors:
    print(auth)
    user = r.redditor(auth)
    try:
        authData = met.getAuthorData(r, user)
        training_df = training_df.append({'author': auth,
                                          'similarity': met.getAvgCosineSimilarity(authData),
                                          'replyTime': met.getMedianReplyTime(),
                                          'commentRate': met.getAvgCommentRate(authData)}, ignore_index=True)
    except:
        logging.error('404 HTTP response')

training_df.to_csv('test', index=False)