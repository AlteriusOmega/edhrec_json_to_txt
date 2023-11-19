import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import requests
import re

def format_commander_name(commander_name:str):
    non_alphas_regex = "[^\w\s]" # Everything that's not alphanumeric or space
    formatted_name = re.sub(non_alphas_regex, "", commander_name)
    formatted_name = formatted_name.lower() # Make lowercase
    formatted_name = formatted_name.replace(" ", "-")  # Replace spaces with hyphens
    print(f"In format_commander_name and formatted name is {formatted_name}")
    return formatted_name

def request_json(commander_name:str):
    formatted_name = format_commander_name(commander_name)
    json_url = f"https://json.edhrec.com/pages/commanders/{formatted_name}.json"
    response = requests.get(json_url)
    if response.status_code == 200:
        json_data = response.json()
        print(f"JSON request successful! Json was {json_data}")
        return json_data
    else:
        print(f"JSON request failed! Try different commander name")

def browse_json_filepath():
    json_file_path = filedialog.askopenfilename(title="Select the EDHREC JSON file", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if json_file_path:
        print(f"Selected file {json_file_path}")
        return json_file_path
    else:
        print(f"Canceled")
        return None
    
def read_json_file(json_file_path):
    try:
        with open (json_file_path, "r") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def get_cardlists(json_data):
    card_lists = {}
    cardlist_json = json_data["container"]["json_dict"]
    commander_name = cardlist_json["card"]["name"]
    card_lists["Commander"] = [commander_name]
    specific_card_lists_data = cardlist_json["cardlists"] # This is list of dicts for some reason
    for cardlist in specific_card_lists_data: # Each cardlist should be a dict with a header of what list it is
        current_cardlist_name = cardlist["header"]
        current_cardlist_cards = []
        for card in cardlist["cardviews"]: # Each card should be dict
            current_card_name = card["name"]
            current_cardlist_cards.append(current_card_name)
        card_lists[current_cardlist_name] = current_cardlist_cards
    return card_lists

def save_info(cardlists:dict, output_directory:str):
    output_path = os.path.join(output_directory, "Info.txt")
    infos = []
    card_counts = {}
    for cardlist_name, cardlist in cardlists.items():
        card_counts[cardlist_name] = 0
        for card in cardlist:
            card_counts[cardlist_name] += 1

    infos.append(card_counts)
    
    with open (output_path, "w") as info_file:
        for info in infos:
            for key, value in info.items():
                info_file.write(f"{key}: {value}\n")
    return

def prompt_output_directory():
    print(f"Select folder to save cardlist txt files")
    output_directory = filedialog.askdirectory(title="Select output directory")
    if not (output_directory):
        print(f"Canceled")
        return
    return output_directory

def save_cardlists(cardlists: dict, output_directory):
    for cardlist_name, cardlist in cardlists.items():
        output_file_path = f"{output_directory}/{cardlist_name}.txt"
        with open(output_file_path, "w", newline="") as file:
            for card_name in cardlist:
                file.write(f"{card_name}\n")
        print(f"Card list '{cardlist_name}' saved to file '{output_file_path}'")

def flatten_cardlists(cardlists:dict):
    flat_cardlist = {"Flat Cardlist": []}
    for cardlist_name, cardlist in cardlists.items():
        for card_name in cardlist:
            flat_cardlist["Flat Cardlist"].append(card_name)
    return flat_cardlist

def main():
    root = tk.Tk()
    root.withdraw() # Hides main window
    # print(f"Select a JSON file:")
    # json_filepath = browse_json_filepath()
    # if not json_filepath: return
    # json_data = read_json_file(json_filepath)
    print(f"Type commander name. Make sure spelling and spaces are correct. Capitalization and symbols don't matter")
    commander_name = input("Commander name:")
    json_data = request_json(commander_name)
    cardlists = get_cardlists(json_data)
    # Make flattened cardlist
    flat_cardlist = flatten_cardlists(cardlists)
    cardlists.update(flat_cardlist)
    output_directory = prompt_output_directory()
    save_cardlists(cardlists, output_directory)
    save_info(cardlists, output_directory)

if __name__ == "__main__":
    main()
