from mega_analysis.crosstab.mega_analysis.custom_semiology_SemioDict_lookup import \
    custom_semiology_lookup


def test_custom_semiology_lookup():
    does_not_exist = custom_semiology_lookup(
        'custom_semio_does_not_exist')

    does_exist_Semio = custom_semiology_lookup('Semiology')
    does_exist_epigastric = custom_semiology_lookup('Epigastric')
    does_exist_butterflies = custom_semiology_lookup('butterflies')
    does_exist_Caps_Cephalic = custom_semiology_lookup('Cephalic')
    does_exist_hEaDrUsh = custom_semiology_lookup('hEaD rUsh')
    does_exist_hEaD_multiple = custom_semiology_lookup('hEaD')

    assert not does_not_exist
    assert does_exist_Semio
    assert 'Epigastric' in does_exist_epigastric
    assert 'Epigastric' in does_exist_butterflies
    assert 'Non-Specific Aura' in does_exist_Caps_Cephalic
    assert 'Non-Specific Aura' in does_exist_hEaDrUsh
    assert 'Non-Specific Aura' in does_exist_hEaD_multiple
    assert 'Head or Body Turn' in does_exist_hEaD_multiple
    assert 'Head Version' in does_exist_hEaD_multiple


if __name__ == "__main__":
    test_custom_semiology_lookup()
