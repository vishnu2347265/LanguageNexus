import streamlit as st
import random
from PIL import Image
from datetime import date
from gtts import gTTS, lang
from googletrans import Translator
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_key(val):
    """function to find the key of the given value in the dict object

    Args:
        val (str): value to find key

    Returns:
        key(str): key for the given value
    """
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def main():
    # instance of Translator()
    trans = Translator()

    # gets gtts supported languages as dict
    langs = lang.tts_langs()

    # Sidebar layout
    st.sidebar.title("Language Nexus")
    st.sidebar.image("image.jpg", use_column_width=True)  # Insert your image here

    # Customize sidebar theme
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content .block-container {
            color: #333333;
            font-size: 16px;  /* Adjust the text size */
        }
        .sidebar .sidebar-content .block-container .radio-item label {
            color: #555555;
            font-size: 16px;  /* Adjust the text size */
        }
        .sidebar .sidebar-content .block-container .radio-item input:checked + label::before {
            border-color: #555555;
            background-color: #555555;
        }
        .sidebar .sidebar-content .block-container .radio-item input:checked + label::after {
            border-color: #555555;
            background-color: #555555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigate", ["Translate", "Dyslexia", "Word Cloud", "About Us"], index=0
    )

    if page == "Translate":
        translate_page(langs, trans)
    elif page == "Dyslexia":
        dyslexia_page()
    elif page == "Word Cloud":
        word_cloud_page()
    else:
        about_us_page()

def translate_page(langs, trans):
    # display current date & header
    st.title("Translation Made Easy")
    st.write(f"Date : {date.today()}")

    input_text = st.text_input("Enter text to translate")  # gets text to translate
    lang_choice = st.selectbox(
        "Language to translate: ", list(langs.values())
    )  # shows the supported languages list as selectbox options

    if st.button("Translate"):
        if input_text == "":
            # if the user input is empty
            st.warning("Please Enter text to translate")
        else:
            detect_expander = st.expander("Detected Language")
            with detect_expander:
                detect = trans.detect([input_text])[0]  # detect the user given text language
                detect_text = f"Detected Language : {langs[detect.lang]}"
                st.success(detect_text)  # displays the detected language

                # convert the detected text to audio file
                detect_audio = gTTS(text=input_text, lang=detect.lang, slow=False)
                detect_audio.save("user_detect.mp3")
                audio_file = open("user_detect.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

            trans_expander = st.expander("Translated Text")
            with trans_expander:
                translation = trans.translate(
                    input_text, dest=get_key(lang_choice)
                )  # translates user given text to target language
                translation_text = f"Translated Text : {translation.text}"
                st.success(translation_text)  # displays the translated text

                # convert the translated text to audio file
                translated_audio = gTTS(
                    text=translation.text, lang=get_key(lang_choice), slow=False
                )
                translated_audio.save("user_trans.mp3")
                audio_file = open("user_trans.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/ogg", start_time=0)

                # download button to download translated audio file
                with open("user_trans.mp3", "rb") as file:
                    st.download_button(
                        label="Download",
                        data=file,
                        file_name="trans.mp3",
                        mime="audio/ogg",
                    )

def dyslexia_page():
    st.title("Dyslexia Text Conversion App")
    st.write("Enter text in the box below to convert it into a dyslexia-friendly format:")

    # Text input box
    text_input = st.text_area("Enter text here:")

    # Button to trigger conversion
    if st.button("Convert to Dyslexia-Friendly Text"):
        # Convert text
        dyslexia_text = convert_to_dyslexia(text_input)

        # Display converted text
        st.write("Dyslexia-Friendly Text:")
        st.write(dyslexia_text)

def convert_to_dyslexia(text):
    """
    Convert text to dyslexia-friendly format
    """
    dyslexic_text = ""
    for word in text.split():
        if len(word) > 3:  # Only shuffle words with 4 or more letters
            middle_part = list(word[1:-1])  # Get the middle part of the word
            random.shuffle(middle_part)  # Shuffle middle letters
            dyslexic_word = word[0] + "".join(middle_part) + word[-1]  # Concatenate first, shuffled middle, and last letters
            dyslexic_text += dyslexic_word + " "
        else:
            dyslexic_text += word + " "  # Keep short words unchanged
    return dyslexic_text

def word_cloud_page():
    st.title("Word Cloud Generation")
    st.write("Enter text to generate a word cloud:")
    text = st.text_area("", height=150)

    if st.button("Generate Word Cloud"):
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        # Plot word cloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

def about_us_page():
    st.title("About Us")
    st.write("**Welcome to Language Nexus - your one-stop solution for translation needs!**")
    st.write("")
    st.subheader("**At Language Nexus, we are committed to providing you with a seamless and efficient translation experience. Our platform offers a range of features designed to cater to your diverse language requirements.**")
    st.write("")
    st.subheader("**Translation Made Easy**")
    st.write("Our translation tool allows you to effortlessly translate text from one language to another. Whether you need to communicate with clients from around the globe or simply want to explore different languages, our intuitive interface makes the process smooth and hassle-free.")
    st.write("")
    st.subheader("**Dyslexia-Friendly Text Conversion**")
    st.write("We understand the importance of accessibility for all users. That's why we've incorporated a dyslexia-friendly text conversion feature into our app. With a simple click, you can transform text into a format that is easier to read for individuals with dyslexia, ensuring inclusivity for all.")
    st.write("")
    st.subheader("**Word Cloud Generation**")
    st.write("Unleash your creativity with our word cloud generation tool. Visualize your text data in a dynamic and engaging way, allowing you to identify key themes and patterns at a glance. Whether for presentations, brainstorming sessions, or data analysis, our word cloud generator empowers you to make the most of your text.")
    st.write("")
    st.subheader("**Meet the Team**")
    st.write("Our team at Language Nexus is comprised of passionate individuals dedicated to delivering high-quality language solutions. From developers and designers to linguists and customer support specialists, each member plays a vital role in ensuring a seamless user experience.")
    st.write("")
    st.write("Feel free to reach out to us at example@example.com with any questions, feedback, or suggestions. We're here to make your translation journey simple and enjoyable.")
    st.write("")
    st.write("Thank you for choosing Language Nexus.")

if __name__ == "__main__":
    main()  # calls the main() first
