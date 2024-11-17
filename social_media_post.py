import tweepy
from tkinter import messagebox

# Function to post a tweet
def post_tweet(message):
    try:
        # Replace these placeholders with your Twitter API credentials
        consumer_key = 'your_consumer_key'
        consumer_secret = 'your_consumer_secret'
        access_token = 'your_access_token'
        access_token_secret = 'your_access_token_secret'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        api.update_status(message)
        messagebox.showinfo("Success", "Tweet sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send tweet: {e}")