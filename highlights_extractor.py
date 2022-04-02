from typing import List, Tuple
import fitz


class HighlightsExtractor:

    def extract_annotated_pages(self, from_path: str, to_path: str):
        doc = fitz.open(from_path)
        doc2 = fitz.open()

        i = 0
        pages_hightlighted = 0
        for page in doc:
            highlights = self.handle_page(page)
            if highlights:
                doc2.insert_pdf(doc, from_page=i, to_page=i)
                pages_hightlighted += 1
            i += 1

        if pages_hightlighted > 10:
            doc2.save(to_path)
        else:
            doc2.close()
        pass

    def handle_page(self, page):
        wordlist = page.getText("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        highlights = []
        annot = page.firstAnnot
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