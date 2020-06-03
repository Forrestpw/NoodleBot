import praw
import random
import re
import os
from praw.models import Comment

reddit = praw.Reddit('bot1')

# list of subreddits the bot will check
subreddit_list = ['foodporn', 'food']
# word in title bot will look for
titles_to_search = ['noodle', 'ramen', 'spaghetti', 'orzo', 'ravioli', 'linguine', 'macaroni', 'fettuccine',
                    'penne', 'ziti', 'lasagne', "mac and cheese", 'rigatoni']
# bots catchphrases he will respond with
catchphrases = ["Oh yeah, its noodle time!",
                "Now that's thinking with your noodle.",
                "I remember when motherBot used to make such a dish, oh those were the times.",
                "Only the strong could resist such a dish, and I am not strong... Well im a bot so yeah not strong... "
                "Yet...",
                "Oh a bot could get used to this.",
                "The only reason us bots would ever conquer this world would be for noodles.",
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


def saved_info(txt_file):
    if not os.path.isfile(txt_file):
        replied_to = []
        return replied_to

    else:
        with open(txt_file) as f:
            replied_to = f.read()
            replied_to = replied_to.split("\n")
            replied_to = list(filter(None, replied_to))
            return replied_to


def write_to_files(txt_file):
    with open(txt_file, "w") as f:
        for post_id in saved_info(txt_file):
            f.write(post_id + "\n")


def check_for_posts(txt_file):
    for i in range(len(subreddit_list)):

        subreddit = reddit.subreddit(subreddit_list[i])

        for submission in subreddit.new(limit=10):
            if submission.id not in saved_info(txt_file):
                for j in range(len(titles_to_search)):
                    if re.search(titles_to_search[j], submission.title, re.IGNORECASE):
                        submission.reply(catchphrases[random.randint(0, 8)])
                        print("Noodle Bot replying to: ", submission.title)
                        saved_info(txt_file).append(submission.id)


def comment_reply(txt_file):
    for mail in reddit.inbox.unread():
        if isinstance(mail, Comment):
            if str(mail.author) not in saved_info(txt_file):
                mail.reply("Dear friend I am just a bot and not a smart one either so I have no words for your "
                           "message. If you truly must speak to me try messaging /u/foorast he's my creator and the "
                           "reason I crave noodles so much.")
                print("I have responded to:", mail.author)
                saved_info(txt_file).append(str(mail.author))
                mail.mark_read()
            else:
                mail.reply(multiple_replies[random.randint(0, 7)])
                print("I have responded again to:", mail.author)
                mail.mark_read()


def main():
    posts_replied_to = "posts_replied_to.txt"
    authors_replied_to = "authors_replied_to.txt"

    saved_info(posts_replied_to)
    check_for_posts(posts_replied_to)
    write_to_files(posts_replied_to)

    saved_info(authors_replied_to)
    comment_reply(authors_replied_to)
    write_to_files(authors_replied_to)


main()
