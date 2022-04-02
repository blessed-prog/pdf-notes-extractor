import os


class PdfFileIterator:

    def iterate(self, dir_path: str):
        tree = os.walk(dir_path)
        for address, dirs, files in tree:
            for file in files:
                if file.endswith('.pdf'):
                    yield os.path.join(address, file)