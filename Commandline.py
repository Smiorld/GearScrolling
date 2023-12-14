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
    2: "Single Analyze",
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
    elif cmd_status != 0:
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
    if cmd_status <= 1:
        if words[0]=='help' or words[0] == 'h':
            deal_home_help(words[1:])
        elif words[0]=='searchgear' or words[0]=='sg':
            deal_searchgear(words[1:])
        elif words[0]=='addgear' or words[0]=='ag':
            deal_addgear(words[1:])
        elif words[0]=='removegear' or words[0]=='rg':
            deal_removegear(words[1:])
        elif words[0]=='searchscroll' or words[0]=='ss':
            deal_searchscroll(words[1:])
        elif words[0]=='addscroll' or words[0]=='as':
            deal_addscroll(words[1:])
        elif words[0]=='removescroll' or words[0]=='rs':
            deal_removescroll(words[1:])
        elif words[0]=='quickcommand' or words[0]=='qc':
            deal_quickcommand(words[1:])
        elif words[0]=='singleanalyse' or words[0]=='sa':
            cmd_status = 2  
            deal_singleanalyse_help(words[1:])
    if cmd_status == 2:
        if words[0]=='help' or words[0] == 'h':
            deal_singleanalyse_help(words[1:])
        elif words[0]=='start' or words[0]=='s':
            deal_singleanalyse_start(words[1:])
        elif words[0]=='home':
            cmd_status = 1
            deal_home_help(words[1:])
    clear_screen()
    ready_to_output += '\n'
    ready_to_output += f"Last Command: {colored(input,"blue")}"
    
# home page commands
        
def deal_home_help(words:list[str]):
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
    ready_to_output += colored("RemoveGear ","yellow")+"name=[name]: remove a specific gear with the given name\n"
    ready_to_output += "\n"
    ready_to_output += colored("SearchScroll ","yellow")+"category=[category] stat=[stat] success_chance=[success_chance]: search the information of the scroll with the given name\n"
    ready_to_output += "\n"
    ready_to_output += colored("AddScroll ","yellow")+"category=[category] stat=[stat] success_chance=[success_chance] price=[price] (survival_chance=[survival_chance]): add or update a new scroll with the given information\n"
    ready_to_output += "\n"
    ready_to_output += colored("RemoveScroll ","yellow")+"category=[category] stat=[stat] success_chance=[success_chance]: remove a specific scroll with the given condition\n"
    ready_to_output += "\n"
    ready_to_output += colored("QuickCommand ","yellow")+"filename=[filename]: load and excute commands from a file (only red command supported)\n"
    ready_to_output += "\n"
    ready_to_output += colored("SingleAnalyse ","red")+" : tool - generate analysis besed on a single scrolling sequence and gear\n"
    
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
    return

def deal_removegear(words:list[str]):
    global cmd_status, ready_to_output, basegears
    gear={'name':''}
    exist_equal = False
    for word in words:
        if word.startswith('name='):
            exist_equal = True
            gear['name'] = word[5:]
    if not exist_equal:
        if 0<len(words):
            gear['name'] = words[0]
    tmp_basegear = basegears.get(gear['name'])
    if tmp_basegear is not None and basegears.remove(tmp_basegear):
        ready_to_output += f"Gear {gear['name']} removed successfully.\n"
    else:
        ready_to_output += f"Input not valid, please make sure there is a gear named '{gear['name']}'\n"
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
    return

def deal_removescroll(words:list[str]):
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
        if 2<len(words):
            tmp_success_chance = float(words[2])
            if tmp_success_chance <= 1:
                scroll['success_chance'] = tmp_success_chance
            else:
                scroll['success_chance'] = tmp_success_chance/100
    tmp_scroll = scrolls.get(scroll['category'], scroll['stat'], scroll['success_chance'])
    if tmp_scroll is not None and scrolls.remove(tmp_scroll):
        ready_to_output += f"Scroll {scroll} removed successfully.\n"
    else:
        ready_to_output += f"Input not valid, please make sure there is a scroll named '{scroll['category']} {scroll['stat']} {scroll['success_chance']}'\n"
    return

# quick command

def deal_quickcommand(words:list[str]):
    global cmd_status, ready_to_output
    filename = ''
    exist_equal = False
    for word in words:
        if word.startswith('filename='):
            exist_equal = True
            filename = word[9:]
    if not exist_equal:
        if 0<len(words):
            filename = words[0]
    if len(filename) == 0:
        ready_to_output += f"Input not valid, please make sure there is a filename.\n"
        return
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            ready_to_output += f"Input not valid, please make sure the file '{filename}' is not empty.\n"
            return
        command = lines[0].strip().lower()
        # check if command is valid. If valid, execute it.
        if command =="singleanalyse" or command =="sa":
            gear_name = lines[1].strip().lower()
            if len(gear_name) == 0:
                ready_to_output += f"QuickCommand not valid. please make sure there is gear name.\n"
                return
            gear = basegears.get(gear_name)
            if gear is None:
                ready_to_output += f"QuickCommand not valid, please make sure there is a gear named '{gear_name}'.\n"
                return
            stat = lines[2].strip().lower()
            if len(stat) == 0:
                ready_to_output += f"QuickCommand not valid. please make sure there is stat.\n"
                return
            scroll_sequence = []
            for i in range(3, len(lines)):
                try:
                    if len(lines[i].strip()) == 0:
                        continue
                    success_chance = float(lines[i].strip().lower())
                except ValueError:
                    ready_to_output += f"QuickCommand not valid. please make sure there are valid success chance.\n"
                    return
                if success_chance > 1:
                    success_chance = success_chance/100
                scroll = scrolls.get(gear.category, stat, success_chance)
                if scroll is None:
                    ready_to_output += f"QuickCommand not valid, please make sure there is a scroll named '{gear.category} {stat} {success_chance}'.\n"
                    return
                scroll_sequence.append(scroll)
            scroll_sequence = tuple(scroll_sequence)
            filename = output_scroll_sequence(scroll_sequence, gear) # type: ignore
            ready_to_output += f"QuickCommand executed successfully. Result has been output to {colored(filename,"cyan")}\n"
        else:
            ready_to_output += f"QuickCommand not valid, please make sure file start with a valid command.\n"
            return
    except FileNotFoundError:
        ready_to_output += f"Input not valid, please make sure there is a file named '{filename}'.\n"
        return
    except Exception as e:
        ready_to_output += f"Input not valid, please check the file '{filename}'.\n"
        return
    return

# scroll analizer page commands

def deal_singleanalyse_help(words:list[str]):
    global cmd_status, ready_to_output
    ready_to_output += "Welcome to single analyse page. Here's the available commdans.\n"
    ready_to_output += "\n"
    ready_to_output += colored("Help ","yellow")+": show this help message\n"
    ready_to_output += "\n"
    ready_to_output += colored("exit ","yellow")+": exit the program\n"
    ready_to_output += "\n"
    ready_to_output += colored("home ","yellow")+": back to home page\n"
    ready_to_output += "\n"
    ready_to_output += colored("Start ","yellow")+": function entrance, start analysing.\n"
    
def deal_singleanalyse_start(words:list[str]):
    global cmd_status, ready_to_output, scrolls, basegears
    # the process as follow:
    # 1. get gear info. use gears.get() to get the gear, if not exist, back to single analse page.
    # 2. get stat, then use scrolls.search() to get the scroll list, if not exist, back to single analse page.
    # 3. repeatedly asking to select scroll to fill in a list[scroll] as the scroll sequence. waiting for empty input to stop.
    # 4. use scroll sequence and gear to calculate the result.
    # 5. output the result.
    clear_screen()
    text = input("please input the exact gear name (no space): ")
    basegear = basegears.get(text.strip().lower())
    if basegear is None:
        ready_to_output += f"Gear named '{text.strip().lower()}' not found, please check your gear data.\n"
        return
    # get stat
    clear_screen()
    text = input("please input the exact stat name: ")
    stat = text.strip().lower()
    # get scroll list
    scroll_list = scrolls.search(basegear.category, stat)
    if len(scroll_list) == 0:
        ready_to_output += f"Scroll for {basegear.category} {stat} not found, please check your scroll data.\n"
        return
    # get scroll sequence. into a loop, waiting for empty input to stop.
    scroll_sequence = []
    while True:
        clear_screen()
        for index, scroll in enumerate(scroll_list):
            print(f"{index}:{scroll}")
        print("")
        print(f"Current scroll sequence: {scroll_sequence}\n")
        print(f"Please input scroll chance to specify which scroll to add. Press enter without anything to exit: ")
        text = input().lower().strip()
        if len(text)== 0:
            break
        try:
            text=float(text)
        except ValueError:
            continue
        if text >1:
            text = text/100
        tmp_scroll = scrolls.get(basegear.category, stat, float(text))
        if tmp_scroll is None:
            continue
        scroll_sequence.append(tmp_scroll) 
    
    # calculate result
    scroll_sequence = tuple(scroll_sequence)
    filename = output_scroll_sequence(scroll_sequence, basegear) # type: ignore
    ready_to_output += f"QuickCommand:\n"
    ready_to_output += f"{colored("sa","red")}\n"
    ready_to_output += f"{colored(basegear.name,"red")}\n"
    ready_to_output += f"{colored(stat,"red")}\n"
    for scroll in scroll_sequence:
        ready_to_output += f"{colored(scroll.success_chance,"red")}\n"
    ready_to_output += f"\n"
    ready_to_output += f"you can copy above QuickCommand (red text) to a .txt file and use QuickCommand in home page to excute it.\n"
    
    ready_to_output += f"result has been output to {colored(filename,"cyan")}\n"