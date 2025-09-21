@echo off
echo CV Değerlendirme Motoru Başlatılıyor...
echo.

REM Sanal ortamı kontrol et
if not exist "venv" (
    echo Sanal ortam oluşturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktifleştir
echo Sanal ortam aktifleştiriliyor...
call venv\Scripts\activate.bat

REM Gerekli paketleri yükle
echo Gerekli paketler yükleniyor...
pip install -r requirements.txt

REM Uygulamayı başlat
echo.
echo Uygulama başlatılıyor...
echo Tarayıcınızda http://localhost:5000 adresine gidin
echo.
python app.py

pause
