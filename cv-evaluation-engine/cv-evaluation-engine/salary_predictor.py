import joblib
import pandas as pd
import re
from typing import Dict, List, Tuple
from utils import TextProcessor

class SalaryPredictor:
    def __init__(self):
        try:
            self.model = joblib.load('salary_prediction_model.joblib')
            self.encoder = joblib.load('salary_label_encoder.joblib')
            self.model_loaded = True
        except FileNotFoundError:
            print("⚠️ Maaş tahmin modeli bulunamadı. Model dosyalarını kontrol edin.")
            self.model_loaded = False
        
        self.label_to_range = {
            'low': '$40.000 - $60.000',
            'mid': '$60.000 - $100.000', 
            'high': '$100.000 - $200.000'
        }
        
        self.job_type_mapping = {
            'data science': 'Analytics',
            'data scientist': 'Analytics',
            'data analyst': 'Analytics',
            'data visualization': 'Analytics',
            'machine learning': 'Analytics',
            'analytics': 'Analytics',
            'software': 'Software Development',
            'software engineer': 'Software Development',
            'developer': 'Software Development',
            'programmer': 'Software Development',
            'web developer': 'Software Development',
            'mobile developer': 'Software Development',
            'backend': 'Software Development',
            'frontend': 'Software Development',
            'full stack': 'Software Development',
            'devops': 'DevOps',
            'cloud': 'DevOps',
            'infrastructure': 'DevOps',
            'system administrator': 'DevOps',
            'product': 'Product Management',
            'product manager': 'Product Management',
            'project manager': 'Product Management',
            'manager': 'Management',
            'lead': 'Management',
            'senior': 'Management',
            'director': 'Management',
            'cto': 'Management',
            'ceo': 'Management'
        }
        
        self.location_mapping = {
            'istanbul': 'Istanbul',
            'ankara': 'Ankara', 
            'izmir': 'Izmir',
            'bursa': 'Bursa',
            'antalya': 'Antalya',
            'adana': 'Adana',
            'konya': 'Konya',
            'gaziantep': 'Gaziantep',
            'mersin': 'Mersin',
            'diyarbakir': 'Diyarbakir',
            'kayseri': 'Kayseri',
            'eskisehir': 'Eskisehir',
            'urfa': 'Urfa',
            'malatya': 'Malatya',
            'erzurum': 'Erzurum',
            'van': 'Van',
            'batman': 'Batman',
            'elazig': 'Elazig',
            'izmit': 'Izmit',
            'manisa': 'Manisa',
            'sivas': 'Sivas',
            'gebze': 'Gebze',
            'balikesir': 'Balikesir',
            'kahramanmaras': 'Kahramanmaras',
            'denizli': 'Denizli',
            'sakarya': 'Sakarya',
            'trabzon': 'Trabzon',
            'ordu': 'Ordu',
            'afyon': 'Afyon',
            'mugla': 'Mugla',
            'san francisco': 'San Francisco',
            'san francisco, ca': 'San Francisco',
            'san francisco ca': 'San Francisco',
            'new york': 'New York',
            'new york, ny': 'New York',
            'new york ny': 'New York',
            'london': 'London',
            'london, uk': 'London',
            'london uk': 'London',
            'berlin': 'Berlin',
            'berlin, germany': 'Berlin',
            'berlin germany': 'Berlin',
            'paris': 'Paris',
            'paris, france': 'Paris',
            'paris france': 'Paris',
            'amsterdam': 'Amsterdam',
            'amsterdam, netherlands': 'Amsterdam',
            'amsterdam netherlands': 'Amsterdam',
            'zurich': 'Zurich',
            'zurich, switzerland': 'Zurich',
            'zurich switzerland': 'Zurich',
            'toronto': 'Toronto',
            'toronto, canada': 'Toronto',
            'toronto canada': 'Toronto',
            'sydney': 'Sydney',
            'sydney, australia': 'Sydney',
            'sydney australia': 'Sydney',
            'tokyo': 'Tokyo',
            'tokyo, japan': 'Tokyo',
            'tokyo japan': 'Tokyo',
            'singapore': 'Singapore',
            'singapore, singapore': 'Singapore',
            'singapore singapore': 'Singapore',
            'dubai': 'Dubai',
            'dubai, uae': 'Dubai',
            'dubai uae': 'Dubai'
        }
    
    def extract_experience(self, text: str) -> float:
        """Deneyim yılını çıkarır - utils.TextProcessor kullanır"""
        return TextProcessor.extract_experience_years(text)
    
    def extract_job_type(self, text: str) -> str:
        text_lower = text.lower()
        
        for keyword, job_type in self.job_type_mapping.items():
            if keyword in text_lower:
                return job_type
        
        return 'Software Development'
    
    def extract_location(self, text: str) -> str:
        text_lower = text.lower()
        
        sorted_mappings = sorted(self.location_mapping.items(), key=lambda x: len(x[0]), reverse=True)
        
        for keyword, location in sorted_mappings:
            if keyword in text_lower:
                return location
        
        return 'Istanbul'
    
    def extract_job_designation(self, text: str) -> str:
        text_lower = text.lower()
        
        title_patterns = [
            r'(data\s+scientist|data\s+analyst|data\s+engineer|data\s+visualization\s+specialist)',
            r'(software\s+engineer|developer|programmer|web\s+developer|mobile\s+developer)',
            r'(senior\s+\w+|\w+\s+manager|lead\s+\w+|principal\s+\w+)',
            r'(cto|ceo|director|head\s+of)',
            r'(product\s+manager|project\s+manager|technical\s+lead)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).title()
        
        return 'Software Engineer'
    
    def extract_skills(self, text: str) -> str:
        """Yetenekleri çıkarır - utils.TextProcessor kullanır"""
        skills_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'redis', 'cassandra', 'elasticsearch',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib',
            'seaborn', 'plotly', 'jupyter', 'anaconda', 'spark', 'hadoop', 'hive', 'pig',
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
            'spring', 'express', 'laravel', 'symfony', 'asp.net', 'rails',
            'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'microsoft azure',
            'kubernetes', 'docker', 'terraform', 'ansible',
            'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'jira', 'confluence', 'slack',
            'tableau', 'power bi', 'excel', 'vba', 'linux', 'unix', 'windows',
            'unity3d', 'unity', 'spss', 'shiny', 'arcgis', 'adobe illustrator', 'illustrator'
        ]
        
        found_skills = TextProcessor.extract_skills_from_text(text, skills_keywords)
        return ', '.join(found_skills[:10])
    
    def predict_salary(self, cv_text: str) -> Dict[str, str]:
        if not self.model_loaded:
            return {
                'salary_group': 'unknown',
                'salary_range': 'Model yüklenemedi',
                'confidence': 0.0
            }
        
        try:
            experience = self.extract_experience(cv_text)
            job_type = self.extract_job_type(cv_text)
            skills = self.extract_skills(cv_text)
            location = self.extract_location(cv_text)
            job_designation = self.extract_job_designation(cv_text)
            skill_count = len(skills.split(', ')) if skills else 0
            sample_data = pd.DataFrame([{
                'experience_num': experience,
                'job_type': job_type,
                'key_skills': skills,
                'location': location,
                'job_desig': job_designation,
                'skill_count': skill_count
            }])
            
            predicted_class = self.model.predict(sample_data)[0]
            predicted_salary_group = self.encoder.inverse_transform([predicted_class])[0]
            
            salary_range = self.label_to_range.get(predicted_salary_group, 'Bilinmeyen Aralık')
            
            confidence = min(0.95, max(0.4, experience / 8 + skill_count / 15))
            
            return {
                'salary_group': predicted_salary_group,
                'salary_range': salary_range,
                'confidence': round(confidence, 2),
                'experience_years': round(experience, 1),
                'job_type': job_type,
                'location': location,
                'skill_count': skill_count
            }
            
        except Exception as e:
            return {
                'salary_group': 'error',
                'salary_range': f'Hata: {str(e)}',
                'confidence': 0.0
            }
