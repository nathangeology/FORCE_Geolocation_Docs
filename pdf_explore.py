import PyPDF2
from data_load_functions import *
from collections import defaultdict

if __name__ == "__main__":
    keywords, types = get_key_words()
    file = 'sample_data/Rock physics models for Cenozoic siliciclastic sediments in the North Sea.pdf'
    with open(file, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        output = defaultdict(list)
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            page_txt = pageObj.extractText()
            for idx, x in enumerate(keywords):
                if not isinstance(x, str):
                    print('why!?')
            [output[x].append(page) for x in keywords if str(x) in string_cleaner(page_txt)]
            # print(page_txt)
        print('here')

    # attach document to matched entities



    # raw = parser.from_file(
    #     'sample_data/Rock physics models for Cenozoic siliciclastic sediments in the North Sea.pdf')
    # print(raw['content'])