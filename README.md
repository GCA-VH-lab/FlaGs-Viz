# FlaGs Visualisation 
A visualisation application to support the graphical output of FlaGs. 
FlaGs Visualisation allows the user to (1) upload their FlaGs 
results from a local machine with or without domain search, (2) visualise domain hits from three domain databases, and (3) create their own custom protein logos. 

<img width="1440" alt="Screenshot 2023-06-26 at 19 03 14" src="https://github.com/vedabojar/FlaGs-Viz/assets/100831180/200bfe0d-8d66-4ef2-ab3a-dc77b1d3c5a1">


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
pip install -r requirements.txt
```

4. Run the program:
```
python app.py
```

Problems fetching files? Might be missing this:
```
pip install html5lib
```


### Folder structure

```
|- README.md
|- app.py
|- index.py
|- requirements.txt
|- wsgi.py
├── assets
│   ├──color_scheme.py
│   ├──custom.css
│   ├──option_0.png
│   ├──option_1.png
│   ├──option_2.png
│   ├──option_3.png
│   ├──favicon.ico
│   ├──logo.png
│   ├──logo_tab.png
│   ├──faq_loading.png
│   └──faq_phylos.png
├── data
│   ├──preping_data.py
│   └──domain_annotation_map.txt
├── functions
│   ├──acessing_server.py
│   ├──drawing_logos.py
│   ├──fetching_server_data.py
│   ├──multi_databases.py
│   ├──operon_plot.py
│   ├──operon_w_domains.py
│   └──phylogeny_tree.py
├── pages
│   ├──a_cover_page.py
│   ├──b_find_submissions.py
│   ├──c_view_domains.py
│   ├──e_create_logos.py
│   ├──f_3_database.py
│   ├──help.py
│   ├──home.py
│   └──navigation.py
├── upload_files
│   ├──3db_example_domains.out
│   ├──3db_example_operon.tsv
│   ├──example_dom_out.txt
│   ├──example_ladderTree.nw
│   └──example_operon.tsv
└── .gitignore
```


