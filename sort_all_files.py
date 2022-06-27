

import os.path
from datetime import datetime

from highlights_extractor import HighlightsExtractor
from pdf_file_iterator import PdfFileIterator

if __name__ == "__main__":
    files = []
    iterator = PdfFileIterator()
    for f in iterator.iterate('.'):
        files.append(f)
        print(datetime.fromtimestamp(os.path.getmtime(f)))
    print(files)

