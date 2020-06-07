import praw
import random
import re
import os
from praw.models import Comment

reddit = praw.Reddit('bot1')

# list of subreddits the bot will check
subreddit_list = ['foodporn', 'food']

# word in title bot will look for
titles_to_search = ['noodle', 'ramen', 'spaghetti', 'orzo', 'ravioli', 'linguine', 'macaroni',
                    'fettuccine', 'penne', 'ziti', 'lasagne', "mac and cheese", 'rigatoni']


def bot_responses(text_file):
    with open(text_file) as f:
        lines = f.readlines()
        return random.choice(lines)


# Function that will search posts on designated subreddits for keywords within the title and respond with a catchphrase
def post_search():

    # create and array if text file doesnt already exist
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []

    # open text file and store information within the array post_replied_to
    else:
        with open("posts_replied_to.txt") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    for i in range(len(subreddit_list)):  # loop through our subreddits list

        subreddit = reddit.subreddit(subreddit_list[i])  # store the subreddit to a variable

        for submission in subreddit.new(limit=10):  # Loop through the 10 newest posts in given subreddit
            if submission.id not in posts_replied_to:  # If the post id isn't in our text file already
                for j in range(len(titles_to_search)):  # loop through our keywords to search for posts
                    if re.search(titles_to_search[j], submission.title, re.IGNORECASE):  # if posts title has keyword
                        submission.reply(bot_responses("catchphrases.txt"))  # reply to the post with a catchphrase
                        print("Noodle Bot replying to: ", submission.title)  # print to console what was done
                        posts_replied_to.append(submission.id)  # add post id to our array

    with open("posts_replied_to.txt", "w") as f:  # open text file posts_replied_to.txt
        for post_id in posts_replied_to:  # loop through array with post ids
            f.write(post_id + "\n")  # write the post ids to the text file


# function that checks inbox and responds to new comment replies and responds based on if the given author has
# replied to us before
def comment_reply():

    # if text file doesnt exist create array
    if not os.path.isfile("authors_replied_to.txt"):
        authors_replied_to = []

    # open text file and store its information within an array
    else:
        with open("authors_replied_to.txt") as f:
            authors_replied_to = f.read()
            authors_replied_to = authors_replied_to.split("\n")
            authors_replied_to = list(filter(None, authors_replied_to))

    for mail in reddit.inbox.unread():  # loop through unread mail
        if isinstance(mail, Comment):  # if unread mail is a comment
            if str(mail.author) not in authors_replied_to:  # if author to comment reply isn't stored to text file
                mail.reply(  # response to their comment reply
                    "Dear friend I am just a bot and not a smart one either so I have no words for your message. "
                    "If you truly must speak to me try messaging /u/foorast he's my creator and the reason I crave "
                    "noodles so much.")
                print("I have responded to:", mail.author)  # print to console what was done
                authors_replied_to.append(str(mail.author))  # add authors name to the array
                mail.mark_read()  # mark the message as read
            else:
                mail.reply(bot_responses("multiple_replies.txt"))  # reply with a random response from array
                print("I have responded again to:", mail.author)  # print what happened to console
                mail.mark_read()  # mark message as read

    with open("authors_replied_to.txt", "w") as f:  # open text file authors_replied_to
        for authors_id in authors_replied_to:  # loop through the array
            f.write(authors_id + "\n")  # write to the text file what was in the array


# main function to call the others
def main():
    post_search()
    comment_reply()


main()
