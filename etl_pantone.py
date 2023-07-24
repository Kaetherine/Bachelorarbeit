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
        })
        print(color)
    # df_pantone_tcx = df_pantone_tcx[['code', 'name', 'rgb.r', 'rgb.g', 'rgb.b', 'hex', 'lab.l', 'lab.a', 'lab.b', 'cmyk']]

    # pantone_tn = get_bucket_file('pantone_tn.json')
    # pantone_tpg = get_bucket_file('pantone_tpg.json')
    # pantone_tsx = get_bucket_file('pantone_tsx.json')
    return None

pantone = normalize_pantone()
print(pantone)
