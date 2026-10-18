# [**Wattpad Audio**](https://github.com/SBPhungNguyen1/wattpad-audio-v1)

> A tiny Python script to turn Wattpad chapters into Vietnamese audiobooks (`.mp3`).

## 🎯 Why?

**I DON'T HAVE TIME TO SIT DOWN AND READ WATTPAD.**

I just want to code while listening to stories.

So I made this.

**No extension. No backend. No complicated setup.**

Just give it a Wattpad chapter link, let it extract the story, and turn the text into audio.

**Code → Listen → Repeat. 🎧**

## ✨ Features

- 📖 **Automatic extraction** — uses Playwright to load and extract chapter content.
- 🎧 **Vietnamese text-to-speech** — powered by Microsoft Edge TTS.
- 🗣️ **Two Vietnamese voices** — choose between female and male voices.
- 📚 **Long-chapter support** — splits long text into smaller chunks for TTS processing.
- 🔄 **Automatic retries** — retries failed audio-generation requests with exponential backoff.
- 🎵 **Single MP3 output** — combines audio chunks into one MP3 file without FFmpeg.
- 🧹 **Automatic cleanup** — temporary audio chunks are deleted after processing.
- 📂 **Organized output** — saves generated audiobooks in the `audiobooks/` directory.

## 🚀 How to use

### 1. Requirements

Make sure you have:

- [Python 3.10+](https://www.python.org/downloads/)
- An internet connection

That's it. No FFmpeg required.

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

**Basic usage:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..."
```

Or run the script without a link and enter it when prompted:

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

**Adjust the speaking rate:**

```bash
python wattpad_to_audio.py "https://www.wattpad.com/..." --rate +10%
```

### 6. Enjoy your audiobook 🎧

Your generated MP3 will be saved in:

```text
audiobooks/
└── Chapter_Title.mp3
```

Each chapter produces one MP3 file, named after the chapter title.

## 🔁 Next time

No need to reinstall anything.

Just open a terminal in the project folder, activate your virtual environment, and run the script again.

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
python wattpad_to_audio.py "https://www.wattpad.com/..."
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
- Respect Wattpad's Terms of Service, copyright, and authors' rights. Use the tool responsibly and do not redistribute copyrighted content without permission.

---

## 🇻🇳 Tiếng Việt

> Một script Python nhỏ giúp chuyển chương truyện Wattpad thành audiobook tiếng Việt (`.mp3`).

### 🎯 Tại sao?

**QUÁ LƯỜI ĐỂ NGỒI ĐỌC CHỮ TRÊN WATTPAD.**

Muốn vừa ngồi code vừa nghe truyện cho có động lực.

Vậy nên viết tạm cái tool này.

**Không extension. Không backend. Không cần FFmpeg.**

Đưa link Wattpad → Chuyển thành audio → Vừa nghe truyện vừa code (hoặc làm bất cứ việc gì khác).

### ✨ Tính năng

- 📖 **Tự động lấy nội dung** — sử dụng Playwright để tải và trích xuất chương truyện.
- 🎧 **Giọng đọc tiếng Việt** — sử dụng Microsoft Edge TTS.
- 🗣️ **Hai giọng đọc** — lựa chọn giọng nữ hoặc nam.
- 📚 **Xử lý chương dài** — chia văn bản thành các đoạn nhỏ để tạo audio.
- 🔄 **Tự động thử lại** — thử lại khi tạo audio thất bại, với thời gian chờ tăng dần.
- 🎵 **Một file MP3 hoàn chỉnh** — ghép các đoạn audio trực tiếp bằng Python, không cần FFmpeg.
- 🧹 **Tự động dọn dẹp** — xóa các file audio tạm sau khi hoàn tất.
- 📂 **Lưu trữ gọn gàng** — file MP3 được lưu trong thư mục `audiobooks/`, với tên dựa trên tiêu đề chương.

### 🚀 Cách sử dụng

**Yêu cầu:** Python 3.10 trở lên và kết nối Internet.

1. Clone repository và mở terminal trong thư mục dự án.
2. Tạo và kích hoạt môi trường ảo `venv`.
3. Cài đặt dependencies:

   ```bash
   python -m pip install -r requirements.txt
   playwright install chromium
   ```

4. Chạy script với link chương truyện Wattpad:

   ```bash
   python wattpad_to_audio.py "https://www.wattpad.com/..."
   ```

   Hoặc chạy script rồi nhập link khi được hỏi:

   ```bash
   python wattpad_to_audio.py
   ```

5. Chọn giọng đọc nếu muốn:

   ```bash
   python wattpad_to_audio.py "https://www.wattpad.com/..." --voice nam
   ```

6. Điều chỉnh tốc độ đọc nếu muốn:

   ```bash
   python wattpad_to_audio.py "https://www.wattpad.com/..." --rate +10%
   ```

7. Tìm file MP3 trong thư mục `audiobooks/`.

### ⚠️ Lưu ý

- Script phụ thuộc vào cấu trúc trang Wattpad hiện tại nên có thể cần cập nhật nếu website thay đổi.
- Edge TTS cần Internet để tạo giọng đọc.
- Chương dài có thể mất vài phút để xử lý.
- Các đoạn MP3 được nối trực tiếp, không thông qua FFmpeg.
- Hãy tôn trọng điều khoản sử dụng của Wattpad, bản quyền và quyền lợi của tác giả.

---

## That's all

I just wanted something **simple enough to let me code while listening to stories**.

So here it is.

**Paste a link → Generate audio → Code while listening. 🎧**
