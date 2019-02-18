import pandas as pd
import praw
import numpy as np
import gc
#import nltk


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from statistics import median

# Metrics class which is used to evaluate whether a user is a bot

class metrics:

    def __init__(self):
        pass


    def getAuthorData(self, r, author):
        user = praw.models.Redditor(r, name = str(author))
        author_df = pd.DataFrame(columns = ['author', 'body', 'created_utc', 'parent_created_utc', 'isRoot'])
        comments = user.comments.new(limit=50)
        for comment in comments:
            author_df = author_df.append({'author':comment.author,
                                          'body':comment.body,
                                          'created_utc':comment.created_utc,
                                          'parent_created_utc':comment.parent().created_utc,
                                          'isRoot': comment.is_root,
                                          }, ignore_index=True)
        author_df = self.__cleanText(author_df)
        return author_df


    def __getAuthorText(self, data):
        return data['body'].tolist()


    def __cleanText(self, data):
        data['body'] = data['body'].str.lower()
        data['body'] = data['body'].str.replace('.', ' ')
        data['body'] = data['body'].str.replace('/', ' ')
        data['body'] = data['body'].str.replace(':', ' ')
        data['body'] = data['body'].str.replace('-', ' ')
        data['body'] = data['body'].str.replace('_', ' ')
        return data


    def __getCommentDiff(self, data):
        return data['created_utc']-data['parent_created_utc']


    def avgTFIDFCosineSimilarity(self, data):
        data = self.__cleanText(data)
        text = self.__getAuthorText(data)
        text = filter(None, text)

        vectorizer = TfidfVectorizer(stop_words=None, strip_accents='ascii')
        v = vectorizer.fit_transform(text)
        avgCosSimilarity = cosine_similarity(v).mean()

        return avgCosSimilarity


    def avgCountCosineSimilarity(self, data):
        data = self.__cleanText(data)
        text = self.__getAuthorText(data)
        text = filter(None, text)

        vectorizer = CountVectorizer(stop_words=None, strip_accents='ascii')
        v = vectorizer.fit_transform(text)
        avgCosSimilarity = cosine_similarity(v).mean()

        return avgCosSimilarity


    def avgCommentRate(self, data):
        numComments = data['created_utc'].count()
        delta = (data['created_utc'].max() - data['created_utc'].min())
        return numComments/delta


    def topLevelProportion(self, data):
        return data['isRoot'].sum()/data['isRoot'].count()


    #getting parent comments takes a very long time
    def getMedianReplyTime(self, data):
        diff = self.__getCommentDiff(data)
        avgReplyTime = median(diff)
        return avgReplyTime


    def aggregateMetrics(self, data):
        metrics_df = pd.DataFrame(columns=['count_similarity', 'tfidf_similarity', 'comment_rate', 'top_level_proportion'])

        metrics_df = metrics_df.append({'count_similarity': self.avgCountCosineSimilarity(data),
                                        'tfidf_similarity': self.avgTFIDFCosineSimilarity(data),
                                        'comment_rate': self.avgCommentRate(data),
                                        'top_level_proportion': self.topLevelProportion(data),
                                        'reply_time': self.getMedianReplyTime(data)}, ignore_index=True)
        return metrics_df

