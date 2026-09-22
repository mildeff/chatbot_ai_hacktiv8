import streamlit as st
import config
from utils import get_openai_client, prepare_message, generate_triage_response

# konfigurasi halaman
st.set_page_config(
      page_title="Asisten Tensi Medis berbasis AI",
      page_icon='*',
      layout='centered'
      )

st.title(config.APP_TITLE)
st.caption(config.APP_CAPTION)
st.sidebar.header("konfigurasi dan parameter")

api_key = st.sidebar.text_input("masukkan api key disini:", type="password")
if not api_key:
      st.info("silahkan masukan api key di sidebar untuk memulai", icon="🌟")
      st.stop()

client = get_openai_client(api_key)
temperature = st.sidebar.slider(
      "temperature (kreativitas)",
      min_value=0.0,
      max_value=1.0,
      value=config.DEFAULT_TEMPERATURE,
      step=0.1,
      help="nilai rendah (0.0 - 0.3) membuat jawaban lebih faktual dan terstruktur"
)

persona_name = st.sidebar.selectbox(
      "pilih gaya bahasa atau persona",
      options=list(config.SYSTEM_PERSONAS.keys())
)

selected_system_prompt = config.SYSTEM_PERSONAS[persona_name]
enable_memory = st.sidebar.checkbox("aktifkan fitur memory", value=True)

if st.sidebar.button("reset percakapan"):
      st.session_state.messages = []
      st.rerun()

# disclaimer
st.sidebar.markdown("---")
st.sidebar.warning(config.DISCLAIMER_TEXT)

#kelola riwayat chat atau session state
if "messages" not in st.session_state:
      st.session_state.messages = []

#tampilin obrolan sebelum nya di UI
for message in st.session_state.messages:
      with st.chat_message(message["role"]):
            st.markdown(message["content"])

#interaksi chat
if user_input := st.chat_input("tuliskan gejala atau pertanyaan kesehatan kamu disini"):
      with st.chat_message("user"):
            st.markdown(user_input)

      api_messages = prepare_message(
            system_prompt=selected_system_prompt,
            chat_history=st.session_state.messages,
            user_input=user_input,
            enable_memory=enable_memory
      )

      #proses response dari si AI
      with st.chat_message("assistant"):
            with st.spinner("menganalisa gejala"):
                  try:
                        response_text = generate_triage_response(client, api_messages, temperature)
                        st.markdown(response_text)

                        st.session_state.messages.append({"role": "user", "content": user_input})
                        st.session_state.messages.append({"role": "assistant", "content": response_text})

                  except Exception as e:
                        st.error(f"terjadi kesalahan saat memanggil API: {e}")