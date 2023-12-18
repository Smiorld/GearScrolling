import json
import requests
class BaseGear:
    '''Class that represents a gear, with its name, clean price and total slots'''
    def __init__(self, name, category, clean_price, tot_slots):
        self.name :str = name
        self.category :str = category
        self.clean_price :float = clean_price
        self.tot_slots :int= tot_slots
    
    def __hash__(self):
        return hash((self.name, self.category, self.clean_price, self.tot_slots))
    
class Gear(BaseGear):
    '''Class that represents a gear, with its name, clean price, total slots and scrolled stats'''
    def __init__(self, name, category, clean_price, tot_slots, scroll_sequence=[], price_ev=0.0, success_rate=1.0, survival_rate=1.0, gear_number_ev=1.0):
        super().__init__(name, category, clean_price, tot_slots)
        self.scroll_sequence :list[Scroll] = scroll_sequence
        self.price_ev :float = clean_price if price_ev == 0.0 else price_ev
        self.success_rate :float = success_rate
        self.survival_rate :float = survival_rate
        self.gear_number_ev :float = gear_number_ev
        
    
    
class BaseGears:
    '''Class that represents a list of gears'''
    file_name :str = 'gears.json'
    
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
            self.save_to_file()
            return True
        else:
            return False
        
        
    def update(self, name, category, clean_price, tot_slots):
        '''Updates the gear with the given name, or adds it if it doesn't exist'''
        tmp_gear = self.get(name)
        if tmp_gear != None:
            tmp_gear.category = category
            tmp_gear.clean_price = clean_price
            tmp_gear.tot_slots = tot_slots
            self.save_to_file()
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
    
    def remove(self, gear: BaseGear):
        '''Remove the given gear from data'''
        self.gears.remove(gear)
        self.save_to_file()
    
    def load_from_file(self):
        '''Loads the gears from the given file'''
        try:
            with open(BaseGears.file_name, 'r') as file:
                # if no such file exists, return
                if file == None:
                    return
                data = json.load(file)
                for gear in data['gears']:
                    self.update(gear['name'], gear['category'], gear['clean_price'], gear['tot_slots'])
        except FileNotFoundError:
            return
        
    def save_to_file(self):
        '''Saves the gears to the given file'''
        with open(BaseGears.file_name, 'w') as file:
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
    def __str__(self) -> str:
        return f"{self.category} {self.stat} {self.success_chance} {self.price}"
    def __repr__(self) -> str:
        return f"{self.category} {self.stat} {self.success_chance} {self.price}"
    
    def __hash__(self):
        return hash((self.category, self.stat, self.success_chance, self.survival_chance, self.price))
        
    
class Scrolls:
    '''Class that represents a list of scrolls'''
    file_name :str = 'scrolls.json'
    
    def __init__(self):
        self.scrolls :list[Scroll] = []
    
    def add(self, category, stat, success_chance, survival_chance, price):
        '''Adds a new scroll to the list, returns True if added successfully, False if it already existed'''
        if category=='' or stat=='' or success_chance==0.0:
            return None
        tmp_scroll = Scroll(category, stat, success_chance, survival_chance, price)
        self.scrolls.append(tmp_scroll)
        self.save_to_file()
        return tmp_scroll
        
    def update(self, category, stat, success_chance, survival_chance, price):
        '''Updates the scroll with the given category and stat, or adds it if it doesn't exist'''
        tmp_scroll = self.get(category, stat, success_chance)
        if tmp_scroll != None:
            tmp_scroll.survival_chance = survival_chance
            tmp_scroll.price = price
            self.save_to_file()
            return True
        else:
            if self.add(category, stat, success_chance, survival_chance, price):
                return True
            return False
    
    def load_from_owlrepo_data(self, category, stat, success_chance=0.0):
        '''load scrolls not in data from owlrepo'''
        if category=='' or stat=='':
            return False
        if success_chance == 0:
            # try load 10, 30, 60, 70, 100 from owlrepo
            has_p10 = False
            has_p30 = False
            has_p60 = False
            has_p70 = False
            has_p100 = False
            for scroll in self.scrolls:
                if scroll.category == category and scroll.stat == stat:
                    if scroll.success_chance == 0.1:
                        has_p10 = True
                    elif scroll.success_chance == 0.3:
                        has_p30 = True
                    elif scroll.success_chance == 0.6:
                        has_p60 = True
                    elif scroll.success_chance == 0.7:
                        has_p70 = True
                    elif scroll.success_chance == 1:
                        has_p100 = True
            if not has_p10:
                # try get p10 from owlrepo
                scroll_name = OwlrepoScrollsCategory.get_name(category, stat, 0.1)
                if scroll_name is not None:
                    scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
                    if scroll_price is not None:
                        self.add(category, stat, 0.1, 1, scroll_price)
            if not has_p30:
                # try get p30 from owlrepo
                scroll_name = OwlrepoScrollsCategory.get_name(category, stat, 0.3)
                if scroll_name is not None:
                    scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
                    if scroll_price is not None:
                        self.add(category, stat, 0.3, 0.65, scroll_price)
            if not has_p60:
                # try get p60 from owlrepo
                scroll_name = OwlrepoScrollsCategory.get_name(category, stat, 0.6)
                if scroll_name is not None:
                    scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
                    if scroll_price is not None:
                        self.add(category, stat, 0.6, 1, scroll_price)
            if not has_p70:
                # try get p70 from owlrepo
                scroll_name = OwlrepoScrollsCategory.get_name(category, stat, 0.7)
                if scroll_name is not None:
                    scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
                    if scroll_price is not None:
                        self.add(category, stat, 0.7, 0.85, scroll_price)
            if not has_p100:
                # try get p100 from owlrepo
                scroll_name = OwlrepoScrollsCategory.get_name(category, stat, 1)
                if scroll_name is not None:
                    scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
                    if scroll_price is not None:
                        self.add(category, stat, 1, 1, scroll_price)
            return True
        else:
            # try load given success_chance scroll from owlrepo
            self.get(category, stat, success_chance)
                    
    def get(self, category, stat, success_chance):
        '''Returns the scroll with the given category and stat, or None if it doesn't exist'''
        for scroll in self.scrolls:
            if scroll.category == category and scroll.stat == stat and scroll.success_chance == success_chance:
                return scroll
        # if no such scroll exists, try get it from owlrepo data
        scroll_name = OwlrepoScrollsCategory.get_name(category, stat, success_chance)
        if scroll_name is not None:
            scroll_price = OwlrepoSearchItemIndex.get_price(scroll_name)
            if scroll_price is not None:
                tmp_scroll = self.add(category, stat, success_chance, 0, scroll_price)
                return tmp_scroll
        return None

    def search(self, category='', stat='', success_chance=0.0) -> list[Scroll]:
        '''Returns the list of scrolls that match the given conditions'''
        self.load_from_owlrepo_data(category, stat, success_chance)
        result = []
        for scroll in self.scrolls:
            if success_chance == 0.0:
                if scroll.category.find(category) != -1 and scroll.stat.find(stat) != -1:
                    result.append(scroll)
            else:
                if scroll.category.find(category) != -1 and scroll.stat.find(stat) != -1 and scroll.success_chance == success_chance:
                    result.append(scroll)
        return result
    
    def remove(self, scroll: Scroll):
        '''Remove the given scroll from data'''
        self.scrolls.remove(scroll)
        self.save_to_file()
    
    def load_from_file(self):
        '''Loads the scrolls from the given file'''
        # if no such file exists, return
        try:
            with open(Scrolls.file_name, 'r') as file:
                data = json.load(file)
                for scroll in data['scrolls']:
                    self.update(scroll['category'], scroll['stat'], scroll['success_chance'], scroll['survival_chance'], scroll['price'])
        except FileNotFoundError:
            return
    
    def save_to_file(self):
        '''Saves the scrolls to the given file'''
        with open(Scrolls.file_name, 'w') as file:
            data = {'scrolls':[]}
            for scroll in self.scrolls:
                data['scrolls'].append({'category':scroll.category, 'stat':scroll.stat, 'success_chance':scroll.success_chance, 'survival_chance':scroll.survival_chance, 'price':scroll.price})
            json.dump(data, file, indent=4)
            
class OwlrepoScroll:
    '''Class that represents a scroll from Owlrepo'''
    def __init__(self, percent, stat, category, is_weapon, name):
        self.percent :int = int(percent)
        self.stat :str = stat
        self.category :str = category
        self.is_weapon :bool = is_weapon
        self.name :str = name
class OwlrepoScrollsCategory:
    '''Class that represents categories of all scrolls from Owlrepo'''
    scrolls :list[OwlrepoScroll] = []
    file_name :str = 'owlrepo_scrolls_category.json'
    @staticmethod
    def load_from_file( ):
        '''Loads the scrolls from the given file'''
        # if no such file exists, return
        try_times = 0
        while try_times < 3:
            try:
                with open(OwlrepoScrollsCategory.file_name, 'rb') as file:
                    data = json.load(file)
                    for scroll in data:
                        OwlrepoScrollsCategory.scrolls.append(OwlrepoScroll(scroll['percent'], scroll['stat'], scroll['category'], scroll['is_weapon'], scroll['name']))
                return True
            except FileNotFoundError:
                OwlrepoScrollsCategory.download_from_owlrepo()
            finally:
                try_times += 1
        return False
        
    
    @staticmethod
    def download_from_owlrepo():
        '''Downloads the .json file from Owlrepo
        No need to call unless file doesn't exist'''
        url = "https://owlrepo.com/api/v2/query/mllib_scrolls_category"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
        
            with open(OwlrepoScrollsCategory.file_name, "wb") as file:
                file.write(response.content)
        
        
        except requests.exceptions.RequestException as e:
            return False
        return True
    
    @staticmethod
    def get_name(category, stat, percent):
        '''Returns the name of the scroll with the given category, stat and percent'''
        for scroll in OwlrepoScrollsCategory.scrolls:
            if scroll.category == category and scroll.stat == stat and (scroll.percent == percent or scroll.percent == percent*100):
                return scroll.name
        return None
    
class OwlrepoSingleSearchResult:
    '''Class that represents a single search result from Owlrepo'''
    def __init__(self, task_id, client_thumbprint, search_item_timestamp, search_item, search_results, search_results_captured, sum_bundle, num_outlier, percent_complete, p0,  p25, p50, p75, p100, mean, std, n_owled):
        self.task_id :str = task_id
        self.client_thumbprint :str = client_thumbprint
        self.search_item_timestamp :str = search_item_timestamp
        self.search_item :str = search_item
        self.search_results :int = int(search_results)
        self.search_results_captured :int = int(search_results_captured)
        self.sum_bundle :int = int(sum_bundle)
        self.num_outlier :int = int(num_outlier)
        self.percent_complete :float = float(percent_complete)
        self.p0 :float = float(p0)/1000000.0
        self.p25 :float = float(p25)/1000000.0
        self.p50 :float = float(p50)/1000000.0
        self.p75 :float = float(p75)/1000000.0
        self.p100 :float = float(p100)/1000000.0
        self.mean :float = float(mean)/1000000.0
        self.std :float = float(std)/1000000.0
        self.n_owled :float = float(n_owled)/1000000.0

class OwlrepoSearchItemIndex:
    '''Class that represents a search item index from Owlrepo'''
    results :list[OwlrepoSingleSearchResult] = []
    file_name :str = 'owlrepo_search_item_index.json'
    
    @staticmethod
    def load_from_file( ):
        '''Loads the search item index from the given file'''
        # if no such file exists, return
        try_times = 0
        while try_times < 3:
            try:
                with open(OwlrepoSearchItemIndex.file_name, 'rb') as file:
                    data = json.load(file)
                    for result in data:
                        OwlrepoSearchItemIndex.results.append(OwlrepoSingleSearchResult(result['task_id'], result['client_thumbprint'], result['search_item_timestamp'], result['search_item'], result['search_results'], result['search_results_captured'], result['sum_bundle'], result['num_outlier'], result['percent_complete'], result['p0'], result['p25'], result['p50'], result['p75'], result['p100'], result['mean'], result['std'], result['n_owled']))
                return True
            except FileNotFoundError:
                OwlrepoSearchItemIndex.download_from_owlrepo()
            finally:
                try_times += 1
        return False

    @staticmethod
    def download_from_owlrepo():
        '''Downloads the .json file from Owlrepo
        No need to call unless file doesn't exist'''
        url = "https://owlrepo.com/api/v2/query/search_item_index"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
        
            with open(OwlrepoSearchItemIndex.file_name, "wb") as file:
                file.write(response.content)
                
        except requests.exceptions.RequestException as e:
            return False
        return True
    
    @staticmethod
    def get_price(scroll_name):
        '''Returns the p20 of the given search item'''
        for result in OwlrepoSearchItemIndex.results:
            if result.search_item == scroll_name:
                return result.p25
        return None