import sqlite3
import database
from search_users import display_user_details
def followers(user,offset):
    #conn = sqlite3.connect('prj-sample.db')
    conn = database.db_conn
    c = conn.cursor()
    # Query to get followers with pagination
    query = """
    SELECT u.usr, u.name, u.email, u.phone
    FROM users u
    JOIN follows f ON u.usr = f.flwer
    WHERE f.flwee = %s
    LIMIT %s, 5;
    """
    c.execute(query, (user, offset))
    followers = c.fetchall()

    if not followers:
        print("End of followers.")
    else:
        for usr, name in followers:
            print(f"User ID: {usr}, Name: {name}")

    
def main(usr):
    offset = 0
    while True:
        users = followers(usr, offset)
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
            display_user_details(id)
    except ValueError:
        pass
    return

main(1)