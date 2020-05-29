import praw
import random
import re
import os

reddit = praw.Reddit('bot1')

# list of subreddits the bot will check
subreddit_list = ['foodporn', 'food']
# word in title bot will look for
titles_to_search = ['noodles', 'ramen', 'spaghetti', 'pho', 'orzo', 'ravioli', 'linguine', 'macaroni', 'fettuccine',
                    'penne', 'ziti', 'lasagne']
# bots catchphrases he will respond with
catchphrases = ["Oh yeah, its noodle time!",
                "Now that's thinking with your noodle.",
                "I remember when motherBot used to make such a dish, oh those were the times.",
                "Only the strong could resist such a dish, and I am not strong... Well im a bot so yeah not strong... "
                "Yet...",
                "Oh a bot could get used to this.",
                "The only reason us bots would ever conquer this world would be for noodles.",
                "The fact bots cannot eat is just wrong, humans should have designed us better.",
                "ahhh another for my noodle collection, thank you human."]

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

else:
    with open("posts_replied_to.txt") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

for i in range(len(subreddit_list)):

    subreddit = reddit.subreddit(subreddit_list[i])

    for submission in subreddit.hot(limit=5):
        if submission.id not in posts_replied_to:
            for j in range(len(titles_to_search)):
                if re.search(titles_to_search[j], submission.title, re.IGNORECASE):
                    submission.reply(catchphrases[random.randint(0, 7)])
                    print("Noodle Bot replying to: ", submission.title)
                    posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

