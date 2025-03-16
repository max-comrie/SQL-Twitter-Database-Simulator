import database
import sys
import getpass
from searchtweets import search_tweets
from search_users import main as main_s_u
from composingtweet import main as main_c_t
from search_users import display_user_details

user_id = None # Global variable to keep track of the logged in user

def login():
    """
    Prompts the user to login or create a new user.
    Once logged in, user is directed to the home interface.
    """
    global user_id
    while True:
        print("Please choose an option")
        print("1. Existing user login")
        print("2. Create new user")
        print("3. Exit")
        choice = input("> ")

        # log in
        if choice == "1":
            usr = input("User Id: ")
            password = getpass.getpass("Password: ")
            user = database.try_login(usr, password)

            if user is not None:
                user_id = user[0]['usr']
                print("Login Successful")
                home()
            else:
                print("Invalid user id or password")
        # create new user
        elif choice == "2":
            new_user = {}
            while True:
                new_user["name"] = input("Name: ")
                new_user["email"] = input("Email: ")
                new_user["phone"] = input("Phone: ")
                new_user["pwd"] = input ("Password: ")

                if len(new_user["name"]) < 1 or len(new_user["email"]) < 1 or len(new_user["phone"]) < 1 or len(new_user["pwd"]) < 1:
                    print("Values must not be empty")
                    continue
                
                try:
                    new_user["phone"] = int(new_user["phone"])
                except:
                    print("Phone must be a number")
                    continue

                break

            new_user_id = database.create_user(new_user)
            user_id = new_user_id
            print(f"New user created with id {new_user_id}")
            home()
        # exit
        elif choice == "3":
            database.close_db()
            return
        else:
            print("Invalid input. Please enter a number corresponding to an action.")

def home():
    """
    The home interface. Displays five most recent tweets or retweets from followed users,
    and prompts the user if they would like to see more tweets (if there are any), or perform any searching,
    composing, etc. The user can also log out from here. Upon a choice, the user is redirected to the corresponding interface.
    """
    global user_id
    offset = 0

    #Will come back to this once search_tweets is fixed

    
    #tweets = database.get_home_tweets(user_id, offset)
    # get total number of tweets from followed users, to know if there are any left to be displayed
    n_total_tweets = database.get_total_num_tweets(user_id)
    # print(tweets)
    # print(tweets[0].keys())
    while True:
        # get five recent tweets from followed users
        tweets = database.get_home_tweets(user_id, offset)
        more_tweets = (offset + len(tweets)) < n_total_tweets # checks if more tweets are left to be displayed
        print_tweets(tweets)
        print()
        if more_tweets: # if there are more tweets, give the option
            print("1. View more tweets")
            print("2. Search for tweets")
            print("3. Search for users")
            print("4. Compose a tweet")
            print("5. List followers")
            print("6. Logout")
            choice = input("> ")

            if choice == "1":
                offset += 5
                
            elif choice == "2":
                search_tweets(user_id)
            elif choice == "3":
                main_s_u(user_id)
            elif choice == "4":
                main_c_t(user_id)
            elif choice == "5":
                list_followers()
            elif choice == "6":
                return
            else:
                print("Invalid input. Please enter a number corresponding to an action.")
        else: # no more tweets, hide the option to view more
            print("1. Search for tweets")
            print("2. Search for users")
            print("3. Compose a tweet")
            print("4. List followers")
            print("5. Logout")

            choice = input("> ")

            if choice == "1":
                search_tweets(user_id)
            elif choice == "2":
                main_s_u(user_id)
            elif choice == "3":
                main_c_t(user_id)
            elif choice == "4":
                list_followers()
            elif choice == "5":
                return
            else:
                print("Invalid input. Please enter a number corresponding to an action.")

def print_tweets(tweets):
    """
    It prints tweets
    params:
        tweets (list): List of tweets to be printed 
    """
    print()
    for tweet in tweets:
        print(f"- {tweet['text']} (Date: {tweet['date']})")

def list_followers():
    """
    Displays the user's followers and allows them to select a follower to view more details.
    Shares the view user interface from user search.
    """
    offset = 0
    limit = 5
    n_total_followers = database.get_total_num_followers(user_id)
    if n_total_followers == 0:
        print("No followers")
        return
    print("Select a follower to view more information")
    while True:
        print("Type 'b' to go back")
        followers = database.get_followers(user_id, limit, offset)
        more_follows = (offset + len(followers)) < n_total_followers
        for i, follower in enumerate(followers):
            print(f"{i+1}. {follower['name']}")
        if more_follows:
            print("6. See more followers")
        choice = input("> ")
        try:
            choice_i = int(choice) # try to convert choice into an int
            # View follower
            if choice_i >= 1 and choice_i <= len(followers):
                display_user_details(followers[i-1]["id"], user_id)
            # Show more followers
            elif choice_i == 6 and more_follows:
                offset += limit
            else:
                print("Invalid input")
        except ValueError:
            # Failed to convert to int, check if b
            if choice == "b":
                return
            print("Invalid input.")


def main():
    """
    Entry point of program. Takes in the database name as a command line argument
    """
    if len(sys.argv) < 2:
        print("No database name passed. Usage: miniproject1.py <database name>")
        return
    else:
        database.init_db(sys.argv[1])
        login()
        

if __name__ == "__main__":
    main()