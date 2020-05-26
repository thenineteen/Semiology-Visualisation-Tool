import mega_analysis
from mega_analysis import Semiology, Laterality




semiology = Semiology(
    # 'Figure of 4',
    # symptoms_side=Laterality.LEFT,
    # dominant_hemisphere=Laterality.LEFT,

    # 'Blink',
    # Laterality.NEUTRAL,
    # Laterality.LEFT,

    'All Automatisms (oral, automotor)',
    Laterality.LEFT,
    Laterality.LEFT,

    # 'Grimace', Laterality.NEUTRAL, Laterality.NEUTRAL,
)
num_patients_dict = semiology.get_num_datapoints_dict()
print('Result:', num_patients_dict)
