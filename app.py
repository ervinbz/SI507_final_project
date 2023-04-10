import os
import json
import googleapiclient.discovery
from config import API_KEY

class DecisionNode:
    def __init__(self, question=None, yes=None, no=None, videos=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.videos = videos or []

    def add_video(self, video):
        self.videos.append(video)

def dict_to_tree(tree_dict):
    if not tree_dict or isinstance(tree_dict, list):
        return None
    question = tree_dict["question"]
    yes = dict_to_tree(tree_dict["yes"]) if tree_dict["yes"] else None
    no = dict_to_tree(tree_dict["no"]) if tree_dict["no"] else None
    videos = tree_dict.get("videos", [])
    return DecisionNode(question, yes, no, videos)

def node_to_dict(node):
    if not node:
        return None
    return {"question": node.question, "yes": node_to_dict(node.yes), "no": node_to_dict(node.no), "videos": node.videos}

def load_tree(filename):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return DecisionNode(None, None, None)
    with open(filename, 'r') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                print("Warning: The root of the tree in the file is a list. Creating an empty decision tree.")
                return DecisionNode(None, None, None)
            return dict_to_tree(data)
        except KeyError:
            print(f"Error: Malformed dictionary in {filename}. Could not construct decision tree.")
            return None


def tree_to_dict(tree):
    if not tree:
        return None
    question, yes, no = tree
    return {"question": question, "yes": tree_to_dict(yes), "no": tree_to_dict(no)}

def save_tree(node, filename):
    json_tree = node_to_dict(node)
    with open(filename, 'w') as file:
        json.dump(json_tree, file, indent=2)



def yes(prompt):
    answer = input(prompt)
    yesList = ["yes", "Yes", "y", "Y", "yep", "yup", "sure"]
    noList = ["no", "No", "n", "N", "nope",]
    if answer in yesList:
        return True
    elif answer in noList:
        return False
    else:
        print("You should type 'yes' or 'no' ")
        return yes(prompt)

def traverse_tree(node):
    if not node or not node.question:
        return node.videos
    user_input = yes(node.question + " (yes/no): ")
    if user_input:
        return traverse_tree(node.yes) if node.yes else []
    else:
        return traverse_tree(node.no) if node.no else []


def update_tree(node, path, video, question, filename):
    if node is None:
        return DecisionNode(question, DecisionNode(videos=[video]), None)

    if not path:
        if not node.question:
            node.add_video(video)
            save_tree(node, filename)
            return node
        else:
            new_yes_node = DecisionNode(videos=[*node.videos, video])
            new_no_node = DecisionNode(videos=node.videos)
            return DecisionNode(question, new_yes_node, new_no_node)
    if path[0] == 'yes':
        updated_node = DecisionNode(node.question, update_tree(node.yes, path[1:], video, question, filename), node.no, node.videos)
    else:
        updated_node = DecisionNode(node.question, node.yes, update_tree(node.no, path[1:], video, question, filename), node.videos)
    save_tree(updated_node, filename)
    return updated_node

def search_youtube(query, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(part="snippet", type="video", q=query, maxResults=5, videoDefinition="high")
    response = request.execute()
    return [(item['id']['videoId'], item['snippet']['title']) for item in response['items']]

def main():
    filename = 'decision_tree.json'
    try:
        root = load_tree(filename)
    except FileNotFoundError:
        root = DecisionNode()

    while True:
        action = input("Load saved video (1) or search for new results (2)?: ")
        if action == "1":
            videos = traverse_tree(root)
            if videos:
                for video in videos:
                    video_id, video_title = video['id'], video['title']
                    video_link = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"{video_title} ({video_link})")
            else:
                print("No saved video or decision tree available.")
        elif action == "2":
            query = input("Enter a search query: ")
            results = search_youtube(query, API_KEY)
            print("Search results:")
            for i, (video_id, title) in enumerate(results):
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                print(f"{i + 1}. {title} ({video_link})")
            index = int(input("Enter the index of the video to save: ")) - 1
            video_id, video_title = results[index]

            answer = yes("Do you want to save this video? (yes/no): ")
            if answer:
                question = input("Enter a question for this decision node: ")
                root = update_tree(root, [], {'id': video_id, 'title': video_title}, question, filename)

if __name__ == '__main__':
    main()

