# FlaGs Visualisation 
A visualisation application to support the graphical output of FlaGs. 
FlaGs Visualisation allows the user to either (1) upload their FlaGs 
results from a local machine or (2) use their e-mail to access FlaGs 
results stored on the server. The application support visualisation of 
the phylogenetic tree and the operon plot. 


## Setting Up

### How to run
1. Clone the repository to your local machine:
```
git clone https://github.com/vedabojar/FlaGs-Viz.git
```

2. Navigate to the directory containing the program
```
cd FlaGs-Viz
```

3. Install dependencies
```
pip3 install -r requirements.txt
```

4. Run the program:
```
python app.py
```

Problems fetching files? Might be missing this:
```
pip install html5lib
```



### Expected output
(Output when pressing on the two buttons)
<img width="1438" alt="Screenshot 2022-12-18 at 13 45 43" src="https://user-images.githubusercontent.com/100831180/208305832-97365f2a-3fcc-47d0-a664-37dd774dcab7.png">


### Folder structure

```
|- README.md
|- app.py
|- index.py
├── assets
│   ├──favicon.ico
│   ├──logo_tab.png
│   ├──faq_loading.png
│   └──faq_phylos.png
├── pages
│   ├──help.py
│   ├──home.py
│   └──navigation.py
├── upload_files
│   ├──ladderTree.nw
│   └──operon.tsv
└── .gitignore
```

## For Artyom 
I'm sorry you have to review this 🙃

Dash Plotly is framework for creating interactive apps built on top of 
Flask so its very similar. In short, the dash app has the the these 
key elements:
- the Layout of the app
    * I have used rows and columns to construct the page layout
- the Callbacks (interactive actions)
    * The callback functions have this structure:
        @callback( 
            Output(element1_id, value),
            Input(element2_id, value),
            Input(element3_id, value)
        )
        def upload_files():
            some function
    * Important to note that the functions can have multiple inputs, but each
    output may be use only once. 

### **app.py**
This one is for running the app. At the bottom you can set the server and host
port. I added the **wsgi.py** I used to deploy the app before. It's almost 
the same as for a Flask 


### **home.py**
The first page of the app, which is also the worst coded one is **home.py**.
Becuase it very long and complicated, here is its structure:
1. Imports
2. Create page
3. Layout
4. Arrow colors (code copied from FlaGs script)
5. Accessing server data
    * Access queueDir (all FlaGs submissions)
6. Fetching server data
    1. User inserts e-mail
    2. Iterates through queueDir and test which runs are still stored on the
    server. This is done by checking for the existance of the operon file URL
    in the run directory. 
    3. All valid runs are appended to a list (later presented to the user)
7. Creating plot from data with two functions
    * get_tree_plot() - creates phylo plot by reading the ladderTree.nw file
    * generate_operon() - creates operon plot by reading the operon.tsv file
8. Actions (callbacks)
    * Action 1 - searching for submissions with e-mail
    * Action 2 - uploading submissions from local machine

I guess the best thing is to have 5 - 7 as classes outside the home.py file.
I can work on this. 
