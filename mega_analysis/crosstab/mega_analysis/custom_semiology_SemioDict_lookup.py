
import re
import yaml

from ...semiology.py import

repo_dir = Path(__file__).parent.parent.parent.parent
resources_dir = repo_dir / 'resources'
# excel_path = resources_dir / 'syst_review_single_table.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

with open(semiology_dict_path) as f:
    SemioDict = yaml.load(f, Loader=yaml.FullLoader)


def custom_semiology_lookup(custom_semiology, nested_dict=SemioDict):
    """
    User enters custom semiology.
    Top level function will use this to find a match within SemioDict:
        semiology_exists_already = custom_semiology_lookup(custom_semiology)
        if semiology_exists_already is None:
            pass
        else:
            pop-up window("Note this custom semiology may already exist within the category {}".format(k))
    """
    for k, v in nested_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if isinstance(v, dict):
            # look for matching keys only in top level
            if re.search(custom_semiology, k) | re.search(k, custom_semiology):
                return k
            else:
                # run it again to open nested dict values:
                custom_semiology_lookup(
                    custom_semiology, nested_dict=v)
        else:
            if re.search(custom_semiology, k) | re.search(custom_semiology, str(v)):
                # could use yield if potentially more than one match
                return k
            if re.search(k, custom_semiology) | re.search(str(v), custom_semiology):
                # could use yield if potentially more than one match
                return k

    return None
