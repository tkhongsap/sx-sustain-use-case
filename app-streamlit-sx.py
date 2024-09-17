import streamlit as st
import openai
import warnings
import base64
from openai import OpenAI
from utils.custom_css_main_page import get_main_custom_css
from utils.custom_css_banner import get_social_news_banner
from utils.openai_utils import generate_response
from utils.message_utils import format_message, message_func  # Import the utility functions
from PIL import Image

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set assistant id
assistant_id = "asst_CsRUOSckEYjuORKgVduj9Yib"  #sx-sustain-guide-mobile

# Set page config
st.set_page_config(
    page_title="🌍 SX-Sustainability-Guide",
    page_icon="🌿",
    layout="wide"
)

# Load and display social news banner
def load_social_news_banner():
    return get_social_news_banner()

st.markdown(load_social_news_banner(), unsafe_allow_html=True)

# Load and display main custom CSS
def load_main_custom_css():
    return get_main_custom_css()

st.markdown(load_main_custom_css(), unsafe_allow_html=True)


warnings.filterwarnings("ignore")
chat_history = []

# Model selection radio button
model = "GPT-4o"
st.session_state["model"] = model

# Load icons for user and assistant
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# Load icons for user and assistant
user_icon_path = "image/user_icon.jpg"
assistant_icon_path = "image/assistant_icon.png"

user_icon_base64 = get_image_base64(user_icon_path)
assistant_icon_base64 = get_image_base64(assistant_icon_path)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Meet your AI-Powered Assistant for today! 📊💼"}
    ]

# Display chat messages
for message in st.session_state["messages"]:
    is_user = message["role"] == "user"
    message_func(message["content"], user_icon_base64, assistant_icon_base64, is_user=is_user, model=model)

# Accept user input and generate a response
prompt = st.chat_input("Your message")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    message_func(prompt, user_icon_base64, assistant_icon_base64, is_user=True, model=model)

    response = generate_response(prompt, assistant_id)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    message_func(response, user_icon_base64, assistant_icon_base64, model=model)

