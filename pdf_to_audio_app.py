import PyPDF2
import pyttsx3
import streamlit as st
import base64

# ----- Function to Encode Local Image as Base64 -----
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ----- Apply Custom CSS with Background Image -----
def set_background(image_path):
    encoded_img = get_base64_image(image_path)
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_img}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #ffffff;
            }}
            h1 {{
                color: #00ffe7;
            }}
            .stButton>button {{
                background-color: #00bfff;
                color: white;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }}
            .stButton>button:hover {{
                background-color: #1e90ff;
            }}
        </style>
    """, unsafe_allow_html=True)

# ----- Set Background Image (update path if needed) -----
set_background("background.jpg")  # Replace with your image filename

# ----- Functions (no change in logic) -----
def init_tts_engine(rate=190, volume=2.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    return engine

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        full_text += page.extract_text()
    return full_text

def text_to_speech(engine, text, output_file):
    engine.save_to_file(text, output_file)
    engine.runAndWait()

# ----- Streamlit App UI -----
st.title("📘DocAudify - PDF to Audio Converter")

uploaded_file = st.file_uploader("📂 Upload a PDF", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    st.subheader("📝 Extracted Text")
    st.write(text)

    if st.button("🎧 Convert to Audio"):
        speaker = init_tts_engine()
        text_to_speech(speaker, text, 'output_audio.mp3')
        speaker.stop()

        st.success("✅ Audio file saved as 'output_audio.mp3'")
        st.audio('output_audio.mp3')
