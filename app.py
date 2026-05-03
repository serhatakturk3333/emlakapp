import streamlit as st

# Uygulama Başlığı
st.title("🏠 Emlak İlan Asistanı")
st.subheader("Notlarınızı profesyonel ilanlara dönüştürün.")

# Giriş Alanı
notlar = st.text_area("Ev özelliklerini buraya yazın:", 
                      placeholder="Örn: 3+1, deniz manzaralı, geniş balkon, Beşiktaş...",
                      height=100)

# Dönüştürme Butonu
if st.button("İlanları Oluştur"):
    if notlar:
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📱 Instagram Reels Senaryosu")
            st.write(f"**Giriş:** Heyecan verici bir ev turuna hazır mısınız? ✨")
            st.write(f"**Metin:** Bugün Beşiktaş'ın kalbinde, {notlar} özelliklerine sahip bu eşsiz evi inceliyoruz.")
            st.write(f"**Kapanış:** Detaylar ve randevu için DM! 📩")
            
        with col2:
            st.success("📝 Profesyonel İlan Metni")
            st.write(f"**Başlık:** Hayallerinizdeki Konfor Burada! 🌟")
            st.write(f"**Açıklama:** Beşiktaş bölgesinde yer alan dairemiz; {notlar} ile hem oturum hem yatırım için kaçırılmayacak bir fırsat sunuyor.")
            st.write(f"**İletişim:** Hemen arayın, bu fırsatı kaçırmayın!")
    else:
        st.warning("Lütfen önce ev özelliklerini girin.")
