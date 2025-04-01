import os
import time
import openai
from ddtrace import tracer
from datadog import initialize, api
import requests
import json
import azure.cognitiveservices.speech as speechsdk

DATADOG_API_KEY = os.getenv("DD_API_KEY")
DATADOG_APP_KEY = os.getenv("DD_APP_KEY")  # only needed for metrics API
ML_APP_NAME = os.getenv("DD_LLMOBS_ML_APP", "azure-openai-app")

initialize(api_key=DATADOG_API_KEY, app_key=DATADOG_APP_KEY)

def send_log_to_datadog(message):
    requests.post(
        "https://http-intake.logs.datadoghq.com/v1/input",
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": DATADOG_API_KEY
        },
        data=json.dumps({
            "message": message,
            "ddsource": "python",
            "service": "azure-openai",
            "ml_app": ML_APP_NAME
        })
    )

@tracer.wrap(service="azure-openai", resource="synthesize_speech")
def synthesize_speech(text):
    start_time = time.time()
    
    speech_config = speechsdk.SpeechConfig(
        endpoint=f"wss://prod-speechservicebyos2.cognitiveservices.azure.com/tts/cognitiveservices/websocket/v1",
        subscription="subscription_key"
    )
    speech_config.speech_synthesis_voice_name = "en-US-AlloyMultilingualNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        with open('output.wav', 'wb') as f:
            f.write(audio_data)
        send_log_to_datadog(f"TTS success: {text}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        send_log_to_datadog(f"TTS canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            send_log_to_datadog(f"Error details: {cancellation_details.error_details}")
    else:
        send_log_to_datadog(f"Unknown TTS result reason: {result.reason}")
    
    duration = round(time.time() - start_time, 2)
    
    api.Metric.send(
        metric="azure_openai.tts.duration",
        points=duration,
        tags=["ml_app:" + ML_APP_NAME, "voice:Alloy"]
    )

if __name__ == "__main__":
    text = "Hi, this is Alloy Multilingual"
    synthesize_speech(text)
