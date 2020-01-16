import pandas as pd
import yaml
import re


def make_simple_list(allv, allv_simple_list = []):
    """
    turns a nested list into one simple list
    Alim-Marvasti Aug 2019

    allv is the list of lists
    """
    for item in allv:
        if isinstance(item, list):
            make_simple_list(item, allv_simple_list=allv_simple_list)
        else:
            allv_simple_list.append(item)

    return allv_simple_list


def dictionary_key_recursion_(dictionary, all_keys=[], all_values=[]):
    # only initialise for first function run, not nested calls
    """
    return all keys and values in a nested dictionary.
    values may be a list of lists hence the use of the make_simple_list function to open nested lists.
    Ali Alim-Marvasti Aug 2019

    """

    for k, v in dictionary.items():
        all_keys.append(k)

        if isinstance(v, dict):
            all_keys, all_values = dictionary_key_recursion_(v, all_keys=all_keys, all_values=all_values)

        else:  # this returns a list of lists
            all_values.append(v)
            continue

    # this returns a single list of single items and removes the nested lists
    all_values = make_simple_list(all_values, allv_simple_list = [])
    return all_keys, all_values


def dictionary_key_recursion_2(dictionary, semiology_key):
    """
    return the value(s) of a particular key, no matter how nested the key is within the dictionary.
    Ali Alim-Marvasti Aug 2019

    """
    if isinstance(dictionary, list):
        print('No such key in semiology dictionary found. Lookup the dictionary keys. Did you miss a plural \"s\" or a hyphen?')
        yield

    for k, v in dictionary.items():
        if re.search(k, semiology_key, re.IGNORECASE):
        # if k == semiology_key:
            print('dictionary_key_recursion_2 found values of key')
            if isinstance(v, list):
                yield v
                break
            elif isinstance(v, dict):
                # for result in dictionary_key_recursion_2(dictionary[k], semiology_key):
                #     yield result
                allk, allv = dictionary_key_recursion_(v, all_keys=[], all_values=[])
                yield allv
                break

        else:
            print('searching for nested key...')
            if isinstance(v, dict):
                # for kk, vv in v.items():
                for result in dictionary_key_recursion_2(dictionary[k], semiology_key):
                    yield result




def use_semiology_dictionary_(semiology_term, semiology_dict_path):
    print('using option use_semiology_dictionary as taxonomy replacement')
    # define the key rather than the terms

    semiology_key = semiology_term

    # open the semiology_dictionary yaml_file
    semiology_dictionary = yaml.load(open(semiology_dict_path))  # yaml file

    # get all the keys from the semiology_dictionary:
    all_keys, _ = dictionary_key_recursion_(semiology_dictionary['semiology'])

    # check the query exists in the keys:
    if not re.search(semiology_key, str(all_keys), re.IGNORECASE):
        print('\nNo such key found in semiology_dictionary matching %s'%semiology_key)
        print('Running with use_semiology_dictionary option DISABLED.')
        return [semiology_term]

    # if it does, then use the list of values of this key:
    elif re.search(semiology_key, str(all_keys), re.IGNORECASE):
        print('...\"%s\" key definitely exists in semiology_dictionary using REGEX...'%semiology_key)

    # find the key, values in first key layers: pretty sure we can skip this and just use dictionary_key_recursion_2
    dict_comprehension = {key:values for (key, values) in semiology_dictionary['semiology'].items() if key.lower()==semiology_key.lower()}
    if dict_comprehension:
        print('dict_comprehension = \n', dict_comprehension)
        _, values = dictionary_key_recursion_(dict_comprehension)
        # # this returns a single list of single items and removes the nested lists
        # values = make_simple_list(values)

        print('values from dictionary_key_recursion_(dict_comprehension): \n', values)
        return values

    # if the key wasn't found then it is nested:
    elif not dict_comprehension:
        values = dictionary_key_recursion_2(semiology_dictionary['semiology'], semiology_key)
        # convert generator to a simple list (list(values) makes a list of lists)
        values = make_simple_list(list(values), allv_simple_list = [])

    # if not re.search(semiology_key, str(semiology_dictionary['semiology'].keys()), re.IGNORECASE):
    #     values = dictionary_key_recursion_2(semiology_dictionary['semiology'], semiology_key)
    #     print('values is of type:', type(values))

    # elif semiology_key in semiology_dictionary['semiology'].keys():
    #     values = semiology_dictionary['semiology'][semiology_key]
    #     print('values is of type:', type(values))

    return values



def regex_ignore_case(term_values):
    """
    turn items in list "term_values" to regexes with ignore case
    """
    output=[]
    for item in term_values:
        output.append(r'(?i)'+item)
    return output



def QUERY_SEMIOLOGY(df, semiology_dict_path, semiology_term=['love'],
                    ignore_case=True, use_semiology_dictionary=False,
                    col1 = 'Reported Semiology',
                    col2 = 'Semiology Category'):
    """
    Search for key terms in both "reported semiology" and "semiology category" and return df if found in either.
    Removes all columns which are entirely null.

    ---
    df is the MegaAnalysis DataFrame
    semiology_term is the query (can be a user-defined list e.g. ["epigastric aura", "rising sensation"]) - treated as "OR"
    ignore_case: ignores case using a regular expression
    use_semiology_dictionary uses the yaml dictionary of equivalent terms, cycles through all equivalent terms and appends
        results to the output df before removing duplicates
        (instead of using user defined semiology_term lists, uses pre-defined yaml dictionary)
        keyword-based user queries are mapped to ontology entities

    returns a DataFrame subset of df input containing all the results from the df - no melting or pivoting.

    """

    # initialise return object
    inspect_result = pd.DataFrame()


    # # atm this does not work
    # # Cycle case where term is a list and use_semiology_dictionary is True:
    # if isinstance(semiology_term, list) & use_semiology_dictionary==True:
    #     for item in semiology_term:
    #         inspect_res = QUERY_SEMIOLOGY(df, semiology_term=item, ignore_case=ignore_case, use_semiology_dictionary=True)
    #         inspect_result.append(inspect_res)
    #     inspect_result.drop_duplicates(inplace=True)
    #     return inspect_result


    # main body of function
    if isinstance(semiology_term, list):
        if ignore_case:
            semiology_terms = []
            for item in semiology_term:
                semiology_terms.append(r'(?i)'+item)
            semiology_term = semiology_terms
        values = semiology_term     # this is to avoid making a double list

    elif isinstance(semiology_term, str):
        # this is if there is only one term e.g. "love" and we don't want each letter to be used
        if ignore_case:
            semiology_term = r'(?i)'+semiology_term
        values = [semiology_term]


    if use_semiology_dictionary:
        values_dict_or_list = use_semiology_dictionary_(
            semiology_term,
            semiology_dict_path,
        )

        if isinstance(values_dict_or_list, list):
            values = values_dict_or_list
        elif isinstance(values_dict_or_list, dict):
            print("this shouldn't occur: use_semiology_dictionary_ has returned a dict. Attempted to correct... ")
            # when the semiology_term used in the dictionary refers to a top level key which is itself a dictionary
            _, values = dictionary_key_recursion_(values_dict_or_list)
            values = make_simple_list(values)
        else:
            print('What just happened? Neither dict nor list.')
            return
        # turn these values to regexes too:
        values = regex_ignore_case(values)


    for term in values:
        inspect_result = inspect_result.append(
            df.loc[df[col1].str.contains(term, na=False)], sort=False
        )
        inspect_result = inspect_result.append(
            df.loc[df[col2].str.contains(term, na=False)], sort=False
        )

    inspect_result = inspect_result.dropna(axis='columns', how='all')  # may remove lateralising or localising if all nan

    try:
        inspect_result.drop_duplicates(inplace=True)
    except ValueError:
        print('QUERY SEMIOLOGY ERROR: This semiology was not found within the reported literature nor in the semiology categories')
        return


    print('\nLocalising Datapoints relevant to query %s: '%semiology_term, inspect_result['Localising'].sum())
    try:
        print('Lateralising Datapoints relevant to query: ', inspect_result['Lateralising'].sum())
    except:
        print('Lateralising Datapoints relevant to query: 0')
    return inspect_result.sort_index()
