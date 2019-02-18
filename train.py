import pandas as pd
from metrics import metrics
import praw
import logging
import config


# Training script for the bot. Gets prediction metrics for every user in a .csv that are
# fed into a classifier

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



training_df = pd.DataFrame(columns = ['author', 'count_similarity', 'tfidf_similarity', 'comment_rate', 'top_level_proportion'])
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
                                          'count_similarity': met.avgCountCosineSimilarity(authData),
                                          'tfidf_similarity': met.avgTFIDFCosineSimilarity(authData),
                                          'comment_rate': met.avgCommentRate(authData),
                                          'top_level_proportion': met.topLevelProportion(authData),
                                          'reply_time': met.getMedianReplyTime(authData)}, ignore_index=True)
    except:
        logging.error('Deleted Account')

training_df.to_csv('test.csv', index=False)
