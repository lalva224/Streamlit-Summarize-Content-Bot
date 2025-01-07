from docx import Document
from io import BytesIO
import PyPDF2
from PIL import Image

def load_word_file(file):
    #bytesIO allows to read and write binary data
    doc= Document(file)
    res =  '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return res
def load_pdf_file(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text+=page.extract_text() + '\n'
    print(text)
    return text
def load_image_file(file):
    image = Image.open(file)
    return image
def load_txt_file(file):
    text = file.read()
    decoded_text = text.decode('utf-8')
    return decoded_text

def load_file(file,file_name):
    if file_name.endswith('.docx'):
        return load_word_file(file)
    elif file_name.endswith('.pdf'):
        return load_pdf_file(file)
    elif file_name.endswith('.txt'):
        return load_txt_file(file)
    elif file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
        return load_image_file(file)
    else:
        return None
