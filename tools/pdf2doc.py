from pdf2docx import Converter


def pdf_convert(pdf_file, docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()


if __name__ == '__main__':
    pdf_file = '/Users/huanglele/Desktop/面单.pdf'
    docx_file = '/Users/huanglele/Desktop/面单.docx'
    pdf_convert(pdf_file, docx_file)
