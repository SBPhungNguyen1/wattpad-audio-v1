"""
Wattpad -> Audio (1 chương = 1 file MP3)

Cài đặt:
    pip install playwright edge-tts
    playwright install chromium

Dùng:
    python wattpad_to_audio.py                      # sẽ hỏi link
    python wattpad_to_audio.py <link_chuong>        # truyền link trực tiếp
    python wattpad_to_audio.py <link> --voice nam   # giọng nam
    python wattpad_to_audio.py <link> --rate +10%   # đọc nhanh hơn
"""

import argparse
import asyncio
import os
import re
import tempfile

import edge_tts
from playwright.async_api import async_playwright

VOICES = {
    "nu": "vi-VN-HoaiMyNeural",
    "nam": "vi-VN-NamMinhNeural",
}
OUTPUT_DIR = "audiobooks"
MAX_CHARS = 2000  # độ dài tối đa mỗi đoạn gửi lên dịch vụ TTS

JS_EXTRACT_CONTENT = """
() => {
    const article = document.querySelector("article.story-part");
    if (!article) return null;

    const partId = article.getAttribute("data-part-id");
    const chapterTitle = document.querySelector(".part-header h1")?.textContent?.trim()
                         || `Chapter_${partId || Date.now()}`;

    const paragraphs = [...article.querySelectorAll("p[data-p-id]")].map((p) => {
        const clone = p.cloneNode(true);
        clone.querySelectorAll(".component-wrapper").forEach((el) => el.remove());
        clone.querySelectorAll("br").forEach((br) => br.replaceWith("\\n"));
        let text = clone.textContent || "";
        return text.replace(/\\u00a0/g, " ")
                   .replace(/\\r?\\n/g, "\\n")
                   .replace(/[ \\t]*\\n[ \\t]*/g, "\\n")
                   .replace(/[ \\t]{2,}/g, " ")
                   .replace(/\\n{3,}/g, "\\n\\n")
                   .trim();
    }).filter(Boolean);

    const normalized = paragraphs.map((t) =>
        t.replace(/([^\\n])\\n(?=[a-zà-ỹA-ZÀ-Ỹ0-9"“‘(])/g, "$1 ").replace(/[ \\t]{2,}/g, " ").trim()
    );

    return { title: chapterTitle, content: normalized.join("\\n\\n") };
}
"""


# ----------------------------------------------------------------------------
# 1. Lấy nội dung chương
# ----------------------------------------------------------------------------
async def scrape_wattpad_chapter(url: str) -> dict | None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        print("[1/3] Đang tải trang web...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Popup cảnh báo nội dung người lớn
        try:
            btn = page.locator(
                "button:has-text('Tiếp tục'), button:has-text('Continue')"
            ).first
            if await btn.is_visible(timeout=3000):
                await btn.click()
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        print("[2/3] Đang cuộn trang để tải toàn bộ nội dung...")
        previous_height, stable = 0, 0
        for _ in range(60):
            await page.evaluate(
                "() => window.scrollTo({ top: document.scrollingElement.scrollHeight, behavior: 'smooth' })"
            )
            await page.wait_for_timeout(800)
            height = await page.evaluate("() => document.scrollingElement.scrollHeight")
            stable = stable + 1 if height == previous_height else 0
            previous_height = height
            if stable >= 3:
                break

        data = await page.evaluate(JS_EXTRACT_CONTENT)
        await browser.close()
        return data


# ----------------------------------------------------------------------------
# 2. Chia văn bản + tạo audio
# ----------------------------------------------------------------------------
def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Chia văn bản ở chỗ xuống dòng / cuối câu, tránh cắt ngang câu."""
    text = text.strip()
    chunks = []

    while len(text) > max_chars:
        limit = min(max_chars, len(text))
        split_at = -1
        for sep in ("\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " "):
            pos = text.rfind(sep, 0, limit)
            if pos >= max_chars // 2:
                split_at = pos + len(sep)
                break
        if split_at <= 0:
            split_at = max_chars

        chunk = text[:split_at].strip()
        if chunk:
            chunks.append(chunk)
        text = text[split_at:].strip()

    if text:
        chunks.append(text)
    return chunks


async def synthesize_chunk(text: str, path: str, voice: str, rate: str, retries: int = 3):
    """Tạo 1 đoạn MP3, tự thử lại nếu lỗi mạng/dịch vụ."""
    for attempt in range(1, retries + 1):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(path)
            if os.path.getsize(path) == 0:
                raise RuntimeError("File MP3 rỗng")
            return
        except Exception as exc:
            if os.path.exists(path):
                os.remove(path)
            if attempt == retries:
                raise RuntimeError(f"Tạo audio thất bại sau {retries} lần thử: {exc}")
            delay = 2 ** attempt
            print(f"      ⚠️ Lần {attempt}/{retries} lỗi: {exc}. Thử lại sau {delay}s...")
            await asyncio.sleep(delay)


async def text_to_speech(text: str, output_path: str, voice: str, rate: str):
    """Tạo audio từng đoạn rồi ghép thành MỘT file MP3 duy nhất (không cần FFmpeg)."""
    chunks = split_text(text)
    if not chunks:
        raise ValueError("Văn bản cần đọc đang trống.")

    print(f"   - Số đoạn cần xử lý: {len(chunks)}")

    # Các đoạn tạm nằm trong thư mục tạm, tự xóa khi xong
    with tempfile.TemporaryDirectory() as tmp_dir, open(output_path, "wb") as out:
        for i, chunk in enumerate(chunks, start=1):
            print(f"   [{i}/{len(chunks)}] Đang tạo audio ({len(chunk)} ký tự)...")
            part_path = os.path.join(tmp_dir, f"{i:03d}.mp3")
            await synthesize_chunk(chunk, part_path, voice, rate)

            # MP3 từ edge-tts cùng định dạng nên có thể nối byte trực tiếp
            with open(part_path, "rb") as part:
                out.write(part.read())


# ----------------------------------------------------------------------------
# 3. Chạy chính
# ----------------------------------------------------------------------------
async def main():
    parser = argparse.ArgumentParser(description="Chuyển chương Wattpad thành 1 file MP3")
    parser.add_argument("url", nargs="?", help="Link chương Wattpad")
    parser.add_argument("--voice", choices=VOICES.keys(), default="nu", help="nu (mặc định) hoặc nam")
    parser.add_argument("--rate", default="+0%", help="Tốc độ đọc, ví dụ +10%% hoặc -10%%")
    args = parser.parse_args()

    url = args.url or input("Dán link chương Wattpad cần đọc: ").strip()
    if not url:
        print("Link không hợp lệ!")
        return

    data = await scrape_wattpad_chapter(url)
    if not data or not data.get("content"):
        print("❌ Không lấy được nội dung chương. Vui lòng kiểm tra lại đường dẫn!")
        return

    title = data["title"]
    content = f"{title}\n\n{data['content']}"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = re.sub(r'[<>:"/\\|?*\n\r\t]', "_", title).strip()[:80]
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name or 'audiobook'}.mp3")

    voice = VOICES[args.voice]
    print(f"\n✅ Đã trích xuất xong: {title} ({len(content):,} ký tự)")
    print(f"[3/3] Đang tạo file MP3 với giọng {voice}...")

    await text_to_speech(content, output_path, voice, args.rate)
    print(f"\n🎉 Hoàn tất! File đã được lưu tại:\n👉 {os.path.abspath(output_path)}")


if __name__ == "__main__":
    asyncio.run(main())