import praw
import config
import logging
import os
from sklearn.ensemble import RandomForestClassifier
from metrics import metrics
import pickle

# TODO: store comments that were replied to in SQLITE db instead of text file

class bot:

    def __init__(self):
        pass


    def botLogin(self):
        try:
            r = praw.Reddit(username = config.username,
                            password = config.password,
                            client_id = config.client_id,
                            client_secret = config.client_secret,
                            user_agent = "some_bot_checker test bot v1.0")
        except:
            logging.error('Login Failed')

        return r

    #Outputs probability that a user is a bot
    def __makePrediction(self, data):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        try:
            with open("RF_model_for_bot.pkl", 'rb') as file:
                model = pickle.load(file)
                return model.predict_proba(data)
        except:
            logging.error('No .pkl file found')


    def runBot(self, r):
        logging.info('Running...')

        for mention in r.inbox.mentions(limit = 25):
            logging.info('Comment found')
            logging.info('Comment.id is: ' + mention.id)

            met = metrics()

            parentAuth = mention.parent().author
            authData = met.getAuthorData(r, parentAuth)

            botProbability = str(self.__makePrediction(met.aggregateMetrics(authData))[:, 1])

            botProbability = botProbability.replace('[', '')
            botProbability = botProbability.replace(']', '')
            mention.reply("User " + str(parentAuth) +
                          " is a bot with a probability of " +
                          str(botProbability) + "0%")


redditBot = bot()
r = redditBot.botLogin()
redditBot.runBot(r)
