import json
import os
import re
import struct
import sys
from io import BytesIO
from pathlib import Path

from google import genai

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "assets" / "characters"

CHARACTER_ANCHORS = (
    "Fındık: a small reddish-brown squirrel with a big bushy tail, round friendly eyes, "
    "warm knit vest, expressive eyebrows. "
    "Kestane: a round brown hedgehog with soft rounded spines, gentle warm smile, "
    "carries a small woven basket."
)

CHARACTERS = {
    "Fındık": "findik_reference.png",
    "Kestane": "kestane_reference.png",
}


def ensure_assets_dir() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)


def parse_png_dimensions(data: bytes) -> tuple[int | None, int | None]:
    if data.startswith(b"\x89PNG"):
        if len(data) >= 24:
            width, height = struct.unpack(">II", data[8:16])
            return int(width), int(height)
    return None, None


def read_image_dimensions(data: bytes) -> tuple[int | None, int | None]:
    if Image is not None:
        try:
            with Image.open(BytesIO(data)) as image:
                return image.size
        except Exception:
            pass
    return parse_png_dimensions(data)


def build_prompt(character_name: str) -> str:
    return (
        f"{CHARACTER_ANCHORS} "
        f"{character_name}: Full body reference image, neutral standing pose, plain light-colored background, "
        "2.5D storybook illustration style, warm color palette"
    )


def extract_image_part(response):
    for candidate in response.candidates or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "mime_type", "").startswith("image/"):
                return inline_data
    return None


def print_usage_metadata(response) -> None:
    usage = getattr(response, "usage_metadata", None)
    if usage is None:
        print("Usage metadata: unavailable")
        return
    payload = {}
    if hasattr(usage, "model_dump"):
        payload = usage.model_dump(mode="json")
    else:
        payload = dict(usage)
    print("Usage metadata:", json.dumps(payload, ensure_ascii=False, default=str))


def main() -> None:
    ensure_assets_dir()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Missing GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=api_key)
    for character_name, filename in CHARACTERS.items():
        prompt = build_prompt(character_name)
        print(f"Generating reference image for {character_name}...")
        response = client.models.generate_content(
            model="gemini-3.1-flash-image",
            contents=prompt,
            config={"response_modalities": ["TEXT", "IMAGE"]},
        )

        image_blob = extract_image_part(response)
        if image_blob is None:
            print("No image returned from API response.")
            print("Response:", response)
            print_usage_metadata(response)
            raise SystemExit(f"Image generation failed for {character_name}")

        output_path = ASSET_DIR / filename
        output_path.write_bytes(image_blob.data)

        width, height = read_image_dimensions(image_blob.data)
        print(f"character name: {character_name}")
        print(f"file path saved: {output_path}")
        print(f"image dimensions: {width}x{height}")
        print_usage_metadata(response)
        print()


if __name__ == "__main__":
    main()
