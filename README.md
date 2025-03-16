[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZQQhHp7h)
# Assignment3

# CMPUT 291 Mini Project 1 -Fall 2024
Group member names and ccids (3-4 members)  
  agbabiak, olutimilehin agbabiaka  
  aflewwel, alex flewwelling  
  mcomrie, max comrie
  njoshi4, nikhil joshi

# Group work break-down strategy
We each contributed to specific components of the system based on our individual strengths and expertise. Alex took responsibility for developing the login and logout functionality, as well as the followers list, ensuring secure user authentication. Timi worked on the search tweets feature, enabling users to retrieve tweets based on keywords or hashtags. Nick handled the search users feature, allowing for efficient user lookup by username or other attributes. Max focused on the compose tweet functionality, ensuring that tweets could be created, validated, and saved to the database while meeting platform constraints. Each of us spent approximately three hours on our respective components, and we collectively spent an additional four hours integrating all the parts of the system. We coordinated our efforts through regular meetings, sharing updates and resolving challenges to ensure cooperation with each other and adherence to project requirements.

# Code execution guide
System Setup
Ensure you have Python (version 3.x or higher) and MongoDB installed on your machine.
Install the pymongo library by running:
pip install pymongo  

Download or clone the project repository to your local machine.
Make sure MongoDB is running on your system. By default, MongoDB runs on port 27017.
Loading Data into MongoDB
To load the JSON file containing tweets into MongoDB:

Open the terminal and navigate to the project directory.

Run the following command:
python load-json.py <json_file> <port>  
Replace <json_file> with the name of the JSON file (e.g., tweets.json) and <port> with the MongoDB port (default is 27017).


This will:
Connect to the MongoDB server.
Create a database named 291db and a collection named tweets.
Insert the tweet data into the collection in batches.
Running the Program
After loading the data, you can start interacting with the system:

Open the terminal and navigate to the project directory.
Run the following command:
bash
Copy code
python operate-on-tweets.py <port>  
Example:
bash
Copy code
python operate-on-tweets.py 27017  
This will connect to the 291db database and present you with a main menu to interact with the system.
Navigating the System
Once the program is running, you will be presented with the following options:

1. Search for Tweets
Enter keywords to search for tweets containing those keywords.
The search is case-insensitive and retrieves tweets matching the query.

2. Search for Users
Look up users by their username, display name, or location.

3. List Top Tweets
Display the top tweets based on metrics such as:
Retweet count
Like count
Quote count

4. List Top Users
Display the top users ranked by their follower count.

5. Compose a Tweet
Enter the content of a new tweet.
The tweet will be stored in the database with:
Username: 291user
Date: Current system date.
The system will validate the tweet content and save it to the tweets collection.

6. Exit the Program
Select this option to log out and exit the system.

# Names of anyone you have collaborated with (as much as it is allowed within the course policy) or a line saying that you did not collaborate with anyone else.  
We did not collaborate with anyone else

# More detail of any AI tool used.
NA
