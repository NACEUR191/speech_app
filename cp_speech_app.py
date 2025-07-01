import streamlit as st
import speech_recognition as sr


# App setup
st.set_page_config(page_title="Online Speech Recognition", layout="centered")
st.title("🎙️ Speech Recognition App")
st.write("Choose an option, then click the button to speak and see the transcribed text.")

# API selection
api_choice = st.selectbox("Choose the recognition service:", ["Google", "Sphinx"])

# Language selection
language = st.text_input("Enter the language code (e.g., fr-FR, en-US)", value="fr-FR")

# Initialize recognizer
recognizer = sr.Recognizer()

if st.button("🎧 Listen and Transcribe"):
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak now.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            st.success("🔍 Audio received, processing...")

            if api_choice == "Google":
                texte = recognizer.recognize_google(audio, language=language)
            elif api_choice == "Sphinx":
                texte = recognizer.recognize_sphinx(audio, language=language)
            else:
                texte = "[Error: Unsupported API]"

            st.subheader("📝 Recognized Text:")
            st.write(texte)

            # Download button
            st.download_button("📥 Download Text", data=texte, file_name="transcription.txt")

    except sr.WaitTimeoutError:
        st.warning("⏱️ No voice detected within the time limit.")
    except sr.UnknownValueError:
        st.error("🤷 I couldn't understand what you said.")
    except sr.RequestError:
        st.error("🚫 Error with the selected recognition service.")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
