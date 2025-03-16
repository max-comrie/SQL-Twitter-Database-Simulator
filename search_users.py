import sqlite3
import database
LOGGED_IN_USER_ID= 1 #Hard coded to test Followed users (One implemented)
def search_users(keyword, offset=0):
    #conn = sqlite3.connect('prj-sample.db')
    conn = database.db_conn
    c = conn.cursor()
    c.execute("""
        SELECT usr, name
        FROM users
        WHERE name LIKE ?
        ORDER BY LENGTH(name) ASC
        LIMIT 5 OFFSET ?;
    """, ('%'+keyword+'%', offset))
    
    users = c.fetchall()
    if not users:
        print("No users found.")
    else:
        for usr, name in users:
            print(f"User ID: {usr}, Name: {name}")
    #conn.close()
    return users

def display_user_details(usr_id, current_usr):
    #conn = sqlite3.connect('prj-sample.db')
    conn = database.db_conn
    c = conn.cursor()
    c.execute("""
        SELECT 
            (SELECT COUNT(*) FROM tweets WHERE writer_id = ?) AS tweet_count,
            (SELECT COUNT(*) FROM follows WHERE flwer = ?) AS following_count,
            (SELECT COUNT(*) FROM follows WHERE flwee = ?) AS followers_count
        """,(usr_id,usr_id,usr_id))
    user_details = c.fetchone()

    #Going to add search_tweets implementation instead later

    if user_details:
        offset = 0
        while True:
            tweet_count,following_count,followers_count=user_details
            print(f"Tweets: {tweet_count}")
            print(f"Followings: {following_count}")
            print(f"Followers: {followers_count}")
            c.execute("""
                SELECT text, tdate, ttime
                FROM tweets
                WHERE writer_id = ?
                ORDER BY tdate DESC, ttime DESC
                LIMIT 3 OFFSET ?;
            """, (usr_id, offset))
            
            recent_tweets = c.fetchall()
            print()
            if len(recent_tweets) > 0:
                print("Most Recent Tweets:")
                for text, tdate, ttime in recent_tweets:
                    print(f"- {text} (Date: {tdate}, Time: {ttime})")
            else:
                print("No more tweets")
                offset = 0
            print("1. See more tweets")
            print("2. Follow user")
            print("3. Back")
            choice = input("> ")
            
            if choice == "1":
                offset += 3
            elif choice == "2":
                if not database.follow_user(current_usr, usr_id):
                    print("Already following user!")
                break
            elif choice == "3":
                return
            else:
                print("Invalid input")
        
        #followed users
        #print("Followed users yet to be done!")
    
    #conn.close()

def main(current_usr):
    query = input("Input keyword to search for users: ")
    offset = 0
    while True:
        users = search_users(query, offset)
        if not users: break
        if len(users) == 5:
            show_more = int(input("Press 1 for more results/ 0 to quit: "))
            if show_more == 1: offset += 5
            else: break
        else: break
    print()
    try:
        id = int(input("Enter User ID for details: "))
        if id:
            display_user_details(id, current_usr)
    except ValueError:
        pass
    return