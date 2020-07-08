from mega_analysis.crosstab.mega_analysis.custom_semiology_SemioDict_lookup import \
    custom_semiology_lookup


def test_custom_semiology_lookup():
    does_not_exist = custom_semiology_lookup(
        'custom_semio_does_not_exist', found=[])

    does_exist_Semio = custom_semiology_lookup('Semiology', found=[])
    does_exist_epigastric = custom_semiology_lookup('Epigastric', found=[])
    does_exist_butterflies = custom_semiology_lookup('butterflies', found=[])
    does_exist_Caps_Cephalic = custom_semiology_lookup('Cephalic', found=[])

    assert not does_not_exist
    assert does_exist_Semio
    assert 'Epigastric' in does_exist_epigastric
    assert 'Epigastric' in does_exist_butterflies
    assert 'Non-Specific Aura' in does_exist_Caps_Cephalic


if __name__ == "__main__":
    test_custom_semiology_lookup()
