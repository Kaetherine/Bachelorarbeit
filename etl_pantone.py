import pandas as pd

from s3_bucket import get_bucket_file

def normalize_pantone(filename):
    '''Takes a pantone catalog as json file and normalizes it
    by seperating it into two tables 'color_configs' and 'color_names'.
    Returns color_configs and color_names of given pantone color catalog.
    '''
    color_data = get_bucket_file(filename)
    color_configs = []
    color_names = []
    for color in color_data['data']['getBook']['colors']:
        color_configs.append({
            'hex': f"#{color['hex']}",
            'rgb_r': color['rgb']['r'],
            'rgb_g': color['rgb']['g'],
            'rgb_b': color['rgb']['b'],
            'lab_l': color['lab']['l'],
            'lab_a': color['lab']['a'],
            'lab_b': color['lab']['b'],
            'cmyk': color['cmyk'],
            'code': color['code'],

            })
        color_names.append({
            'code': color['code'],
            'color_name': color['name']
            })
        
    color_configs = pd.DataFrame(color_configs)
    color_names = pd.DataFrame(color_names)

    return color_configs, color_names

def organize_colors():
    '''Normalizes pantone color data, merges the color_configs and 
    color_names of different pantone catalouges. Returns merged
    color_configs and color_names.'''
    tcx_color_configs, tcx_color_names = normalize_pantone('pantone_tcx.json')
    tn_color_configs, tn_color_names = normalize_pantone('pantone_tn.json')
    tpg_color_configs, tpg_color_names = normalize_pantone('pantone_tpg.json')
    tsx_color_configs, tsx_color_names = normalize_pantone('pantone_tsx.json')

    color_configs = pd.concat([
        tcx_color_configs, tn_color_configs,
        tpg_color_configs, tsx_color_configs
    ])

    color_names = pd.concat([
        tcx_color_names, tn_color_names,
        tpg_color_names, tsx_color_names
    ])

    return color_configs, color_names

color_configs, color_names = organize_colors()

print(color_configs,'\n', '\n', color_names)