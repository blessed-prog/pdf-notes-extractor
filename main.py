import os.path

from highlights_extractor import HighlightsExtractor
from pdf_file_iterator import PdfFileIterator

if __name__ == "__main__":
    for filepath in PdfFileIterator().iterate('.'):
        file_name = os.path.basename(filepath)
        dir_name = os.path.dirname(filepath)
        output_file_name = file_name.replace('.pdf', '') + '_highlighted.pdf'
        output_filepath = os.path.join(dir_name, output_file_name)
        print(f'Will process ${filepath}, output path is ${output_filepath}')

        extractor = HighlightsExtractor()
        extractor.extract_annotated_pages(filepath, output_filepath)