1. DESCRIPTION

~~general file structure~~

root/ 
   /templates
   This folder contains the index.html file
app.py (The main python file and data are hosted in the root folder)

2. REQUIREMENTS
   1) Install Python 3.7.X
   2) Install the packages from requirements.txt (via conda or manually)

	******************* IF INSTALLING VIA CONDA **********************
	navigate to/run the following command from the directory where the
        requirements.txt is located.
	
        >> conda create --name <env_name> --file requirements.txt
        >> conda activate <env_name>
        ******************************************************************

3. INSTALLATION
   1) Open a terminal window from within the root of the project folder.
   2) run the command py -3.7 -m flask run

3. EXECUTION
   1) Select weather and time from the dropdown boxes.
   2) Click submit button. 
   3) Enter location information 
	a) Click on the map and choose start location and end location.
	OR
	b) Type an address in the textbox and press enter key to select the address.
   4) Click reset button to clear the map.
   5) Other functions
	a) map: zoom in, zoom out, and dragging
	b) routing: reverse routing, adding stops, and dragging start and end locations. 

4. DEMO VIDEO
   url: 

