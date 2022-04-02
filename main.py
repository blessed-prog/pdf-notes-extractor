from highlights_extractor import HighlightsExtractor

if __name__ == "__main__":
    extractor = HighlightsExtractor()
    extractor.extract_annotated_pages('mongo.pdf', 'mongo_out.pdf')