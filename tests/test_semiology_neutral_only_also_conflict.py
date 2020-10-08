

from pathlib import Path
repo_dir = Path(__file__).parent.parent
resources_dir = repo_dir / 'resources'

# Read default list
default_path = resources_dir / 'semiologies_lateralised_only_default_list.txt'
default_list = default_path.read_text().splitlines()

# Read lateralities for GUI
neutral_only_path = resources_dir / 'semiologies_neutral_only.txt'
neutral_also_path = resources_dir / 'semiologies_neutral_also.txt'
semiologies_neutral_only = neutral_only_path.read_text().splitlines()
semiologies_neutral_also = neutral_also_path.read_text().splitlines()

# Read postictal lateralities for GUI
postictal_neutral_only_path = resources_dir / \
    'semiologies_postictalsonly_neutral_only.txt'
postictal_neutral_also_path = resources_dir / \
    'semiologies_postictalsonly_neutral_also.txt'
postictal_semiologies_neutral_only = postictal_neutral_only_path.read_text().splitlines()
postictal_semiologies_neutral_also = postictal_neutral_also_path.read_text().splitlines()


def test_semiology_neutrality_conflicts():
    semio_conflicts = [
        i for i in semiologies_neutral_only if i in semiologies_neutral_also]
    postictal_semio_conflicts = [
        i for i in postictal_semiologies_neutral_only if i in postictal_semiologies_neutral_also]

    # print(postictal_semio_conflicts)
    assert not semio_conflicts
    assert not postictal_semio_conflicts


# test_semiology_neutrality_conflicts()
