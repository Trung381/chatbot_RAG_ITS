'''
pip uninstall -y torch torchvision torchaudio fastai
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0
pip install marker-pdf surya-ocr
'''

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import re
import pathlib

class MdConverter:
    def __init__(self, pdf_converter: PdfConverter = None):
        self.pdf_converter = pdf_converter or PdfConverter(
            artifact_dict=create_model_dict()
        )

    def pdf2md(self, file_path):
        rendered = self.pdf_converter(file_path)
        text, _, images = text_from_rendered(rendered)
        textFormatted = re.sub(r"<(.*?)>", r"[\1]", text)
        pathlib.Path("output.md").write_bytes(textFormatted.encode())
        return True
