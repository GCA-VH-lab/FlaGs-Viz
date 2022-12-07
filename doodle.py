import pandas as pd
import re

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
email = input('Your e-mail: ')
# code = 2322122110935
storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'
# link_folder = f'http://130.235.240.53/scripts/writable/{email}%{code}/'
# link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_TreeOrder_operon.tsv'
# link_phylo = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_ladderTree.nw'


server_table = pd.read_html(storred_runs, header=0)
server_df = server_table[0]
print(server_df)
submissions = server_df.loc[:, 'Name':'Last modified'].dropna()

submitters = server_df.loc[:, 'Name'].dropna()

email_list = []
codes_list = []
# for s in submitters.iloc[1:]:
#     if '@' in s:
#         email_list.append(s.split('#')[0])
#         codes_list.append(s.split('#')[1])
    
#print(email_list)
#print(submissions['Name'])

# if email not in email_list:
#     for s in submitters.iloc[1:]:
#         if '@' in s:
#             email_list.append(s.split('#')[0])
#             code_a = re.search('#(.*).run', s)
#             code_b = code_a.group(1)
#             print(code_b)


# link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/{email_name}_flagsOut_TreeOrder_operon.tsv'

# print(email_list)

try: 
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email):
            if email != '':
                print(email)
                email = email.split('#')[0]
                email_name = email.split("@")[0]
                code_a = re.search('#(.*).run', s)
                code_b = code_a.group(1)
                code = '23' + str(code_b)
                print(code_b)
                link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/{email_name}_flagsOut_TreeOrder_operon.tsv'
                df = pd.read_csv(link_operon)
                print(df)
                if email not in email_list:
                    print('E-mail address cannot be found')
        else:
            print('Email address cannot be found')
                
        for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
            if s.startswith(email):
                run = submissions[submissions['Name']==s]['Last modified']
                #print(run)
    else:
        print('E-mail address cannot be found')        
except:
    print('Incorrect email or code')