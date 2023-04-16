import json
import requests
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, YELP_API_KEY


class FoodFinder:
    def __init__(self):
        self.food_preferences = {}
        self.location = ""
        self.data = {}
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        self.yelp_url = "https://api.yelp.com/v3/businesses/search"
        self.yelp_headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    def get_user_input(self):
        num_cuisines = int(input("How many cuisines would you like to search for? "))
        for i in range(num_cuisines):
            cuisine = input(f"Enter cuisine {i+1}: ")
            num_topics = int(input(f"How many topics for {cuisine}? "))
            topics = []
            for j in range(num_topics):
                topic = input(f"Enter topic {j+1}: ")
                topics.append(topic)
            self.food_preferences[cuisine] = topics
        self.location = input("Enter location: ")

    def get_data(self):
        for cuisine, topics in self.food_preferences.items():
            cuisine_node = {}
            for topic in topics:
                topic_node = {}
                query = f"{cuisine} {topic}"
                max_results = 5
                part = 'id,snippet'
                response = self.youtube.search().list(
                    q=query,
                    type='video',
                    part=part,
                    maxResults=max_results
                ).execute()
                video_data = {}
                for item in response['items']:
                    video_id = item['id']['videoId']
                    video_title = item['snippet']['title']
                    video_description = item['snippet']['description']
                    video_data[video_title] = {
                        'video_id': video_id,
                        'description': video_description
                    }
                topic_node["Videos"] = video_data

                params = {
                    "term": cuisine,
                    "location": self.location,
                    "sort_by": "rating"
                }
                yelp_response = requests.get(self.yelp_url, headers=self.yelp_headers, params=params).json()
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

            self.data[cuisine] = cuisine_node

    def save_data_to_json(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def load_data_from_json(self):
        with open('data.json', 'r') as f:
            self.data = json.load(f)

    def display_videos_and_get_preference(self):
        print("Here are some videos to help you decide:")
        for cuisine, cuisine_data in self.data.items():
            print(f"{cuisine} videos:")
            for topic, topic_data in cuisine_data.items():
                print(f"  {topic}:")
                for video_title, video_info in topic_data["Videos"].items():
                    print(f"    - {video_title}: https://www.youtube.com/watch?v={video_info['video_id']}")

        return input("Which cuisine type do you want? ")
    
    def show_restaurants(self, preferred_cuisine):
        favorite_restaurant = None
        while favorite_restaurant is None:
            if preferred_cuisine in self.data:
                print("Here are some restaurants for your preferred cuisine:")
                i = 1
                restaurants = list(self.data[preferred_cuisine][list(self.data[preferred_cuisine].keys())[0]]["Restaurants"].items())
                for restaurant_name, restaurant_info in restaurants:
                    print(f"{i}. {restaurant_name} - {restaurant_info['address']} ({restaurant_info['rating']} stars, {restaurant_info['reviews']} reviews)")
                    i += 1

                restaurant_choice = int(input("Enter the number of your favorite restaurant or 0 to change restaurants: "))
                if restaurant_choice > 0 and restaurant_choice <= len(restaurants):
                    favorite_restaurant = restaurants[restaurant_choice - 1]
                    print(f"Great! Enjoy your meal at {favorite_restaurant[0]}!")
                elif restaurant_choice == 0:
                    preferred_cuisine = input("Which cuisine type do you want? ")
                else:
                    print("Invalid input, please try again.")
            else:
                print("Cuisine not found in data. Please enter a valid cuisine.")
                preferred_cuisine = input("Which cuisine type do you want? ")

        print("Bye!")

def main():
    food_finder = FoodFinder()
    food_finder.get_user_input()
    food_finder.get_data()
    food_finder.save_data_to_json()
    food_finder.load_data_from_json()
    preferred_cuisine = food_finder.display_videos_and_get_preference()
    food_finder.show_restaurants(preferred_cuisine)

if __name__ == "__main__":
    main()
