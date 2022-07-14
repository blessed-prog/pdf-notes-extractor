import os.path
from datetime import datetime

from pdf_file_iterator import PdfFileIterator

if __name__ == "__main__":
    files = []
    iterator = PdfFileIterator()
    for file in iterator.iterate('.'):
        files.append(file)
        print(datetime.fromtimestamp(os.path.getmtime(file)))

    files.sort(key=os.path.getmtime)

    for file in files:
        print(f'{datetime.fromtimestamp(os.path.getmtime(file))}: {file}')
