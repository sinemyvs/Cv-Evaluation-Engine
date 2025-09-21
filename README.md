[README.md](https://github.com/user-attachments/files/22454864/README.md)
# CV Değerlendirme Motoru (CV Evaluation Engine)

Bu proje, PDF, TXT ve DOCX formatındaki CV dosyalarını analiz ederek otomatik puanlama yapan bir web uygulamasıdır.

## 🚀 Özellikler

- **Çoklu Format Desteği**: PDF, TXT ve DOCX dosyalarını destekler
- **Otomatik Metin Çıkarma**: CV dosyalarından metin çıkarır ve temizler
- **Akıllı Puanlama Sistemi**:
  - **Yetenekler (50 puan)**: Programlama dilleri, veritabanları, veri bilimi araçları
  - **Deneyim (30 puan)**: Toplam iş tecrübesi yılına göre
  - **Eğitim (20 puan)**: Mezuniyet derecesi ve alan uygunluğuna göre
- **Modern Web Arayüzü**: Bootstrap ile responsive tasarım
- **RESTful API**: Programatik erişim için API endpoint'leri

## 📋 Gereksinimler

- Python 3.7+
- Flask 2.3.3
- PyPDF2 3.0.1
- python-docx 0.8.11

## 🛠️ Kurulum

1. **Projeyi klonlayın:**
   ```bash
   git clone <repository-url>
   cd cv-evaluation-engine
   ```

2. **Sanal ortam oluşturun:**
   ```bash
   python -m venv venv
   ```

3. **Sanal ortamı aktifleştirin:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Gerekli paketleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Uygulamayı çalıştırın:**
   ```bash
   python app.py
   ```

6. **Tarayıcınızda açın:**
   ```
   http://localhost:5000
   ```

## 📁 Proje Yapısı

```
cv-evaluation-engine/
├── app.py                 # Ana Flask uygulaması
├── cv_processor.py        # CV metin çıkarma modülü
├── scoring_engine.py      # Puanlama motoru
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Proje dokümantasyonu
├── templates/
│   └── index.html        # Web arayüzü
├── uploads/              # Geçici dosya yükleme klasörü
└── test_files/           # Test dosyaları
```

## 🔧 Kullanım

### Web Arayüzü

1. Tarayıcınızda `http://localhost:5000` adresine gidin
2. CV dosyanızı sürükleyip bırakın veya "Dosya Seç" butonuna tıklayın
3. "Analiz Et" butonuna tıklayın
4. Sonuçları görüntüleyin

### API Kullanımı

#### Metin Analizi
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "CV metni buraya..."}'
```

#### Dosya Yükleme
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@cv_dosyasi.pdf"
```

## 📊 Puanlama Sistemi

### Yetenekler (0-50 puan)
- Programlama dilleri: Python, Java, JavaScript, C++, vb.
- Veritabanları: SQL, MySQL, PostgreSQL, MongoDB, vb.
- Veri bilimi araçları: Pandas, NumPy, TensorFlow, PyTorch, vb.
- Web teknolojileri: HTML, CSS, React, Angular, Django, vb.
- Bulut platformları: AWS, Azure, GCP, Docker, vb.
- Araçlar: Git, Jenkins, Tableau, Linux, vb.

### Deneyim (0-30 puan)
- 10+ yıl: 30 puan
- 5-9 yıl: 25 puan
- 3-4 yıl: 20 puan
- 1-2 yıl: 15 puan
- 6-12 ay: 10 puan
- 0-6 ay: 5 puan

### Eğitim (0-20 puan)
- Doktora/PhD: 20 puan
- Yüksek Lisans: 15 puan
- Lisans: 10 puan
- Ön Lisans: 5 puan
- Lise: 2 puan
- Alan uygunluğu: +5 puan

## 🧪 Test

Test dosyalarını kullanarak uygulamayı test edebilirsiniz:

```bash
python test_cv_engine.py
```

## 🔍 Desteklenen Dosya Formatları

- **PDF**: PyPDF2 kütüphanesi ile
- **TXT**: UTF-8 ve Latin-1 encoding desteği
- **DOCX**: python-docx kütüphanesi ile

## 🚨 Bilinen Sınırlamalar

- PDF dosyalarında görsel tablolar ve resimler işlenmez
- Karmaşık formatlar (çok sütunlu düzenler) için metin çıkarma kalitesi düşük olabilir
- OCR desteği yoktur (sadece metin tabanlı PDF'ler desteklenir)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açabilir veya iletişime geçebilirsiniz.

---

**Not**: Bu uygulama eğitim amaçlı geliştirilmiştir. Gerçek CV değerlendirmelerinde insan müdahalesi gereklidir.
