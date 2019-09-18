import PyPDF2
from .data_load_functions import *

if __name__ == "__main__":
    keywords, types = get_key_words()
    file =  'sample_data/Rock physics models for Cenozoic siliciclastic sediments in the North Sea.pdf'
    with open(file, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            page_txt = pageObj.extractText()

            print(page_txt)

    # raw = parser.from_file(
    #     'sample_data/Rock physics models for Cenozoic siliciclastic sediments in the North Sea.pdf')
    # print(raw['content'])