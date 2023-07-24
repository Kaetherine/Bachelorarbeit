import pandas as pd

from s3_bucket import *
from get_zara import extract_products
from logger import setup_logger
from helper_functions import convert_date, date

logger = setup_logger()

def normalize_pantone():
    '''docstring here'''
    tcx = get_bucket_file('pantone_tcx.json')
    pantone_tcx = []
    for color in tcx['data']['getBook']['colors']:
        pantone_tcx.append({
            'code': color['code'],
            'name': color['name'],
            'rgb_r': color['rgb']['r'],
            'rgb_g': color['rgb']['g'],
            'rgb_b': color['rgb']['b'],
            'hex': color['hex'],
            'lab_l': color['lab']['l'],
            'lab_a': color['lab']['a'],
            'lab_b': color['lab']['b'],
            'cmyk': color['cmyk']
            })
    # pantone_tn = get_bucket_file('pantone_tn.json')
    # pantone_tpg = get_bucket_file('pantone_tpg.json')
    # pantone_tsx = get_bucket_file('pantone_tsx.json')
    return None

pantone = normalize_pantone()
print(pantone)
