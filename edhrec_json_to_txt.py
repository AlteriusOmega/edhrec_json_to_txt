import json
import csv
import tkinter as tk
from tkinter import filedialog, simpledialog

def browse_json_filepath():
    json_file_path = filedialog.askopenfilename(title="Select the EDHREC JSON file", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if json_file_path:
        print(f"Selected file {json_file_path}")
        # json_to_csv(json_file_path)
        # print_json(json_file_path)
        # cardlists = get_cardlists(json_file_path)
        # save_cardlists(cardlists)
        return json_file_path
    else:
        print(f"Canceled")
        return None

def json_to_csv(json_file_path):
    try:
        with open (json_file_path, "r") as json_file:
            data = json.load(json_file)
            return data # TODO finish this!
    except:
        print(f"Error opening file!")

def print_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def get_cardlists(json_file_path):
    try:
        card_lists = {}
        with open (json_file_path, "r") as json_file:
            data = json.load(json_file)
            specific_card_lists_data = data["container"]["json_dict"]["cardlists"] # This is list of dicts for some reason
            for cardlist in specific_card_lists_data: # Each cardlist should be a dict with a header of what list it is
                current_cardlist_name = cardlist["header"]
                # print(f"Current cardlist header is {current_cardlist_name}")
                current_cardlist_cards = []
                for card in cardlist["cardviews"]: # Each card should be dict
                    current_card_name = card["name"]
                    # print(f"Current card name is {current_card_name}")
                    current_cardlist_cards.append(current_card_name)
                card_lists[current_cardlist_name] = current_cardlist_cards
        # print(f"card_lists is {card_lists}")
        return card_lists

    except Exception as e:
        print(f"Error reading JSON file: {e}")

def save_cardlists(cardlists: dict, file_format="txt"):
    output_directory = filedialog.askdirectory(title="Select output directory")

    if not (output_directory):
        print(f"Canceled")
        return
    
    for cardlist_name, cardlist in cardlists.items():
        output_file_path = f"{output_directory}/{cardlist_name}.{file_format}"
        
        with open(output_file_path, "w", newline="") as file:
            if file_format == "txt":
                    for card_name in cardlist:
                        file.write(f"{card_name}\n")
            elif file_format == "csv":
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Card Name']) # Write header
                for card_name in cardlist:
                    csv_writer.writerow([card_name])
            else:
                print(f"Unsupported file format: {file_format}")
                continue

        print(f"Card list '{cardlist_name}' saved to file '{output_file_path}'")

def flatten_cardlists(cardlists:dict):
    flat_cardlists = {"Flat Cardlist": []}
    for cardlist_name, cardlist in cardlists.items():
        for card_name in cardlist:
            flat_cardlists["Flat Cardlist"].append(card_name)
    return flat_cardlists

def prompt_file_format():
    root = tk.Tk()
    root.withdraw()

    file_format = simpledialog.askstring(
        title="Choose file format",
        prompt="Enter txt or csv",
        initialvalue="txt"
    )
    return file_format.lower()

def prompt_cardlists(): # TODO implement this
    result = None
    
    def on_submit(choice):
        nonlocal result
        result = choice
        root.destroy()

    root = tk.Tk()
    root.title("Choose card list: separate or one giant flat list")

    choice_var = tk.StringVar()

    option_separate = tk.Radiobutton(root, text="Separate", variable=choice_var, value="Separate")
    option_single = tk.Radiobutton(root, text="Single", variable=choice_var, value="Single")

    option_separate.pack()
    option_single.pack()

    submit_button = tk.Button(root, text="OK", command=lambda: on_submit(choice_var.get() ) )
    submit_button.pack()

    root.mainloop()

    return result

def main():
    root = tk.Tk()
    root.withdraw() # Hides main window

    print(f"Select a JSON file:")
    json_filepath = browse_json_filepath()
    if not json_filepath: return
    # print(f"Save as txt or csv?")
    cardlists = get_cardlists(json_filepath)
    # file_format = prompt_file_format()
    file_format = "txt"
    # cardlists_type = prompt_cardlists()
    # print(f"cardlists_type is {cardlists_type}")

    # Make flattened cardlist
    flat_cardlist = flatten_cardlists(cardlists)
    cardlists.update(flat_cardlist)
    save_cardlists(cardlists, file_format)

if __name__ == "__main__":
    main()
