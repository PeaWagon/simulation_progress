# Simulation Progress Monitor :shipit:

###This repository contains two items:
* DataSheet code
* simulation_progress.csv file  

Only the DataSheet code is required if you want to track your own simulations.

#### Regarding the .csv file
* instances are separated by commas
* text is contained within single quotes 
* note: this has the implication that commas may be found between single quotes

#### Regarding the DataSheet code
* this code is CLI-based 
* the user can:
    1. Make a new simulation record
    2. Update a current simulation record
    3. View details about a current simulation record
* future work involves enabling the user to add categories to the .csv file
* the user can also specify a new name for a .csv file 
* going back to the main menu/quitting is accomplished by typing 'q'

#### To run the DataSheet code
This code uses python 3.6. However, it does not import any modules other than os and sys. The following commands work on ubuntu 16.04.  
1. Make sure you have python 3.x installed.  
  
    ```
    $ python3
    Python 3.6.0 |Anaconda 4.3.0 (64-bit)| (default, Dec 23 2016, 12:22:00)  
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux  
    Type "help", "copyright", "credits" or "license" for more information.  
    >>> 
    ```

OR  

    ```
    $ python3 --version
    Python 3.6.0 :: Anaconda 4.3.0 (64-bit)
    ```  

2. (Optional) Find out where your python executable is located.  

    ```
    $ which python
    /home/username/anaconda3/bin/python
    ```  

3. (Optional) Add the executable path to the top of the DataSheet_main.py file, as shown: `#!/home/username/anaconda3/bin/python`. Make sure this is the first line in the file (no empty lines). Most exectuable files are found in the `/usr/bin/python` directory.  
4. (Optional) Make sure the file is executable.  

    ```
    $ chmod u+x DataSheet_main.py
    ```  

5. Run the code. If you followed the (Optional) markers, do: `./DataSheet_main.py`. Otherwise, do: `python3 DataSheet_main.py`.  
6. Follow the prompts as given to make your selection/navigate the .csv file. 
