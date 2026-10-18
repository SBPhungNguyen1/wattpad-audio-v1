# [**Wattpad Audio**](https://github.com/SBPhungNguyen1/wattpad-audio-v1)

> A tiny Python tool to turn Wattpad chapters into audiobooks — so you can code, work, or do anything else while listening. 🎧

## 🎯 Why?

**I DON'T HAVE TIME TO SIT DOWN AND READ WATTPAD.**

I just want to code while listening to stories.

So I made this.

**No extension. No backend. No complicated setup.**

Just give it a Wattpad chapter link, let it extract the story, and turn the text into audio.

**Code → Listen → Repeat. 🎧**

## ✨ Features

- 📖 **Automatic extraction** — uses Playwright to load and extract Wattpad chapter content.
- 🌍 **Two language versions** — Vietnamese and English, each with its own script and voice options.
- 🗣️ **Multiple voices** — choose between female and male voices, including American and British English options.
- 📚 **Long-chapter support** — splits long text into smaller chunks for TTS processing.
- 🔄 **Automatic retries** — retries failed audio-generation requests with exponential backoff.
- 🎵 **Single MP3 output** — combines audio chunks into one MP3 file without FFmpeg.
- 🧹 **Automatic cleanup** — temporary audio chunks are deleted after processing.
- 📂 **Organized output** — saves generated audiobooks in the `audiobooks/` directory.

## 🌐 Choose your version

**Pick the script that matches the language of the story you want to listen to — not your nationality.**

| Version       | Script                   | Recommended for    | Default voice     |
| ------------- | ------------------------ | ------------------ | ----------------- |
| 🇻🇳 Vietnamese | `wattpad_to_audio.py`    | Vietnamese stories | Vietnamese female |
| 🇺🇸 English    | `wattpad_to_audio_en.py` | English stories    | American female   |

Both versions share the same setup and basic workflow. Choose whichever fits your story.

## 🚀 How to use

### 1. Requirements

Make sure you have:

- [Python 3.10+](https://www.python.org/downloads/)
- An internet connection

No FFmpeg required.

### 2. Clone the repository

```bash
git clone https://github.com/SBPhungNguyen1/wattpad-audio-v1.git
cd wattpad-audio-v1
```

### 3. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

With your virtual environment activated, run:

```bash
python -m pip install -r requirements.txt
playwright install chromium
```

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

### 5. Generate your audiobook

#### 🇻🇳 Vietnamese version

Use `wattpad_to_audio.py` for Vietnamese stories.

**Basic usage:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..."
```

Or run it without a link and enter the URL when prompted:

```bash
python wattpad_to_audio.py
```

**Choose a voice:**

Female voice (default):

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --voice nu
```

Male voice:

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --voice nam
```

#### 🇺🇸 English version

Use `wattpad_to_audio_en.py` for English stories.

**Basic usage:**

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..."
```

Or run it without a link and enter the URL when prompted:

```bash
python wattpad_to_audio_en.py
```

**Choose a voice:**

| Voice option | Voice           |
| ------------ | --------------- |
| `female`     | American female |
| `male`       | American male   |
| `uk-female`  | British female  |
| `uk-male`    | British male    |

Examples:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --voice female
```

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --voice uk-female
```

You can also specify any supported Edge TTS voice directly:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --voice en-AU-NatashaNeural
```

To see all available voices:

```bash
edge-tts --list-voices
```

### 6. Adjust the speaking rate

Both versions support adjusting the speaking rate.

**Read 10% faster:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --rate +10%
```

For English:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --rate +10%
```

**Read 10% slower:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --rate -10%
```

Replace the script name with `wattpad_to_audio_en.py` if you're using the English version.

### 7. Enjoy your audiobook 🎧

Both versions save generated MP3 files in:

```text
audiobooks/
└── Chapter_Title.mp3
```

Each chapter produces one MP3 file named after its chapter title.

## 🔁 Next time

No need to reinstall anything.

Open a terminal in the project folder, activate your virtual environment, and run the version you want.

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

For Vietnamese:

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..."
```

For English:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..."
```

When you're done:

```bash
deactivate
```

## ⚠️ Note

- This project relies on Wattpad's current page structure. Changes to the website may break content extraction.
- Audio generation requires an internet connection because Edge TTS processes text online.
- Long chapters may take several minutes to process.
- MP3 chunks are concatenated directly, relying on their compatible encoding and format.
- Choose a voice that matches the language of your story for the best listening experience.
- Respect Wattpad's Terms of Service, copyright, and authors' rights. Use the tool responsibly and do not redistribute copyrighted content without permission.

---

## 🇻🇳 Tiếng Việt

> Một công cụ Python nhỏ giúp chuyển chương truyện Wattpad thành audiobook MP3, để vừa code, vừa làm việc, vừa nghe truyện. 🎧

### 🎯 Tại sao?

**QUÁ LƯỜI ĐỂ NGỒI ĐỌC CHỮ TRÊN WATTPAD.**

Muốn vừa ngồi code vừa nghe truyện cho có động lực.

Vậy nên viết tạm cái tool này.

**Không extension. Không backend. Không cần FFmpeg.**

Đưa link Wattpad → Chuyển thành audio → Vừa nghe truyện vừa code (hoặc làm bất cứ việc gì khác).

### 🌍 Hiện tại có 2 phiên bản

Bạn không cần là người Việt để dùng bản tiếng Việt, cũng không cần là người nước ngoài để dùng bản tiếng Anh.

**Hãy chọn phiên bản theo ngôn ngữ truyện bạn muốn nghe.**

| Phiên bản     | File chạy                | Phù hợp với                             |
| ------------- | ------------------------ | --------------------------------------- |
| 🇻🇳 Vietnamese | `wattpad_to_audio.py`    | Truyện tiếng Việt, giọng đọc tiếng Việt |
| 🇺🇸 English    | `wattpad_to_audio_en.py` | Truyện tiếng Anh, giọng Mỹ hoặc Anh     |

### ✨ Tính năng

- 📖 **Tự động lấy nội dung** — sử dụng Playwright để tải và trích xuất chương truyện.
- 🌍 **Hai phiên bản ngôn ngữ** — tiếng Việt và tiếng Anh, mỗi bản có lựa chọn giọng đọc riêng.
- 🗣️ **Nhiều giọng đọc** — giọng nữ, nam; bản tiếng Anh có thêm lựa chọn giọng Mỹ và Anh.
- 📚 **Xử lý chương dài** — chia văn bản thành các đoạn nhỏ để tạo audio.
- 🔄 **Tự động thử lại** — thử lại khi tạo audio thất bại, với thời gian chờ tăng dần.
- 🎵 **Một file MP3 hoàn chỉnh** — ghép các đoạn audio trực tiếp bằng Python, không cần FFmpeg.
- 🧹 **Tự động dọn dẹp** — xóa các file audio tạm sau khi hoàn tất.
- 📂 **Lưu trữ gọn gàng** — MP3 được lưu trong thư mục `audiobooks/`.

### 🚀 Cách sử dụng

**Yêu cầu:** Python 3.10 trở lên và kết nối Internet.

1. Clone repository và mở terminal trong thư mục dự án.
2. Tạo và kích hoạt môi trường ảo `venv`.
3. Cài dependencies:

   ```bash
   python -m pip install -r requirements.txt
   playwright install chromium
   ```

4. Chạy phiên bản phù hợp với truyện muốn nghe.

**Truyện tiếng Việt:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..."
```

Giọng nam:

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --voice nam
```

**Truyện tiếng Anh:**

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..."
```

Giọng nữ Anh:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --voice uk-female
```

Giọng nam Anh:

```bash
python wattpad_to_audio_en.py "https://www.wattpad.com/..." --voice uk-male
```

5. Nếu muốn, điều chỉnh tốc độ đọc bằng `--rate +10%` hoặc `--rate -10%`.
6. Tìm file MP3 trong thư mục `audiobooks/`.

### ⚠️ Lưu ý

- Script phụ thuộc vào cấu trúc trang Wattpad hiện tại nên có thể cần cập nhật nếu website thay đổi.
- Edge TTS cần Internet để tạo giọng đọc.
- Chương dài có thể mất vài phút để xử lý.
- Các đoạn MP3 được nối trực tiếp, không thông qua FFmpeg.
- Nên chọn giọng đọc phù hợp với ngôn ngữ truyện để có trải nghiệm nghe tốt hơn.
- Hãy tôn trọng điều khoản sử dụng của Wattpad, bản quyền và quyền lợi của tác giả.

---

## That's all

I just wanted something **simple enough to let me code while listening to stories — in either Vietnamese or English.**

So here it is.

**Choose your language → Paste a link → Generate audio → Code while listening. 🎧**
