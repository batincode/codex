# Interview Analyzer

This is a simple Flask web application that analyzes emotions in an interview video.

## Features
- Upload a video file of the interview.
- Process the video using the [FER](https://github.com/justinshenk/fer) library to detect facial emotions.
- Display a score for each emotion on a 0-10 scale and indicate pass/fail status.

## Requirements
See `requirements.txt` for Python dependencies. You can install them with:

```bash
pip install -r requirements.txt
```

This command installs all required Python packages, including
[MoviePy](https://zulko.github.io/moviepy/).
MoviePy relies on `ffmpeg` for video processing, so ensure `ffmpeg` is installed
and available on your `PATH`.
If you still see `ModuleNotFoundError: No module named 'moviepy.editor'`, run
`pip install moviepy` to ensure the package is available.

## Running

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.
