# [Wattpad Audio](https://github.com/SBPhungNguyen1/wattpad-audio-v1)

> Turn Wattpad chapters into MP3 audiobooks. Code, work, and listen. 🎧

## Why?

**I DON'T HAVE TIME TO SIT DOWN AND READ WATTPAD.**

I just want to code while listening to stories. So I made this.

No extension. No backend. No FFmpeg.

<br>

**MADE FOR VIETNAMESE READERS, TOO! 🇻🇳**

Bạn thích đọc truyện trên Wattpad nhưng không có thời gian ngồi đọc?

**Wattpad Audio** chuyển nội dung chương truyện thành file MP3, giúp bạn vừa nghe truyện vừa code, làm việc hoặc thư giãn.

Hỗ trợ cả **truyện tiếng Việt và tiếng Anh**, với nhiều giọng đọc để lựa chọn.

## Features

- 📖 Automatically extract Wattpad chapter content
- 🌍 Support for Vietnamese and English stories
- 🗣️ Multiple AI voices
- 🎵 Generate one MP3 file per chapter
- 🔄 Automatic retries for failed requests

## Quick Start

**Requirements:** Python 3.10+ and an internet connection.

```bash
git clone https://github.com/SBPhungNguyen1/wattpad-audio-v1.git
cd wattpad-audio-v1

python -m venv venv
```

Activate the environment:

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage | Cách sử dụng

Choose the script based on **the language of your story**, not your nationality.

_Chọn script theo ngôn ngữ của truyện, không phải quốc tịch của bạn._

### 🇻🇳 Vietnamese stories | Truyện tiếng Việt

**Method 1: Run and paste the URL | Chạy rồi dán URL**

```bash
python wattpad_to_audio.py
```

When prompted, paste your Wattpad chapter URL and press Enter.

_Khi được hỏi, hãy dán URL chương truyện Wattpad rồi nhấn Enter._

**Method 2: Pass the URL directly | Truyền URL trực tiếp**

```bash
python wattpad_to_audio.py "WATTPAD_CHAPTER_URL"
```

**Choose a voice | Chọn giọng đọc**

- `nu` — Female / Nữ (default / mặc định)
- `nam` — Male / Nam

```bash
python wattpad_to_audio.py "WATTPAD_CHAPTER_URL" --voice nam
```

### 🇺🇸 English stories | Truyện tiếng Anh

**Method 1: Run and paste the URL | Chạy rồi dán URL**

```bash
python wattpad_to_audio_en.py
```

When prompted, paste your Wattpad chapter URL and press Enter.

_Khi được hỏi, hãy dán URL chương truyện Wattpad rồi nhấn Enter._

**Method 2: Pass the URL directly | Truyền URL trực tiếp**

```bash
python wattpad_to_audio_en.py "WATTPAD_CHAPTER_URL"
```

**Choose a voice | Chọn giọng đọc**

- `female` — US female
- `male` — US male
- `uk-female` — UK female
- `uk-male` — UK male

```bash
python wattpad_to_audio_en.py "WATTPAD_CHAPTER_URL" --voice uk-female
```

### Adjust reading speed | Điều chỉnh tốc độ đọc

Use `--rate` to make the narration faster or slower.

_Dùng `--rate` để tăng hoặc giảm tốc độ đọc._

```bash
# 10% faster
python wattpad_to_audio.py "WATTPAD_CHAPTER_URL" --rate +10%

# 10% slower
python wattpad_to_audio.py "WATTPAD_CHAPTER_URL" --rate -10%
```

You can combine options, too:

```bash
python wattpad_to_audio_en.py "WATTPAD_CHAPTER_URL" --voice uk-female --rate +10%
```

Your MP3 files will be saved in `audiobooks/`.

## Notes

- An internet connection is required for Wattpad extraction and Edge TTS.
- Long chapters may take a few minutes to process.
- Please respect Wattpad's Terms of Service and authors' copyrights.

## That's all

I just wanted to code while listening to stories. Now I can.

**Choose a language → Paste a link → Generate audio → Code while listening. 🎧**

One tiny problem, though...

**I built this tool to listen to stories, only to discover that the story I picked had been dropped. 💀**

Now I can automate the reading, but I can't automate the author's motivation to continue. 😭

Anyway, at least the code is still running.
