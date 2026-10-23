import streamlit as st
from openai import OpenAI

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 DeepSeek Chatbot Assistant")
st.caption("Aplikasi chatbot menggunakan Streamlit dan DeepSeek via TokenHarbor")

# 1. Manajemen Keamanan & Validasi API Key
if "TOKENHARBOR_API_KEY" not in st.secrets:
    st.error("🚨 Konfigurasi API Key tidak ditemukan!")
    st.info("Pastikan file `.streamlit/secrets.toml` sudah dibuat untuk lokal, atau konfigurasikan Secrets di dashboard Streamlit Community Cloud.")
    st.stop()

api_key = st.secrets["TOKENHARBOR_API_KEY"]

if not api_key or api_key == "masukkan_api_key_openai_anda_di_sini":
    st.warning("⚠️ API Key masih menggunakan nilai default template. Silakan masukkan API Key yang valid.")
    st.stop()

# 2. Inisialisasi client OpenAI & Model
# PERBAIKAN: Gunakan variabel api_key dari st.secrets, bukan os.environ
client = OpenAI(
    api_key=api_key,
    base_url="https://tokenharbor.ai/v1",
)

# PERBAIKAN: Definisikan nama model agar bisa dipanggil di logika obrolan bawah
MODEL_NAME = "deepseek-v4.1-flash:free"

# 3. Manajemen Riwayat Percakapan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Inisialisasi pesan sambutan
    st.session_state.messages.append({"role": "assistant", "content": "Halo! Saya adalah asisten AI dari TokenHarbor. Ada yang bisa saya bantu hari ini?"})

# Render ulang seluruh riwayat chat saat ada pembaruan UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Logika Input Pengguna & Pemrosesan LLM
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Render dan simpan pesan pengguna
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            # PERBAIKAN: Menggunakan variabel MODEL_NAME yang sudah dideklarasikan di atas
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=True,
            )
            
            # Rendering respons secara streaming (real-time)
            response = st.write_stream(stream)
            
        # Simpan respons asisten ke state
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghubungi API TokenHarbor: {str(e)}")
