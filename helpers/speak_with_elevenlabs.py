import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame
import asyncio

# Initialize the ElevenLabs client

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

# Function to convert text to speech and play it

def text_to_speech_file(text: str) -> str:
    response = elevenlabs_client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    save_file_path = f"{uuid.uuid4()}.mp3"
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path

async def speak_with_elevenlabs(text: str):
    try:
        audio_file_path = text_to_speech_file(text)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        os.remove(audio_file_path)

    except Exception as e:
        print(f"[Error] ElevenLabs TTS synthesis failed: {e}") 