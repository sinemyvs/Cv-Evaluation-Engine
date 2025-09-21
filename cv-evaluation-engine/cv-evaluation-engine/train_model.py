#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

def extract_experience(exp):
    try:
        exp = str(exp).lower().strip()
        if '-' in exp:
            parts = exp.replace('yrs', '').replace('yr', '').split('-')
            return (int(parts[0]) + int(parts[1])) / 2
        elif '>' in exp:
            return int(exp.replace('>', '').replace('yrs', '').replace('yr', '').strip())
        elif '<' in exp:
            return int(exp.replace('<', '').replace('yrs', '').replace('yr', '').strip()) - 1
        else:
            return int(exp.replace('yrs', '').replace('yr', '').strip())
    except:
        return 0

def simplify_salary(s):
    if s in ['0to3', '3to6']:
        return 'low'
    elif s in ['6to10', '10to15']:
        return 'mid'
    elif s in ['15to25', '25to50']:
        return 'high'
    return 'unknown'

def train_salary_model():
    print("Model eğitimi başlatılıyor...")
    
    try:
        train_df = pd.read_csv("train.csv")
        print(f"Train data yüklendi: {train_df.shape}")
    except Exception as e:
        print(f"Train data yükleme hatası: {e}")
        return None, None
    
    columns_needed = ['experience', 'job_type', 'key_skills', 'location', 'job_desig', 'salary']
    train_df = train_df[columns_needed].dropna()
    print(f"Temizlenmiş data: {train_df.shape}")
    
    train_df['experience_num'] = train_df['experience'].apply(extract_experience)
    train_df['skill_count'] = train_df['key_skills'].apply(lambda x: len(str(x).split(',')))
    train_df['salary_group'] = train_df['salary'].apply(simplify_salary)
    
    print(f"Salary groups: {train_df['salary_group'].value_counts()}")
    
    salary_encoder = LabelEncoder()
    train_df['salary_encoded'] = salary_encoder.fit_transform(train_df['salary_group'])
    
    X = train_df[['experience_num', 'job_type', 'key_skills', 'location', 'job_desig', 'skill_count']]
    y = train_df['salary_encoded']
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('job_type', TfidfVectorizer(min_df=2, ngram_range=(1, 2)), 'job_type'),
            ('key_skills', TfidfVectorizer(max_features=300, min_df=2, ngram_range=(1, 2)), 'key_skills'),
            ('location', TfidfVectorizer(min_df=2), 'location'),
            ('job_desig', TfidfVectorizer(min_df=2), 'job_desig'),
            ('experience_num', StandardScaler(), ['experience_num']),
            ('skill_count', StandardScaler(), ['skill_count']),
        ]
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            class_weight='balanced',
            random_state=42
        ))
    ])
    
    print("Model eğitimi başlıyor...")
    pipeline.fit(X_train, y_train)
    print("Model eğitimi tamamlandı!")
    
    y_val_pred = pipeline.predict(X_val)
    print("\nValidation Sonuçları:")
    print(classification_report(y_val, y_val_pred, target_names=salary_encoder.classes_))
    
    joblib.dump(pipeline, 'salary_prediction_model.joblib')
    joblib.dump(salary_encoder, 'salary_label_encoder.joblib')
    print("\nModel ve LabelEncoder kaydedildi.")
    
    return pipeline, salary_encoder

if __name__ == "__main__":
    print("Script başlatılıyor...")
    train_salary_model()
    print("Script tamamlandı!")