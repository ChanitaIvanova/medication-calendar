import PyPDF2
from docx import Document
import os

class FileReaderService:
    @staticmethod
    def read_file(file, file_extension):
        """
        Read the content of a file based on its extension.

        :param file: The file to be read.
        :type file: FileStorage (werkzeug.datastructures.FileStorage)
        :param file_extension: The file extension (e.g., '.pdf', '.docx').
        :type file_extension: str
        :return: The content of the file as a string.
        :rtype: str
        :raises ValueError: If the file type is not supported or if file_extension is invalid.
        """
        # Validate file_extension input
        if not isinstance(file_extension, str) or not file_extension:
            raise ValueError("file_extension must be a non-empty string")
        
        # Mapping file extensions to their respective read methods
        read_methods = {
            '.pdf': FileReaderService._read_pdf,
            '.docx': FileReaderService._read_docx,
            '.txt': FileReaderService._read_text,
            '.md': FileReaderService._read_text
        }

        read_method = read_methods.get(file_extension.lower())
        if read_method:
            return read_method(file)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    @staticmethod
    def _read_pdf(file):
        """
        Extract text from a PDF file.

        :param file: The PDF file to be read.
        :type file: FileStorage (werkzeug.datastructures.FileStorage)
        :return: The extracted text from the PDF.
        :rtype: str
        :raises IOError: If the PDF file cannot be read properly.
        """
        try:
            reader = PyPDF2.PdfReader(file)
            return ' '.join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            raise IOError(f"An error occurred while reading the PDF file: {str(e)}")

    @staticmethod
    def _read_docx(file):
        """
        Extract text from a DOCX file.

        :param file: The DOCX file to be read.
        :type file: FileStorage (werkzeug.datastructures.FileStorage)
        :return: The extracted text from the DOCX file.
        :rtype: str
        :raises IOError: If the DOCX file cannot be read properly.
        """
        try:
            doc = Document(file)
            return ' '.join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            raise IOError(f"An error occurred while reading the DOCX file: {str(e)}")

    @staticmethod
    def _read_text(file):
        """
        Extract text from a plain text file.

        :param file: The text file to be read.
        :type file: FileStorage (werkzeug.datastructures.FileStorage)
        :return: The extracted text from the text file.
        :rtype: str
        :raises UnicodeDecodeError: If the file cannot be decoded using UTF-8.
        """
        try:
            return file.read().decode('utf-8')
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(f"An error occurred while decoding the text file: {str(e)}")
