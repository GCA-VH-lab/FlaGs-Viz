
# FUNCTIONS FOR PREPING DATA AND READING FILES

# Import packages
import pandas as pd
import base64
import io


# Operon data - relevant info
def create_operon_df(operon_file):
    '''
    Extracts relevant info from operon file and updates domain.
    
    Args:
        operon_file (pandas.DataFrame): The operon file. 

    Returns:
        Operon dict with relevant data from original domain search
    '''
    # 1. Creating a dictionary to store relevant data from the input file
    operon_data = {
        'organism': [],
        'query_accession': [],
        'gene_accession': [],
        'hmlgs_group': [],
        'gene_direction': [],
        'gene_start': [],
        'gene_end': [],
        'gene_length': [],
        'y_level': [],
    }

    # 2. Extracts relevant info from each row
    for g in operon_file.iloc[:, 0]:
        if g != '':
            org = g.split('|')[1]
            operon_data['organism'].append(str(org))

            q_acc = g.split('|')[0]
            operon_data['query_accession'].append(str(q_acc))

    for g in operon_file.iloc[:, 9]:
        if g != '':
            operon_data['y_level'].append(int(0))
            g_acc = g.split('#')[0]
            operon_data['gene_accession'].append(str(g_acc))

    # 3 Appends data to the dictionary
    operon_data['hmlgs_group'] = list(operon_file.iloc[:, 4].astype(int))
    operon_data['gene_direction'] = list(operon_file.iloc[:, 3].astype(str))
    operon_data['gene_start'] = list(operon_file.iloc[:, 5].astype(int))
    operon_data['gene_end'] = list(operon_file.iloc[:, 6].astype(int))
    operon_data['gene_length'] = list(operon_file.iloc[:, 1].astype(int))
    
    # 4 Turns the dictioanry to a pandas df
    operon_df_org = pd.DataFrame.from_dict(operon_data)

    # 5 Adds the y-axis value to all genes of the same operon
    operon_df_org['y_level'] = operon_df_org.groupby('query_accession', sort = False).ngroup()
    operon_df = operon_df_org
    
    return operon_df



# Domain data - relevant info 
def create_domain_df(domain_file):
    '''
    Extracts relevant info from domain file and updates domain codes 
    to names.
    
    Args:
        domain_search_file (pandas.DataFrame): The domain search file. 

    Returns:
        Domain dict with relevant data from the original domain search
    '''

    domain_dict = {
        'domain':[],
        'domain_code': [],
        'domain_start': [],
        'domain_end': [],
        'e_value': [],
        'score': [],
    }

    domain_dict["domain"] = list(domain_file.iloc[:, 0])
    domain_dict["domain_start"] = list(domain_file.iloc[:, 19])
    domain_dict["domain_end"] = list(domain_file.iloc[:, 20])
    domain_dict["e_value"] = list(domain_file.iloc[:, 12])
    domain_dict["score"] = list(domain_file.iloc[:, 13])

    for str in domain_file.iloc[:, 3]:
        if str != '':
            str1 = str.split('#')[0]
            domain_dict["domain_code"].append(str1)
    
    # Convert dictionary to DataFrame
    domain_df = pd.DataFrame(domain_dict)
    domain_df_updated = rename_domains(domain_df)
    
    # Keep only the domain with the highest score within each domain code group
    domain_df_updated = domain_df_updated.loc[domain_df_updated.groupby('domain_code')['score'].idxmax()]
    
    return domain_df_updated




def create_domain_3db_df(domain_file):
    '''
    Extracts relevant info from domain file and updates domain codes 
    to names.
    
    Args:
        domain_search_file (pandas.DataFrame): The domain search file. 

    Returns:
        Domain dict with relevant data from the original domain search
    '''

    domain_dict = {
        'database': [],
        'domain_accession':[],
        'domain': [],
        'domain_start': [],
        'domain_end': [],
    }

    domain_dict["database"] = list(domain_file.iloc[:, 1])
    domain_dict["domain_accession"] = list(domain_file.iloc[:, 0])

    for str in domain_file.iloc[:, 10]:
        if str != '':
            str1 = str.split('-')[0]
            domain_dict["domain_start"].append(str1)
            str2 = str.split('-')[1]
            domain_dict["domain_end"].append(str2)

    domain_dict["domain"] = list(domain_file.iloc[:, 3])
    
    # Convert dictionary to DataFrame
    domain_df = pd.DataFrame(domain_dict)
    domain_df_updated = rename_domains(domain_df)
    
    return domain_df_updated


# Domain rename 
def rename_domains(domain_search_file):
    '''
    Replaces the domain codes to domain names in the domain search file.
    
    Args:
        domain_search_file (pandas.DataFrame): The domain search file. 

    Returns:
        pandas.DataFrame: The domain search file but with domain names 
        instead of codes where this is applicable.
    '''
    # Domain annotations file
    domain_annotations_file = pd.read_csv('./data/domain_annotations_map.txt', sep = '\t')

    # Creating a dictionary mapping domain codes to domain names
    domain_name_dict = dict(zip(domain_annotations_file.iloc[:, 0], domain_annotations_file.iloc[:, 1]))

    # Replace "PF" with "pfam" in the domain file
    domain_search_file['domain'] = domain_search_file['domain'].str.replace("PF", "pfam")

    handled_count = 0

    # Loop over domains in the domain file
    for i, domain in domain_search_file['domain'].items():
        if domain:
            domain_code = domain.split('.')[0]
            domain_name = domain_name_dict.get(domain_code)
            if domain_name:
                domain_search_file.at[i, 'domain'] = domain.replace(domain_code, domain_name)
                handled_count += 1
                
    return domain_search_file




def parse_file_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'tsv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\t', header=None)
        elif 'txt' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\s+', skiprows=3, skipfooter=10, engine='python')
        elif 'out' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\s+', skiprows=3, skipfooter=10, engine='python')
        return df
    except Exception as e:
        print(e)
        return None