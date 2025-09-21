import re
from typing import Dict, List, Tuple
from utils import TextProcessor

class ScoringEngine:
    def __init__(self):
        self.skills_keywords = {
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'redis', 'cassandra', 'elasticsearch',
                'sqlite', 'mariadb', 'dynamodb', 'neo4j', 'influxdb'
            ],
            'data_science': [
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib',
                'seaborn', 'plotly', 'jupyter', 'anaconda', 'spark', 'hadoop', 'hive', 'pig',
                'spss', 'shiny', 'arcgis', 'adobe illustrator', 'illustrator'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
                'spring', 'express', 'laravel', 'symfony', 'asp.net', 'rails'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'microsoft azure',
                'kubernetes', 'docker', 'terraform', 'ansible'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'jira', 'confluence', 'slack',
                'tableau', 'power bi', 'excel', 'vba', 'linux', 'unix', 'windows',
                'unity3d', 'unity'
            ]
        }
        
        self.education_levels = {
            'doktora': 20,
            'phd': 20,
            'yüksek lisans': 15,
            'master': 15,
            'm.s.': 15,
            'm.a.': 15,
            'lisans': 10,
            'bachelor': 10,
            'b.s.': 10,
            'b.a.': 10,
            'ön lisans': 5,
            'associate': 5,
            'lise': 2,
            'high school': 2
        }
        
        self.relevant_fields = [
            'bilgisayar', 'computer', 'yazılım', 'software', 'veri', 'data', 'matematik', 'mathematics',
            'istatistik', 'statistics', 'mühendislik', 'engineering', 'bilişim', 'informatics',
            'sistem', 'system', 'teknoloji', 'technology', 'elektronik', 'electronics',
            'economics', 'ekonomi', 'business', 'işletme'
        ]
    
    def calculate_scores(self, text: str) -> Dict[str, int]:
        text_lower = text.lower()
        
        skills_score = self._calculate_skills_score(text_lower)
        experience_score = self._calculate_experience_score(text_lower)
        education_score = self._calculate_education_score(text_lower)
        
        return {
            'skills': skills_score,
            'experience': experience_score,
            'education': education_score
        }
    
    def _calculate_skills_score(self, text: str) -> int:
        total_skills = 0
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill in text:
                    total_skills += 1
        
        return min(total_skills, 50)
    
    def _calculate_experience_score(self, text: str) -> int:
        year_patterns = [
            r'(\d+)\s*yıl',
            r'(\d+)\s*year',
            r'(\d+)\s*ay',
            r'(\d+)\s*month',
            r'(\d+)\s*hafta',
            r'(\d+)\s*week'
        ]
        
        total_months = 0
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                value = int(match)
                if 'yıl' in pattern or 'year' in pattern:
                    total_months += value * 12
                elif 'ay' in pattern or 'month' in pattern:
                    total_months += value
                elif 'hafta' in pattern or 'week' in pattern:
                    total_months += value / 4
        
        if total_months > 0:
            total_years = total_months / 12
        else:
            experience_periods = []
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
                r'(\w+\s+\d{4})\s*-\s*(\w+\s+\d{4})',  # January 2015 - February 2018
                r'(\w+\s+\d{4})\s*-\s*(current|present|şimdi|şu\s*an)',  # January 2015 - current
                r'(\d{4})\s*-\s*(\d{4})',  # 2020-2023
                r'(\d{4})\s*/\s*(\d{4})',  # 2020/2023
                r'(\d{4})\s*to\s*(\d{4})', # 2020 to 2023
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, work_text, re.IGNORECASE)
                for start_date, end_date in matches:
                    try:
                        start_year = re.search(r'(\d{4})', start_date)
                        end_year = re.search(r'(\d{4})', end_date)
                        
                        if start_year and end_year:
                            years = int(end_year.group(1)) - int(start_year.group(1))
                            if years > 0 and years <= 10:
                                experience_periods.append(years)
                        elif start_year and ('current' in end_date.lower() or 'present' in end_date.lower() or 'şimdi' in end_date.lower()):
                            years = 2024 - int(start_year.group(1))
                            if years > 0 and years <= 10:
                                experience_periods.append(years)
                    except (ValueError, AttributeError):
                        continue
            
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
                        years = 2024 - int(start_year)
                        if years > 0 and years <= 10:
                            experience_periods.append(years)
                    except (ValueError, AttributeError):
                        continue
            
            total_years = sum(experience_periods)
        
        if total_years >= 10:
            return 30
        elif total_years >= 5:
            return 25
        elif total_years >= 3:
            return 20
        elif total_years >= 1:
            return 15
        elif total_years >= 0.5:
            return 10
        else:
            return 5
    
    def _calculate_education_score(self, text: str) -> int:
        max_score = 0
        field_relevance = 0
        
        for level, score in self.education_levels.items():
            if level in text:
                max_score = max(max_score, score)
        
        for field in self.relevant_fields:
            if field in text:
                field_relevance = 5
                break
        
        return min(max_score + field_relevance, 20)
    
    def get_skills_found(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))
    
    def get_experience_years(self, text: str) -> float:
        """Deneyim yılını hesaplar - utils.TextProcessor kullanır"""
        return round(TextProcessor.extract_experience_years(text), 1)
    
    def get_education_info(self, text: str) -> Dict[str, str]:
        text_lower = text.lower()
        
        education_info = {
            'level': 'Belirtilmemiş',
            'field': 'Belirtilmemiş',
            'relevance_score': 0
        }
        
        for level in self.education_levels.keys():
            if level in text_lower:
                education_info['level'] = level.title()
                break
        
        for field in self.relevant_fields:
            if field in text_lower:
                education_info['field'] = field.title()
                education_info['relevance_score'] = 5
                break
        
        return education_info