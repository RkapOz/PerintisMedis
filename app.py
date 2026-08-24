import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="ER Triage AI", page_icon="🚑", layout="wide")

st.title("🚑 AI ER Triage Assistant")
st.markdown("Sistem pendukung keputusan IGD untuk memprediksi kategori triase dan disposisi pasien berdasarkan keluhan dan hasil lab sederhana.")

# Sidebar untuk API Key
with st.sidebar:
    st.header("Konfigurasi API")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
    st.markdown("[Dapatkan API Key Gratis di Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.info("Kategori Triase:\n- 🔴 Merah: Resusitasi / Gawat Darurat\n- 🟡 Kuning: Urgent\n- 🟢 Hijau: Rawat Jalan\n- ⚫ Hitam: DOA / Palliative")

# Form Input Data Pasien
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Klinis Pasien")
    usia = st.number_input("Usia (Tahun)", min_value=0, max_value=120, value=30)
    keluhan = st.text_area("Keluhan Utama & Riwayat Singkat", "Misal: Nyeri dada kiri menjalar ke lengan, keringat dingin, mual sejak 2 jam lalu.")
    kesadaran = st.selectbox("Tingkat Kesadaran (GCS)", ["Compos Mentis (Sadar Penuh)", "Apatis", "Somnolen", "Sopor", "Koma"])

with col2:
    st.subheader("Hasil Lab (Rapid Test)")
    gula_darah = st.number_input("Gula Darah Sewaktu (mg/dL)", min_value=0, value=110)
    hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, value=13.0, step=0.1)
    leukosit = st.number_input("Leukosit (/uL)", min_value=0, value=8000)
    trombosit = st.number_input("Trombosit (/uL)", min_value=0, value=250000)

if st.button("🚨 Analisis Triase Sekarang", use_container_width=True, type="primary"):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key di sidebar sebelah kiri!")
    else:
        with st.spinner("Menganalisis data pasien..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
                Kamu adalah Dokter Jaga IGD Senior. Analisis kasus berikut dan tentukan status triase (Merah, Kuning, Hijau, atau Hitam) dan disposisi ruangan (Rawat Jalan, Rawat Inap Biasa, HDU, atau ICU).
                
                Data Pasien:
                - Usia: {usia} tahun
                - Keluhan: {keluhan}
                - Kesadaran: {kesadaran}
                
                Hasil Lab:
                - Gula Darah Sewaktu: {gula_darah} mg/dL
                - Hemoglobin: {hb} g/dL
                - Leukosit: {leukosit} /uL
                - Trombosit: {trombosit} /uL
                
                Fokuskan kemungkinan diagnosa pada 20 penyakit IGD tersering. 
                Berikan jawaban dalam format persis seperti ini (tanpa markdown tebal):
                TRIASE: [Pilih warna]
                DIAGNOSA: [1-2 kemungkinan diagnosa]
                DISPOSISI: [Rawat Jalan / Rawat Inap / HDU / ICU]
                ALASAN: [Penjelasan medis singkat maksimal 3 kalimat]
                """
                
                response = model.generate_content(prompt)
                hasil = response.text
                
                # Menampilkan Hasil dengan Warna Streamlit
                st.divider()
                st.subheader("📋 Hasil Analisis AI")
                
                if "Merah" in hasil.upper():
                    st.error(hasil)
                elif "Kuning" in hasil.upper():
                    st.warning(hasil)
                elif "Hijau" in hasil.upper():
                    st.success(hasil)
                else:
                    st.info(hasil)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
