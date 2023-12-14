from Classes import *
import csv

def one_step_scroll(scroll:Scroll, gear: Gear):
    gear.scroll_sequence.append(scroll)
    gear.price_ev = (gear.price_ev + scroll.price)*(1 / scroll.success_chance)
    gear.success_rate = gear.success_rate * scroll.success_chance
    gear.survival_rate = gear.survival_rate * scroll.survival_chance
    gear.gear_number_ev = gear.gear_number_ev * (1 / scroll.success_chance)
    
