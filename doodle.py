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
#email = '4timis@gmail.com'


# Server links
storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'

def operon(s):
    link_operon = f'http://130.235.240.53/scripts/writable/{submission_components(s)[0]}%23{submission_components(s)[2]}/{submission_components(s)[1]}_flagsOut_TreeOrder_operon.tsv'
    return link_operon


def phylo(email):
    email_search(email)
    link_phylo_ladder = f'http://130.235.240.53/scripts/writable/{email_search(email)[0]}%23{email_search(email)[2]}/{selected_submission(option)}_flagsOut_ladderTree.nw'
    return link_phylo_ladder


# Returning databases from server links
server_table = pd.read_html(storred_runs)
server_df = server_table[0]
submissions = server_df.loc[:, 'Name':'Last modified'].dropna()
submitters = server_df.loc[:, 'Name'].dropna()

# Lists
email_list = []
codes_list = []
finished_runs = []
stored_subs = []
runs = []
email_runs = []


def run_stored(url):
    # Validates the existance of an URL link. Returns True/False
    response = requests.head(url)
    return response.status_code in range(200, 400)


def email_search(email):
    # Makes a list with all runs based on inserted email (email_runs)
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email):
            email_runs.append(s)
    return email_runs


def submission_components(submission):
    # For a run, the key components are split for easier access
    email = submission.split('#')[0]
    email_name = submission.split('@')[0]
    code = re.search('#(.*).run', submission)
    submission_id = code.group(1)
    return email, email_name, submission_id


def stored_submissions(email):
    # Makes a list with all runs based on inserted email (email_runs)
    for r in email_search(email):
        if run_stored(operon(email)) == True:
            stored_runs.append(s)
    return stored_subs


def stored(email):
    # For the user's email, append the date ('Last modified') of all 
    # server stored runs to runs. This list is later used as the options 
    # in the dropdown menu.  
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email): 
            if run_stored(operon(s)) == True:
                print(email) 
                run = str(submissions[submissions['Name']==s]['Last modified'])
                run_date = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', run)
                submission_id = run_date.group(0)
                finished_runs.append(submission_id)
                finished_runs.sort(reverse=True)
    return finished_runs



# def stored_submissions(run):
#     # For the user's email, append the submission ID
#     for s in submissions.loc[1:, 'Name':'Last modified']['Name']: 
#         if s.startswith(email) and run_stored(operon(email)) == True:
#             run = str(submissions[submissions['Name']==s]['Last modified'])
#             run_date = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', run)
#             submission_id = run_date.group(0)
#             finished_runs.append(submission_id)
#     return finished_runs


# def stored_submissions(run):
#     # From all finished submission make a list with only the ones 
#     # currentlystored on the server. This list is later used as the 
#     # options in the dropdown menu.   
#     for r in finished_submissions(run):
#         submission_id = selected_submission(r)
#         if run_stored(operon(email)):



def finished_submissions(run):
    # For the user's email, append the date ('Last modified') of all 
    # runs. 
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']: 
        if s.startswith(email): 
            run = str(submissions[submissions['Name']==s]['Last modified'])
            run_date = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', run)
            submission_id = run_date.group(0)
            finished_runs.append(submission_id)
    return finished_runs
        


def selected_submission(option):
    # Once the user selects one of their runs from the dropdown menu, 
    # files for generating graphs are retrived from the server.
    sub = str(submissions[submissions['Last modified']==option]['Name'])
    code = re.search('#(.*).run', sub)
    submission_id = code.group(1)
    return submission_id


if email != '':
    print(stored(email))
    df_operon = pd.read_csv(operon(email))
    df_phylo = pd.read_csv(phylo(email))
    print(df)
    print(phylo)

