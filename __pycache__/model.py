import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Parameter tuning done in modelAnalysis.ipynb
# Used f1 score as the evaluation metric

data = pd.read_csv('botData.csv')

train, test = train_test_split(data, test_size=0.25, random_state=1)

train_Y = train['isBot']
train_X = train.drop(columns = ['isBot', 'author'], axis = 1)

test_Y = test['isBot']
test_X = test.drop(columns = ['isBot', 'author'], axis = 1)

RF_model = RandomForestClassifier(bootstrap = True, oob_score = True,
                                  criterion = 'gini',
                                  max_depth = None,
                                  max_features=2,
                                  min_samples_leaf = 3,
                                  min_samples_split = 4,
                                  n_estimators = 1000,
                                  random_state=1)

RF_model.fit(train_X, train_Y)

pkl_filename = "RF_model_for_bot.pkl"
with open(pkl_filename, 'wb') as file:
 pickle.dump(RF_model, file)