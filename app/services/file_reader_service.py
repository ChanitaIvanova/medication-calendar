import PyPDF2
from docx import Document
import os

class FileReaderService:
    @staticmethod
    def read_file(file, file_extension):
        # file_extension should be passed as a string like '.pdf', '.docx', etc.
        
        if file_extension.lower() == '.pdf':
            return FileReaderService._read_pdf(file)
        elif file_extension.lower() == '.docx':
            return FileReaderService._read_docx(file)
        elif file_extension.lower() in ['.txt', '.md']:
            return FileReaderService._read_text(file)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    @staticmethod
    def _read_pdf(file):
        reader = PyPDF2.PdfReader(file)
        return ' '.join(page.extract_text() for page in reader.pages)

    @staticmethod
    def _read_docx(file):
        doc = Document(file)
        return ' '.join(paragraph.text for paragraph in doc.paragraphs)

    @staticmethod
    def _read_text(file):
        return file.read().decode('utf-8')