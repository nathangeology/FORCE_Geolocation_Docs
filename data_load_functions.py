try:
    import geopandas as gpd
except Exception as ex:
    print(ex)
import pandas as pd
import pickle as pkl
import re
import numpy as np

def load_shape_file(file):
    output = gpd.read_file(file)
    return output

def create_npd_shapefile_dict():
    files = {
        'blocks': 'sample_data/shapefiles/loc_npd_blocks.shp',
        'discoveries': 'sample_data/shapefiles/loc_npd_discoveries.shp',
        'well_bores': 'sample_data/shapefiles/loc_npd_ea_wells.shp',
        'wells': 'sample_data/shapefiles/loc_npd_ea_wells.shp',
        'facilities': 'sample_data/shapefiles/loc_npd_facilities.shp',
        'fields': 'sample_data/shapefiles/loc_npd_fields.shp',
        # 'licenses': 'sample_data/shapefiles/loc_npd_licenses.shp',
        'structures': 'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'structures_en': 'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'basins':  'sample_data/shapefiles/loc_npd_struct_elements.shp',
        'sub_areas': 'sample_data/shapefiles/loc_npd_subareas.shp',
    }
    output = {}
    for key, value in files.items():
        output[key] = load_shape_file(value)
    output['well_header'] = pd.read_csv('sample_data/with-coordinates.csv', delimiter=';')
    return output


def string_cleaner(a_string:str):
    output = a_string
    output = output.replace('\u00C5', 'aa')
    output = output.replace('\u00E5', 'aa')
    output = output.replace('\u00C6', 'ae')
    output = output.replace('\u00E6', 'ae')
    output = output.replace('\u00C8', 'oe')
    output = output.replace('\u00E8', 'oe')
    output = output.lower()

    return output


def get_key_cols():
    key_cols = {
        'blocks': 'LABEL',
        'discoveries': 'DISCNAME',
        'well_bores': 'wlbWellbor',
        'wells': 'wlbWell',
        'facilities': 'FACNAME',
        'fields': 'FIELDNAME',
        'structures': 'steNameNO',
        'structures_en': 'steNameEN',
        'basins': 'steTopogra',
        'sub_areas': 'NAME',
    }
    return key_cols

def get_key_words():
    key_cols = get_key_cols()
    output = []
    type_of = []
    try:
        data_dict = create_npd_shapefile_dict()
    except Exception as ex:
        objects = []
        with open('npd_lookup_dfs_no_geopandas.pkl', 'rb') as openfile:
            while True:
                try:
                    objects.append(pkl.load(openfile))
                except EOFError:
                    break
        data_dict = objects[0]
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            temp = list(df[key_cols[key]])
            temp = [string_cleaner(x) for x in temp]
            temp_type = [key] * len(temp)
            type_of += temp_type
            output += temp
    return output, type_of

def strip_out_geopandas(data_dict):
    output = {}
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            output[key] = df
        else:
            output[key] = value
    return output


### Clean up text file
def clean_text(txt):
    """
    Function to clean out any problematic or illegal characters

    Arguments:
        txt:  List of character strings

    Returns:  List of character strings

    @ author:  Christopher Olsen, ConocoPhillips
    """
    if isinstance(txt, str):
        txt = [txt]
    txt = [x.lower() for x in txt]  # For ease of use, convert all characters to lowercase
    txt = [x.replace('/', '_') for x in txt]  # Convert forward slash to underscore
    txt = [x.replace('\u00C5', 'aa') for x in txt]  # Convert Norwegian (uppercase version, just in case) to aa
    txt = [x.replace('\u00E5', 'aa') for x in txt]  # Convert Norwegian (lowercase version) to aa
    txt = [x.replace('\u00C6', 'ae') for x in txt]  # Convert Norwegian (uppercase version, just in case) to ae
    txt = [x.replace('\u00E6', 'ae') for x in txt]  # Convert Norwegian (lowercase version) to ae
    txt = [x.replace('\u00C8', 'oe') for x in txt]  # Convert Norwegian (uppercase version, just in case) to oe
    txt = [x.replace('\u00E8', 'oe') for x in txt]  # Convert Norwegian (lowercase version) to oe
    txt = [x.replace('\u00E3', 'oe') for x in txt]  # Convert Norwegian a tilde to oe
    txt = [x.replace('¸', '') for x in txt]  # Replace special character with nothing
    txt = [x.replace('\u25A1', '') for x in txt]  # Replace 'Yen' symbol with nothing
    txt = [x.replace('\25', '') for x in txt]  # Replace unfilled square with nothing
    #     txt = [x.replace(' ', '_') for x in txt]             # Not used:  Convert whitespace to underscores
    if len(txt) == 1:
        txt = txt[0]
    return txt


def PreprocessKeyWords(key_words, clean=True, exception_list=None, min_chars=3):
    """
    Function used to further process a list of key words that have been generated via a shapefile compendium

    Arguments:
        key_words:  List of strings of key words prepared by other functions in this file
        clean:  boolean, whether or not to run some cleaning functions to remove illegal or problematic characters
        exception_list:  List of strings to ensure are included after trimming down the list
        min_chars:  integer, minimum length of a keyword string to minimize high frequency linguistic combinations

    Returns:  list of strings, key words of a certain form and format

    @ author:  Christopher Olsen, ConocoPhillips
    """

    # Verify some initial conditions first
    if isinstance(key_words, (list,)):
        pass
    else:
        print('Key words must be a proper python list')
        return None

        # Copy list to new variable for simplicity
    kw = key_words

    # If clearn option is selected (True by default)
    if clean:
        kw = clean_text(kw)

    # define regex patterns
    pattern1 = re.compile('\d')  # search/match only digits
    pattern2 = re.compile('^_')  # search/match only a single underscore at beginning of word
    pattern3 = re.compile('\W+')  # search/match only non-alphanumeric characters

    # define complex regex pattern based on Norway Well name convention
    pattern_Norway_Well = re.compile(
        '(\d\d\d\d|\d\d|\d)([\/, ]{1}|[_, ]{1})(\d\d|\d)([-, ]{0,1})(\d\d|\d){0,1}([-, ]{0,1})([a-zA-Z0-9.+_]{0,2})([-]{0,1})(\d\d|\d{0,1})')

    # first prepare non-numeric based keywords
    kw_nonum = [x.replace('_', '').replace('-', '').isdigit() for x in
                kw]  # remove digits after temporarily cutting _ and -
    kw_alpha_inds = np.nonzero(np.array(kw_nonum, dtype=bool) == False)[0]  # grab indices based on boolean array
    kw_alpha = [kw[x] for x in kw_alpha_inds]  # create subsetted list with leading digits cut
    kw_alpha = [re.sub(pattern1, '', x) for x in kw_alpha]  # concatenate characters between pattern1
    kw_alpha = [x.replace('_', '').replace('-', '') for x in kw_alpha]  # concatenate characters around _ and -
    kw_alpha = [x.replace('(', '').replace(')', '') for x in kw_alpha]  # remove leading and trailing parenthesis
    kw_alpha = [re.sub(pattern2, ' ', x) for x in kw_alpha]  # replace pattern2 with whitespace
    # kwc_alpha = [x.replace(' ', '_') for x in kwc_alpha]                     # not used: replace whitespace with _
    kw_alpha = [re.sub(pattern3, ' ', x) for x in kw_alpha]  # replace pattern3 with whitespace
    kw_alpha = [x.replace('__', '_') for x in kw_alpha]  # replace double underscore with single underscore
    kw_alpha = [x if len(x) > min_chars else x for x in kw_alpha]  # return only strings greater than the minimum
    if exception_list is not None:  # if exception list is populated
        kw_alpha.extend(exception_list)  # add back in excepted key words
    kw_alpha = sorted(set(kw_alpha))  # create sorted unique list letter based of key words

    # Second prepare numeric based keywords (e.g. well names)
    kw_well = [re.search(pattern_Norway_Well, x) for x in kw]  # apply complex pattern to find wells
    kw_num = []  # Initialize empty list
    for i in kw_well:  # Iterate over list of matched terms
        if i:  # Since none matches are empty [None], if not empty
            kw_num.append(i.group(0))  # Append to the list the matched first group

    # Combine whittled key words lists
    kw_comb = kw_alpha + kw_num

    return kw_comb

def clean_doc_name(x):
    output = x.split('/')
    return output[-1]


def get_prepped_dfs():
    objects = []
    output = {}
    with open('joined_dfs.pkl', 'rb') as openfile:
        while True:
            try:
                objects.append(pkl.load(openfile))
            except EOFError:
                break
    mudlog_well_header = objects[0]
    output['mudlog_wells'] = mudlog_well_header
    get_keywords_doc = pd.read_csv('result.csv')
    get_keywords_doc['cleaned_doc'] = get_keywords_doc['document'].apply(clean_doc_name)
    get_keywords_doc.set_index(['keyword', 'cleaned_doc'],
                               inplace=True,
                               drop=False)
    doc_keywords_set = set(get_keywords_doc['keyword'])
    shape_files_dict = create_npd_shapefile_dict()
    key_cols = get_key_cols()
    for key, value in shape_files_dict.items():
        value['document'] = None
        if key == 'well_header':
            continue
        keyword_col = key_cols[key]
        value['cleaned_keywords'] = value[keyword_col].apply(clean_text)
        value.set_index(['cleaned_keywords'], drop=False, inplace=True)
        shape_keyset = set(list(pd.Series(value['cleaned_keywords'])))
        matched_keys = shape_keyset.intersection(doc_keywords_set)
        for matched_key in list(matched_keys):
            matches = get_keywords_doc.loc[matched_key]
            if isinstance(matches, pd.DataFrame):
                docs = list(matches['cleaned_doc'])
                list_of_docs = ','.join(docs)
                value.loc[matched_key, 'document'] = list_of_docs
            else:
                value.loc[matched_key, 'document'] = matches['cleaned_doc']
        output[key] = value
    return output
