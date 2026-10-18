"""
Wattpad -> Audio (1 chapter = 1 MP3 file), English version

Setup:
    python -m venv venv
    (activate the venv)
    pip install -r requirements.txt
    playwright install chromium

Usage:
    python wattpad_to_audio_en.py                       # prompts for the link
    python wattpad_to_audio_en.py <chapter_url>         # pass the link directly
    python wattpad_to_audio_en.py <url> --voice male    # male voice
    python wattpad_to_audio_en.py <url> --voice uk-female
    python wattpad_to_audio_en.py <url> --rate +10%     # read faster
    python wattpad_to_audio_en.py <url> --voice en-AU-NatashaNeural   # any edge-tts voice

List every available voice with:
    edge-tts --list-voices
"""

import argparse
import asyncio
import os
import re
import tempfile

import edge_tts
from playwright.async_api import async_playwright

# Friendly aliases -> edge-tts voice names (you can also pass a full voice name)
VOICES = {
    "female": "en-US-AriaNeural",
    "male": "en-US-GuyNeural",
    "uk-female": "en-GB-SoniaNeural",
    "uk-male": "en-GB-RyanNeural",
}
OUTPUT_DIR = "audiobooks"
MAX_CHARS = 2000  # max characters per request sent to the TTS service

JS_EXTRACT_CONTENT = """
() => {
    const article = document.querySelector("article.story-part");
    if (!article) return null;

    const partId = article.getAttribute("data-part-id");
    const chapterTitle = document.querySelector(".part-header h1")?.textContent?.trim()
                         || `Chapter_${partId || Date.now()}`;

    // Clean up each paragraph
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

    // Join lines that were broken in the middle of a sentence
    const normalized = paragraphs.map((t) =>
        t.replace(/([^\\n])\\n(?=[a-zA-Z0-9"“‘(])/g, "$1 ").replace(/[ \\t]{2,}/g, " ").trim()
    );

    return { title: chapterTitle, content: normalized.join("\\n\\n") };
}
"""


# ----------------------------------------------------------------------------
# 1. Scrape the chapter
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

        print("[1/3] Loading the page...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Dismiss the mature-content warning popup, if any
        try:
            btn = page.locator(
                "button:has-text('Continue'), button:has-text('Yes')"
            ).first
            if await btn.is_visible(timeout=3000):
                await btn.click()
                await page.wait_for_timeout(2000)
        except Exception:
            pass

        print("[2/3] Scrolling to load the full chapter...")
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
# 2. Split the text + generate audio
# ----------------------------------------------------------------------------
def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split at paragraph / sentence boundaries to avoid cutting mid-sentence."""
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
    """Generate one MP3 chunk, retrying on network/service errors."""
    for attempt in range(1, retries + 1):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(path)
            if os.path.getsize(path) == 0:
                raise RuntimeError("Generated MP3 is empty")
            return
        except Exception as exc:
            if os.path.exists(path):
                os.remove(path)
            if attempt == retries:
                raise RuntimeError(f"Audio generation failed after {retries} attempts: {exc}")
            delay = 2 ** attempt
            print(f"      ⚠️ Attempt {attempt}/{retries} failed: {exc}. Retrying in {delay}s...")
            await asyncio.sleep(delay)


async def text_to_speech(text: str, output_path: str, voice: str, rate: str):
    """Generate audio chunk by chunk, then merge into ONE MP3 file (no FFmpeg needed)."""
    chunks = split_text(text)
    if not chunks:
        raise ValueError("There is no text to read.")

    print(f"   - Chunks to process: {len(chunks)}")

    # Temporary chunks live in a temp folder that is deleted automatically
    with tempfile.TemporaryDirectory() as tmp_dir, open(output_path, "wb") as out:
        for i, chunk in enumerate(chunks, start=1):
            print(f"   [{i}/{len(chunks)}] Generating audio ({len(chunk)} characters)...")
            part_path = os.path.join(tmp_dir, f"{i:03d}.mp3")
            await synthesize_chunk(chunk, part_path, voice, rate)

            # edge-tts MP3 chunks share the same format, so they can be concatenated directly
            with open(part_path, "rb") as part:
                out.write(part.read())


# ----------------------------------------------------------------------------
# 3. Main
# ----------------------------------------------------------------------------
async def main():
    parser = argparse.ArgumentParser(description="Convert a Wattpad chapter into a single MP3 file")
    parser.add_argument("url", nargs="?", help="Wattpad chapter URL")
    parser.add_argument(
        "--voice",
        default="female",
        help="female (default), male, uk-female, uk-male, or any full edge-tts voice name",
    )
    parser.add_argument("--rate", default="+0%", help="Speech rate, e.g. +10%% or -10%%")
    args = parser.parse_args()

    url = args.url or input("Paste the Wattpad chapter link: ").strip()
    if not url:
        print("Invalid link!")
        return

    data = await scrape_wattpad_chapter(url)
    if not data or not data.get("content"):
        print("❌ Could not extract the chapter. Please check the URL!")
        return

    title = data["title"]
    content = f"{title}\n\n{data['content']}"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = re.sub(r'[<>:"/\\|?*\n\r\t]', "_", title).strip()[:80]
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name or 'audiobook'}.mp3")

    voice = VOICES.get(args.voice, args.voice)
    print(f"\n✅ Extracted: {title} ({len(content):,} characters)")
    print(f"[3/3] Generating MP3 with voice {voice}...")

    await text_to_speech(content, output_path, voice, args.rate)
    print(f"\n🎉 Done! Saved to:\n👉 {os.path.abspath(output_path)}")


if __name__ == "__main__":
    asyncio.run(main())