import speech_recognition as sr

def listen_for_question(timeout: int = 100, phrase_time_limit: int = 100) -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please ask your question. Listening for up to 100 seconds...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        recognized_text = r.recognize_google(audio)
        print(f"Recognized text: '{recognized_text}'")
        return recognized_text
    except sr.UnknownValueError:
        raise RuntimeError("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        raise RuntimeError(f"Could not request results from speech recognition service; {e}") 