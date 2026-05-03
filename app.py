import streamlit as st
import os
import tempfile
from PIL import Image

# MoviePy kütüphanesini güvenli bir şekilde içeri aktarma
try:
    from moviepy.editor import ImageClip, concatenate_videoclips
except ImportError:
    # Eğer kütüphane yüklü değilse yüklemeye çalışır
    os.system("pip install moviepy")
    from moviepy.editor import ImageClip, concatenate_videoclips

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="EmlakAI Video Maker", page_icon="🎬")

st.title("🎬 EmlakAI: Otomatik Reels Oluşturucu")
st.markdown("""
1. Evin fotoğraflarını yükleyin.
2. 'Video Oluştur' butonuna basın.
3. Videoyu indirip Instagram'da paylaşırken üzerine metin ve müzik ekleyin!
""")

# --- DOSYA YÜKLEME ---
uploaded_files = st.file_uploader("Fotoğrafları Seçin (Önerilen: En az 3 adet)", 
                                  type=['jpg', 'jpeg', 'png'], 
                                  accept_multiple_files=True)

if st.button("🚀 Videoyu Hazırla"):
    if uploaded_files:
        with st.spinner('Fotoğraflar işleniyor ve video oluşturuluyor...'):
            clips = []
            temp_files = [] # Geçici dosyaları temizlemek için tutuyoruz
            
            try:
                for uploaded_file in uploaded_files:
                    # Fotoğrafı aç ve Reels boyutuna (1080x1920) uyarla
                    img = Image.open(uploaded_file).convert("RGB")
                    
                    # En boy oranını koruyarak boyutlandırma
                    img.thumbnail((1080, 1920), Image.Resampling.LANCZOS)
                    
                    # Arka planı siyah olan 1080x1920 bir tuval oluştur (Dikey video için)
                    canvas = Image.new('RGB', (1080, 1920), (0, 0, 0))
                    # Fotoğrafı merkeze yerleştir
                    offset = ((1080 - img.width) // 2, (1920 - img.height) // 2)
                    canvas.paste(img, offset)
                    
                    # Geçici bir yere kaydet
                    t_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    canvas.save(t_file.name)
                    temp_files.append(t_file.name)
                    
                    # Her fotoğraf 2.5 saniye görünsün
                    clip = ImageClip(t_file.name).set_duration(2.5)
                    clips.append(clip)
                
                # Fotoğrafları birleştir
                final_clip = concatenate_videoclips(clips, method="compose")
                
                # Geçici video dosyası oluştur
                t_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                
                # Videoyu yazdır (Basit ve hızlı ayarlar)
                final_clip.write_videofile(t_video.name, fps=24, codec='libx264', audio=False)
                
                # Videoyu ekranda göster
                st.video(t_video.name)
                
                # İndirme butonu
                with open(t_video.name, "rb") as file:
                    st.download_button(
                        label="📥 Videoyu Telefona/Bilgisayara İndir",
                        data=file,
                        file_name="emlak_ilan_reels.mp4",
                        mime="video/mp4"
                    )
                
                st.success("✅ Video başarıyla oluşturuldu!")

                # Temizlik: Geçici görselleri sil
                for f in temp_files:
                    if os.path.exists(f):
                        os.remove(f)

            except Exception as e:
                st.error(f"Hata oluştu: {e}")
    else:
        st.warning("Lütfen önce en az bir adet fotoğraf yükleyin.")

st.divider()
st.caption("EmlakAI v1.0 - Sermayesiz Girişimcilik Projesi")
