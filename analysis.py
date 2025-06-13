import cv2
from fer import FER


def analyze_emotions(video_path):
    """Analyze emotions in a video using the FER library.

    Returns a dictionary mapping emotions to scores out of 10.
    The score is computed based on the average intensity of each emotion.
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
        # result is a list of dicts; we take the first face detected
        emotions = result[0]["emotions"]
        for emotion, score in emotions.items():
            emotions_sum[emotion] = emotions_sum.get(emotion, 0) + score

    cap.release()

    if frame_count == 0:
        return {}

    # Average and scale to 0-10
    averaged = {
        emotion: min(10, (value / frame_count) * 10)
        for emotion, value in emotions_sum.items()
    }
    return averaged
