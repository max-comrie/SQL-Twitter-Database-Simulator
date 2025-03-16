import sqlite3 as sq
import re
from composingtweet import compose_tweet
import miniproject1

db_conn = None # global to hold database connection

# def regexp(value, expression):
#     r = re.compile(expression)
#     return r.search(value) is not None

def init_db(db_name):
    """
    Initializes database connection with row factory and foreign keys on
    params: 
        db_name (string): the database name to connect to
    """
    global db_conn
    db_conn = sq.connect(db_name)
    db_conn.row_factory = sq.Row
    #db_conn.create_function("REGEXP", 2, regexp)
    c = db_conn.cursor()
    c.execute("PRAGMA foreign_keys=ON;") # Turns on foreign keys
    db_conn.commit()

    print(f"Database initialized: {db_name}")


def try_login(usr, password):
    """
    Attempts to log in with the given user id and password
    params:
        usr (string): The user id of the account
        password (string): Password of the account
    """
    query = """SELECT * FROM Users U
               WHERE U.usr = ?
               AND U.pwd = ?;"""
    
    c = db_conn.cursor()
    c.execute(query, (usr, password))
    rows = c.fetchall()

    if len(rows) > 0:
        return rows
    
    return None

def create_user(user):
    """
    Creates a user in the users table.
    params:
        user (dict): Dictionary with keys matching the name of attributes in the user table, except for usr
    return:
        The user id of the newly created user
    """
    query = """INSERT INTO Users (usr, name, email, phone, pwd)
               VALUES (:usr, :name, :email, :phone, :pwd)"""
    
    c = db_conn.cursor()
    # finds the max_usr so that we can increment it by one for the new user
    max_usr = c.execute("SELECT MAX(usr) FROM Users").fetchone()["MAX(usr)"]
    user["usr"] = max_usr + 1

    c.execute(query, user)
    db_conn.commit()

    return max_usr+1

def get_home_tweets(user_id, offset):
    """
    Gets the five most recent tweets or retweets from followed users.
    params:
        user_id: id of logged in user
        offset: offset for viewing more tweets
    """
    query = """SELECT * FROM
                (SELECT T.text, T.tdate AS date 
                FROM tweets T
                JOIN follows F ON F.flwee = T.writer_id
                WHERE F.flwer = :user
                
                UNION
                
                SELECT T.text, R.rdate AS date
                FROM tweets T
                JOIN retweets R ON R.tid = T.tid
                JOIN follows F ON F.flwee = R.retweeter_id
                WHERE F.flwer = :user)
            ORDER BY Date DESC
            LIMIT 5 OFFSET :offset;"""

    c = db_conn.cursor()
    c.execute(query, { "user": user_id, "offset": offset })
    result = c.fetchall()

    return result

def get_total_num_tweets(user_id):
    """
    Gets the total number of tweets from followed users
    params:
        user_id: user id of logged in user
    """
    query = """SELECT COUNT(*) FROM
                (SELECT T.text, T.tdate AS date 
                FROM tweets T
                JOIN follows F ON F.flwee = T.writer_id
                WHERE F.flwer = :user
                
                UNION
                
                SELECT T.text, R.rdate AS date
                FROM tweets T
                JOIN retweets R ON R.tid = T.tid
                JOIN follows F ON F.flwee = R.retweeter_id
                WHERE F.flwer = :user)
            """

    c = db_conn.cursor()
    c.execute(query, { "user": user_id })
    result = c.fetchone()["COUNT(*)"]

    return result

def get_followers(user_id, limit, offset):
    """
    Gets a certain number of followers
    params:
        user_id: user id of logged in user
        limit: number of followers to return
        offset: offset for viewing more followers
    """
    query = """SELECT F.flwer AS id, U.name AS name
               FROM follows F
               JOIN users U ON U.usr = F.flwer
               WHERE F.flwee = :user
               LIMIT :limit OFFSET :offset"""
    
    c = db_conn.cursor()
    c.execute(query, { "user": user_id, "limit":limit, "offset": offset })
    result = c.fetchall()

    return result

def get_total_num_followers(user_id) -> int:
    """
    Gets the total number of followers for a user
    params:
        user_id: user id that followers are following
    """
    query = """SELECT COUNT(*)
               FROM follows F
               JOIN users U ON U.usr = F.flwer
               WHERE F.flwee = :user"""

    c = db_conn.cursor()
    c.execute(query, { "user": user_id })
    result = c.fetchone()["COUNT(*)"]

    return result

def search_tweets(keyword_string, limit, offset):

    keywords = keyword_string.split(',')
    search_conditions = []
    params= []

    for keyword in keywords:
        if keyword.startswith("#"):
            #match as hashtag or in text field  ('abcd" and '#abcd')
            search_conditions.append("hashtag_mentions.term = ? OR tweets.text LIKE ?")
            params.append(keyword) #exact hashtag match
            params.append(f"%{keyword[1:]}%") #match term in tweet text

        else:
            #search_conditions.append("tweets.text REGEXP ?")
            #params.append(r'\b' + re.escape(keyword) + r'\b') #no partial matching, double check
            #params.append(rf"\b{re.escape(keyword)}\b")

            # regex wasn't working... so this instead
            for _ in range(4):
                search_conditions.append("tweets.text LIKE ?") # yes I know this code looks terrible but it works OKAY
            params.append(f"% {keyword}")
            params.append(f"% {keyword} %")
            params.append(f"{keyword} %")
            params.append(keyword)

    where_clause= " OR ".join(search_conditions)

    query= f"""
        SELECT tweets.tid, tweets.writer_id, tweets.text, tweets.tdate, tweets.ttime,
           CASE 
            WHEN retweets.tid IS NOT NULL THEN 'retweet' 
            ELSE 'tweet' END 
            AS tweet_type, --check if tweet is retweet or not
           GROUP_CONCAT(hashtag_mentions.term) AS hashtag --get all hashtags associated with tweet, concatenate into string.
        FROM tweets
        LEFT JOIN retweets ON tweets.tid = retweets.tid
        LEFT JOIN hashtag_mentions ON hashtag_mentions.tid = tweets.tid
        WHERE {where_clause}  -- insert conditions 
        GROUP BY tweets.tid, tweets.writer_id, tweets.text, tweets.tdate, tweets.ttime
        ORDER BY tweets.tdate DESC, tweets.ttime DESC  -- sorting
        LIMIT ? OFFSET ?;  -- retrieval
    """

    params.extend([limit, offset])

    #execute query
    params = tuple(params)
    cursor = db_conn.cursor()
    cursor.execute(query, params)
    
    results = [{"tid": row["tid"], "writer_id": row["writer_id"], "text": row["text"],
                "tdate": row["tdate"],   "ttime": row["ttime"], "tweet_type": row["tweet_type"], "tweet_hashtags": row['hashtag']} 
               for row in cursor.fetchall()]

    
    return results

def view_tweet_details(current_usr, tweet_id):
    cursor = db_conn.cursor()

    # SQL Query to get tweet details (including retweets and replies)
    query = """
        SELECT 
            tweets.tid, 
            tweets.text, 
            tweets.tdate, 
            tweets.ttime,
            tweets.writer_id,
            -- Count the number of retweets for this tweet
            (SELECT COUNT(*) FROM retweets WHERE retweets.tid = tweets.tid) AS retweet_count,
            -- Count the number of replies to this tweet
            (SELECT COUNT(*) FROM tweets AS replies WHERE replies.replyto_tid = tweets.tid) AS reply_count
        FROM tweets
        WHERE tweets.tid = ?;
    """
    
    cursor.execute(query, (tweet_id,))
    tweet_details = cursor.fetchone()

    if tweet_details:
        print(f"\nSelected Tweet Details:")
        print(f"Tweet ID: {tweet_details['tid']}")
        print(f"Text: {tweet_details['text']}")
        print(f"Date: {tweet_details['tdate']}")
        print(f"Time: {tweet_details['ttime']}")
        print(f"Retweet Count: {tweet_details['retweet_count']}")
        print(f"Reply Count: {tweet_details['reply_count']}")

        while True:
            print("1. Reply to this tweet")
            print("2. Retweet this tweet")
            print("3. Back")
            choice = input("> ")
            if choice == "1":
                content = input("Reply content: ")
                compose_tweet(current_usr, content, tweet_id)
                break
            elif choice == "2":
                if not retweet(current_usr, tweet_id, tweet_details['writer_id']):
                    print("Already retweeted!")
                break
            elif choice == "3":
                break
            else:
                print("Invalid input")
    else:
        print("Tweet not found.")
   
    
    cursor.close()

def retweet(current_usr, tweet_id, writer_id):
    check = """SELECT 1 FROM retweets
               WHERE tid = ? AND retweeter_id = ?"""
    query = """INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate)
               VALUES (?, ?, ?, ?, date())"""
    
    c = db_conn.cursor()
    c.execute(check, (tweet_id, current_usr))
    if len(c.fetchall()) > 0:
        return False
    c.execute(query, (tweet_id, current_usr, writer_id, 0))
    db_conn.commit()
    return True

def follow_user(flwer_id, flwee_id):
    check = """SELECT 1 FROM follows
               WHERE flwer = ? AND flwee = ?"""
    
    query = """INSERT INTO follows (flwer, flwee, start_date)
               VALUES (?, ?, date())
            """
    
    c = db_conn.cursor()
    c.execute(check, (flwer_id, flwee_id))
    if len(c.fetchall()) > 0:
        return False
    c.execute(query, (flwer_id, flwee_id))
    db_conn.commit()
    return True

def close_db():
    db_conn.close()