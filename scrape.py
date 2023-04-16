import json
import requests
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, YELP_API_KEY

# Accept user input for food preferences and location
food_preferences = {}
num_cuisines = int(input("How many cuisines would you like to search for? "))
for i in range(num_cuisines):
    cuisine = input(f"Enter cuisine {i+1}: ")
    num_topics = int(input(f"How many topics for {cuisine}? "))
    topics = []
    for j in range(num_topics):
        topic = input(f"Enter topic {j+1}: ")
        topics.append(topic)
    food_preferences[cuisine] = topics
location = input("Enter location: ")

# Create a Yelp API client
yelp_url = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Retrieve restaurant data for each cuisine and location, and video data for each cuisine and topic
data = {}
for cuisine, topics in food_preferences.items():
    cuisine_node = {}
    for topic in topics:
        topic_node = {}
        query = f"{cuisine} {topic}"
        max_results = 5
        part = 'id,snippet'
        response = youtube.search().list(
            q=query,
            type='video',
            part=part,
            maxResults=max_results
        ).execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_description = item['snippet']['description']
            topic_node[video_title] = {
                'video_id': video_id,
                'description': video_description
            }
        
        params = {
            "term": cuisine,
            "location": location,
            "sort_by": "rating"
        }
        yelp_response = requests.get(yelp_url, headers=headers, params=params).json()
        restaurant_data = {}
        for business in yelp_response["businesses"]:
            restaurant_name = business["name"]
            restaurant_rating = business["rating"]
            restaurant_reviews = business["review_count"]
            restaurant_address = ", ".join(business["location"]["display_address"])
            restaurant_data[restaurant_name] = {
                "rating": restaurant_rating,
                "reviews": restaurant_reviews,
                "address": restaurant_address
            }
        
        topic_node["Restaurants"] = restaurant_data
        cuisine_node[topic] = topic_node
    
    data[cuisine] = cuisine_node

# Save the data to a JSON file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
