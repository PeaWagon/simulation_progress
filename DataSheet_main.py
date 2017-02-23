#!/home/jgarne01/anaconda3/bin/python3.6

# simulation class to instantiate and update simulation times

import os

class DataSheet(object):
    
    def __init__(self):
        self.fname = self.get_filename()
        self.num_simulations = self.count_sim()
        self.simulation_names = self.get_sim_names()
        self.main_dict = self.read_datafile()
    
    def get_filename(self):
        """ the user will be prompted for a name to same simulation
            data to. this file will also be used to pull out current
            simulation progress. if no filename is given, the default
            is set to "simulation_times.csv".
        """
        print("Enter a filename for storing information. The default filename is \"simulation_times.csv\". Press enter to use the default filename: ")
        fname = input()
        if fname == '':
            print("Data will be stored in simulation_times.csv.")
            return "simulation_times.csv"
        else:
            print("Data will be stored in "+fname+'.')
            return fname
    
    def write_header(self):
        """ writes header to file 
            called if file does not exist (self.count_sim())
            or if file is to be updated with new information
        """ 
        with open(self.fname, 'w') as f:
            f.write('"Simulation Name", "Description", "Residue Range", "Salt Concentration", "Salt Type", "Progress (ns)", "Server Name", "Server Directory"\n')
    
    
    def count_sim(self):
        """ 
            
        """
        # if fname does not exist, fill with header, return 0 simulations
        if os.path.isfile(self.fname) == False:
            self.write_header()
            return 0
        # check if file is empty, fill with header
        elif os.path.getsize(self.fname) == 0:
            self.write_header()
            return 0
        # if not empty, ignore header, count the number of simulations    
        else:
            with open(self.fname, 'r') as f:
                first = True
                counter = 0
                for line in f:
                    if first == True:
                        first = False
                        continue
                    else:
                        counter+=1
            return counter

    def get_sim_names(self):
        if os.path.isfile(self.fname) == False or self.num_simulations == 0:
            print("No data has been written yet to "+self.fname+'.')
            return []
        else:
            print("Data will now be read from file "+fname+'.')
            simulation_names = []
            with open(self.fname, 'r') as f:
                for line in f:
                    simulation_names.append(line[:line.index(',')])
            self.simulation_names = sorted(simulation_names)
            return self.simulation_names
    
    def read_datafile(self):
        """ pulls all data from the fname file and stores it
            in a dictionary
        """
        if self.count_sim() == 0:
            return {}
        else:
            self.main_dict = {}
            with open(self.fname, 'r') as f:
                for line in self.fname:
                    self.main_dict[line[:line.index(',')]] = line
            return self.main_dict
                    
                
        
        
        
    def print_sim_names(self):
        if self.num_simulations == 0:
            print("No simulation data found in "+self.fname+'.')
            return
        else:
            print(str(self.num_simulations)+" simulations found in "+self.fname+'.')
            print("          Simulation Name                 | Number ")
            print("------------------------------------------|--------") 
            for i, name in enumerate(self.simulation_names):
                # : is for padding. ^ means centre, > means right justified
                # left justified is default
                print("{:42}|{:^8}".format(name, i))            
            return


    def choose_sim(self):
        if self.num_simulations == 0:
            return
        while True:
            print("Please select a simulation number. To quit, type 'q'.")
            sim_num = input()
            if sim_num == 'q':
                return 'q'
            try:
                sim_num = int(sim_num)
            except ValueError:
                print("Input should be an integer (whole number). Please try again.")
            else:
                if sim_num not in range(self.num_simulations):
                    print("Number not available. Please try again.")
                else:
                    return sim_num

# instantiate class members

"""
 labelling:
        WT = wild type
        CCD = coiled-coil dimer
        465_500 = residue start_residue end
        025M = concentration of salt 
        KCl = type of salt
        ap = anti-parallel

WT_CCD_465_500_025M_KCl_ap = Simulation("WT_CCD_465_500_025M_KCl_ap", 100, 
        
"""

if __name__ == "__main__":
    sim_data = DataSheet()
    while True:
        print('', "Options: ", sep='\n')
        print("(1) Make a new simulation record.")
        print("(2) Update a current simulation record in "+sim_data.fname+'.')
        print("(3) Quit.", '', sep='\n')
        choice = input()
        print()
        if choice == '3':
            break
        elif choice == '2':
            sim_data.print_sim_names()
            sim_num = sim_data.choose_sim()
            if sim_num == 'q':
                break
        elif choice == '1':
            pass
        else:
            print("Invalid input. Try again.")



