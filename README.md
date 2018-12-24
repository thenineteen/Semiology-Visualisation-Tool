***Ali Alim-Marvasti Dec 2018***
**Wellcome/EPSRC Centre for Interventional and Surgical Sciences WEISS**
***University College London***

First thing is first: 
1. the sample PDFs with 'PDF_form_example' are the only PDFs which are read by the PyPDF2 methods of .getFields() and .getFormTextFields()
2. Currently .getFormTextFields() is used on line 32 - but .getFields() works best with these PDFs 'PDF_form_example'
3.  none of the following methods of PyPDF2 work for the epilepsy PDFs (but they do for other PDFs)
    .getFields()
    .getFormTextFields()
    .extractText()
4. What we want is for the other PDFs to be read which isn't working currently. I've also tried pdfminer.six - can't even read number of pages
   1. not an excryption problem as read_pdf.isEncrypted returns False
what is the solution?



***USELESS CODE***
***THIS CODE doesn't work with the epilepsy PDFs!***
import io

pdf_path = (
'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\preprocessing\\tests\\test pdfs\\Marie_C_5403296 19.12.91.pdf'
)

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text
    else:
        print("no!")
 
 ***NEITHER DOES THIS CODE***
import io
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()
 
def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()


***NOR THIS CODE***
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine



with open(path, 'rb') as fp:
    
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()

*MetaData*

*Files*

*Installation*




*Running from command line cmd*
*Syntax and Exceptions*