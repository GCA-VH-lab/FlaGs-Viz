# import pandas as pd
# import re

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
# email = input('Your e-mail: ')
# # code = 2322122110935
# storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'
# # link_folder = f'http://130.235.240.53/scripts/writable/{email}%{code}/'
# # link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_TreeOrder_operon.tsv'
# # link_phylo = f'http://130.235.240.53/scripts/writable/{email}%{code}/veda.bojar_flagsOut_ladderTree.nw'


# server_table = pd.read_html(storred_runs, header=0)
# server_df = server_table[0]
# print(server_df)
# submissions = server_df.loc[:, 'Name':'Last modified'].dropna()

# submitters = server_df.loc[:, 'Name'].dropna()

# email_list = []
# codes_list = []
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

# try: 
#     for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
#         if email not in email_list:
#             print('E-mail address cannot be found')
#         elif s.startswith(email):
#             if email != '':
#                 print(email)
#                 email = email.split('#')[0]
#                 email_name = email.split("@")[0]
#                 code_a = re.search('#(.*).run', s)
#                 code_b = code_a.group(1)
#                 code = '23' + str(code_b)
#                 print(code_b)
#                 link_operon = f'http://130.235.240.53/scripts/writable/{email}%{code}/{email_name}_flagsOut_TreeOrder_operon.tsv'
#                 df = pd.read_csv(link_operon)
#                 print(df)
#         else:
#             print('Email address cannot be found')
                
#         for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
#             if s.startswith(email):
#                 run = submissions[submissions['Name']==s]['Last modified']
#                 #print(run)
#     else:
#         print('E-mail address cannot be found')        
# except:
#     print('Incorrect email or code')




import pandas as pd
import re
import requests


# E-mail input
# email = input('Your e-mail: ')
email = 'veda.bojar@med.lu.se'


# Server links
storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'

def operon(email):
    link_operon = f'''http://130.235.240.53/scripts/writable/
                    {email_search(email)[0]}%23{email_search(email)[1]}/
                    {email_search(email)[2]}_flagsOut_TreeOrder_operon.tsv'''
    return link_operon
    
def phylo(email):
    email_search(email)
    link_phylo = f'''http://130.235.240.53/scripts/writable/
                    {email_search(email)[0]}%23{email_search(email)[1]}/
                    {email_search(email)[2]}_flagsOut_Tree.nw'''
    return link_phylo
    
def phylo_ladder(email):
    email_search(email)
    link_phylo_ladder = f'''http://130.235.240.53/scripts/writable/
                    {email_search(email)[0]}%23{email_search(email)[1]}/
                    {email_search(email)[2]}_flagsOut_ladderTree.nw'''
    return link_phylo_ladder


# Returning databases from server links
server_table = pd.read_html(storred_runs, header=0)
server_df = server_table[0]
submissions = server_df.loc[:, 'Name':'Last modified'].dropna()
submitters = server_df.loc[:, 'Name'].dropna()

# Lists
email_list = []
codes_list = []
finished_runs = []
runs = []


def email_search(email):
    # Validates that the user's email is found in the queueDir and fetches the
    # user email, email_name, and the FlaGs submission_id
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email):
            email = email.split('#')[0]
            email_name = email.split('@')[0]
            code = re.search('#(.*).run', s)
            submission_id = code.group(1)
        else:
            print('''Your email could not be found, please insert the same 
            email address you used to submit your FlaGs run.''')
    return email, email_name, submission_id


def run_stored(url):
    # Validates the existance of an URL link
    response = requests.head(url)
    return response.status_code in range(200, 400)


def finished_submissions(run):
    # For a selected run by the user, the 
    # user email, email_name, and the FlaGs submission code    
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:    
        if run_stored(run):
            finished_runs.append(s)
            print('Added')
            print(finished_runs)
        else:
            print('''These results are no longer stored on our server. To view 
            them please use the upload button below.''')


if email != '':
    e = email_search(email)[0]
    finished_runs(e)
    print('Done')



# df = pd.read_csv(link_operon)
# print(df)


# email_name = 'veda.bojar'
# submission_id = '22128093847'

# print( f'http://130.235.240.53/scripts/writable/{email}%23{submission_id}/{email_name}_flagsOut_TreeOrder_operon.tsv')