# SI507_final_project

My 507 project is FoodFinder, an app designed to help users find videos and restaurants related to their preferred cuisine and location. The app uses Yelp's API and Google's YouTube Data API to provide relevant data to users. 

## Brief instructions for how to interact with the program 

Users are prompted to enter their favorite foods and topics that interest them. The app then uses the YouTube data API to find videos related to the user's preferences. In addition, the app uses the Yelp API to find restaurants that are relevant to a user's preferences in their location. The results are saved in a JSON file for future reference. 
 
When the user runs the application again, they can choose to load previously saved data from the JSON file or retrieve new data. The user is then prompted to select their preferred dish from the available options. The app then displays a list of restaurants associated with the selected meal, from which users can select their favorite restaurant.

To use the program, users must have a valid Yelp API key and a valid YouTube API key, which they must enter into the "config.py" file. Once the API key is set, the user can run the program and interact with it from the command line.

## Requirements:

* Python 3.6 or higher
* Google API Client Library (can be installed using pip: pip install google-api-python-client)
* Yelp API Key (obtained from the Yelp Developers website)

## Data Structure:

The data is organized into a nested dictionary structure, with cuisines at the top and topics at the second. Each topic contains a list of videos and a list of restaurants, and each topic has its own information, such as video ID, title, description, restaurant name, rating, review, and address.

## example:##  
- How many cuisines would you like to search for? 3
  - Enter cuisine 1: asian food  
  - How many topics for asian food? 3
    - Enter topic 1: sushi
    - Enter topic 2: ramen
    - Enter topic 3: chinese dumplings 

  - Enter cuisine 2: american food 
  - How many topics for american food? 3
    - Enter topic 1: hamburgers
    - Enter topic 2: barbecue recipes
    - Enter topic 3: mac and cheese 

  - Enter cuisine 3: italian food
  - How many topics for italian food? 3 
    - Enter topic 1: pasta dishes  
    - Enter topic 2: pizza recipes
    - Enter topic 3: italian desserts

Enter location: New York, NY


## Required Python package:

* import json 
* import requests 

