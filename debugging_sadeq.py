import mega_analysis
from mega_analysis import Semiology, Laterality




patient = Semiology(
    # 'Figure of 4',
    # symptoms_side=Laterality.LEFT,
    # dominant_hemisphere=Laterality.LEFT,

    # 'Blink',
    # Laterality.NEUTRAL,
    # Laterality.LEFT,

    # 'All Automatisms (oral, automotor)',
    # Laterality.LEFT,
    # Laterality.LEFT,

    # 'Grimace', Laterality.NEUTRAL, Laterality.NEUTRAL,

    'love',
    Laterality.NEUTRAL,
    Laterality.NEUTRAL,
)

heatmap = patient.get_num_datapoints_dict()
print('Result:', heatmap)
