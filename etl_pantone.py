from s3_bucket import get_bucket_file
from postgres_db import copy_csv_to_db

def normalize_pantone(filename):
    '''Takes a pantone catalog as json file and normalizes it
    by seperating it into two tables 'color_configs' and 'color_names'.
    Returns color_configs and color_names of given pantone color catalog.
    '''
    color_data = get_bucket_file(filename)
    color_configs = []
    color_names = []
    for color in color_data['data']['getBook']['colors']:
        color_configs.append((
            f"#{color['hex']}", color['rgb']['r'],
            color['rgb']['g'], color['rgb']['b'],
            color['lab']['l'], color['lab']['a'],
            color['lab']['b'], color['cmyk'],
            color['code']
            ))
        
        color_names.append((color['code'],color['name']))

    return color_configs, color_names

def organize_colors():
    '''Normalizes pantone color data, merges the color_configs and 
    color_names of different pantone catalouges. Returns merged
    color_configs and color_names.'''
    color_configs = []
    color_names = []

    tcx_color_configs, tcx_color_names = normalize_pantone('pantone_tcx.json')
    tn_color_configs, tn_color_names = normalize_pantone('pantone_tn.json')
    tpg_color_configs, tpg_color_names = normalize_pantone('pantone_tpg.json')
    tsx_color_configs, tsx_color_names = normalize_pantone('pantone_tsx.json')

    color_configs.extend(tcx_color_configs)
    color_configs.extend(tn_color_configs)
    color_configs.extend(tpg_color_configs)
    color_configs.extend(tsx_color_configs)

    color_names.extend(tcx_color_names)
    color_names.extend(tn_color_names)
    color_names.extend(tpg_color_names)
    color_names.extend(tsx_color_names)

    return color_configs, color_names

color_configs, color_names = organize_colors()
copy_csv_to_db(color_configs, 'hex_colors.csv', 'hex_colors')
copy_csv_to_db(color_names, 'color_names.csv', 'color_names')