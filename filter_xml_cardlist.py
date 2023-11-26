from tkinter import filedialog
import xml.etree.ElementTree as XET
import re
from copy import deepcopy
from bisect import bisect_left

def format_card_name(card_name:str):
    non_alphas_regex = "[^\w\s]" # Everything that's not alphanumeric or space
    formatted_name = re.sub(non_alphas_regex, "", card_name)
    formatted_name = formatted_name.lower() # Make lowercase
    # print(f"In format_commander_name and formatted name is {formatted_name}")
    return formatted_name

def browse_filepath(title:str):
    filepath = filedialog.askopenfilename(title=title) #, filetypes=[("All files", "*.*")]
    if filepath:
        print(f"Selected file {filepath}")
        return filepath
    else:
        print(f"Canceled")
        return None
    
def read_decklist(filepath):
    try:
        with open (filepath, "r", newline="") as decklist:
            decklist = decklist.readlines()
            stripped_decklist = [cardname.strip() for cardname in decklist]
            return stripped_decklist
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def read_xml(xml_filepath):
    try:
        xml_tree = XET.parse(xml_filepath)
        return xml_tree
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def make_anti_decklist(formatted_decklist, formatted_xml_cardnames):
    # print(f"In make_anti_decklist and formatted_decklist is {formatted_decklist} \n\n and formatted_xml_cardnames is {formatted_xml_cardnames}")
    anti_decklist = []
    for cardname in formatted_xml_cardnames:
        # print(f"In make_anti_decklist and cardname is {cardname}")
        if cardname not in formatted_decklist:
            anti_decklist.append(cardname)
    return anti_decklist

def get_gap_sum_lower(fronts_removed, slot:int):
    sum_lower = 0
    for card in fronts_removed:
        this_card_slot = int(card.find("slots").text)
        if this_card_slot < slot:
            print(f"found lower slot, adding {this_card_slot} to sum_lower")
            sum_lower += 1
        else: break
    return sum_lower

def update_counts_2(xml_root, fronts_removed):
    xml_fronts = xml_root.find("fronts")
    xml_backs = xml_root.find("backs")
    xml_details = xml_root.find("details")
    new_slot_index = 0
    # Set fronts slots to ascending
    for card in xml_fronts:
        card.find("slots").text = str(new_slot_index)
        new_slot_index += 1
    # Calculate new back slots using gap sum
    for card in xml_backs:
        back_card_name = card.find('query').text
        print(f"slot for card {back_card_name}: {card.find('slots').text}")
        if back_card_name is not None:
            slot = int(card.find("slots").text)
            sum_lower = get_gap_sum_lower(fronts_removed, slot)
            new_slot = slot - sum_lower
            print(f"slot: {slot}, sum_lower: {sum_lower}, new_slot: {new_slot}")
            card.find("slots").text = str(new_slot)
    # Update total quantity
    xml_details.find("quantity").text = str(new_slot_index)

def make_filtered_xml_tree(filter_cardlist_formatted: list, xml_tree):
    xml_copy = deepcopy(xml_tree)
    xml_copy_root = xml_copy.getroot()
    xml_copy_fronts = xml_copy_root.find("fronts")
    xml_copy_backs = xml_copy_root.find("backs")
    fronts_to_remove = []
    backs_to_remove = []
    for front_card in xml_copy_fronts:
        card_name = front_card.find("query").text
        print(f"In make_filtered_xml_tree, card_name is {card_name}, slots: {front_card.find('slots').text}")
        if card_name not in filter_cardlist_formatted:
            print(f"card_name {card_name} not found in filter_cardlist_formatted")
            removed_card_slot = front_card.find("slots").text
            fronts_to_remove.append(front_card)
            for back_card in xml_copy_backs:
                current_back_card_slot = back_card.find("slots").text
                # print(f"current_back_card_slot: {current_back_card_slot}, removed_card_slot: {removed_card_slot}")
                if current_back_card_slot == removed_card_slot:
                    print(f"Found back card {back_card.find('query').text} with matching slot {current_back_card_slot}")
                    backs_to_remove.append(back_card)
    for card in fronts_to_remove:
        xml_copy_fronts.remove(card)
    for card in backs_to_remove:
        xml_copy_backs.remove(card)
    update_counts_2(xml_copy_root, fronts_to_remove)
    return xml_copy

def main():
    decklist_filepath = browse_filepath("Decklist txt file")
    xml_filepath = browse_filepath("MPC Fill xml file")
    decklist = read_decklist(decklist_filepath)
    xml_tree = read_xml(xml_filepath)
    xml_root = xml_tree.getroot()
    xml_fronts = xml_root.find("fronts")
    xml_cardnames = [card.find("query").text for card in xml_fronts]
    formatted_xml_cardnames = [format_card_name(card) for card in xml_cardnames]
    formatted_decklist = [format_card_name(card) for card in decklist]
    print(f"\n\n Formatted decklist:")
    for card_name in formatted_decklist:
        print(card_name)
    filtered_xml_tree = make_filtered_xml_tree(formatted_decklist, xml_tree)
    filtered_xml_tree.write("filtered_xml.xml", encoding="utf-8", xml_declaration=True)
    anti_decklist = make_anti_decklist(formatted_decklist, formatted_xml_cardnames)
    print(f"anti_decklist is: ")
    for card_name in anti_decklist:
        print(card_name)

if __name__ == "__main__":
    main()
