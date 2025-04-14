import streamlit as st
import requests, os, uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Talkie", page_icon="🌍")

# Background Image for the page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image:  url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL3mG12vmDPKUpx-86D_ZJFYO1HYdupGO9_vKu1KBes-m73Tmlhf_jH44Hueqxhw_CkME&usqp=CAU");
background-size: cover;
}

[data-testid="stHeader"]{
background-color: rgba(0, 0, 0, 0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
    <h1 style="text-align: center; font-size: 60px;">Talkie 🌍</h1>
    <br>
    <p style="text-align: center; font-size: 24px;font-weight: 600;">
        Talkie helps you break language barriers — just type, and it translates.
    </p>
    <br>
    <p style="text-align: center; font-size: 20px;">
        Choose your desired output language, type your message, and let Talkie instantly translate it by automatically detecting the language you're writing in.
    </p>
""", unsafe_allow_html=True)


# Language flags and their corresponding codes
languages = {
    'English': {'code': 'en', 'flag': 'https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg'},
    'French': {'code': 'fr', 'flag': 'https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg'},
    'German': {'code': 'de', 'flag': 'https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg'},
    'Italian': {'code': 'it', 'flag': 'https://upload.wikimedia.org/wikipedia/en/0/03/Flag_of_Italy.svg'},
    'Japanese': {'code': 'ja', 'flag': 'https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg'},
    'Korean': {'code': 'ko', 'flag': 'https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg'},
    'Romanian': {'code': 'ro', 'flag': 'https://upload.wikimedia.org/wikipedia/commons/7/73/Flag_of_Romania.svg'},
    'Russian': {'code': 'ru', 'flag': 'https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg'},
    'Spanish': {'code': 'es', 'flag': 'https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg'}
}

# Dropdown menu for selecting the output language, no default option
language_options = ["Choose a language"] + list(languages.keys())  # Add "Choose a language" as the first option

selected_language = st.selectbox(
    '',
    options=language_options,
    index=0  # Set the index to 0 to have the default option be "Choose a language"
)

# Check if the user has selected a language
if selected_language != "Choose a language":
    # Show selected language and flag
    selected_flag = languages[selected_language]['flag']
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; padding: 30px 0;">
            <img src="{selected_flag}" width="40" style="margin-right: 10px;"/>
            {selected_language}
        </div>
        """, unsafe_allow_html=True
    )

    # Map the selected language to its code
    target_language_code = languages[selected_language]['code']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language_code
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Initialize session state variables
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "inp_text" not in st.session_state:
        st.session_state.inp_text = ""

    # Layout: Left for Input and Right for Output
    t1, t2 = st.columns(2)

    # Left side: Input text box
    with t1:
        st.markdown(
            '''
            <h5 style="text-align: center; margin: 0; padding-bottom: 5px;">Enter text to translate:</h5>
            ''', 
            unsafe_allow_html=True
        )
        inp_text = st.text_area(" ", st.session_state.inp_text, key="input_text_area", height=100)

        # Update session state whenever the input changes
        st.session_state.inp_text = inp_text

        # Translate button
        if st.button('Translate'):
            # Create the body of the request with the text to be translated
            body = [{ 'text': st.session_state.inp_text }]
            # Make the call using post
            translator_request = requests.post(constructed_url, headers=headers, json=body)
            # Retrieve the JSON response
            translator_response = translator_request.json()
            # Retrieve the translation
            translated_text = translator_response[0]['translations'][0]['text']

            # Update the session state with the translated text
            st.session_state.translated_text = translated_text

    # Right side: Output text box
    with t2:
        st.markdown(
            '''
            <h5 style="text-align: center; margin: 0; padding-bottom: 5px;">Translated text:</h5>
            ''', 
            unsafe_allow_html=True
        )
        st.text_area(" ", st.session_state.translated_text, key="output_text_area", height=100)
