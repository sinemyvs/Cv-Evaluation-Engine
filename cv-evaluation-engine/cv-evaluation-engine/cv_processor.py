import PyPDF2
import os
import re
from typing import Dict, List
from utils import TextProcessor

class CVProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt', '.docx']
    
    def extract_text(self, file_path: str) -> str:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension == '.txt':
            return self._extract_from_txt(file_path)
        elif file_extension == '.docx':
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Desteklenmeyen dosya formatı: {file_extension}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return self._clean_text(text)
        except Exception as e:
            raise Exception(f"PDF dosyası okunamadı: {str(e)}")
    
    def _extract_from_txt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                return self._clean_text(text)
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                    return self._clean_text(text)
            except Exception as e:
                raise Exception(f"TXT dosyası okunamadı: {str(e)}")
        except Exception as e:
            raise Exception(f"TXT dosyası okunamadı: {str(e)}")
    
    def _extract_from_docx(self, file_path: str) -> str:
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self._clean_text(text)
        except Exception as e:
            raise Exception(f"DOCX dosyası okunamadı: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Metni temizler - utils.TextProcessor kullanır"""
        return TextProcessor.clean_text(text)
    
    def get_file_info(self, file_path: str) -> Dict:
        if not os.path.exists(file_path):
            return {"error": "Dosya bulunamadı"}
        
        file_stats = os.stat(file_path)
        
        return {
            "filename": os.path.basename(file_path),
            "file_size": file_stats.st_size,
            "file_extension": os.path.splitext(file_path)[1].lower(),
            "is_supported": os.path.splitext(file_path)[1].lower() in self.supported_formats
        }
