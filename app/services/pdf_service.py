import fitz


class PDFReader:

    def extract_text(
            self,
            pdf_path):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:

            text += page.get_text()

        return text