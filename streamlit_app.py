import streamlit as st
from openai import OpenAI

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 OpenAI Chatbot Assistant")
st.caption("Aplikasi chatbot interaktif menggunakan Streamlit dan OpenAI")

# 1. Manajemen Keamanan & Validasi API Key
if "TOKENHARBOR_API_KEY" not in st.secrets:
    st.error("🚨 Konfigurasi API Key tidak ditemukan!")
    st.info("Pastikan file `.streamlit/secrets.toml` sudah dibuat untuk lokal, atau konfigurasikan Secrets di dashboard Streamlit Community Cloud.")
    st.stop()

api_key = st.secrets["TOKENHARBOR_API_KEY"]

if not api_key or api_key == "masukkan_api_key_openai_anda_di_sini":
    st.warning("⚠️ API Key masih menggunakan nilai default template. Silakan masukkan API Key OpenAI yang valid.")
    st.stop()

# Inisialisasi client OpenAI
client = OpenAI(api_key=api_key)
# Anda bisa mengganti model ke "gpt-4o" atau "gpt-3.5-turbo" sesuai kebutuhan
MODEL_NAME = "deepseek-v4.1-flash:free"

# 2. Manajemen Riwayat Percakapan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Inisialisasi pesan sambutan
    st.session_state.messages.append({"role": "assistant", "content": "Halo! Saya adalah asisten AI. Ada yang bisa saya bantu hari ini?"})

# Render ulang seluruh riwayat chat saat ada pembaruan UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Logika Input Pengguna & Pemrosesan LLM
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Render dan simpan pesan pengguna
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            # Karena format Streamlit state sudah cocok dengan format API OpenAI, 
            # kita bisa langsung mengoper st.session_state.messages
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
        st.error(f"Terjadi kesalahan saat menghubungi API OpenAI: {str(e)}")
