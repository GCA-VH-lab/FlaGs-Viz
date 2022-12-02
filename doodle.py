import pandas as pd

# email = input('Your e-mail: ')
# code = 2322122110935
# link = f'http://130.235.240.53/scripts/writable/{email}%{code}/'

# try: 
#     df = pd.read_csv(link)
#     print(df)
# except:
#     print('Incorrect email or code')



# works
# email = input('Your e-mail: ')
# code = 2322122110935
# link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_TreeOrder_operon.tsv'
# link_phylo = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_ladderTree.nw'

# try: 
#     df = pd.read_csv(link_operon)
#     print(df)
# except:
#     print('Incorrect email or code')



# works
import os

email = input('Your e-mail: ')
code = 2322122110935
storred_runs = 'http://130.235.240.53/scripts/writable/?C=M;O=D'
link_folder = f'http://130.235.240.53/scripts/writable/{email}%{code}/'
link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_TreeOrder_operon.tsv'
link_phylo = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_ladderTree.nw'

try: 
    if email == '':
        server_runs = pd.read_html(storred_runs)
        runs = []
        for run in server_runs:
            if '@' in server_runs['Name']:
    print(df)
except:
    print('Incorrect email or code')