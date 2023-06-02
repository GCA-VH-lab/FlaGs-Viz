# FUNCTIONS USEED FOR ACCESSING THE SERVER

# Import packages
import pandas as pd
import requests
import urllib.request
import io
from Bio import AlignIO, Phylo


# Reads the queueDir HTML and retrives the runs and dates
storred_runs = 'http://130.235.240.53/scripts/writable/queueDir/'
server_table = pd.read_html(storred_runs)
server_df = server_table[0]
submissions = server_df.loc[:, 'Name':'Last modified'].dropna()
submitters = server_df.loc[:, 'Name'].dropna()


def test_url(s):
    '''
    Uses the URL to operon file to check if the URL is accessible 
    (i.e if the submission is still stored).
    '''
    link_operon = f'http://130.235.240.53/scripts/writable/{submission_components(s)[0]}%23{submission_components(s)[2]}/{submission_components(s)[1]}_flagsOut_TreeOrder_operon.tsv'
    return link_operon

def operon_url(email, email_name, sub_id):
    # Reads URL of operon file
    link_operon = f'http://130.235.240.53/scripts/writable/{email}%23{sub_id}/{email_name}_flagsOut_TreeOrder_operon.tsv'
    operon_file = pd.read_csv(link_operon, delimiter = '\t', header = None)
    return operon_file

def phylo_url(email, email_name, sub_id):
    # Reads URL of phylo tree (newick format)
    link_phylo_ladder = f'http://130.235.240.53/scripts/writable/{email}%23{sub_id}/{email_name}_flagsOut_ladderTree.nw'
    read_url = urllib.request.urlopen(link_phylo_ladder)
    string = read_url.read().decode()
    phylo_file = io.StringIO(string)
    tree = Phylo.read(phylo_file, "newick")
    return tree