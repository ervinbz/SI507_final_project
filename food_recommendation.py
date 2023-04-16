import json

# Load the data from the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Display videos and ask the user for their food type preference
print("Here are some videos to help you decide:")
for cuisine, cuisine_data in data.items():
    print(f"{cuisine} videos:")
    for topic, topic_data in cuisine_data.items():
        print(f"  {topic}:")
        for video_title, video_info in topic_data["Videos"].items():
            print(f"    - {video_title}: https://www.youtube.com/watch?v={video_info['video_id']}")

preferred_cuisine = input("Which cuisine type do you want? ")

# Show restaurants based on the user's food type preference
favorite_restaurant = None
while favorite_restaurant is None:
    if preferred_cuisine in data:
        print("Here are some restaurants for your preferred cuisine:")
        i = 1
        restaurants = list(data[preferred_cuisine][list(data[preferred_cuisine].keys())[0]]["Restaurants"].items())
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
