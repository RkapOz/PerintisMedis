import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="ER Triage AI", page_icon="🚑", layout="wide")

st.title("🚑 AI ER Triage Assistant (Advanced EMR)")
st.markdown("Sistem pendukung keputusan IGD dengan analisis komprehensif meliputi parameter anamnesis, sosiodemografi, dan serologi medis.")

st.warning("⚠️ **DISCLAIMER MEDIS:** Aplikasi ini adalah purwarupa (prototype) Sistem Pendukung Keputusan berbasis AI. Hasil analisis **TIDAK** menggantikan diagnosis medis profesional.")

# Sidebar untuk Konfigurasi API
with st.sidebar:
    st.header("Konfigurasi API")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
    st.markdown("[Dapatkan API Key Gratis di Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()
    
# Logika Auto-Detect Model
selected_model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if available_models:
            model_options = [name.replace("models/", "") for name in available_models]
            st.sidebar.success("API Key Valid!")
            
            default_index = 0
            if "gemini-3.6-flash" in model_options:
                default_index = model_options.index("gemini-3.6-flash")
            elif "gemini-pro" in model_options:
                default_index = model_options.index("gemini-pro")
                
            selected_model = st.sidebar.selectbox("Pilih Model AI (Auto-detect):", options=model_options, index=default_index)
        else:
            st.sidebar.error("API Key valid, tapi tidak ada model text-generation yang tersedia.")
    except Exception as e:
        st.sidebar.error(f"Gagal memverifikasi API Key: {e}")

st.sidebar.info("Kategori Triase:\n- 🔴 Merah: Resusitasi / Gawat Darurat\n- 🟡 Kuning: Urgent\n- 🟢 Hijau: Rawat Jalan\n- ⚫ Hitam: DOA / Palliative")

# --- UI FORM REKAM MEDIS DENGAN TABS ---
st.header("📋 Form Triage & Rekam Medis Terpadu")

tab1, tab2, tab3 = st.tabs(["👤 Profil & Sosiodemografi", "🩺 Anamnesis Klinis", "🔬 Pemeriksaan Fisik & Lab"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        usia = st.number_input("Usia (Tahun)", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        gol_darah = st.selectbox("Golongan Darah & Rhesus", ["Belum Diketahui", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        etnis = st.text_input("Etnis / Ras (Opsional)", placeholder="Misal: Asia Tenggara")
    with col_b:
        pendidikan = st.selectbox("Pendidikan Terakhir", ["Tidak Sekolah", "SD", "SMP", "SMA", "Diploma", "Sarjana", "Pascasarjana"])
        pekerjaan = st.text_input("Pekerjaan", placeholder="Misal: Pegawai Swasta, Petani, IRT...")
        status_nikah = st.selectbox("Status Pernikahan", ["Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"])
        
        c_bb, c_tb = st.columns(2)
        with c_bb:
            bb = st.number_input("Berat Badan (kg)", min_value=0.0, value=65.0)
        with c_tb:
            tb = st.number_input("Tinggi Badan (cm)", min_value=0.0, value=165.0)

with tab2:
    col_c, col_d = st.columns(2)
    with col_c:
        keluhan = st.text_area("Keluhan Utama & Riwayat Singkat", "Nyeri dada kiri menjalar ke lengan, keringat dingin, mual sejak 2 jam lalu.")
        riwayat_penyakit = st.text_area("Riwayat Penyakit Dahulu (Komorbid)", placeholder="Misal: Hipertensi, DM Tipe 2, Asma...")
        riwayat_obat = st.text_area("Riwayat Penggunaan Obat", placeholder="Misal: Amlodipine 5mg, Metformin...")
    with col_d:
        alergi = st.text_input("Alergi (Obat/Makanan)", placeholder="Misal: Alergi Amoxicillin, Seafood...")
        riwayat_perjalanan = st.text_area("Riwayat Perjalanan (14 Hari Terakhir)", placeholder="Misal: Baru pulang dari daerah endemis malaria, umroh...")
        kebiasaan_makan = st.text_area("Gaya Hidup & Diet", placeholder="Misal: Merokok 1 bungkus/hari, diet tinggi natrium, alkohol...")

with tab3:
    col_e, col_f, col_g = st.columns(3)
    with col_e:
        st.markdown("**Klinis Dasar**")
        kesadaran = st.selectbox("Tingkat Kesadaran (GCS)", ["Compos Mentis (Sadar Penuh)", "Apatis", "Somnolen", "Sopor", "Koma"])
        gula_darah = st.number_input("Gula Darah Sewaktu (mg/dL)", min_value=0, value=110)
    
    with col_f:
        st.markdown("**Darah Lengkap (CBC)**")
        hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, value=13.0, step=0.1)
        hematokrit = st.number_input("Hematokrit (%)", min_value=0.0, value=40.0, step=0.1)
        leukosit = st.number_input("Leukosit (/uL)", min_value=0, value=8000)
        trombosit = st.number_input("Trombosit (/uL)", min_value=0, value=250000)
        
    with col_g:
        st.markdown("**Serologi & Infeksi**")
        status_hiv = st.selectbox("Screening HIV", ["Belum Diperiksa", "Non-Reaktif", "Reaktif"])
        status_hepatitis = st.selectbox("Screening Hepatitis B (HBsAg)", ["Belum Diperiksa", "Non-Reaktif", "Reaktif"])
        status_sifilis = st.selectbox("Screening Sifilis (VDRL/TPHA)", ["Belum Diperiksa", "Non-Reaktif", "Reaktif"])

st.divider()

# --- LOGIKA INFERENSI AI ---
if st.button("🚨 Analisis Triase Sekarang", use_container_width=True, type="primary"):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key di sidebar sebelah kiri!")
    elif not selected_model:
        st.error("Silakan pilih model AI di sidebar terlebih dahulu.")
    else:
        with st.spinner(f"Menganalisis matriks rekam medis dengan {selected_model}..."):
            try:
                model = genai.GenerativeModel(selected_model)
                
                # Menggabungkan seluruh data ke dalam satu Prompt terstruktur
                prompt = f"""
                Kamu adalah Dokter Jaga IGD Senior. Analisis kasus pasien ini dan tentukan status triase (Merah, Kuning, Hijau, atau Hitam) dan disposisi ruangan (Rawat Jalan, Rawat Inap Biasa, HDU, atau ICU).
                
                Data Profil & Sosiodemografi:
                - Usia: {usia} tahun
                - Jenis Kelamin: {gender}
                - Etnis: {etnis if etnis else 'Tidak spesifik'}
                - Pendidikan: {pendidikan}
                - Pekerjaan: {pekerjaan if pekerjaan else 'Tidak spesifik'}
                - Status Kawin: {status_nikah}
                - Golongan Darah: {gol_darah}
                - BB: {bb} kg, TB: {tb} cm
                
                Anamnesis & Riwayat Klinis:
                - Keluhan Utama: {keluhan}
                - Riwayat Penyakit (Komorbid): {riwayat_penyakit if riwayat_penyakit else 'Disangkal'}
                - Riwayat Obat: {riwayat_obat if riwayat_obat else 'Tidak ada data'}
                - Alergi: {alergi if alergi else 'Disangkal'}
                - Riwayat Perjalanan (14 hr): {riwayat_perjalanan if riwayat_perjalanan else 'Disangkal'}
                - Gaya Hidup & Diet: {kebiasaan_makan if kebiasaan_makan else 'Tidak spesifik'}
                
                Pemeriksaan Fisik & Lab:
                - Kesadaran: {kesadaran}
                - Gula Darah Sewaktu: {gula_darah} mg/dL
                - Darah Lengkap: Hb {hb} g/dL, Ht {hematokrit}%, Leukosit {leukosit}/uL, Trombosit {trombosit}/uL
                - Serologi: HIV {status_hiv}, HBsAg {status_hepatitis}, Sifilis {status_sifilis}
                
                Fokuskan diferensial diagnosis pada penyakit IGD akut dengan memperhatikan potensi infeksi menular, faktor risiko pekerjaan/perjalanan, serta interaksi obat dan alergi.
                Berikan jawaban dalam format persis seperti ini (tanpa markdown tebal):
                TRIASE: [Pilih warna]
                DIAGNOSA: [1-2 kemungkinan diagnosa]
                DISPOSISI: [Rawat Jalan / Rawat Inap / HDU / ICU]
                ALASAN: [Penjelasan medis komprehensif maksimal 4 kalimat, mengaitkan faktor risiko anamnesis dan lab]
                RENCANA TINDAKAN: [Sebutkan 3 langkah penanganan awal di IGD, termasuk isolasi jika ada kecurigaan penyakit menular, dan perhatikan alergi]
                """
                
                response = model.generate_content(prompt)
                hasil = response.text
                
                st.divider()
                st.subheader("📋 Hasil Analisis Clinical Decision Support (CDS)")
                
                if "MERAH" in hasil.upper():
                    st.error(hasil)
                elif "KUNING" in hasil.upper():
                    st.warning(hasil)
                elif "HIJAU" in hasil.upper():
                    st.success(hasil)
                else:
                    st.info(hasil)
                
                st.download_button(
                    label="📄 Download Laporan Triase Lengkap (.txt)",
                    data=hasil,
                    file_name="Laporan_Triase_IGD_Komprehensif.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat inferensi: {e}")
