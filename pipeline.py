# Import the key used libraries
import os
import sys
import pandas as pd
import numpy as np
import PyPDF2
import re
from data_load_functions import *
from joblib import Parallel, delayed
import pickle
try:
    import geopandas as gpd
except:
    print('geopandas not found, will enter exception blocks throughout')
    pass


def create_npd_shapefile_dict_preprocess(main_path='./sample_data/'):
    """
    Function designed to grab a variety of shape files from the NPD database.  Assumes hard coded files are present

    Arguments:
        main_path:  string, absolute file path to the shapefiles

    Returns:  dictionary of files

    @ author:  Nathan Jones
    """

    # Create a dictionary of file paths
    try:
        files = {'blocks': os.path.join(main_path, 'shapefiles', 'loc_npd_blocks.shp'),
                 'discoveries': os.path.join(main_path, 'shapefiles', 'loc_npd_discoveries.shp'),
                 'well_bores': os.path.join(main_path, 'shapefiles', 'loc_npd_ea_wells.shp'),
                 'wells': os.path.join(main_path, 'shapefiles', 'loc_npd_ea_wells.shp'),
                 'facilities': os.path.join(main_path, 'shapefiles', 'loc_npd_facilities.shp'),
                 'fields': os.path.join(main_path, 'shapefiles', 'loc_npd_fields.shp'),
                 'structures': os.path.join(main_path, 'shapefiles', 'loc_npd_struct_elements.shp'),
                 'structures_en': os.path.join(main_path, 'shapefiles', 'loc_npd_struct_elements.shp'),
                 'basins': os.path.join(main_path, 'shapefiles', 'loc_npd_struct_elements.shp'),
                 'sub_areas': os.path.join(main_path, 'shapefiles', 'loc_npd_subareas.shp')}
    except:
        print('Check list of files for exact files and name matches')
        return None

    # Initialize empty output dictionary and iterate through file dictionary and read over the shapefiles
    output = {}
    for key, value in files.items():
        # Read shape file - Uses geopandas
        output[key] = gpd.read_file(value)

    # Grab well header information from a CSV file
    output['well_header'] = pd.read_csv(os.path.join(main_path, 'with-coordinates.csv'), delimiter=';')

    return output


def get_key_words_preprocess(main_path):
    """
    Function to create a list of possible key words from a shapefile compendium for a certain region

    Arguments:
        main_path: string, absolute file path to the shapefiles

    Returns:  List of alphanumeric + special character strings, and type

    @ author:  Nathan Jones
    """

    # Create dictionary of key columns to go through to find key words from shape files
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

    # Initialize empty lists for output and key word type
    output = []
    type = []

    # This function is presently specific to the Norway Petroleum Database shapefile, if it doesn't work, try a pre-save pkl file
    # should return a dictionary
    try:
        data_dict = create_npd_shapefile_dict_preprocess()
    except Exception as ex:
        object = []
        with open(os.path.join(main_path, 'npd_lookup_dfs_no_geopandas.pkl'), 'rb') as openfile:
            while True:
                try:
                    object.append(pkl.load(openfile))
                except EOFError:
                    break
        data_dict = object[0]

    # Iterate through the returned data dictionary from the shapefiles
    for key, value in data_dict.items():
        if 'well_header' not in key:
            df = pd.DataFrame(value)
            temp = list(df[key_cols[key]])
            temp_type = [key] * len(temp)
            type += temp_type
            output += temp

    return output, type


### Clean up text file
def clean_text(txt):
    """
    Function to clean out any problematic or illegal characters

    Arguments:
        txt:  List of character strings

    Returns:  List of character strings

    @ author:  Christopher Olsen, ConocoPhillips
    """

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
    kw_alpha = [x for x in kw_alpha if len(x) > min_chars]  # return only strings greater than the minimum
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


def ProcessTextFile(document, key_words):
    """
    Function that takes in an absolute file path (e.g. C:\\User\\Documents\\TextFiles\\TextFile.pdf)
    and a list of key words to search over

    Returns:  Dataframe of search results narrowed down to just the positive findings

    @ author:  Christopher Olsen, ConocoPhillips
    """
    try:
        # Verify some initial conditions first
        if isinstance(key_words, (list,)):
            pass
        else:
            print('Key words must be a proper python list')
            return None

        if isinstance(document, (list,)):
            print('This function is for a single pdf document only')
            return None
        else:
            pass

        assert isinstance(document, (str,))
        if not document[-4:].lower() == '.pdf':
            print('This function is presently designed only to process OCR complete PDF documents')
            return None
        else:
            pass

        # Open the document as a PDF object, read each page, and shove into a list
        with open(document, 'rb') as pdfFileObj:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            txt = []
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                page_txt = pageObj.extractText()
                txt.extend(page_txt)

        # Join all characters together as one single character string
        txt = ''.join(txt)

        # Split apart each line into a list of lines based on the common \n newline character
        txt = txt.splitlines()

        # Run a text cleaning process on the text file that will roughly match the same process as for key words
        txt = clean_text(txt)

        # Create dataframe framework to build off of
        df_txt = pd.DataFrame({'Document': [document] * len(txt), 'Lines': txt})

        # Iterate over each line of text (may take a moment)
        for word in key_words:
            df_txt[word] = pd.Series([x.find(word) for x in txt])

        # Convert numeric results to numeric flag, ignore positional location from result here
        ndf = df_txt._get_numeric_data()
        ndf[ndf < 0] = 0
        ndf[ndf > 1] = 1

        # Aggregate the results
        results = [df_txt[col].sum() for col in df_txt.columns[2:]]

        # Create new dataframe based on the document, key words, and sum of matches
        df = pd.DataFrame(
            {'Document': [document] * len(df_txt.columns[2:]), 'Key_Words': df_txt.columns[2:], 'Total_Matches': results})

        # Reduce size of dataframe only to matches to key words
        df = df[df['Total Matches'] > 0]

        return df
    except Exception as ex:
        print(ex)
        return pd.DataFrame()

if __name__ == '__main__':
    # Define our main data path where the shape files may be loaded from
    data_path ='/media/nathanieljones/New Volume/univ stavanger documents-20190918T063414Z-001/univ stavanger documents/'
    document_folder = data_path
    # document_folder = os.path.join(data_path, 'text_documents\\')
    # singular document used for testing purposes
    test_document = 'Rock physics models for Cenozoic siliciclastic sediments in the North Sea.pdf'
    # Used only if geopandas doesn't work, pre-exported list of raw key words as a list
    keywords_list = 'keywords.pkl'
    # Try to use the primary coded functions, otherwise default back to pickle file
    try:
        kw, _ = get_key_words_preprocess('/')
    except Exception as ex:
        print(ex)
        print('Possibly missing GeoPandas package')
        with open(os.path.join(data_path, keywords_list), 'rb') as openfile:
            kw = pkl.load(openfile)
    # Created exception list of character strings we want to make sure are included in the search strings
    exception_list = [' tor ']    # Note, extra white space on either side given it's combination is frequently part of larger words
    # Clean up key words creating letter based key words as well as supposed well names
    kw = PreprocessKeyWords(kw, clean=True, exception_list = exception_list, min_chars = 3)
    # Create list of text documents (PDFs)
    documents = os.listdir(document_folder)
    documents = [os.path.join(document_folder, x) for x in documents]
    # Initialize empty list
    df_list = []

    # Iterate over the list of documents (may take a little while, would benefit from parallelization)
    df_list = Parallel(n_jobs=1)(
       delayed(ProcessTextFile)(doc, kw) for doc, kw in zip(documents, [kw] * len(documents)))
    # for doc in documents:
    #     df_list.append(ProcessTextFile(doc, kw))

    # Stack together the output dataframes from the search string results
    ResultDF = pd.concat(df_list)
    with open('thesis_docs.pkl', 'wb') as f:
        pickle.dump(ResultDF, f)