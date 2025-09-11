Group_11
===============
# Requirements
See `requirements.txt` for required dependencies. 

Run `pip install -r requirements.txt` to install all

---
# Github/Gitbucket Dual Push
*Daniel needs to add you to the GitHub repository before you can push to it*

CD to the cloned down isgb repo

run this: `git remote set-url --add --push origin https://isgb.otago.ac.nz/cosc345/git/paxda981/Group_11.git`

then this `git remote set-url --add --push origin https://github.com/Manwithacape/COSC345---Group_11.git`

now pulling only pulls from isgb. pushing now pushes to isgb and github.

as always pull before you push. 

# General Git
*Please DO NOT commit directly to main. This will be our stable branch.*

to see your local branches:
`git branch`

to create a branch:
`git branch <branch-name>`

to get onto a branch
`git checkout <branch-name>`
commits are now commited to that branch and pushing now pushes the branch to the online origin

I think Daniel is our git guy and will most likely handle merging in branches. And commiting to the stable branch. 
# Building 
Step 1:
Ensure you have pyinstaller installed. 
``` 
pip install pyinstaller
```


Step 2: 
Run 
```
pyinstaller --onefile --windowed app.py --add-data "schema.sql;." --icon "app.ico"
```

Step 3: 
Find the executable in:
```
.\dist\app.exe
``` 
# Python Environment
Step 1:
run: 
```
conda --version
```
 if that doesnt work make sure conda is installed. Recommended miniconda.

Step 2:
set up the environment by running: 
```
conda env create -f environment.yml
```

Step 3:
Run 
```
conda activate photosift
```  

Step 4:
 
In vscode use ctrl+shift+p and type `Python: Select Interpreter` and select photosift.

# Group Members
Daniel Paxton 

Kevin Wang

Cam

Will

Marick 
# Organization 

## Function Duplication 
Please search for a functions before creating a new one.

## Javascript
please do not use inlined js functions in .html files. please use main.js or seperate .js files and include them in main.js




