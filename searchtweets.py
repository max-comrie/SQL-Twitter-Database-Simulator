import sqlite3
import database
# had to make a new function for after user selects tweet, also user 
# should be able to compose reply but i think it relies on the 
# compose a tweet section by max
# IMPLEMENTED IN database.py
# def view_tweet_details(tweet_id):
#     cursor = db_conn.cursor()

#     # SQL Query to get tweet details (including retweets and replies)
#     query = """
#         SELECT 
#             tweets.tid, 
#             tweets.text, 
#             tweets.tdate, 
#             tweets.ttime,
#             -- Count the number of retweets for this tweet
#             (SELECT COUNT(*) FROM retweets WHERE retweets.tid = tweets.tid) AS retweet_count,
#             -- Count the number of replies to this tweet
#             (SELECT COUNT(*) FROM tweets AS replies WHERE replies.replyto_tid = tweets.tid) AS reply_count
#         FROM tweets
#         WHERE tweets.tid = ?;
#     """
    
#     cursor.execute(query, (tweet_id,))
#     tweet_details = cursor.fetchone()

#     if tweet_details:
#         print(f"\nSelected Tweet Details:")
#         print(f"Tweet ID: {tweet_details['tid']}")
#         print(f"Text: {tweet_details['text']}")
#         print(f"Date: {tweet_details['tdate']}")
#         print(f"Time: {tweet_details['ttime']}")
#         print(f"Retweet Count: {tweet_details['retweet_count']}")
#         print(f"Reply Count: {tweet_details['reply_count']}")
#     else:
#         print("Tweet not found.")
    
#     cursor.close()
#SEARCH TWEETS- main.py Olutimilehin

def search_tweets(current_usr):
    keyword_string= input("Enter keyword(s) or hashtag(s) separated by commas to search: ")
    limit=5
    offset=0
    while True:
        results= database.search_tweets(keyword_string, limit, offset)

        if results:
            print("\nSearch Results: ")
            for tweet in results:
        
                print(f"\nTweet Type: {tweet['tweet_type']}\n"
                    f"Tweet ID:{tweet['tid']}\n"
                    f"Date: {tweet['tdate']}\n"
                    f"Time: {tweet['ttime']}\n"
                    f"Text: {tweet['text']}\n"
                    f"Hashtags: {tweet['tweet_hashtags']}") 
                    

            user_input = input("\nWould you like to (1) see more tweets (2) select a tweet, or (3) exit? ").strip().lower()
            if user_input == '1':
                offset += limit  # increase the offset + get next 5 tweets
            elif user_input == '2':
                selected_tid= int(input("Enter the tweet id to view details: "))
                database.view_tweet_details(current_usr, selected_tid)
            else:
                print("Exiting search.")
                break
        else:
            print("\nNo more tweets found.") #should this happen if user requests to see tweets but there are no more?
            break


#SEARCH TWEETS for DATABASE (IMPLEMENTED IN database.py)
# def search_tweets_db(keyword_string, limit, offset):

#     keywords = keyword_string.split(',')
#     search_conditions = []
#     params= []

#     for keyword in keywords:
#         if keyword.startswith("#"):
#             #match as hashtag or in text field  ('abcd" and '#abcd')
#             search_conditions.append("hashtag_mentions.term = ? OR tweets.text LIKE ?")
#             params.append(keyword) #exact hashtag match
#             params.append(f"%{keyword[1:]}%") #match term in tweet text

#         else:
#             search_conditions.append("tweets.text REGEXP ?")
#             params.append(r'\b' + re.escape(keyword) + r'\b') #no partial matching, double check

#     where_clause= " OR ".join(search_conditions)

#     query= f"""
#         SELECT tweets.tid, tweets.writer_id, tweets.text, tweets.tdate, tweets.ttime,
#            CASE 
#             WHEN retweets.tid IS NOT NULL THEN 'retweet' 
#             ELSE 'tweet' END 
#             AS tweet_type --check if tweet is retweet or not
#             GROUP_CONCAT(hashtag_mentions.term) AS hashtag --get all hashtags associated with tweet, concatenate into string.
#         FROM tweets
#         LEFT JOIN retweets ON tweets.tid = retweets.tid
#         LEFT JOIN hashtag_mentions ON hashtag_mentions.tid = tweets.tid
#         WHERE {where_clause}  -- insert conditions 
#         ORDER BY tweets.tdate DESC, tweets.ttime DESC  -- sorting
#         LIMIT ? OFFSET ?;  -- retrieval
#     """

#     params.extend([limit, offset])

#     #execute query
#     cursor = db_conn.cursor()
#     cursor.execute(query, params)
    
#     results = [{"tid": row["tid"], "writer_id": row["writer_id"], "text": row["text"],
#                 "tdate": row["tdate"],   "ttime": row["ttime"], "tweet_type": row["tweet_type"], "tweet_hashtags": row['hashtag']} 
#                for row in cursor.fetchall()]

    
#     return results