from flask import Flask, render_template, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from utils import ModelManager, SecurityValidator

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return SecurityValidator.validate_file_extension(filename, ALLOWED_EXTENSIONS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Dosya varlığını kontrol et
        if 'file' not in request.files:
            logger.warning("Dosya seçilmedi")
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("Boş dosya adı")
            return jsonify({'error': 'Dosya seçilmedi'}), 400
        
        # Güvenlik kontrolleri
        if not allowed_file(file.filename):
            logger.warning(f"Geçersiz dosya formatı: {file.filename}")
            return jsonify({'error': 'Geçersiz dosya formatı. Sadece PDF, TXT ve DOCX dosyaları desteklenir.'}), 400
        
        # Dosya boyutunu kontrol et
        file.seek(0, 2)  # Dosyanın sonuna git
        file_size = file.tell()
        file.seek(0)  # Başa dön
        
        if not SecurityValidator.validate_file_size(file_size, MAX_FILE_SIZE):
            logger.warning(f"Dosya çok büyük: {file_size} bytes")
            return jsonify({'error': f'Dosya çok büyük. Maksimum {MAX_FILE_SIZE // (1024*1024)}MB olmalıdır.'}), 400
        
        # Güvenli dosya adı oluştur
        filename = SecurityValidator.sanitize_filename(secure_filename(file.filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Dosyayı kaydet
        file.save(filepath)
        logger.info(f"Dosya kaydedildi: {filename}")
        
        try:
            # Model manager kullanarak singleton instance'ları al
            model_manager = ModelManager()
            
            # Metin çıkarma
            extracted_text = model_manager.cv_processor.extract_text(filepath)
            if not extracted_text.strip():
                raise ValueError("Dosyadan metin çıkarılamadı")
            
            # Puanlama
            scores = model_manager.scoring_engine.calculate_scores(extracted_text)
            
            # Maaş tahmini
            salary_prediction = model_manager.salary_predictor.predict_salary(extracted_text)
            
            result = {
                'filename': filename,
                'extracted_text': extracted_text,
                'scores': scores,
                'total_score': sum(scores.values()),
                'skills_found': model_manager.scoring_engine.get_skills_found(extracted_text),
                'experience_years': model_manager.scoring_engine.get_experience_years(extracted_text),
                'education_info': model_manager.scoring_engine.get_education_info(extracted_text),
                'salary_prediction': salary_prediction
            }
            
            logger.info(f"CV analizi tamamlandı: {filename}")
            return jsonify(result)
            
        except ValueError as ve:
            logger.error(f"Değer hatası: {str(ve)}")
            return jsonify({'error': f'Dosya işleme hatası: {str(ve)}'}), 400
        except Exception as e:
            logger.error(f"Beklenmeyen hata: {str(e)}")
            return jsonify({'error': f'Dosya işlenirken hata oluştu: {str(e)}'}), 500
        finally:
            # Geçici dosyayı temizle
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Geçici dosya silindi: {filename}")
    
    except Exception as e:
        logger.error(f"Upload endpoint hatası: {str(e)}")
        return jsonify({'error': 'Sunucu hatası'}), 500

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            logger.warning("API analyze: Metin verisi bulunamadı")
            return jsonify({'error': 'Metin verisi bulunamadı'}), 400
        
        text = data['text'].strip()
        if not text:
            logger.warning("API analyze: Boş metin")
            return jsonify({'error': 'Metin boş olamaz'}), 400
        
        if len(text) > 50000:  # 50KB metin sınırı
            logger.warning("API analyze: Metin çok uzun")
            return jsonify({'error': 'Metin çok uzun. Maksimum 50,000 karakter olmalıdır.'}), 400
        
        # Model manager kullanarak singleton instance'ları al
        model_manager = ModelManager()
        
        # Puanlama
        scores = model_manager.scoring_engine.calculate_scores(text)
        
        # Maaş tahmini
        salary_prediction = model_manager.salary_predictor.predict_salary(text)
        
        result = {
            'scores': scores,
            'total_score': sum(scores.values()),
            'skills_found': model_manager.scoring_engine.get_skills_found(text),
            'experience_years': model_manager.scoring_engine.get_experience_years(text),
            'education_info': model_manager.scoring_engine.get_education_info(text),
            'salary_prediction': salary_prediction
        }
        
        logger.info("API analyze tamamlandı")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API analyze hatası: {str(e)}")
        return jsonify({'error': f'Analiz sırasında hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
