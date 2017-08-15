#!/home/jgarne01/anaconda3/bin/python3.6

# simulation class to instantiate and update simulation times


# TO DO

# make updater viable
# enable addition of new categories
# fix auto format issue with excel

# NOTE
# with regards to formatting, excel likes "words" to 
# indicate text, and does not use ', ' to separate
# values (rather it uses ',' - just a comma, no space)


import os
import sys
import csv

### csv reader defaults to:
# delimiter as ','
# quotechar as '"'
# csv.QUOTE_MINIMAL = only quote fields containing 
#                     special chars (delim, quotechar)
# newline character is \r\n

class DataSheet(object):

    """
    """
    
    def __init__(self):
        """ note: length of each header item should not exceed 26 characters
            to avoid formatting issues
        """
        self.fname = self.get_filename()
        self.names = []
        self.main_dict = {}
        # if file already exists and is non-empty
        if os.path.isfile(self.fname) and os.path.getsize(self.fname) != 0:
            print("Data will now be read from file "+self.fname+'.')
            self.header = self.get_header()
            self.header_length = len(self.header)
            self.num = self.count()
            self.read_datafile()                # updates main_dict and names
        # there isn't a file or file is empty
        else:
            print("No data has been written yet to "+self.fname+'.')
            self.header = ['Name']
            self.header_length = 1
            self.num = 0

    def get_filename(self):
        """ the user will be prompted for a name to same simulation
            data to. this file will also be used to pull out current
            simulation progress. if no filename is given, the default
            is set to "datasheet.csv".
        """
        print("Enter a filename for storing information. The default filename is \"datasheet.csv\". Press enter to use the default filename: ")
        fname = input()
        if fname == '':
            print("Data will be stored in datasheet.csv.")
            return "datasheet.csv"
        else:
            print("Data will be stored in "+fname+'.')
            return fname
    
    def count(self):
        """ determines how many rows there are
            in the fname given
        """
        with open(self.fname, 'r') as f:
            first = True
            counter = 0
            for line in f:
                if first:
                    first = False
                else:
                    counter += 1
        return counter
    
    def get_header(self):
        """ determines the category names
            from the fname
        """
        with open(self.fname, 'r', newline='') as f:
            cf = csv.reader(f)
            for line in cf:
                header = line
                break
        return header

    def read_datafile(self):
        """ pulls all data from the fname file and stores it
            in a dictionary
        """
        # avoids trying to open non-existent file
        if self.num == 0:
            return {}
        header = True
        with open(self.fname, 'r', newline='') as f:
            cf = csv.reader(f)
            for line in cf:
                if header:          # ignore header
                    header = False
                else:
                    self.names.append(line[0])
                    self.main_dict[line[0]] = line

    def print_names(self):
        if self.num == 0:
            print("No data found in "+self.fname+'.')
            return 'q'
        else:
            print(str(self.num)+" entries found in "+self.fname+'.')
            print()
            print("          Entry Name                      | Number ")
            print("------------------------------------------|--------") 
            for i, name in enumerate(self.names):
                # : is for padding. ^ means centre, > means right justified
                # left justified is default
                print("{:42}|{:^8}".format(name, i))
                # for increased legibility
                if i%5 == 0:
                    print("                                          |        ")
            print()
            return    

    def choose_entry(self):
        if self.num == 0:
            return 'q'
        while True:
            print("Please select a simulation number. To return to the main menu, type 'q'.")
            numi = input()
            if numi == 'q':
                return 'q'
            try:
                numi = int(numi)
            except ValueError:
                print("Input should be an integer. Please try again.")
            else:
                if numi not in range(self.num):
                    print("Number not available. Please try again.")
                else:
                    return numi

    def print_entry(self, numi):
        """ prints information about the entry number given (numi)
        """
        key = self.names[numi]
        print("Getting data for entry:", str(key))
        print()
        values = self.main_dict[key]
        print("       Category Name      |             Value             ")
        print("--------------------------|-------------------------------")
        for i, entry in enumerate(self.header):
            print(" "*26, "|", " "*31, sep='')
            
            # avoid issues with floats/integers
            v = str(values[i])[:]
            
            # determine how much space the entry will take up
            if len(v) <= 31:
                value = v
                value_lines = 1
            else:    
                value_lines = len(v) // 30 + 1
                value = v[:30]
                if entry != 'Source Directory':
                    value += '-'
            print("{:26}|{:^31}".format(entry, value))
            start = 30
            end = 60            
            if value_lines > 1:
                for m in range(1, value_lines):
                    # note, here is sort of weird
                    # python will not return index out of range error
                    # for a string len>30 with len%30 = 0
                    # instead it prints an extra line
                    # see note 4 from:
                    # https://docs.python.org/3/library/stdtypes.html
                    if m == value_lines-1:
                        if v[start:] != '':
                            print("{:26}|{:^31}".format('', v[start:]))
                    else:    
                        value = v[start:end]
                        if entry != 'Source Directory':
                            value += '-'
                        print("{:26}|{:^31}".format('', value))
                        start = end
                        end += 30
        print(" "*26, "|", " "*31, sep='')
        print()
        return

    def add_entry(self):
        """ gets information from user about a new data entry
            that will be added to the file
        """
        print("Data will now be collected for the new entry.")
        print("To go back to the main menu, please type 'q'.")
        print()

        # get data for new entry
        new = []
        first = True
        for category in self.header:
            if first:
                first = False
                name = self.get_name()
                if name == 'q':
                    return 'q'
                else:
                    new.append(name)
            else:
                value = self.get_category(category)
                if value == 'q':
                    return 'q'
                else:
                    new.append(value)
        return new

    def confirm_entry(self, entry):
        """ the addition of the entry is
            confirmed and then added to the main_dict
            and names
        """
        # confirm addition:
        print('', entry, '', "Add this entry to "+self.fname+"?", sep='\n')
        while True:
            ans = input("Y/n ") 
            if ans in ('yes', 'YES', 'Yes', 'Y', 'y'):
                print("Entry will be added to "+self.fname+'.')
                break
            elif ans in ('no', 'NO', 'No', 'N', 'n', 'q'):
                print("Entry was not added to the database.")
                return 'q'
            else:
                print("Invalid input. Try again.")
        
        # add to database
        self.num += 1                       # add 1 to number of entries
        self.main_dict[entry[0]] = entry    # update dictionary
        self.names.append(entry[0])         # update name list
        self.names = sorted(self.names)     # sort name list alphabetically
        
        # re-write file
        self.write_data()

    def write_data(self):
        """ this function writes the contents of the main dictionary
            self.main_dict to a file, called fname
            the first instance of each simulation (the sim_name) is
            used to sort the keys and hense the file is written
            in alphabetical order according to sim_name
        """
        with open(self.fname, 'w', newline='') as f:
            cf = csv.writer(f)
            cf.writerow(self.header)                # write header
            for entry in self.names:                # write entries
                cf.writerow(self.main_dict[entry])

    def get_name(self):        
        """ returns the name of the row or q for qutting/going 
            up a level in the nested loops. User cannot input a name
            if it already exists in the data file.
        """
        while True:
            print("Enter a name for the new data entry.")
            name = input()
            if name == 'q':
                return 'q'
            elif name in self.names:
                print("That name already exists. Please enter a new one.", '', sep='\n')
            elif name == 'DUMMY':
                print("That name is reserved by the system. Please enter a different name.")
            else:
                return name

    def choose_category(self):
        """ the user is prompted to select a category
            number, which can then be deleted
        """
        while True:
            print("", "Please select a category number to remove:", sep='\n')
            rm = input()
            if rm == 'q':
                return 'q'
            elif rm == '0':
                print("The name category cannot be deleted. Please try again.")
            else:
                try:
                    rm = int(rm)
                except ValueError:
                    print("Category chosen should be an integer value.")
                    continue
                if rm not in range(1, self.header_length):
                    print("Category not available. Please try again.")
                else:
                    return rm

    def confirm_category(self, category, da):
        """ the da variable indicates either "delete"
            or "add"
        """
        print('', "Please note that any change to the categories will add or delete values from all the entries in the database.", '', sep='\n')
        print("Confirm:", da, category, "?")
        while True:
            ans = input("Y/n ") 
            if ans in ('yes', 'YES', 'Yes', 'Y', 'y'):
                print("The database has been updated.")
                return
            elif ans in ('no', 'NO', 'No', 'N', 'n', 'q'):
                print("The database has not been updated.")
                return 'q'
            else:
                print("Invalid input. Try again.")
    
    def print_category(self):
        """ prints the current categories to the terminal
        """
        print("", "The current categories are:", "", sep='\n')
        print("       Category Name      |             Value             ")
        print("--------------------------|-------------------------------")
        for i, entry in enumerate(self.header):
            print(" "*26, "|", " "*31, sep='')
            print("{:26}|{:^31}".format(entry, i))
            print(" "*26, "|", " "*31, sep='')
        
    def make_category(self):
        """ the user is prompted to make a new
            category name. it cannot be in the header
            already
        """
        while True:
            print("", "Enter a name for the new category:", sep='\n')
            n = input()
            if n == 'q':
                return 'q'
            elif n in self.header:
                print("New name cannot already be in the category list.")
                print("Please try again.")
            else:
                return n

    def add_category(self):
        """ adds a new category to the csv file
        """
        print("This is a placeholder for the add_category() function.")
        self.print_category()
        n = self.make_category()
        if n == 'q':
            return 'q'
        else:
            a = self.confirm_category(n, 'add')
        if a == 'q':
            return 'q'
        else:
            self.header.append(n)
            self.header_length += 1
            for key in self.main_dict:
                self.main_dict[key].append('')
            self.write_data()

    def remove_category(self):
        """ removes a category from the csv file
        """
        self.print_category()
        rm = self.choose_category()
        if rm == 'q':
            return 'q'
        else:
            c = self.confirm_category(self.header[rm], "delete")
        if c == 'q':
            return 'q'
        else:
            self.header.remove(self.header[rm])
            self.header_length -= 1
            for key in self.main_dict:
                self.main_dict[key].remove(self.main_dict[key][rm])
            self.write_data()

    def get_category(self, category):
        """ this is a general function that will allow the user
            to enter input based-upon the given category

            note: the only separate function is the naming for 
            the rows; this category cannot be deleted. There 
            cannot be duplicates in this category (since they
            are stored in a dictionary).
        """
        print("Enter a value for ", category, ': ', sep='')
        value = input()
        if value == 'q':
            return 'q'
        else:
            return value

    def get_update_choice(self): 
        """ user is prompted to chose a category to update
        """
        while True:        
            print() 
            print("Choose a category to update, or type 'q' to quit.")
            for i, option in enumerate(self.header):
                print('(', i, ') ', option, sep='')
            print()
            choice = input()
            if choice == 'q':
                return 'q'
            elif choice not in [ str(x) for x in range(self.header_length)]:
                print("Option not available. Please try again.")
            else:
                return int(choice)
        
    def update_choice(self, numi, cat_num):
        """ is called after user selects choice from get_update_choice
        """
        # hold on to impt info
        cat_name = self.header[cat_num]
        old_entry_name = self.names[numi]
        old_entry = self.main_dict[old_entry_name][cat_num]
        old = self.main_dict[old_entry_name][:]

        print("Category", cat_name, 'will now be updated.')
        new = self.get_category(cat_name)
        if new == 'q':
            return 'q'
        else:
            # confirm change
            print("Confirm data change:", old_entry,'to', new)
            while True:
                ans = input("Y/n ") 
                if ans in ('yes', 'YES', 'Yes', 'Y', 'y'):
                    print("Database will be updated.")
                    break
                elif ans in ('no', 'NO', 'No', 'N', 'n', 'q'):
                    print("Database was not updated.")
                    return 'q'
                else:
                    print("Invalid input. Try again.")
            # do entry addition
            # changing the name might mean an order change
            if cat_num == 0:
                print("Since a name change has been requested, the program will now update the file alphabetically.")
                self.main_dict[new] = old
                self.main_dict[new][0] = new
                self.names.append(new)
                self.names.remove(old_entry_name)
                self.names = sorted(self.names)
                del self.main_dict[old_entry_name]
                self.write_data()
                return 'name_change'
            else:
                self.main_dict[old_entry_name][cat_num] = new
                self.write_data()
                return

    def update_entry(self, numi):
        """ numi is the entry number from the 
            alphabetical list (by name)
            this function calls the other functions
            necessary for updating a given category
        """
        while True:
            self.print_entry(numi)
            category = self.get_update_choice()
            if category == 'q':
                return 'q'
            else:
                update = data.update_choice(numi, category)
                if update == 'name_change':
                    return 'name_change'

    def remove_entry(self, numi):
        """ remove entry from database
        """
        entry = self.main_dict[self.names[numi]]
        # confirm deletion
        print("Delete entry", entry, "?")
        while True:
                ans = input("Y/n ") 
                if ans in ('yes', 'YES', 'Yes', 'Y', 'y'):
                    print("Database will be updated.")
                    break
                elif ans in ('no', 'NO', 'No', 'N', 'n', 'q'):
                    print("Database was not updated.")
                    return 'q'
                else:
                    print("Invalid input. Try again.")
        del self.main_dict[self.names[numi]]
        self.names.remove(self.names[numi])
        self.num -= 1
        self.write_data()

if __name__ == "__main__":
    data = DataSheet()
    while True:
        print('', "Options: ", sep='\n')
        print("(1) Make a new record.")
        print("(2) Remove an existing record.")
        print("(3) Update a current record in "+data.fname+'.')
        print("(4) View details about a current record.")
        print("(5) Add a category.")
        print("(6) Remove a category.")
        print("(7) Quit.", '', sep='\n')
        choice = input()
        print()

        # quit
        if choice in ('7', 'q'):
            break

        # remove existing record from database
        elif choice == '2':
            data.print_names()
            numi = data.choose_entry()
            if numi != 'q':
                data.remove_entry(numi)

        # print data for chosen entries
        elif choice == '4':
            data.print_names()
            numi = data.choose_entry()
            if numi != 'q':
                data.print_entry(numi)
        
        # allow user to update simulation record with new data
        elif choice == '3':
            data.print_names()
            numi = data.choose_entry()
            if numi != 'q':
                data.update_entry(numi)

        # add new entry to the database
        elif choice == '1':
            new = data.add_entry()
            if new != 'q':
                data.confirm_entry(new)

        # add new category (IN PROGRESS)
        elif choice == '5':
            data.add_category()
            
        # remove category (IN PROGRESS)
        elif choice == '6':
            data.remove_category()
        
        # invalid input (choice not available)    
        else:
            print("Invalid input. Try again.")



