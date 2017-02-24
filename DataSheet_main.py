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
            f.write("'Simulation Name', 'WT/Mu', 'Protein Name', 'Bacteria Name', 'Residue Range', 'Salt Type', 'Salt Concentration', 'Extra Comments', 'Progress (ns)', 'Server Name', 'Source Directory'\n")
    
    
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

    def add_sim(self):
        """ gets information from user about a new simulation
            the data will be added to the file
        """
        print("Data will now be collected for the new simulation.")
        print("To go back to the main menu, please type 'q'.")
        print()
        
        new_sim = []
        
        while True:
            print("Enter the name of the new simulation.")
            sim_name = input()
            if sim_name == 'q':
                return 'q'
            elif sim_name in self.simulation_names:
                print("That simulation name already exists. Please enter a new one.", '', sep='\n')
            else:
                new_sim.append(sim_name)
                break
                
        while True:
            print("Is simulation of a wild-type (1) or mutant (2) peptide?")
            p_type = input()
            if p_type == 'q':
                return 'q'
            elif p_type != '1' and p_type != '2':
                print("Invalid input. Please try again.")
            elif p_type == '1':
                p_type = 'WT'
                new_sim.append(p_type)
                break
            elif p_type == '2':
                p_type = 'Mu'
                new_sim.append(p_type)
                break

        print("Provide the name of the protein being simulated (ex ProP):")
        protein = input()
        if protein == 'q':
            return 'q'
        else:
            new_sim.append(protein)
      
        print("What bacteria name is your protein from (ex Ec, Xc)?")
        bacteria = input()
        if bacteria == 'q':
            return 'q'
        else:
            new_sim.append(bacteria)
        
        while True:
            print("For the protein being simulated, what is the first residue number?")
            res_start = input()
            if res_start == 'q':
                return 'q'
            try:
                res_start = int(res_start)
            except ValueError:
                print("An integer value (whole number) should be given. Please try again.")
            else:
                if res_start <= 0:
                    print("Residue number should be greater than 0. Please try again.")
                else:
                    break

        while True:
            print("Similarly, what is the last residue number?")
            res_finish = input()
            if res_finish == 'q':
                return 'q'
            try:
                res_finish = int(res_finish)
            except ValueError:
                print("An integer value (whole number) should be given. Please try again.")                                
            else:
                if res_finish < res_start:
                    print("The last residue number should be greater than the first residue number. Please try again.")
                else:
                    residue_range = str(res_start)+'-'+str(res_finish)
                    new_sim.append(residue_range)
                    break
        
        print("Enter the salt type used in the simulation. Use \"N/A\" if no salt was used.")
        salt_type = input()
        if salt_type == 'q':
            return 'q'
        else:
            new_sim.append(salt_type)
            
        while True:
            print("Enter the concentration of salt used. Use \"N/A\" if no salt was used.")         
            salt_conc = input()
            if salt_conc == 'q':
                return 'q'
            elif salt_conc == 'N/A':
                break
            try:
                salt_conc = float(salt_conc)
            except ValueError:
                print("This value should be a number. Please try again.")
            else:
                if salt_conc <= 0:
                    print("This value should be greater than zero. Please try again.")
                else:
                    new_sim.append(salt_conc)
                    break
        
        while True:
            print("Extra comments can be put about the simulation here (i.e. coiled-coil, single helix, parallel, anti-parallel, etc.).")
            print("Note: there should NOT be any commas in this comment.")
            comments = input()
            if comments == 'q':
                return 'q'
            elif comments.count(',') > 0:
                print("Do not put any commas in the comments section. Please try again.")
            else:
                new_sim.append(comments)
                break
            
        while True:
            print("Please enter the number of nanoseconds completed so far for this simulation.")
            ns = input()
            if ns == 'q':
                return 'q'
            try:
                ns = float(ns)
            except ValueError:
                print("Value should be a number. Please try again.")
            else:
                if ns < 0:
                    print("Value should be greater than, or equal to, zero. Please try again.")
                else:
                    new_sim.append(ns)
                    break

        print("Please enter the name of the server where the simulation is currently running: ")
        server = input()
        if server == 'q':
            return 'q'
        else:
            new_sim.append(server)
        
        print("Please enter the directory path to where the simulation data is stored (i.e. the namd folder): ")
        dir_path = input()
        if dir_path == 'q':
            return 'q'
        else:
            new_sim.append(dir_path)
       
        return new_sim
        
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
            sim_data.add_sim()
        else:
            print("Invalid input. Try again.")



