# CrossTok
## Project Members
- Taylor Nastally
- Anthony Lim
## Member Contributions
- Taylor:
 	- Planning
    - Designing
    - Coding
    - Testing
    - Documentation
    - Recording
    - Release versioning the program
- Anthony:
	- Assisted in Testing
## How to Run
### Simple User Experience
1. Double click CrossTok.exe to run
2. Enjoy
### A User Experience
1. If python is not installed on your computer, [download](https://www.python.org/downloads/) it
	- Follow the instructions for installation
2. Open CMD or Terminal, navigate to the folder containing CrossTok.py
3. Run `pip install cx_freeze` and/or `pip install tabulate` in a CMD terminal opened to the location your download for CrossTok.py is
	- There is a dependency issue for these two imports that must be resolved (discovered 11/12/2023)
	- If you want to run CrossTok.py, only `pip install tabulate` is required
	- If the exe is causing problems, you will need to rebuild the exe and run setup.py, you will then need to use `pip install cx_freeze`
	- Sometimes the exe works without needing a rebuild 
4. Type the command: `python CrossTok.py` or `python CrossTok.py <desired port number>`
	- The program contains a default port of 5959
 	- Please note that if you have a NAT device between the two devices or a firewall active on either device, you will not be able to use the program
    - To fix the NAT issue, both devices must be on the same internal network e.g. `xxx.xxx.1.xxx` and `xxx.xxx.1.xxx`
    - To fix the firewall issue please look up the specifics for your firewall/anti-virus/anti-maleware provider and disable the feature
### To Make Source Code into EXE
1. Run `pip install cx_freeze` in CMD located in download folder
    - May encounter issues with PATH variables for your operating system
        - To fix you will have to edit user variables
        - Find the install location of your version of python
        - Paste that location into the var
        - Save changes
2. `setup.py` and `CrossTok.py` must be in same folder
3. CMD to folder
4. Run `python setup.py build` 
### Extra Documentation
This contains a bunch of HTML for a browser based code documentation viewer
- To view, double click `_cross_tok_8py.html`
This will open your browser so you can click through the documentation of the functions and variables
    - Generated with Doxygen 
### CrossTok.exe
This is the executable and all you have to do for this file is double click CrossTok.exe in the likewise named folder, no hassle required
## Special Thanks
Thank you to the family members who supported us through this time consuming project and encouraged us to complete it, we couldn't have done it without you