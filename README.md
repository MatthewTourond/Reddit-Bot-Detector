# Reddit-Bot-Detector

Reddit bot that detects if a user is a bot based on their comment history. Returns a percent probability that a user is bot. Called by mentioning /u/some_bot_checker.

metrics.py contains the key metrics that are used to determine if a user is a bot. These include how similar the user's posts are, measured by cosine similairty, how frequently they post, their median reply time, and whether they primiarly reply at the "top" of a comment chain or reply to users.

The .ipynb files contain the analysis of the models and metrics
