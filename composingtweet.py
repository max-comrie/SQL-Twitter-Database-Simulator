
import sqlite3
import database
from datetime import datetime
# Function to compose a tweet
def compose_tweet(user_id, content, replyto_tid):
    """
    Compose a tweet. Inserts the tweet data into the database, including:
    - The writer's user ID
    - The tweet's content
    - The current date and time
    - Optional: A reply-to tweet ID
    
    Args:
        user_id (int): The ID of the user composing the tweet
        content (str): The text content of the tweet
        reply_to_tid (int or None): The tweet ID being replied to, if any (default is None)
    
    Returns:
        None
    """
    # Connecting to the SQLite database
    #conn = sqlite3.connect('prj-sample.db')
    conn = database.db_conn
    c = conn.cursor()

    # Checking for duplicate hashtags
    hashtags = [word for word in content.split() if word.startswith("#")]
    hashtags_set = set(word for word in content.split() if word.startswith("#"))
    if len(hashtags) != len(hashtags_set):
        print("Tweets cannot have duplicate hashtags.") # Error message if duplicates exist
        #conn.close() # Closing the database connection
    else:
        # Getting the current date and time, required for entry in 'tweets' table
        current_time = datetime.now()
        tdate = current_time.strftime('%Y-%m-%d')  # Formatting as YYYY-MM-DD
        ttime = current_time.strftime('%H:%M:%S')  # Formatting as HH:MM:SS
        
        
        # Executing the query and fetching the result to find tid
        c.execute("""
        SELECT tid
        FROM tweets
        ORDER BY tid DESC
        """)
        result = c.fetchone()

        # Incrementing the tid from the tid of the last tweet
        if result:
            tweet_id = result[0]+1
        else:
            tweet_id = 1
        # Inserting the tweet into the 'tweets' table
        c.execute('''
        INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES (?, ?, ?, ?, ?, ?)
        ''', (tweet_id, user_id, content, tdate, ttime, replyto_tid))
        conn.commit()  # Commit the transaction to save the tweet



        # Inserting the hashtags into the 'hashtag_mentions' table
        for hashtag in hashtags:
                # Insert the new hashtag
                c.execute("INSERT INTO hashtag_mentions (tid,term) VALUES (?, ?)", (tweet_id,hashtag))
                conn.commit()
            

        #conn.close()  # Closing the database connection
        
def main(user_id):
    content = input("Enter tweet: ")
    replyto_tid = None #not asked for in the q
    compose_tweet(user_id, content, replyto_tid)     



