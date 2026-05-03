import streamlit as st
import os

# MoviePy kütüphanesini daha güvenli çağırmak için
try:
    from moviepy.editor import ImageClip, concatenate_videoclips
except ImportError:
    os.system("pip install moviepy")
    from moviepy.editor import ImageClip, concatenate_videoclips

from PIL import Image
# ... kodun geri kalanı aynı kalabilir

st.set_page_config(page_title="EmlakAI Video Pro", page_icon="🎬")

st.title("🎬 EmlakAI: Otomatik Reels Oluşturucu")
st.markdown("Fotoğrafları yükleyin, profesyonel videonuzu anında indirin.")

# --- GİRİŞ ALANLARI ---
uploaded_files = st.file_uploader("Evin fotoğraflarını seçin (En az 3 adet)", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
ilan_baslik = st.text_input("Video üzerine yazılacak başlık:", "HAYALLERİNİZDEKİ EV!")

if st.button("Reels Videosu Oluştur"):
    if uploaded_files and len(uploaded_files) >= 1:
        with st.spinner('Video hazırlanıyor, bu işlem 1 dakika sürebilir...'):
            clips = []
            try:
                for uploaded_file in uploaded_files:
                    # Fotoğrafı aç ve boyutlandır (Reels boyutu: 1080x1920)
                    img = Image.open(uploaded_file).convert("RGB")
                    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
                    
                    # Geçici bir dosyaya kaydet
                    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    img.save(temp_img.name)
                    
                    # Video klibi oluştur (her fotoğraf 2 saniye)
                    clip = ImageClip(temp_img.name).set_duration(2)
                    clips.append(clip)
                
                # Klipleri birleştir
                final_clip = concatenate_videoclips(clips, method="compose")
                
                # Videoyu kaydet
                temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                final_clip.write_videofile(temp_video.name, fps=24, codec='libx264')
                
                # Videoyu göster ve indir
                st.video(temp_video.name)
                
                with open(temp_video.name, "rb") as file:
                    st.download_button(
                        label="Videoyu İndir 📥",
                        data=file,
                        file_name="emlak_reels.mp4",
                        mime="video/mp4"
                    )
                
                # Temizlik
                st.success("Videonuz hazır! Şimdi indirip paylaşabilirsiniz.")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen en az bir fotoğraf yükleyin.")
