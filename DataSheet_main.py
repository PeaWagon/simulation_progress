#!/home/jgarne01/anaconda3/bin/python3.6

# simulation class to instantiate and update simulation times


# TO DO

# make sure no fields contain '
# this will cause issues for 
# fun shit happens with random characters inserted. need to fix


import os

class DataSheet(object):
    
    def __init__(self):
        self.fname = self.get_filename()
        self.num_simulations = self.count_sim()
        self.main_dict = self.read_datafile()
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
    
    def count_sim(self):
        """ determines how many simulations currently exist
            in the fname given
        """
        # if fname does not exist, return 0 simulations
        if os.path.isfile(self.fname) == False:
            return 0
        # check if file is empty
        elif os.path.getsize(self.fname) == 0:
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
        """ returns empty list if there is no data in fname
            needs to be updated AFTER the dictionary has been updated
            as it uses the dictionary to pull out simulation names
        """
        if self.count_sim == 0:
            print("No data has been written yet to "+self.fname+'.')
            return []
        else:
            print("Data will now be read from file "+self.fname+'.')
            self.simulation_names = []
            for key in sorted(self.main_dict):
                self.simulation_names.append(key)
            return self.simulation_names
    
    def read_datafile(self):
        """ pulls all data from the fname file and stores it
            in a dictionary
        """
        # avoids trying to open non-existent file
        if self.count_sim() == 0:
            return {}
        
        header = True
        self.main_dict = {}
        with open(self.fname, 'r') as f:
            for line in f:
                if header == True:
                    header = False
                else:
                    sim_name = line[1:line.index(',')-1]  
                    values = line[:-1].split(', ')
                    # gross formatting crap
                    # text is indicated by ' ' 
                    # may have commas within text
                    data = []
                    start = True
                    entry = ''
                    add_entry = False
                    for item in values:
                        if item.startswith("'") and item.endswith("'"):
                            data.append(item[1:-1])
                        elif start == True and item.startswith("'"):
                            entry+=item
                            start = False
                            add_entry = True
                        elif start == False and add_entry == True and item.endswith("'"):
                            entry+=item
                            data.append(entry[1:-1])
                            start = True
                            add_entry = False
                        elif start == False and add_entry == True:
                            entry+=item
                        else:
                            data.append(float(item))
              
                    
                    self.main_dict[sim_name] = data
            return self.main_dict
                    
                
        
        
        
    def print_sim_names(self):
        if self.num_simulations == 0:
            print("No simulation data found in "+self.fname+'.')
            return
        else:
            print(str(self.num_simulations)+" simulations found in "+self.fname+'.')
            print()
            print("          Simulation Name                 | Number ")
            print("------------------------------------------|--------") 
            for i, name in enumerate(self.simulation_names):
                # : is for padding. ^ means centre, > means right justified
                # left justified is default
                print("{:42}|{:^8}".format(name, i))            
            print()
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

    def write_data(self):
        """ this function writes the contents of the main dictionary
            self.main_dict to a file, called fname
            the first instance of each simulation (the sim_name) is
            used to sort the keys and hense the file is written
            in alphabetical order according to sim_name
        """
        with open(self.fname, 'w') as f:
            # write header
            f.write("'Simulation Name', 'WT/Mu', 'Protein Name', 'Bacteria Name', 'Residue Range', 'Salt Type', 'Salt Concentration', 'Extra Comments', 'Progress (ns)', 'Server Name', 'Source Directory'\n")
            for key in sorted(self.main_dict):
                sim = self.main_dict[key][:]    # make copy of dict item
                sim = str(sim).strip('[""]')+'\n' # rm sq brackets, add newline
                f.write(sim)
    
    def add_sim(self):
        """ gets information from user about a new simulation
            the data will be added to the file
        """
        print("Data will now be collected for the new simulation.")
        print("To go back to the main menu, please type 'q'.")
        print()
        
        new_sim = []
        new_sim.append(self.get_sim_name())
        if new_sim[0] == 'q':
            return 'q'
        new_sim.append(self.get_sim_type())
        if new_sim[1] == 'q':
            return 'q'
        new_sim.append(self.get_protein_name())
        if new_sim[2] == 'q':
            return 'q'
        new_sim.append(self.get_protein_bacteria())
        if new_sim[3] == 'q':
            return 'q'
        new_sim.append(self.get_res_range())
        if new_sim[4] == 'q':
            return 'q'
        new_sim.append(self.get_salt_name())
        if new_sim[5] == 'q':
            return 'q'
        new_sim.append(self.get_salt_conc())
        if new_sim[6] == 'q':
            return 'q'
        new_sim.append(self.get_comments())
        if new_sim[7] == 'q':
            return 'q'                  
        new_sim.append(self.get_sim_length())
        if new_sim[8] == 'q':
            return 'q'
        new_sim.append(self.get_sim_server())
        if new_sim[9] == 'q':
            return 'q'
        new_sim.append(self.get_sim_dir())
        if new_sim[10] == 'q':
            return 'q'
        
        print('', new_sim, '', "Add this simulation to "+self.fname+"?", sep='\n')
        # confirm addition:
        while True:
            ans = input("Y/n ") 
            if ans in ('yes', 'YES', 'Yes', 'Y', 'y'):
                print("Simulation will be added to "+self.fname+'.')
                break
            elif ans in ('no', 'NO', 'No', 'N', 'n', 'q'):
                print("Simulation was not added to the database.")
                return 'q'
            else:
                print("Invalid input. Try again.")
        
        # add to database
        self.simulation_names.append(new_sim[0])
        self.main_dict[new_sim[0]] = new_sim
        self.num_simulations += 1
        
        # re-write file
        self.write_data()
        
            
    def get_sim_name(self):        
        """ returns the name of the simulation or q for qutting/going 
            up a level in the nested loops. User cannot input a name
            if it already exists in the data file.
        """
        while True:
            print("Enter the name of the new simulation.")
            sim_name = input()
            if sim_name == 'q':
                return 'q'
            elif sim_name in self.simulation_names:
                print("That simulation name already exists. Please enter a new one.", '', sep='\n')
            else:
                return sim_name
    
    def get_sim_type(self):
        """ the user provides information as to whether the simulation
            is of a wild-type peptide or mutant peptide
        """                
        while True:
            print("Is simulation of a wild-type (1) or mutant (2) peptide?")
            p_type = input()
            if p_type == 'q':
                return 'q'
            elif p_type != '1' and p_type != '2':
                print("Invalid input. Please try again.")
            elif p_type == '1':
                p_type = 'WT'
                return p_type
            elif p_type == '2':
                mutation = input("Enter the mutation (ex E480C): ")
                p_type = 'Mu_'+mutation
                return p_type

    def get_protein_name(self):
        """ user provides name of protein for peptide being simulated
        """       
        print("Provide the name of the protein being simulated (ex ProP):")
        protein = input()
        if protein == 'q':
            return 'q'
        else:
            return protein

    def get_protein_bacteria(self):
        """ user provides name of bacteria that protein is from
        """      
        print("What bacteria name is your protein from (ex Ec, Xc)?")
        bacteria = input()
        if bacteria == 'q':
            return 'q'
        else:
            return bacteria

    def get_res_range(self):
        """ user provides first residue being simulated, followed
            by the last residue
            first number has to be a non-zero, positive integer
            second integer has to be higher/equal to than the first, 
            and a non-zero, positive integer
        """        
        while True:
            print("For the protein being simulated, what is the first residue number?")
            res_start = input()
            if res_start == 'q':
                return 'q'
            # note that trying to convert the string to a integer directly
            # will NOT work if the string is a floating point number! 
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
                    return residue_range
        
    def get_salt_name(self):
        """ user provides salt type for simulation
        """        
        print("Enter the salt type used in the simulation. Use \"N/A\" if no salt was used.")
        salt_type = input()
        if salt_type == 'q':
            return 'q'
        else:
            return salt_type

    def get_salt_conc(self):    
        """ user gives salt concentration in moles/litre (M)
            input cannot include units
        """            
        while True:
            print("Enter the concentration of salt used in moles/litre. Use \"N/A\" if no salt was used. Do not put units.")         
            salt_conc = input()
            if salt_conc == 'q':
                return 'q'
            elif salt_conc == 'N/A':
                return 'N/A'
            try:
                salt_conc = float(salt_conc)
            except ValueError:
                print("This value should be a number. Please try again.")
            else:
                if salt_conc <= 0:
                    print("This value should be greater than zero. Please try again.")
                else:
                    return salt_conc
    
    def get_comments(self):
        """ user inputs comments about their simulation
        """        
        while True:
            print("Extra comments can be put about the simulation here (i.e. coiled-coil, single helix, parallel, anti-parallel, etc.): ")
            comments = input()
            if comments == 'q':
                return 'q'
            else:
                return comments

    def get_sim_length(self):
        """ user provides length of simulation completed in nanoseconds
        """            
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
                    return ns
    def get_sim_server(self):
        """ user inputs where the simulation is currently running
        """
        print("Please enter the name of the server where the simulation is currently running: ")
        server = input()
        if server == 'q':
            return 'q'
        else:
            return server
        
    def get_sim_dir(self):
        """ user inputs where the data for their simulation is stored
        """        
        print("Please enter the directory path to where the simulation data is stored (i.e. the namd folder): ")
        dir_path = input()
        if dir_path == 'q':
            return 'q'
        else:
            return dir_path
        
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
        print("(3) View details about a current simulation record.")
        print("(4) Quit.", '', sep='\n')
        choice = input()
        print()
        if choice == '4':
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



