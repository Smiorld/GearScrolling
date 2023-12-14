# TODO: print some color. structure current output pannels. add more commands.
from Classes import BaseGears, Scrolls, Gear
from Methods import *
import csv, os
from termcolor import colored, cprint

cmd_status = 0  
ready_to_output = ''
status_dict ={
    0: "Initial",
    1: "Home",
    2: "",
}

def clear_screen():
    os.system('cls')
    cprint(f"-----{status_dict[cmd_status]} Page-----", 'green')
    print(f"")

def display_default_info():
    global cmd_status, ready_to_output
    if cmd_status == 0:
        # program starts, print welcome message
        print(f"Welcome to use GearScrolling Tool developed by T2Julius!")
        print(f"")
        print(f"Type 'help' for a list of commands.")
        cmd_status = 1   
    elif cmd_status == 1:
        # home page, print home page
        cprint(ready_to_output)
        ready_to_output = ''
    else:
        print(f"Command not valud, you can use 'help' to see a list of commands.")
    print(f"")
    cprint(f"Please enter a command:",'green')

def parse_cmd_input(input:str):
    global cmd_status, ready_to_output
    clear_screen()
    print(f"Command: {input}")
    print(f"Processing...")
    words = input.lower().strip().split()
    if words[0]=='help' or words[0] == 'h':
        deal_help(words[1:])
    elif words[0]=='searchgear' or words[0]=='sg':
        deal_searchgear(words[1:])
    elif words[0]=='addgear' or words[0]=='ag':
        deal_addgear(words[1:])
    elif words[0]=='searchscroll' or words[0]=='ss':
        deal_searchscroll(words[1:])
    elif words[0]=='addscroll' or words[0]=='as':
        deal_addscroll(words[1:])
    ready_to_output += '\n'
    ready_to_output += f"Last Command: {colored(input,"blue")}"
    clear_screen()
    

        
def deal_help(words:list[str]):
    global cmd_status, ready_to_output
    ready_to_output += "All commands are not case-insensitive. () means optional, [] should be replaced by your real input.\n"
    ready_to_output += "The upper case of the characters in below commands can be used as alias.\n"
    ready_to_output += "e.g. " + colored("SearchGear","yellow") + ", " + colored("searchgear","yellow") + " and "+colored("sg","yellow")+" works the same.\n"
    ready_to_output += "And "+colored("xxx=","yellow")+" can be ignored, e.g. "+colored("SearchGear name=abc","yellow")+" and "+colored("SearchGear abc","yellow")+" works the same.\n"
    ready_to_output += "\n"
    ready_to_output += "\n"
    ready_to_output += colored("Help","yellow")+": show this help message\n"
    ready_to_output += "\n"
    ready_to_output += colored("exit","yellow")+": save and exit the program\n"
    ready_to_output += "\n"
    ready_to_output += colored("SearchGear ","yellow")+"name=[name] category=[category]: search the information of the gear with the given condition\n"
    ready_to_output += "\n"
    ready_to_output += colored("AddGear ","yellow")+"name=[name] category=[category] clean_price=[clean_price] tot_slots=[tot_slots]: add or update a new gear with the given information\n"
    ready_to_output += "\n"
    ready_to_output += colored("SearchScroll ","yellow")+"category=[category] stat=[stat] success_chance=[success_chance]: search the information of the scroll with the given name\n"
    ready_to_output += "\n"
    ready_to_output += colored("AddScroll ","yellow")+"category=[category] stat=[stat] success_chance=[success_chance] price=[price] (survival_chance=[survival_chance]): add or update a new scroll with the given information\n"
    
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
        ready_to_output += f"Search Result:\n\n"
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
        ready_to_output += f"Gear {gear['name']} updated and saved successfully.\n"
    else:
        ready_to_output += f"Input not valid, please make sure both name and category are not empty.\n"
    basegears.save_to_file()
    return

def deal_searchscroll(words:list[str]):
    global cmd_status, ready_to_output, scrolls
    scroll={'category':'', 'stat':'', 'success_chance':0.0}
    exist_equal = False
    for word in words:
        if word.startswith('category='):
            exist_equal = True
            scroll['category'] = word[9:]
        elif word.startswith('stat='):
            exist_equal = True
            scroll['stat'] = word[5:]
        elif word.startswith('success_chance='):
            exist_equal = True
            tmp_success_chance = float(word[15:])
            if tmp_success_chance <= 1:
                scroll['success_chance'] = tmp_success_chance
            else:
                scroll['success_chance'] = tmp_success_chance/100
    if not exist_equal:
        if 0<len(words):
            scroll['category'] = words[0]
        if 1<len(words):
            scroll['stat'] = words[1]
    search_result = scrolls.search(scroll['category'], scroll['stat'], scroll['success_chance'])
    # here's a thing, limited by screen size, if more than 10 results, output to csv file
    if len(search_result)>10:
        with open('search_result.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['category', 'stat', 'success_chance', 'survival_chance', 'price'])
            for scroll in search_result:
                writer.writerow([scroll.category, scroll.stat, scroll.success_chance, scroll.survival_chance, scroll.price])
        ready_to_output += f"Search result is too large, please check search_result.csv for details."
    else:
        ready_to_output += f"Search Result:\n\n"
        for scroll in search_result:
            ready_to_output += f"Category: {scroll.category}, Stat: {scroll.stat}, Success Chance: {scroll.success_chance}, Survival Chance: {scroll.survival_chance}, Price: {scroll.price}\n"
    return

def deal_addscroll(words:list[str]):
    global cmd_status, ready_to_output, scrolls
    scroll={'category':'', 'stat':'', 'success_chance':0.0, 'price':0.0, 'survival_chance':0.0 }
    exist_equal = False
    for word in words:
        if word.startswith('category='):
            exist_equal = True
            scroll['category'] = word[9:]
        elif word.startswith('stat='):
            exist_equal = True
            scroll['stat'] = word[5:]
        elif word.startswith('success_chance='):
            exist_equal = True
            tmp_success_chance = float(word[15:])
            if tmp_success_chance <= 1:
                scroll['success_chance'] = tmp_success_chance
            else:
                scroll['success_chance'] = tmp_success_chance/100
        elif word.startswith('price='):
            exist_equal = True
            scroll['price'] = float(word[6:])
        elif word.startswith('survival_chance='):
            exist_equal = True
            tmp_survival_chance = float(word[16:])
            if tmp_survival_chance <= 1:
                scroll['survival_chance'] = tmp_survival_chance
            else:
                scroll['survival_chance'] = tmp_survival_chance/100
        
    if not exist_equal:
        if 0<len(words):
            scroll['category'] = words[0]
        if 1<len(words):
            scroll['stat'] = words[1]
        if 2<len(words):
            tmp_success_chance = float(words[2])
            if tmp_success_chance <= 1:
                scroll['success_chance'] = tmp_success_chance
            else:
                scroll['success_chance'] = tmp_success_chance/100
        if 3<len(words):
            scroll['price'] = float(words[3])
        if 4<len(words):
            tmp_survival_chance = float(words[4])
            if tmp_survival_chance <= 1:
                scroll['survival_chance'] = tmp_survival_chance
            else:
                scroll['survival_chance'] = tmp_survival_chance/100
    if scroll['survival_chance'] == 0:
        if scroll['success_chance'] == 0.1:
            scroll['survival_chance'] = 1
        elif scroll['success_chance'] == 0.3:
            scroll['survival_chance'] = 0.65
        elif scroll['success_chance'] == 0.6:
            scroll['survival_chance'] = 1
        elif scroll['success_chance'] == 0.7:
            scroll['survival_chance'] = 0.85
        elif scroll['success_chance'] == 1:
            scroll['survival_chance'] = 1
    
    if scrolls.update(scroll['category'], scroll['stat'], scroll['success_chance'], scroll['survival_chance'], scroll['price']):
        ready_to_output += f"Scroll {scroll} updated and saved successfully.\n"
    else:
        ready_to_output += f"Input not valid, please make sure category, stat, success_chance are not empty.\n"
    scrolls.save_to_file()
    return