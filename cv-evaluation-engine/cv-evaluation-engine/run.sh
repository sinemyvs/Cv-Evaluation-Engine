#!/bin/bash

echo "CV Değerlendirme Motoru Başlatılıyor..."
echo

# Sanal ortamı kontrol et
if [ ! -d "venv" ]; then
    echo "Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Gerekli paketleri yükle
echo "Gerekli paketler yükleniyor..."
pip install -r requirements.txt

# Uygulamayı başlat
echo
echo "Uygulama başlatılıyor..."
echo "Tarayıcınızda http://localhost:5000 adresine gidin"
echo
python app.py
