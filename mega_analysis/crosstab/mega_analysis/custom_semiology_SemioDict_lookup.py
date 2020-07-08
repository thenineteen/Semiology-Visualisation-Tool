from pathlib import Path
import re
import yaml

repo_dir = Path(__file__).parent.parent.parent.parent
resources_dir = repo_dir / 'resources'
# excel_path = resources_dir / 'syst_review_single_table.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

with open(semiology_dict_path) as f:
    SemioDict = yaml.load(f, Loader=yaml.FullLoader)


def custom_semiology_lookup(custom_semiology, nested_dict=SemioDict,
                            found=[]) -> list:
    """
    User enters custom semiology.
    Top level function will use this to find a match within SemioDict:
        semiology_exists_already = custom_semiology_lookup(custom_semiology)
        if semiology_exists_already is None:
            pass
        else:
            pop-up window("Note this custom semiology may already exist within the category {}".format(k))

    Depending on what functionality is required, could change returns to yield:
        could use yield if potentially more than one match
    """
    for k, v in nested_dict.items():
        # look for matching keys only in top level
        if re.search(r'(?i)' + custom_semiology, k):
            found.append(k)
        elif re.search(r'(?i)' + k, custom_semiology):
            found.append(k)
        elif isinstance(v, list):
            for regex_item in v:
                if re.search(r'(?i)' + regex_item, custom_semiology):
                    found.append(k)
        elif isinstance(v, dict):
            # run it again to open nested dict values:
            custom_semiology_lookup(
                custom_semiology, nested_dict=v, found=found)
        else:  # single regex term in the value of the key
            if re.search(r'(?i)' + v, custom_semiology):
                found.append(k)

    return found
