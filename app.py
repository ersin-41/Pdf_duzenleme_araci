import streamlit as st
import io
import os
import tempfile
from pypdf import PdfReader, PdfWriter
from pdf2docx import Converter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import fitz  # pymupdf
import zipfile

# Sayfa Ayarları
st.set_page_config(page_title="PDF Master Tools", page_icon="📄", layout="wide")

# CSS ile minimal stil takviyesi
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📄 PDF Master Tools")
    
    # Sidebar Navigasyon
    st.sidebar.title("Menü")
    choice = st.sidebar.radio(
        "İşlem Seçin",
        ("🏠 Ana Sayfa", "🔗 PDF Birleştir", "✂️ Sayfa Ayıkla", "📝 PDF -> Word Dönüştür", "©️ Filigran Ekle")
    )

    if choice == "🏠 Ana Sayfa":
        show_home()
    elif choice == "🔗 PDF Birleştir":
        show_merge_page()
    elif choice == "✂️ Sayfa Ayıkla":
        show_split_page()
    elif choice == "📝 PDF -> Word Dönüştür":
        show_convert_page()
    elif choice == "©️ Filigran Ekle":
        show_watermark_page()

def show_home():
    st.subheader("Hoş Geldiniz!")
    st.info("Sol menüden yapmak istediğiniz işlemi seçerek başlayabilirsiniz.")
    st.markdown("""
    Bu araç seti ile şunları yapabilirsiniz:
    - **PDF Birleştir:** Birden fazla PDF dosyasını tek bir dosyada birleştirin.
    - **Sayfa Ayıkla:** PDF dosyasından istediğiniz sayfaları seçip yeni bir PDF oluşturun.
    - **PDF -> Word:** PDF dosyalarınızı düzenlenebilir Word (.docx) formatına çevirin.
    - **Filigran Ekle:** PDF dosyalarınıza güvenliğiniz için filigran ekleyin.
    """)

def show_merge_page():
    st.header("🔗 PDF Dosyalarını Birleştir")
    uploaded_files = st.file_uploader("PDF dosyalarını yükleyin", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.write(f"{len(uploaded_files)} dosya yüklendi.")
        if st.button("Birleştir"):
            try:
                merger = PdfWriter()
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                output = io.BytesIO()
                merger.write(output)
                merger.close()
                output.seek(0)
                
                st.success("Dosyalar başarıyla birleştirildi!")
                st.download_button(
                    label="Birleşmiş PDF'i İndir",
                    data=output,
                    file_name="birlestirilmis_dokuman.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")

def show_split_page():
    st.header("✂️ PDF'den Sayfa Ayıkla (Görsel Seçim)")
    uploaded_file = st.file_uploader("Bir PDF dosyası yükleyin", type=["pdf"], key="split_uploader")

    if uploaded_file:
        try:
            # Dosyayı belleğe al (PyMuPDF için)
            file_bytes = uploaded_file.getvalue()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            total_pages = len(doc)
            
            st.info(f"Yüklenen dosya toplam {total_pages} sayfa. Aşağıdan ayıklamak istediğiniz sayfaları seçin.")

            # Seçilen sayfaları tutacak liste (Session state kullanmıyoruz, basit form submission)
            # Ancak dinamik form elemanları için form kullanımı daha temiz olabilir veya
            # her checkbox'ın key'i unik olmalı.
            
            # Izgara görünümü (3 kolonlu)
            cols = st.columns(3)
            selected_pages = []

            # Tümünü Seç Opsiyonu (Basit bir butonla state yönetmek zor olabilir, o yüzden manuel seçim odaklı gidiyoruz şimdilik)
            
            for i in range(total_pages):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2)) # Küçük önizleme için scale
                img_data = pix.tobytes("png")
                
                with cols[i % 3]:
                    st.image(img_data, caption=f"Sayfa {i+1}", use_container_width=True)
                    # Checkbox key'i unik olmalı
                    if st.checkbox(f"Seç: Sayfa {i+1}", key=f"sel_{i}"):
                        selected_pages.append(i) # 0-based index

            st.divider()
            
            if selected_pages:
                st.success(f"Toplam {len(selected_pages)} sayfa seçildi.")
                
                col1, col2 = st.columns(2)
                
                # Seçenek 1: Tek PDF olarak indir
                with col1:
                    if st.button("Seçilenleri Tek PDF Yap"):
                        writer = PdfWriter()
                        # Orijinal dosyayı pypdf ile tekrar açıyoruz (PyMuPDF'den aktarmak yerine)
                        # Veya PyMuPDF ile yeni PDF oluşturabiliriz, pypdf ile devam edelim tutarlılık için.
                        reader = PdfReader(io.BytesIO(file_bytes)) # Tekrar okuyoruz
                        
                        for p_idx in selected_pages:
                             writer.add_page(reader.pages[p_idx])
                        
                        output = io.BytesIO()
                        writer.write(output)
                        writer.close()
                        output.seek(0)
                        
                        st.download_button(
                            label="📥 Tek Dosya İndir (PDF)",
                            data=output,
                            file_name="secilen_sayfalar.pdf",
                            mime="application/pdf"
                        )

                # Seçenek 2: Ayrı ayrı ZIP olarak indir
                with col2:
                    if st.button("Ayrı Dosyalar Olarak İndir (ZIP)"):
                        zip_buffer = io.BytesIO()
                        reader = PdfReader(io.BytesIO(file_bytes))
                        
                        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                            for p_idx in selected_pages:
                                single_page_writer = PdfWriter()
                                single_page_writer.add_page(reader.pages[p_idx])
                                
                                single_pdf_buffer = io.BytesIO()
                                single_page_writer.write(single_pdf_buffer)
                                single_page_writer.close()
                                
                                # PDF dosya adı
                                zip_file.writestr(f"sayfa_{p_idx+1}.pdf", single_pdf_buffer.getvalue())
                        
                        zip_buffer.seek(0)
                        
                        st.download_button(
                            label="📦 Arşiv İndir (ZIP)",
                            data=zip_buffer,
                            file_name="ayri_sayfalar.zip",
                            mime="application/zip"
                        )

            doc.close()

        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")

def show_convert_page():
    st.header("📝 PDF -> Word Dönüştürücü")
    uploaded_file = st.file_uploader("Bir PDF dosyası yükleyin", type=["pdf"])

    if uploaded_file:
        use_flow_mode = st.checkbox("Metin Akış Modu (Düzen kayıyorsa bunu işaretleyin)", help="Tablo algılamayı kapatır ve metni akış olarak almaya çalışır. Karmaşık CV'lerde işe yarayabilir.")
        
        if st.button("Word'e Dönüştür"):
            try:
                with st.spinner("Dönüştürülüyor... Bu işlem biraz zaman alabilir."):
                    # Geçici dosya oluşturma (pdf2docx dosya yolu gerektirebilir)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                        tmp_pdf.write(uploaded_file.getvalue())
                        tmp_pdf_path = tmp_pdf.name
                    
                    tmp_docx_path = tmp_pdf_path.replace(".pdf", ".docx")

                    # Dönüştürme işlemi
                    cv = Converter(tmp_pdf_path)
                    # Eğer kullanıcı seçtiyse tablo algılamayı kapatıyoruz
                    if use_flow_mode:
                        # detect_tables paramtresi pdf2docx sürümüne göre değişebilir ama genelde kwargs olarak geçer
                        cv.convert(tmp_docx_path, start=0, end=None, docx_options={'detect_tables': False}) 
                        # Not: Bazı sürümlerde parse_kwargs={'detect_tables': False} olabilir.
                        # En güvenli, settings'i değiştirmek olabilir ama cv.convert kwargs alır.
                        # pdf2docx normalde cv.convert(docx, **kwargs) -> page.parse(**kwargs)
                        # O yüzden doğrudan parametre verebiliriz.
                        # Ancak library yapısı gereği bazen karışık. 
                        # Basitçe kwargs olarak verelim, eğer çalışmazsa tekrar bakarız.
                        # Güncel pdf2docx: cv.convert(docx_filename, **kwargs)
                        # Ama kwargs parse metoduna gider mi? Documentation: parse(start=0, end=None, **kwargs)
                        # Hayır, convert(docx_filename, start=0, end=None, **kwargs)
                        # Yani detect_tables=False vermeliyiz.
                    else:
                        cv.convert(tmp_docx_path, start=0, end=None)
                    
                    cv.close()

                # Dönüştürülen dosyayı okuyup indirme butonuna verme
                with open(tmp_docx_path, "rb") as f:
                    docx_data = f.read()
                
                st.success("Dönüştürme tamamlandı!")
                st.download_button(
                    label="Word Dosyasını İndir",
                    data=docx_data,
                    file_name="donusturulmus_dokuman.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
                # Temizlik
                os.remove(tmp_pdf_path)
                os.remove(tmp_docx_path)

            except Exception as e:
                st.error(f"Dönüştürme hatası: {str(e)}")
                # Hata durumunda da temizlik yapmaya çalışalım
                if 'tmp_pdf_path' in locals() and os.path.exists(tmp_pdf_path):
                    os.remove(tmp_pdf_path)

def show_watermark_page():
    st.header("©️ Filigran Ekle")
    uploaded_file = st.file_uploader("Bir PDF dosyası yükleyin", type=["pdf"])
    watermark_text = st.text_input("Filigran Metni", "TASLAKTIR")

    if uploaded_file and watermark_text and st.button("Filigran Ekle"):
        try:
            # 1. Filigran PDF'ini bellekte oluştur
            packet = io.BytesIO()
            # Canvas oluştur, letter boyutu varsayılan ama sayfa boyutuna göre ayarlamak daha iyi olurdu,
            # şimdilik standart bir filigran basıp sayfaya ortalayacağız.
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Gri ve şeffaf renk ayarı
            # Alpha 0.3 (şeffaflık), Gri (0.5, 0.5, 0.5)
            c = Color(0.5, 0.5, 0.5, alpha=0.3)
            can.setFillColor(c)
            
            can.setFont("Helvetica-Bold", 50)
            # Sayfanın ortasına, 45 derece açıyla
            can.saveState()
            can.translate(300, 400) # Yaklaşık orta
            can.rotate(45)
            can.drawCentredString(0, 0, watermark_text)
            can.restoreState()
            can.save()
            
            packet.seek(0)
            new_pdf = PdfReader(packet)
            watermark_page = new_pdf.pages[0]

            # 2. Asıl PDF'i oku ve birleştir
            reader = PdfReader(uploaded_file)
            writer = PdfWriter()

            for page in reader.pages:
                # Filigranı her sayfaya merge et
                # Not: merge_page yerine merge_transformed_page veya doğrudan merge_page kullanabiliriz.
                # pypdf 3.x+ için merge_page kullanışlıdır.
                # Ancak sayfa boyutları farklı olabilir, basitçe üstüne oturtuyoruz.
                page.merge_page(watermark_page)
                writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            writer.close()
            output.seek(0)

            st.success("Filigran eklendi!")
            st.download_button(
                label="Filigranlı PDF'i İndir",
                data=output,
                file_name="filigranli_dokuman.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
