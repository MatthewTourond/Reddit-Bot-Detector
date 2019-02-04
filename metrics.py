import pandas as pd
import praw
import numpy as np
import gc
import nltk
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class metrics:
    def __init__(self):
        pass




    def getCommentHistory(self, r, author):
        user = praw.models.Redditor(r, name = str(author))
        author_df = pd.DataFrame(columns = ['author', 'body', 'created_utc', 'parent_created_utc'])

        for comment in user.comments.new(limit=40):
            author_df = author_df.append({'author':comment.author,
                                          'body':comment.body,
                                          'created_utc':comment.created_utc,
                                          'parent_created_utc':comment.parent().created_utc},
                                         ignore_index=True)

        return author_df




    def getAvgCosineSimilarity(self, comment_df):
        vectorizer = CountVectorizer(strip_accents='unicode')
        X = vectorizer.fit_transform(comment_df['body'])
        avgCosSimilarity = cosine_similarity(X).mean()
        return avgCosSimilarity




    def getAvgReplyTime(self, comment_df):
        comment_df['delta'] = comment_df['created_utc'] - comment_df['parent_created_utc']
        avgReplyTime = comment_df['delta'].mean()
        return avgReplyTime


    #More metrics to be implemented