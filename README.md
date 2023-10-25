# Installing required modules
Installing the required modules is very easy, simply open `cmd.exe` and type `python -m pip install -r requirements.txt` alternatively you can use `python -m pip install colorama`

# How To Use
1. Put all the globals that you wish to update into a file and call that file whatever you want, we will use `globals.txt` 
2. Make sure that you have the old and new scripts downloaded, you can get them from [here](https://github.com/Primexz/GTAV-Decompiled-Scripts)
3. Open `cmd.exe`, use `cd` command to change to the directory of the script
4. Now that you're in the correct directory type `python main.py -h` into `cmd.exe`

# Example Usage
`python main.py C:/path/to/old/script.c C:/path/to/new/script.c globals.txt`

# Accuracy
During testing the script was able to find 90% of the globals within `globals.txt` file but every single global that was found appeared to have 100% accuracy

# Notes
Using the default settings has the greatest accuracy
