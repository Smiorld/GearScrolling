from Classes import *
from functools import lru_cache
from typing import Union
import csv, copy
from itertools import permutations

basegears = BaseGears()
basegears.load_from_file()
scrolls = Scrolls()
scrolls.load_from_file()

def one_step_scroll(scroll:Scroll, gear: Gear):
    gear.scroll_sequence.append(scroll)
    gear.price_ev = (gear.price_ev + scroll.price)*(1 / scroll.success_chance)
    gear.success_rate = gear.success_rate * scroll.success_chance
    gear.survival_rate = gear.survival_rate * scroll.survival_chance
    gear.gear_number_ev = gear.gear_number_ev * (1 / scroll.success_chance)
    
@lru_cache(maxsize=None)
def sequence_scroll(scroll_sequence: tuple[Scroll], gear: BaseGear):
    '''Scrolls the gear with the given sequence of scrolls'''
    if len(scroll_sequence) == 0 or gear.tot_slots < len(scroll_sequence):
        return False, "gear has less slots than given scrolls, or no scrolls given"
    tmp_gear = Gear(gear.name, gear.category, gear.clean_price, gear.tot_slots)
    for scroll in scroll_sequence:
        one_step_scroll(scroll, tmp_gear)
    return True, tmp_gear

def output_scroll_sequence(scroll_sequence: tuple[Scroll], gear: BaseGear, filename:str = 'output.csv'):
    '''Outputs the result to csv of scrolling the gear with the given sequence of scrolls'''
    while True:
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['','gear name', 'category', 'scroll stat', 'clean price', 'total slots'])
                writer.writerow(['gear',gear.name, gear.category, scroll_sequence[0].stat, gear.clean_price, gear.tot_slots])
                writer.writerow([])
                writer.writerow(['scroll type', '10%', '30%', '60%', '70%', '100%'])
                scroll_10p = scrolls.get(gear.category, scroll_sequence[0].stat, 0.1)
                scroll_30p = scrolls.get(gear.category, scroll_sequence[0].stat, 0.3)
                scroll_60p = scrolls.get(gear.category, scroll_sequence[0].stat, 0.6)
                scroll_70p = scrolls.get(gear.category, scroll_sequence[0].stat, 0.7)
                scroll_100p = scrolls.get(gear.category, scroll_sequence[0].stat, 1)
                price_10p = scroll_10p.price if scroll_10p is not None else 'no data'
                price_30p = scroll_30p.price if scroll_30p is not None else 'no data'
                price_60p = scroll_60p.price if scroll_60p is not None else 'no data'
                price_70p = scroll_70p.price if scroll_70p is not None else 'no data'
                price_100p = scroll_100p.price if scroll_100p is not None else 'no data'
                writer.writerow(['scroll price', price_10p, price_30p, price_60p, price_70p, price_100p])
                writer.writerow([])
                writer.writerow(['Slots\\columns','scrolls', 'cost EV', 'pass rate', 'survival rate', 'gears usage'])
                tmp_gear = Gear(gear.name, gear.category, gear.clean_price, gear.tot_slots)
                for index, scroll in enumerate(scroll_sequence):
                    one_step_scroll(scroll, tmp_gear)
                    writer.writerow([index+1, scroll.success_chance, tmp_gear.price_ev, tmp_gear.success_rate, tmp_gear.survival_rate, tmp_gear.gear_number_ev])
            return filename
        except PermissionError as e:
            input(f"Please close the file {filename} and press enter to continue")
            continue

def find_best_order(scroll_sequence: tuple[Scroll], gear: BaseGear):
    '''Finds the best order of given scrolls for the gear'''
    orders = permutations(range(len(scroll_sequence)))
    best_sequence = None
    best_gear = None
    for order in orders:
        tmp_scroll_sequence = []
        for i in order:
            tmp_scroll_sequence.append(scroll_sequence[i])
        success, tmp_gear = sequence_scroll(tuple(tmp_scroll_sequence), gear)
        if success and type(tmp_gear)==Gear:
            if best_gear is None or tmp_gear.price_ev < best_gear.price_ev:
                best_sequence = tmp_scroll_sequence
                best_gear = tmp_gear
        else:
            return False, tmp_gear
    return True, (best_sequence , best_gear)

    
    
def find_best_sequence(statresult:list[int], gear: BaseGear, stat:str):
    '''Finds the best scrolling sequence of expected stats for the gear
    statresult: [ 10%+30% success number, 60%+70% success number ]
    '''
    success, scroll_sequences = generate_sequences_form_statresult(statresult, gear, stat)
    if not success:
        return False, scroll_sequences
    # which means scrolL_sequences is a list of tuples of scrolls
    best_sequence = None
    best_gear = None
    for scroll_sequence in scroll_sequences:
        success, tmp_result = find_best_order(scroll_sequence, gear) # type: ignore
        if success:
            if best_gear is None or  tmp_result[1].price_ev < best_gear.price_ev:   # type: ignore
                best_gear = tmp_result[1]                                           # type: ignore
                best_sequence = tmp_result[0]                                       # type: ignore
    return True, best_sequence


def generate_sequences_form_statresult(statresult:list[int], gear: BaseGear, stat:str):
    '''Generates all possible sequences of scrolls that can give the given statresult'''
    scroll_sequences = []
    all_scrolls = scrolls.search(category=gear.category, stat=stat)
    if len(all_scrolls) == 0:
        return False, "no available scrolls found"
    if len(statresult) != 2:
        return False, "statresult must be a list of 2 int"
    if statresult[0] < 0 or statresult[1] < 0:
        return False, "statresult must be non-negative"
    if statresult[0] + statresult[1] > gear.tot_slots:
        return False, "scrolls must be less than gear's total slots"
    scroll_10p = None
    scroll_30p = None
    scroll_60p = None
    scroll_70p = None
    for scroll in all_scrolls:
        if scroll.success_chance == 0.1:
            scroll_10p = scroll
        elif scroll.success_chance == 0.3:
            scroll_30p = scroll
        elif scroll.success_chance == 0.6:
            scroll_60p = scroll
        elif scroll.success_chance == 0.7:
            scroll_70p = scroll
    if statresult[0] > 0:
        if scroll_10p is None or scroll_30p is None:
            return False, f"please add {gear.category} {stat} 10p and 30p scrolls to the data"
    if statresult[1] > 0:
        if scroll_60p is None or scroll_70p is None:
            return False, f"please add {gear.category} {stat} 60p and 70p scrolls to the data"
    for i in range(statresult[0]+1):
        for j in range(statresult[1]+1):
            scroll_sequence = []
            for k in range(i):
                scroll_sequence.append(scroll_10p)
            for k in range(statresult[0]-i):
                scroll_sequence.append(scroll_30p)
            for k in range(j):
                scroll_sequence.append(scroll_60p)
            for k in range(statresult[1]-j):
                scroll_sequence.append(scroll_70p)
            scroll_sequences.append(tuple(scroll_sequence)) 
    return True, scroll_sequences


        
   