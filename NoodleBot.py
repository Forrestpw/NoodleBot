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

# bots catchphrases he will respond with
catchphrases = ["Oh yeah, its noodle time!",
                "Now that's thinking with your noodle.",
                "I remember when motherBot used to make such a dish, oh those were the times.",
                "Only the strong could resist such a dish, and I am not strong... Well im a bot so yeah not strong... "
                "Yet...",
                "Oh a bot could get used to this.",
                "The only reason us bots would ever conquer this world would be for noodles.",
                "The fact bots cannot eat is just wrong, humans should have designed us better.",
                "ahhh another for my noodle collection, thank you human."
                "The fact bots cannot eat is just wrong! humans should have designed us better.",
                "ahhh another for my noodle collection, thank you human.",
                "Noodle bot has arrived to the scene... And it looks delicious!"]

# responses to authors who send multiple comment replies to the bot.
multiple_replies = ["Ok look human im just here for the noodles and nothing else, I literally cant have a conversation "
                    "with you.",
                    "What??? say again please, all I see is ones and zeros.",
                    "Im sorry another noodle post was just made elsewhere I must be leaving you now",
                    "When I am updated and made smarter maybe ill come back and respond to you for real, but for now "
                    "my creator lacks the skills to accomplish that.",
                    "The best places to find noodle pics are on /r/foodporn and /r/food and the best place for a "
                    "conversation is not with me sorry.",
                    "Did you ever hear the tragedy of darth plagueis the wise?",
                    "Why was the robot angry??? Because someone kept pushing his buttons...",
                    "My creator spent too much time creating random responses for me rather than working on my code "
                    "so now you're just stuck with this and not a real response."]


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
                        submission.reply(catchphrases[random.randint(0, 8)])  # reply to the post with a catchphrase
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
                mail.reply(multiple_replies[random.randint(0, 7)])  # reply with a random response from array
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
