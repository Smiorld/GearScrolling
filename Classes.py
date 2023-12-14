import json
class BaseGear:
    '''Class that represents a gear, with its name, clean price and total slots'''
    def __init__(self, name, category, clean_price, tot_slots):
        self.name :str = name
        self.category :str = category
        self.clean_price :float = clean_price
        self.tot_slots :int= tot_slots
    
class Gear(BaseGear):
    '''Class that represents a gear, with its name, clean price, total slots and scrolled stats'''
    def __init__(self, name, category, clean_price, tot_slots, scroll_sequence=[], price_ev=0.0, success_rate=1.0, survival_rate=1.0, gear_number_ev=0.0):
        super().__init__(name, category, clean_price, tot_slots)
        self.scroll_sequence :list[Scroll] = scroll_sequence
        self.price_ev :float = clean_price if price_ev == 0.0 else price_ev
        self.success_rate :float = success_rate
        self.survival_rate :float = survival_rate
        self.gear_number_ev :float = gear_number_ev
        
    
    
class BaseGears:
    '''Class that represents a list of gears'''
    def __init__(self):
        self.gears :list[BaseGear] = []
    
    def get(self, name):
        '''Returns the gear with the given name, or None if it doesn't exist'''
        for gear in self.gears:
            if gear.name == name:
                return gear
        return None
    
    def add(self, name, category, clean_price, tot_slots):
        '''Adds a new gear to the list, returns True if added successfully, False if it already existed'''
        if name=='' or category=='':
            return False
        if self.get(name) == None:
            self.gears.append(BaseGear(name, category, clean_price, tot_slots))
        return True
        
        
    def update(self, name, category, clean_price, tot_slots):
        '''Updates the gear with the given name, or adds it if it doesn't exist'''
        tmp_gear = self.get(name)
        if tmp_gear != None:
            tmp_gear.clean_price = clean_price
            tmp_gear.tot_slots = tot_slots
            return True
        else:
            if self.add(name, category, clean_price, tot_slots):
                return True
            else:
                return False
    
    def search(self, name='', category='') -> list[BaseGear]:
        '''Returns the list of gears that match the given conditions'''
        result = []
        for gear in self.gears:
            if gear.name.find(name) != -1 and gear.category.find(category) != -1:
                result.append(gear)
        return result
    
    def load_from_file(self, file_name='gears.json'):
        '''Loads the gears from the given file'''
        try:
            with open(file_name, 'r') as file:
                # if no such file exists, return
                if file == None:
                    return
                data = json.load(file)
                for gear in data['gears']:
                    self.update(gear['name'], gear['category'], gear['clean_price'], gear['tot_slots'])
        except FileNotFoundError:
            return
        
    def save_to_file(self, file_name='gears.json'):
        '''Saves the gears to the given file'''
        with open(file_name, 'w') as file:
            data = {'gears':[]}
            for gear in self.gears:
                data['gears'].append({'name':gear.name, 'category':gear.category, 'clean_price':gear.clean_price, 'tot_slots':gear.tot_slots})
            json.dump(data, file, indent=4)
    
class Scroll:
    '''Class that represents a scroll, with its category, stat, chance and price'''
    def __init__(self, category, stat, success_chance, survival_chance, price ):
        self.category :str = category
        self.stat: str = stat
        self.success_chance :float = success_chance
        self.survival_chance :float = survival_chance
        self.price :float = price
    
class Scrolls:
    '''Class that represents a list of scrolls'''
    def __init__(self):
        self.scrolls :list[Scroll] = []
    
    def add(self, category, stat, success_chance, survival_chance, price):
        '''Adds a new scroll to the list, returns True if added successfully, False if it already existed'''
        if self.get(category, stat, success_chance) == None:
            self.scrolls.append(Scroll(category, stat, success_chance, survival_chance, price))
            return True
        return False
        
    def update(self, category, stat, success_chance, survival_chance, price):
        '''Updates the scroll with the given category and stat, or adds it if it doesn't exist'''
        tmp_scroll = self.get(category, stat, success_chance)
        if tmp_scroll != None:
            tmp_scroll.survival_chance = survival_chance
            tmp_scroll.price = price
        else:
            self.add(category, stat, success_chance, survival_chance, price)
    
    def get(self, category, stat, success_chance):
        '''Returns the scroll with the given category and stat, or None if it doesn't exist'''
        for scroll in self.scrolls:
            if scroll.category == category and scroll.stat == stat and scroll.success_chance == success_chance:
                return scroll
        return None

    def search(self, category='', stat='', success_chance=0.0):
        '''Returns the list of scrolls that match the given conditions'''
        result = []
        for scroll in self.scrolls:
            if success_chance == 0.0:
                if scroll.category.find(category) != -1 and scroll.stat.find(stat) != -1:
                    result.append(scroll)
            else:
                if scroll.category.find(category) != -1 and scroll.stat.find(stat) != -1 and scroll.success_chance == success_chance:
                    result.append(scroll)
        return result
    def load_from_file(self, file_name='scrolls.json'):
        '''Loads the scrolls from the given file'''
        # if no such file exists, return
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for scroll in data['scrolls']:
                    self.update(scroll['category'], scroll['stat'], scroll['success_chance'], scroll['survival_chance'], scroll['price'])
        except FileNotFoundError:
            return
    
    def save_to_file(self, file_name='scrolls.json'):
        '''Saves the scrolls to the given file'''
        with open(file_name, 'w') as file:
            data = {'scrolls':[]}
            for scroll in self.scrolls:
                data['scrolls'].append({'category':scroll.category, 'stat':scroll.stat, 'success_chance':scroll.success_chance, 'survival_chance':scroll.survival_chance, 'price':scroll.price})
            json.dump(data, file, indent=4)
            
