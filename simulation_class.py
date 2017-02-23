#!/home/jgarne01/anaconda3/bin/python3.6

# simulation class to instantiate and update simulation times

import os

class Simulation(object):

    def __init__(self, name, progress_ns, server_name, server_directory):
        self.name = name
        self.progress_ns = progress_ns
        self.server_name = server_name
        self.server_directory = server_directory
    
    def update_progress_ns(self):
        self.progress_ns = input("Enter time in ns that has been completed for simulation "+self.name+": ")
        print("The current progress is now "+self.progress_ns+'ns.')
        return
        
    def update_server_name(self):
        self.server_name = input("Enter the server where simulation "+self.name+" currently resides: ")
        print("The current server is now "+self.server_name+'.')
        return
        
    def update_server_directory(self):
        self.server_directory = input("Enter the new directory where the simulation data for "+self.name+" is located: ")
        print("The directory is now "+self.server_directory+'.')
        return

class DataSheet(object):
    
    def __init__(self):
        self.fname = self.get_filename()
        self.num_simulations = self.count_sim()
        self.simulation_names = self.get_sim_names()
    
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
            f.write('"Simualtion Name", "Description", "Residue Range", "Salt Concentration", "Salt Type", "Progress (ns)", "Server Name", "Server Directory"\n')
    
    
    def count_sim(self):
        if os.path.isfile(self.fname) == False:
            self.write_header()
            return 0
        else:
            with open(self.fname, 'r') as f:
                counter = 0
                for line in f:
                    if line.startswith("\"Simulation Name\""):
                        continue
                    else:
                        counter+=1
            return counter

    def get_sim_names(self):
        if os.path.isfile(self.fname) == False or self.num_simulations == 0:
            print("No data has been written yet to "+self.fname+'.')
            return 'none'
        else:
            print("Data will now be read from file "+fname'.')
            simulation_names = []
            with open(self.fname, 'r') as f:
                for line in f:
                    simulation_names.append(line[:line.index(',')])
            self.simulation_names = sorted(simulation_names)
            return self.simulation_names
    
    def print_sim_names(self):
        print(str(self.num_simulations)+" simulations found in "+self.fname'.')
        print("          Simulation Name                 | Number ")
        print("------------------------------------------|--------") 
        for i, name in enumerate(self.simulation_names):
            print("{}|{}".format(name, i))            






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
        print("(2) Update a current simulation record in "+fname+'.')
        print("(3) Quit.", '', sep='\n')
        choice = input()
        if choice == '3':
            break
        elif choice == '2':
            sim_data.print_sim_names()
        elif choice == '1':
            pass
        else:
            print("Invalid input. Try again.")



