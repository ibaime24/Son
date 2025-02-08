from dotenv import load_dotenv
from datetime import datetime
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Load environment variables from .env file
load_dotenv()

import os
import openai
import lmnt
import cv2
import pygame
import speech_recognition as sr
import requests
import time
import base64
from openai import OpenAI
import asyncio
from lmnt.api import Speech

# Import helper functions
from helpers.listen_for_question import listen_for_question
from helpers.capture_photo import capture_photo
from helpers.process_image_and_question import process_image_and_question
from helpers.speak_with_elevenlabs import speak_with_elevenlabs

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
LMNT_API_KEY = os.getenv("LMNT_API_KEY", "YOUR_LMNT_API_KEY")
openai.api_key = OPENAI_API_KEY

# If you have a local or specialized endpoint (replace or remove this if not needed):
BACKEND_URL = "http://127.0.0.1:5000/process-image"


# ------------------------------------------------------------------------------
# Main Workflow
# ------------------------------------------------------------------------------

def log_timing(operation: str, start_time: datetime) -> float:
    """Calculate and log the duration of an operation."""
    duration = (datetime.now() - start_time).total_seconds()
    print(f"{operation}: {duration:.2f} seconds")
    return duration

async def main():
    camera = None
    photo_path = None
    running = True

    try:
        total_start_time = datetime.now()
        # Initialize and warm up camera
        camera_start = datetime.now()
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Unable to access the camera.")
            return

        # Camera setup and warmup
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        camera.set(cv2.CAP_PROP_FPS, 30)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        for _ in range(2):
            camera.read()
            await asyncio.sleep(0.05)
        
        log_timing("Camera initialization", camera_start)

        print("Son is ready! Say 'stop' to exit.")
        
        # Use ElevenLabs for the intro
        await speak_with_elevenlabs("Hi! I'm Son. I'm here to help you navigate the world.")
        
        print(f"API Key: {os.getenv('ELEVENLABS_API_KEY')}")
        
        while running:   # while loop so it wont stop after one request
            try:
                iteration_start = datetime.now()
                
                # 1) Listen for the user's question
                listen_start = datetime.now()
                question = listen_for_question()
                listen_duration = log_timing("Speech recognition", listen_start)
                
                # Check if user wants to stop
                if question.lower().strip() == "stop":
                    print("Stopping the assistant...")
                    break

                # 2) Capture a photo
                photo_start = datetime.now()
                photo_path = capture_photo()
                photo_duration = log_timing("Photo capture", photo_start)

                # 3) Send the question & image to OpenAI
                gpt_start = datetime.now()
                answer = process_image_and_question(photo_path, question)
                gpt_duration = log_timing("GPT processing", gpt_start)

                # 4) Speak the response with LMNT
                speech_start = datetime.now()
                await speak_with_elevenlabs(answer)
                speech_duration = log_timing("Speech synthesis and playback", speech_start)

                # Log total iteration time
                total_duration = log_timing("Total iteration", iteration_start)
                print(f"\nBreakdown for this iteration:")
                print(f"Speech Recognition: {listen_duration:.2f}s ({(listen_duration/total_duration)*100:.1f}%)")
                print(f"Photo Capture: {photo_duration:.2f}s ({(photo_duration/total_duration)*100:.1f}%)")
                print(f"GPT Processing: {gpt_duration:.2f}s ({(gpt_duration/total_duration)*100:.1f}%)")
                print(f"Speech Synthesis: {speech_duration:.2f}s ({(speech_duration/total_duration)*100:.1f}%)")
                print(f"Total Time: {total_duration:.2f}s\n")

                # Clean up photo after each successful interaction
                if photo_path and os.path.exists(photo_path):
                    os.remove(photo_path)

            except Exception as e:
                print(f"[Error in interaction] {e}")
                print("Ready for next question...")
                continue

        # Use ElevenLabs for the outro
        await speak_with_elevenlabs("Goodbye!")

    except Exception as e:
        print(f"[Critical Error] {e}")
    finally:
        # Cleanup and log total runtime
        if camera is not None:
            camera.release()
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        total_runtime = log_timing("Total runtime", total_start_time)
        print("Assistant stopped. Goodbye!")

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())