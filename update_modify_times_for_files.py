import os.path

from highlights_extractor import HighlightsExtractor
from pdf_file_iterator import PdfFileIterator

if __name__ == "__main__":

    dir_to_scan = '/Users/andreycheboksarov/Yandex.Disk.localized/Lib'

    for filepath in PdfFileIterator().iterate(dir_to_scan):
        print(filepath)
        extractor = HighlightsExtractor()
        time = extractor.find_last_modify_time_from_annotations(filepath)
        if time > 10000:
            os.utime(filepath, (time, time))
        pass

