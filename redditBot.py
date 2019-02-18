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
                print(data)
                model = pickle.load(file)
                print("loaded")
                return model.predict_proba(data)
        except:
            logging.error('No .pkl file found')

    #
    def runBot(self, r):
        logging.info('Running...')
        commentsRepliedTo = []

        for mention in r.inbox.mentions(limit = 25):
            print('stuff')
            logging.info('Comment found')
            logging.info('Comment.id is: ' + mention.id)

            met = metrics()

            parentAuth = mention.parent().author
            authData = met.getAuthorData(r, parentAuth)

            botProbability = str(self.__makePrediction(met.aggregateMetrics(authData))[:, 1])
            botProbability = botProbability[1:-5]

            mention.reply("User " + str(parentAuth) +
                          " is a bot with a probability of " +
                          str(botProbability) + "%")

            commentsRepliedTo.append(mention.id)
            with open("commentsRepliedTo.txt", "a") as f:
                f.write(mention.id + "\n")


def getSavedComments():
    if not os.path.isfile("commentsRepliedTo.txt"):
        commentsRepliedTo = []
    with open("commentsRepliedTo.txt", "r") as f:
        commentsRepliedTo = f.read()
        commentsRepliedTo = commentsRepliedTo.split("\n")
        commentsRepliedTo = filter(None, commentsRepliedTo)
        return commentsRepliedTo

commentsRepliedTo = getSavedComments()

redditBot = bot()
r = redditBot.botLogin()
redditBot.runBot(r)
