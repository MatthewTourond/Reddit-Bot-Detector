import praw
import config
import logging
import time
import os
from metrics import metrics


def botLogin():
    try:
        r = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = "some_bot_checker test bot v0.1")
    except:
        logging.error('Login Failed')

    return r


def runBot(r, commentsRepliedTo):

    commentsRepliedTo = []

    for comment in r.subreddit('test').comments(limit=25):
        if "!isBot" in comment.body and comment.id not in commentsRepliedTo:
            logging.info('Comment found')
            logging.info('Comment.id is: ' + comment.id)

            met = metrics()
            authHist = met.getCommentHistory(r, comment.parent().author)
            authText = met.getAuthorText(authHist)
            comment.reply("similarity score: " + str(met.getAvgCosineSimilarity(authText)))
            #comment.reply("avg reply time: " + str(met.getAvgReplyTime(authHist['body'].tolist()) + "seconds"))

            commentsRepliedTo.append(comment.id)
            with open("commentsRepliedTo.txt", "a") as f:
                f.write(comment.id + "\n")

    time.sleep(20)

def getSavedComments():
    #windows os makes me :(
    os.chdir('c:\\Users\\matt\\Desktop')

    if not os.path.isfile('commentsRepliedTo.txt'):
        commentsRepliedTo = []
        return commentsRepliedTo

    with open("commentsRepliedTo.txt", "r") as f:
        commentsRepliedTo = f.read()
        commentsRepliedTo = commentsRepliedTo.split("\n")
        commentsRepliedTo = filter(None, commentsRepliedTo)
        return commentsRepliedTo


commentsRepliedTo = getSavedComments()
r = botLogin()
runBot(r, commentsRepliedTo)
