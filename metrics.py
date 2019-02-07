import pandas as pd
import praw
import numpy as np
import gc
#import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from statistics import median

class metrics:

    def __init__(self):
        pass


    def getAuthorData(self, r, author):
        user = praw.models.Redditor(r, name = str(author))
        author_df = pd.DataFrame(columns = ['author', 'body', 'created_utc', 'parent_created_utc'])
        for comment in user.comments.new(limit=50):
            author_df = author_df.append({'author':comment.author,
                                          'body':comment.body,
                                          'parent_created_utc': comment.parent().created_utc,
                                          'created_utc':comment.created_utc}, ignore_index=True)
        author_df = self.__cleanText(author_df)
        return author_df


    def __getAuthorText(self, data):
        return data['body'].tolist()


    def __getCommentTimestamps(self, data, parent):
        if parent:
            return data['parent_created_utc'].tolist()
        else:
            return data['created_utc'].tolist()


    def __cleanText(self, data):
        data['body'] = data['body'].str.lower()
        data['body'] = data['body'].str.replace('\.', ' ')
        data['body'] = data['body'].str.replace('\/', ' ')
        data['body'] = data['body'].str.replace(':', ' ')
        data['body'] = data['body'].str.replace('-', ' ')
        return data


    def getAvgCosineSimilarity(self, data):
        data = self.__cleanText(data)
        text = self.__getAuthorText(data)
        text = filter(None, text)

        vectorizer = CountVectorizer(stop_words=None, strip_accents='ascii')
        v = vectorizer.fit_transform(text)
        avgCosSimilarity = cosine_similarity(v).mean()

        return avgCosSimilarity


    def getAvgCommentRate(self, data):
        numComments = data['created_utc'].count()
        delta = (data['created_utc'].max() - data['created_utc'].min())
        return numComments/delta


    def getMedianReplyTime(self, data):
        t1 = self.__getCommentTimestamps(data, 0)
        t2 = self.__getCommentTimestamps(data, 1)
        avgReplyTime = median(abs(x-y) for x, y in zip(t1, t2))
        return avgReplyTime






