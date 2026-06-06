# ASCII Pictures at a Virtual Exhibition

Submission for [textjam2026](https://textjam.github.io/spring2026/)

A terminal-based exhibit of Modest Mussorgsky's Pictures at an Exhibition.

## How to run

The exhibit requires ffplay:

```bash
brew install ffmpeg # MacOS
sudo apt install ffmpeg # Linux
winget install ffmpeg # Windows
```

Install dependencies in a virtual environment

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the exhibit with python

```bash
python text.py
```
