# CV Değerlendirme Motoru - Docker Kurulumu

Bu proje Docker kullanarak kolayca çalıştırılabilir.

## Gereksinimler

- Docker
- Docker Compose

## Kurulum ve Çalıştırma

### 1. Docker Compose ile Çalıştırma (Önerilen)

```bash
# Projeyi çalıştır
docker-compose up -d

# Logları görüntüle
docker-compose logs -f

# Durdur
docker-compose down
```

### 2. Docker ile Manuel Çalıştırma

```bash
# Image oluştur
docker build -t cv-evaluation-engine .

# Container çalıştır
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/salary_prediction_model.joblib:/app/salary_prediction_model.joblib \
  -v $(pwd)/salary_label_encoder.joblib:/app/salary_label_encoder.joblib \
  --name cv-evaluation \
  cv-evaluation-engine
```

## Erişim

Uygulama şu adreste çalışacak:
- http://localhost:5000

## Önemli Notlar

- Model dosyaları (`salary_prediction_model.joblib` ve `salary_label_encoder.joblib`) proje dizininde bulunmalıdır
- Uploads klasörü otomatik olarak oluşturulur
- Production ortamında Gunicorn kullanılır (4 worker)

## Geliştirme Modu

Geliştirme için Flask'ın debug modunu kullanmak isterseniz:

```bash
# Dockerfile'da CMD satırını değiştirin:
CMD ["python", "app.py"]
```

## Sorun Giderme

### Container çalışmıyor
```bash
# Logları kontrol edin
docker-compose logs cv-evaluation

# Container'ı yeniden başlatın
docker-compose restart
```

### Model dosyaları bulunamıyor
Model dosyalarının proje dizininde olduğundan emin olun:
- salary_prediction_model.joblib
- salary_label_encoder.joblib

