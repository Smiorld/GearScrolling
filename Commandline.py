# TODO: print some color. structure current output pannels. add more commands.
from Classes import BaseGears, Scrolls, Gear
import csv, os
basegears = BaseGears()
basegears.load_from_file()
scrolls = Scrolls()
scrolls.load_from_file()

cmd_status = 0  
ready_to_output = ''
status_dict ={
    0: "Initial",
    1: "Home",
    2: "",
}

def clear_screen():
    os.system('cls')

def display_default_info():
    global cmd_status, ready_to_output
    print(f"-----{status_dict[cmd_status]} Page-----")
    print(f"")
    if cmd_status == 0:
        # program starts, print welcome message
        print(f"Welcome to use GearScrolling Tool developed by T2Julius!")
        print(f"")
        print(f"Type 'help' for a list of commands.")
        cmd_status = 1   
    elif cmd_status == 1:
        # home page, print home page
        print(ready_to_output)
        ready_to_output = ''
    else:
        print(f"Command not valud, you can use 'help' to see a list of commands.")
    print(f"")
    print(f"Please enter a command:")

def parse_cmd_input(input:str):
    global cmd_status, ready_to_output
    clear_screen()
    print(f"-----{status_dict[cmd_status]} Page-----")
    print(f"")
    print(f"Command: {input}")
    print(f"Processing...")
    words = input.lower().strip().split()
    if words[0]=='help' or words[0] == 'h':
        deal_help(words[1:])
    elif words[0]=='searchgear' or words[0]=='sg':
        deal_searchgear(words[1:])
    elif words[0]=='addgear' or words[0]=='ag':
        deal_addgear(words[1:])
    clear_screen()
    

        
def deal_help(words:list[str]):
    global cmd_status, ready_to_output
    ready_to_output += "All commands are not case-insensitive. () means optional, [] should be replaced by your real input.\n"
    ready_to_output += "The upper case of the characters in below commands can be used as alias.\n"
    ready_to_output += "e.g. 'SearchGear', 'searchgear' and 'sg' works the same.\n"
    ready_to_output += "And xxx= can be ignored, e.g. 'SearchGear name=abc' and 'SearchGear abc' works the same.\n"
    ready_to_output += "\n"
    ready_to_output += "\n"
    ready_to_output += "Help: show this help message\n"
    ready_to_output += "\n"
    ready_to_output += "exit: save and exit the program\n"
    ready_to_output += "\n"
    ready_to_output += "SearchGear name=[name] category=[category]: search the information of the gear with the given condition\n"
    ready_to_output += "\n"
    ready_to_output += "AddGear name=[name] category=[category] clean_price=[clean_price] tot_slots=[tot_slots]: add or update a new gear with the given information\n"
    ready_to_output += "\n"
    ready_to_output += "SearchScroll category=[category] stat=[stat]: search the information of the scroll with the given name\n"
    ready_to_output += "\n"
    
def deal_searchgear(words:list[str]):
    global cmd_status, ready_to_output, basegears
    gear={'name':'', 'category':''}
    exist_equal = False
    for word in words:
        if word.startswith('name='):
            exist_equal = True
            gear['name'] = word[5:]
        elif word.startswith('category='):
            exist_equal = True
            gear['category'] = word[9:]
    if not exist_equal:
        if 0<len(words):
            gear['name'] = words[0]
        if 1<len(words):
            gear['category'] = words[1]
    search_result = basegears.search(gear['name'], gear['category'])
    # here's a thing, limited by screen size, if more than 10 results, output to csv file
    if len(search_result)>10:
        with open('search_result.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'category', 'clean_price', 'tot_slots'])
            for gear in search_result:
                writer.writerow([gear.name, gear.category, gear.clean_price, gear.tot_slots])
        ready_to_output += f"Search result is too large, please check search_result.csv for details."
    else:
        for gear in search_result:
            ready_to_output += f"Name: {gear.name}, Category: {gear.category}, Clean Price: {gear.clean_price}, Total Slots: {gear.tot_slots}\n"
    return

def deal_addgear(words:list[str]):
    global cmd_status, ready_to_output, basegears
    gear={'name':'', 'category':'', 'clean_price':0.0, 'tot_slots':0}
    exist_equal = False
    for word in words:
        if word.startswith('name='):
            exist_equal = True
            gear['name'] = word[5:]
        elif word.startswith('category='):
            exist_equal = True
            gear['category'] = word[9:]
        elif word.startswith('clean_price='):
            exist_equal = True
            gear['clean_price'] = float(word[12:])
        elif word.startswith('tot_slots='):
            exist_equal = True
            gear['tot_slots'] = int(word[10:])
    if not exist_equal:
        if 0<len(words):
            gear['name'] = words[0]
        if 1<len(words):
            gear['category'] = words[1]
        if 2<len(words):
            gear['clean_price'] = int(words[2])
        if 3<len(words):
            gear['tot_slots'] = int(words[3])
    if basegears.update(gear['name'], gear['category'], gear['clean_price'], gear['tot_slots']):
        ready_to_output += f"Gear {gear['name']} updated and saved successfully."
    else:
        ready_to_output += f"Input not valid, please make sure both name and category are not empty."
    basegears.save_to_file()
    return
