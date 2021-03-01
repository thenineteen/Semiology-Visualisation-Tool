import time
import logging
import pandas as pd
from tqdm import tqdm
from mega_analysis import get_all_semiology_terms, Semiology, Laterality


log_path = 'benchmark_output.log'
csv_path = 'benchmark_output.csv'


LEFT = 'L'
RIGHT = 'R'
sides = Laterality.LEFT, Laterality.RIGHT

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    filemode='w',
)

rows = []
for semiology_term in get_all_semiology_terms():
    for symptoms_side in sides:
        for dominant_hemisphere in sides:
            tic = time.time()
            semiology = Semiology(
                semiology_term,
                symptoms_side,
                dominant_hemisphere,
            )
            try:
                scores_dict, _ = semiology.get_num_datapoints_dict()
            except Exception as e:
                logging.error(e)
                scores_dict = None
            toc = time.time()
            seconds = toc - tic
            if scores_dict is None:
                function = logging.error
            elif seconds > 1:
                function = logging.warning
            else:
                function = logging.info
            function(f'Semiology term: {semiology_term}')
            function(f'Symptoms side: {symptoms_side}')
            function(f'Dominant hemisphere: {dominant_hemisphere}')
            function(f'Time: {seconds} seconds')
            function('')
            row = dict(
                Semiology=semiology_term,
                Symptoms=symptoms_side,
                Dominant=dominant_hemisphere,
                Seconds=seconds,
                Error=(scores_dict is None),
            )
            rows.append(row)
    logging.info('')
    logging.info('')
    logging.info('')
    logging.info('')

df = pd.DataFrame.from_records(rows)
df.to_csv(csv_path)
