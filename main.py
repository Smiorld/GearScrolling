import csv
from Classes import *
from Commandline import *
from termcolor import colored, cprint
# This is the main function of the program. It is called when the program is run.
# The logic of the program is contained here.
# 1. Read data from files
# 2. Enter command line interface, waiting user input
# 3. Execute command and return result (either through cmd print or through file write)
# 4. Repeat 2-3 until user exits
def main():
    load_owlrepo_data()
    clear_screen()
    try:
        while True:
            display_default_info()
            cmd = input()
            if cmd == 'exit':
                break
            parse_cmd_input(cmd)
    except Exception as e:
        clear_screen()
        basegears.save_to_file()
        scrolls.save_to_file()
        cprint(f"Thank you for using, all data has been saved.","green")
        print(f"")
        raise e
    except KeyboardInterrupt as e:
        clear_screen()
        basegears.save_to_file()
        scrolls.save_to_file()
        cprint(f"Thank you for using, all data has been saved.","green")
        print(f"")
        raise e
    clear_screen()
    basegears.save_to_file()
    scrolls.save_to_file()
    cprint(f"Thank you for using, all data has been saved.","green")
    print(f"")
    print(f"Press enter to exit")
    input()
    
def load_owlrepo_data():
    '''Updates the data from owlrepo'''
    if OwlrepoScrollsCategory.load_from_file() and OwlrepoSearchItemIndex.load_from_file():
        return True
    return False
if __name__ == '__main__':
    main()

