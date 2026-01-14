# 📄 PDF Master Tools

PDF Master Tools, Python ve Streamlit kullanılarak geliştirilmiş, modern ve kullanıcı dostu bir PDF düzenleme ve işleme aracıdır. Tüm işlemleri bellekte (RAM) gerçekleştirerek hızlı ve güvenli bir deneyim sunar.

![Ekran görüntüsü 2026-01-14 205513](https://github.com/user-attachments/assets/d3592f27-8e81-4c22-bbda-13ca3504ec2a)

## Canlı Link : https://pdfduzenlemearaci-eufobms5pyfbsbbcqwhdwk.streamlit.app/

## 🚀 Özellikler

Uygulama sol menüden erişilebilen 4 temel modülden oluşur:

### 1. 🔗 PDF Birleştir (Merge)
Birden fazla PDF dosyasını yükleyin ve tek bir tıklamayla birleştirilmiş tek bir PDF olarak indirin.

### 2. ✂️ Sayfa Ayıkla (Split & Visual Selection)
- **Görsel Önizleme:** Yüklediğiniz PDF'in her sayfasını görsel olarak görüntüleyin.
- **Çoklu Seçim:** İstediğiniz sayfaları görsel üzerinden seçin.
- **Esnek İndirme:** Seçtiğiniz sayfaları ister **tek bir PDF** olarak birleştirip, ister **ZIP arşivi** içinde ayrı ayrı dosyalar olarak indirin.

### 3. 📝 PDF -> Word Dönüştür (Convert)
- PDF dosyalarınızı düzenlenebilir Word (.docx) belgelerine dönüştürün.
- **Metin Akış Modu:** Tablo yapısı nedeniyle kayma yapan belgelerde (örn. CV'ler) "Metin Akış Modu"nu aktif ederek daha temiz bir çıktı alabilirsiniz.

### 4. ©️ Filigran Ekle (Watermark)
Belgelerinizin güvenliği için sayfaların üzerine "TASLAKTIR", "GİZLİDİR" gibi istediğiniz metni şeffaf filigran olarak ekleyin.

## 🛠️ Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
- Python 3.8 veya üzeri

### Adım 1: Repoyu Klonlayın
```bash
git clone https://github.com/ersin-41/Pdf_duzenleme_araci.git
cd Pdf_duzenleme_araci
```

### Adım 2: Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Uygulamayı Başlatın
```bash
streamlit run app.py
```
*Eğer `streamlit` komutu bulunamazsa:*
```bash
python -m streamlit run app.py
```

## 📦 Kullanılan Teknolojiler
- **[Streamlit](https://streamlit.io/):** Web arayüzü
- **[PyMuPDF (Fitz)](https://pymupdf.readthedocs.io/):** PDF görselleştirme ve işleme
- **[pypdf](https://pypdf.readthedocs.io/):** PDF birleştirme ve yazma
- **[pdf2docx](https://dothinking.github.io/pdf2docx/):** PDF'ten Word'e dönüşüm
- **[ReportLab](https://www.reportlab.com/):** Filigran oluşturma

## 🤝 Katkıda Bulunma
Katkılarınızı bekliyoruz! Bir sorun bulursanız issue açabilir veya pull request gönderebilirsiniz.

## 📄 Lisans
Bu proje açık kaynaklıdır.
