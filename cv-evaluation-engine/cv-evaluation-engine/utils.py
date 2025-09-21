#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime
from typing import List, Tuple, Dict

class TextProcessor:
    """Ortak metin işleme fonksiyonları"""
    
    @staticmethod
    def extract_experience_years(text: str) -> float:
        """Metinden deneyim yılını çıkarır"""
        text_lower = text.lower()
        
        # Direkt yıl belirtimi
        year_patterns = [
            r'(\d+)\s*yıl',
            r'(\d+)\s*year',
            r'(\d+)\s*ay',
            r'(\d+)\s*month'
        ]
        
        total_months = 0
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                value = int(match)
                if 'yıl' in pattern or 'year' in pattern:
                    total_months += value * 12
                elif 'ay' in pattern or 'month' in pattern:
                    total_months += value
        
        if total_months > 0:
            return total_months / 12
        
        # Tarih aralıklarından deneyim çıkarma
        return TextProcessor._extract_experience_from_dates(text_lower)
    
    @staticmethod
    def _extract_experience_from_dates(text: str) -> float:
        """Tarih aralıklarından deneyim çıkarır"""
        experience_periods = []
        current_year = datetime.now().year
        
        work_section_patterns = [
            r'work\s+experience.*?(?=education|skills|$)',
            r'employment.*?(?=education|skills|$)',
            r'professional\s+experience.*?(?=education|skills|$)',
            r'career.*?(?=education|skills|$)',
            r'iş\s+deneyimi.*?(?=eğitim|yetenek|$)',
            r'çalışma\s+geçmişi.*?(?=eğitim|yetenek|$)',
        ]
        
        work_text = text
        for pattern in work_section_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                work_text = match.group(0)
                break
        
        work_text = re.sub(r'education.*?(?=work|skills|$)', '', work_text, flags=re.IGNORECASE | re.DOTALL)
        
        date_patterns = [
            r'(\w+\s+\d{4})\s*-\s*(\w+\s+\d{4})',
            r'(\w+\s+\d{4})\s*-\s*(current|present|şimdi|şu\s*an)',
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*/\s*(\d{4})',
            r'(\d{4})\s*to\s*(\d{4})',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, work_text, re.IGNORECASE)
            for start_date, end_date in matches:
                try:
                    start_year = re.search(r'(\d{4})', start_date)
                    end_year = re.search(r'(\d{4})', end_date)
                    
                    if start_year and end_year:
                        years = int(end_year.group(1)) - int(start_year.group(1))
                        if 0 < years <= 50:  # Makul deneyim aralığı
                            experience_periods.append(years)
                    elif start_year and ('current' in end_date.lower() or 'present' in end_date.lower() or 'şimdi' in end_date.lower()):
                        years = current_year - int(start_year.group(1))
                        if 0 < years <= 50:
                            experience_periods.append(years)
                except (ValueError, AttributeError):
                    continue
        
        # Mevcut iş için özel pattern'lar
        current_job_patterns = [
            r'(\d{4})\s*-\s*şimdi',
            r'(\d{4})\s*-\s*şu\s*an',
            r'(\d{4})\s*-\s*present',
            r'(\d{4})\s*-\s*current',
        ]
        
        for pattern in current_job_patterns:
            matches = re.findall(pattern, work_text, re.IGNORECASE)
            for start_year in matches:
                try:
                    years = current_year - int(start_year)
                    if 0 < years <= 50:
                        experience_periods.append(years)
                except (ValueError, AttributeError):
                    continue
        
        return sum(experience_periods)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Metni temizler"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\/]', '', text)
        return text
    
    @staticmethod
    def extract_skills_from_text(text: str, skills_list: List[str]) -> List[str]:
        """Metinden yetenekleri çıkarır"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in skills_list:
            if skill in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))

class SingletonMeta(type):
    """Singleton pattern için metaclass"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ModelManager:
    """Model yönetimi için singleton sınıf"""
    __metaclass__ = SingletonMeta
    
    def __init__(self):
        self._scoring_engine = None
        self._salary_predictor = None
        self._cv_processor = None
    
    @property
    def scoring_engine(self):
        if self._scoring_engine is None:
            from scoring_engine import ScoringEngine
            self._scoring_engine = ScoringEngine()
        return self._scoring_engine
    
    @property
    def salary_predictor(self):
        if self._salary_predictor is None:
            from salary_predictor import SalaryPredictor
            self._salary_predictor = SalaryPredictor()
        return self._salary_predictor
    
    @property
    def cv_processor(self):
        if self._cv_processor is None:
            from cv_processor import CVProcessor
            self._cv_processor = CVProcessor()
        return self._cv_processor

class SecurityValidator:
    """Güvenlik doğrulama sınıfı"""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """Dosya uzantısını doğrular"""
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """Dosya boyutunu doğrular"""
        return file_size <= max_size
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Dosya adını güvenli hale getirir"""
        # Tehlikeli karakterleri kaldır
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            filename = filename.replace(char, '')
        
        # Uzunluk sınırı
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')
        
        return filename
