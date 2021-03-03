"""
Command-line entry point from setup links to this file.
It runs the preprocessing sections without visualisation.
It should be called with "MEGA_ANALYSIS_CONSOLE" followed by args.

"""
from argparse import ArgumentParser
from mega_analysis.crosstab.mega_analysis import MEGA_ANALYSIS, QUERY_SEMIOLOGY, QUERY_LATERALISATION
import yaml
import mega_analysis
from mega_analysis import Semiology, Laterality


def run_preprocess():
    parser = ArgumentParser(description="Epilepsy SVT Preprocessing")
    parser.add_argument('excel_data')  # where the data is locally for dev purposes when updating data to ensure works- make into test later
    parser.add_argument('plot')  # add default later
    parser.add_argument('kwargs')
    parser.add_argument('--true', '-t', action='store_true')  # -t: future use to be able to run or omit a section of the code
    arguments = parser.parse_args()

    output1 = MEGA_ANALYSIS (excel_data=arguments.excel_data,
                             n_rows=2815,
                             usecols="A:DY",
                             header=1,
                             exclude_data=False,
                             plot=True,
                             **arguments.kwargs,
                            )
    # output2 = output1.SOMEFUNCTION(arguments.true)

    # -t: future use to be able to run or omit a section of the code
    try:
        if arguments.true:
            pass
        else:
            pass
    except(TypeError):
            pass


def run_query():
    parser = ArgumentParser(description="Epilepsy SVT query")
    parser.add_argument('semio')  # where the data is locally for dev purposes when updating data to ensure works- make into test later
    parser.add_argument('symptoms_side')
    parser.add_argument('dominant_hemisphere')  # add default later e.g. Laterality.LEFT
    parser.add_argument('--true', '-t', action='store_true')  # -t: future use to be able to run or omit a section of the code
    arguments = parser.parse_args()

    symptoms_side = arguments.semio
    dominant_hemisphere = arguments.dominant_hemisphere

    heatmap = Semiology(
        arguments.semio,
        Laterality.symptoms_side,
        Laterality.dominant_hemisphere,
        )
    num_patients_dict, _ = heatmap.get_num_datapoints_dict()
    print('Result:', num_patients_dict)

    # output2 = output1.SOMEFUNCTION(arguments.true)

    # -t: future use to be able to run or omit a section of the code
    try:
        if arguments.true:
            pass
        else:
            pass
    except(TypeError):
            pass


if __name__ == "__main__":
    run_query()
