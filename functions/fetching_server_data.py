


# Lists
runs = []
email_runs = []
all_runs_list = []
stored_runs_list = []


def email_search(email):
    '''
    Validates that the user's email is found in the queueDir and 
    fetches the user email, email_name, and the FlaGs submission_id
    '''
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        if s.startswith(email):
            email = email.split('#')[0]
            email_name = email.split('@')[0]
            code = re.search('#(.*).run', s)
            submission_id = code.group(1)
    return email, email_name, submission_id


def run_finished(url):
    '''
    Validates the existance of an URL link. In this case used to check
    if a submission is still stored on the server
    '''
    response = requests.head(url)
    return response.status_code in range(200, 400)


def selected_submission(option):
    '''
    Once the user selects one of their runs from the dropdown menu, 
    files for generating graphs are retrived from the server.
    '''
    sub = str(submissions[submissions['Last modified']==option]['Name'])
    code = re.search('#(.*).run', sub)
    submission_id = code.group(1)
    return submission_id


def submission_components(submission):
    '''
    For a run, the key components are split for easier access. Used 
    for filling out the URL links
    '''
    email = submission.split('#')[0]
    email_name = submission.split('@')[0]
    code = re.search('#(.*).run', submission)
    submission_id = code.group(1)
    return email, email_name, submission_id


def submission_lists(email):
    all_runs_list = []
    stored_runs_list = []
    '''
    Outputs necessary lists for checking the email against the runs.
    all_runs_list = all runs in queueDir associated with the email
    stored_runs_list = only the server stored runs for the email
    '''
    for s in submissions.loc[1:, 'Name':'Last modified']['Name']:
        # Find all runs associated with the email from the queueDir
        if s.startswith(email) and s not in all_runs_list:
            all_runs_list.append(s)
            # Find all runs that are still accessible (stored) by 
            # testing the URL for one of the ouput files (operon.tsv)
            if run_finished(test_url(s)) == True:
                run = str(submissions[submissions['Name']==s]['Last modified'])
                run_date = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', run)
                submission_id = run_date.group(0)
                # Add only unique runs' submission_id to list
                if submission_id not in stored_runs_list:
                    stored_runs_list.append(submission_id)
                stored_runs_list.sort(reverse=True)
    return all_runs_list, stored_runs_list
