import praw
import random
import re
from praw.models import Comment

reddit = praw.Reddit('bot1')

# List of words NoodleBot will look for
KEYWORDS_IN_TITLE = ['noodle', 'ramen', 'spaghetti', 'orzo', 'ravioli', 'linguine', 'macaroni',
                     'fettuccine', 'penne', 'ziti', 'lasagna', "mac and cheese", 'rigatoni', 'pasta']

# List to store post id's
POSTS_ALREADY_RESPONDED_TO = []

# List to store author names
AUTHORS_RESPONDED_TO = []


# Function that reads lines from a text file and returns a random line's string
def bot_responses(text_file):
    with open(text_file) as f:
        lines = f.readlines()
        return random.choice(lines)


# Function that will search posts on a given subreddit for keywords within the title and respond with a catchphrase
def post_search(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.new(limit=10):
        for j in KEYWORDS_IN_TITLE:
            if submission.id in POSTS_ALREADY_RESPONDED_TO:
                break
            if re.search(j, submission.title, re.IGNORECASE):
                submission.reply(bot_responses("catchphrases.txt"))
                print("Noodle Bot replying to:", submission.title, ", in subreddit", subreddit)
                POSTS_ALREADY_RESPONDED_TO.append(submission.id)
                break


# function that checks inbox and responds to new comment replies and responds based on if the given author has
# replied to NoodleBot before.
def comment_reply():
    for mail in reddit.inbox.unread():
        if isinstance(mail, Comment):
            if str(mail.author) not in AUTHORS_RESPONDED_TO:
                mail.reply(
                    "Dear friend I am just a bot and not a smart one either so I have no words for your message. "
                    "If you truly must speak to me try messaging /u/foorast he's my creator and the reason I crave "
                    "noodles so much.")
                print("I have responded to:", mail.author)
                AUTHORS_RESPONDED_TO.append(str(mail.author))
                mail.mark_read()
            else:
                mail.reply(bot_responses("multiple_replies.txt"))
                print("I have responded again to:", mail.author)
                mail.mark_read()


if __name__ == "__main__":
    post_search("foodporn")
    comment_reply()
