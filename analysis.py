import os
import cv2
from fer import FER
from moviepy.editor import VideoFileClip
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures
import whisper
import openai


def extract_audio(video_path, audio_path="audio.wav"):
    """Extract audio from video and save to a file."""
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    return audio_path


def analyze_emotions(video_path):
    """Analyze emotions in a video using the FER library.

    Returns a dictionary mapping emotions to scores out of 10 based on
    average intensity over detected faces.
    """
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    emotions_sum = {}
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        result = detector.detect_emotions(frame)
        if not result:
            continue
        emotions = result[0]["emotions"]
        for emotion, score in emotions.items():
            emotions_sum[emotion] = emotions_sum.get(emotion, 0) + score

    cap.release()

    if frame_count == 0:
        return {}

    averaged = {
        emotion: min(10, (value / frame_count) * 10)
        for emotion, value in emotions_sum.items()
    }
    return averaged


def analyze_audio_emotions(audio_path):
    """Extract basic audio features as a proxy for emotion."""
    [sr, signal] = audioBasicIO.read_audio_file(audio_path)
    st_features, _ = ShortTermFeatures.feature_extraction(signal, sr,
                                                         0.05 * sr,
                                                         0.05 * sr)
    energy = st_features[1].mean()
    zcr = st_features[0].mean()
    return {"energy": float(energy), "zcr": float(zcr)}


def transcribe_audio(audio_path, model="base"):
    """Transcribe speech in the audio using Whisper."""
    whisper_model = whisper.load_model(model)
    result = whisper_model.transcribe(audio_path)
    return result["text"]


def honesty_analysis(text, api_key=None):
    """Send the text to OpenAI API for a sincerity analysis."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        return "No API key provided."
    openai.api_key = key
    prompt = (
        "Aşağıdaki konuşma metnini analiz et. Konuşma samimi mi? "
        "Kişi dürüst mü konuşuyor gibi görünüyor mu?\n\nMetin:\n" + text
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()


def full_analysis(video_path, api_key=None):
    """Run the full analysis pipeline on a video file."""
    audio_path = extract_audio(video_path)
    face_scores = analyze_emotions(video_path)
    audio_scores = analyze_audio_emotions(audio_path)
    transcript = transcribe_audio(audio_path)
    honesty = honesty_analysis(transcript, api_key)
    return {
        "faces": face_scores,
        "audio": audio_scores,
        "transcript": transcript,
        "honesty": honesty,
    }
