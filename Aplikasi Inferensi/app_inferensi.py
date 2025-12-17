# app_inferensi.py

# Untuk menjalankan aplikasi ini:
# 1. Pastikan SWI-Prolog dan Streamlit terinstal.
# 2. Pastikan file 'prolog_kb.pl' berada di folder yang sama.
# 3. Jalankan di terminal: streamlit run app_inferensi.py

import streamlit as st
from pyswip import Prolog

# Nama file Knowledge Base Prolog
KB_FILE = 'prolog_kb.pl'

# --- 1. SETUP DAN INISIALISASI PROLOG ---
# Menggunakan st.session_state untuk menjaga koneksi Prolog tetap hidup selama sesi Streamlit
if 'prolog' not in st.session_state:
    try:
        # Inisialisasi Prolog dan memuat KB
        prolog = Prolog()
        # Menggunakan consult() untuk memuat file .pl eksternal
        prolog.consult(KB_FILE) 
        
        st.session_state.prolog = prolog
        st.session_state.kb_loaded = True
        
    except Exception as e:
        # Menampilkan pesan error jika SWI-Prolog atau file KB tidak ditemukan
        st.error(f"Gagal memuat SWI-Prolog atau file '{KB_FILE}'. Pastikan SWI-Prolog terinstal dan file KB ada.")
        st.error(f"Error detail: {e}")
        st.stop()

prolog = st.session_state.prolog

# --- 2. DEFINISI INFERENSI/QUERY ---

# List 8 Inferensi wajib untuk Tugas Besar (Disesuaikan dari 5 inferensi yang kita rancang)
inferensi_list = [
    {
        "nama": "Inferensi 1: Cek Kepopuleran (Facts)",
        "query": "lokasi_populer(X)",
        "deskripsi": "Uji Modus Ponens Sederhana: Lokasi mana saja yang terdaftar sebagai lokasi populer? (Uji Fakta)"
    },
    {
        "nama": "Inferensi 2: Potensi Antrean (Rule 1)",
        "query": "antrean_panjang(X)",
        "deskripsi": "Uji Modus Ponens: Lokasi mana yang diprediksi memiliki antrean panjang karena populer?"
    },
    {
        "nama": "Inferensi 3: Wisatawan Lelah (Rule 2)",
        "query": "fisik_lelah(Y)",
        "deskripsi": "Uji Konjungsi Kompleks: Siapa wisatawan yang lelah karena mengantre di lokasi populer?"
    },
    {
        "nama": "Inferensi 4: Dampak Pengalaman (Rantai Penuh)",
        "query": "pengalaman_buruk(X)",
        "deskripsi": "Uji Rantai Inferensi 3 Langkah (Hypothetical Syllogism): Siapa yang akhirnya mendapatkan pengalaman buruk?"
    },
    {
        "nama": "Inferensi 5: Analisis Lokasi Sulit (Tambahan)",
        "query": "lokasi_sulit(X)",
        "deskripsi": "Uji Rule Tambahan dari KB: Daerah mana yang macet DAN susah parkir? (Uji Konjungsi Sederhana)"
    },
    # Tambahan Inferensi untuk memenuhi target 8 Query wajib
    {
        "nama": "Inferensi 6: Lokasi Terisolasi (Rule 5)",
        "query": "terisolasi(X)",
        "deskripsi": "Uji Rule 5: Lokasi mana yang jaraknya JAUH (> 7 km) dari lokasi lain? (Uji Perbandingan)"
    },
    {
        "nama": "Inferensi 7: Wisatawan Repot (Rule 6)",
        "query": "wisatawan_repot(Y)",
        "deskripsi": "Uji Rule 6: Siapa wisatawan yang repot karena mengunjungi lokasi populer tanpa fasilitas parkir mobil? (Uji Negasi)"
    },
    {
        "nama": "Inferensi 8: Cek Kepuasan (Rule 7)",
        "query": "wisatawan_puas(Z)",
        "deskripsi": "Uji Rule 7: Siapa wisatawan yang TIDAK mendapat pengalaman buruk? (Uji Negasi)"
    }
]

def run_query(query):
    """Menjalankan query Prolog dan memformat hasilnya."""
    try:
        # Menjalankan query Prolog
        results = list(prolog.query(query))
        
        if not results:
            return "Kesimpulan: TIDAK VALID / TIDAK DITEMUKAN (False)"
        
        # Memformat hasil untuk variabel terikat (e.g., X = area_dago)
        if results and isinstance(results[0], dict):
            # Menggunakan set untuk memastikan variabel unik, meskipun dalam konteks ini biasanya cukup
            formatted_results = ", ".join([f"{k} = {v}" for item in results for k, v in item.items()])
            return f"Kesimpulan: VALID. Hasil: {formatted_results}"
        
        # Jika hasilnya hanya True (e.g., query 'lokasi_populer(area_dago)')
        return "Kesimpulan: VALID. Proposisi terbukti benar (True)."

    except Exception as e:
        # Menangani kesalahan sintaks Prolog di query kustom
        return f"ERROR: Terjadi kesalahan sintaks Prolog: {e}"

# --- 3. TAMPILAN APLIKASI STREAMLIT ---

st.set_page_config(layout="wide")
st.title("🤖 Logic Programming GUI: Analisis Itinerary Kuliner Bandung")
st.markdown(f"Status KB: **File `{KB_FILE}`** berhasil dimuat.")
st.markdown("---")

col_kb, col_query = st.columns([1, 2])

with col_kb:
    st.header("Knowledge Base (KB)")
    st.markdown("KB dimuat dari file eksternal `prolog_kb.pl`")
    
    st.subheader("Struktur Prolog (.pl)")
    # Membaca isi file prolog_kb.pl untuk ditampilkan
    try:
        with open(KB_FILE, 'r') as f:
            kb_content = f.read()
        st.code(kb_content, language="prolog")
    except FileNotFoundError:
        st.warning(f"File {KB_FILE} tidak ditemukan. Mohon pastikan file KB ada di direktori yang sama.")


with col_query:
    st.header("Uji Inferensi Rantai Penalaran (FOL)")
    st.info("Pilih salah satu dari 8 Inferensi yang telah Anda rancang:")

    for i, item in enumerate(inferensi_list):
        # Menggunakan st.expander untuk tampilan yang rapi
        with st.expander(f"{item['nama']} (Uji Query)", expanded=False):
            st.markdown(f"**Tujuan:** {item['deskripsi']}")
            # Menampilkan query yang akan diuji
            st.code(item['query'], language="prolog")
            
            if st.button(f"UJI INFERENSI {i+1}", key=f"btn_{i}"):
                # Menjalankan fungsi run_query
                result = run_query(item['query'])
                st.success("Hasil Inferensi Ditemukan:")
                st.markdown(f"**Query:** `{item['query']}`")
                st.markdown(f"**Hasil:** {result}")

    st.markdown("---")
    st.subheader("Uji Query Kustom")
    custom_query = st.text_input("Masukkan Query Prolog Anda (cth: lokasi_populer(area_braga) )")
    
    # Menjalankan query kustom
    if st.button("JALANKAN QUERY KUSTOM"):
        if custom_query:
            result = run_query(custom_query)
            st.markdown(f"**Hasil Query Kustom:** {result}")