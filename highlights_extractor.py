from typing import List, Tuple
import fitz
from datetime import datetime


class HighlightsExtractor:

    def find_last_modify_time_from_annotations(self, file_path: str):
        doc = fitz.open(file_path)

        mod_time = 0

        for page in doc:
            annotation = page.first_annot
            if annotation:
                mod_time = max(mod_time, self._parse_time(annotation))
                pass
        return mod_time

    def _parse_time(self, annotation):
        to_parse = annotation.info['modDate']
        try:
            return datetime.strptime(to_parse[2:14], '%Y%m%d%H%M').timestamp()
        except ValueError:
            print(f'Could not extract timestamp from {to_parse}')
            return 0

    def extract_annotated_pages(self, from_path: str, to_path: str):
        doc = fitz.open(from_path)
        doc2 = fitz.open()

        pages_index = 0
        pages_hightlighted = 0
        for page in doc:
            highlights = self.handle_page(page)
            if highlights:
                doc2.insert_pdf(doc, from_page=pages_index, to_page=pages_index)
                pages_hightlighted += 1
            pages_index += 1

        if pages_hightlighted > 10 and pages_index > 25:
            doc2.save(to_path)
        else:
            doc2.close()
        pass

    def handle_page(self, page):
        wordlist = page.get_text("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        highlights = []
        annot = page.first_annot
        while annot:
            if annot.type[0] == 8:
                highlights.append(self._parse_highlight(annot, wordlist))
            annot = annot.next
        return highlights

    def _parse_highlight(self, annot: fitz.Annot,
                         wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
        points = annot.vertices
        quad_count = int(len(points) / 4)
        sentences = []
        for i in range(quad_count):
            # where the highlighted part is
            r = fitz.Quad(points[i * 4: i * 4 + 4]).rect

            words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
            sentences.append(" ".join(w[4] for w in words))
        sentence = " ".join(sentences)
        return sentence