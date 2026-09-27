import json
import os
import re
import time
from pathlib import Path

import yaml
from google import genai
from google.genai.errors import ServerError
from pydantic import ValidationError

from schema import Episode


ROOT = Path(__file__).resolve().parents[2]
MODEL_ID = "gemini-3.8-flash"
CHARACTER_ANCHORS = (
    "Fındık: a small reddish-brown squirrel with a big bushy tail, round friendly eyes, "
    "warm knit vest, expressive eyebrows. "
    "Kestane: a round brown hedgehog with soft rounded spines, gentle warm smile, "
    "carries a small woven basket."
)


def read_project_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_pilot_episode(markdown: str, title: str) -> str:
    pattern = rf"##\s*1\.\s*{re.escape(title)}\s*(.*?)(?=\n##\s*2\.|\Z)"
    match = re.search(pattern, markdown, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find pilot episode section for title: {title}")
    return match.group(1).strip()


def load_character_names() -> list[str]:
    config_path = ROOT / "config" / "characters.yaml"
    with config_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    characters = data.get("characters", [])
    return [item.get("name", "") for item in characters if item.get("name")]


def build_prompt(project_bible: str, world_bible: str, characters_yaml: str, pilot_section: str) -> str:
    character_names = load_character_names()
    prompt = f"""
You are writing a single original 90-second children's episode for Fındıkdere Mahallesi.

CORE FACTS:
- Target age: 5-8. Warm, playful, positive story with humor, friendship, nature, and gentle problem-solving.
- Visual style: 2.5D storybook, warm earth tones, golden-hour light, soft paper/s watercolor texture, no neon or over-photorealism.
- Fixed world: Fındıkdere Mahallesi with homes, park, school, forest, lake, and the neighborhood as the main setting.
- Only use established characters and locations from this world; do not invent new named characters or core locations.
- The story must be original and not based on folklore or any existing book.
- The key episode pattern is: Olay / Mesaj / Komik sahne. For this episode, Fındık loses the acorn he stored for winter, cannot find it, and the comedy comes from him accidentally falling into the wrong burrow / neighboring underground space while searching.

PROJECT_BIBLE_SUMMARY:
{project_bible[:1200]}

WORLD_BIBLE_SUMMARY:
{world_bible[:800]}

CHARACTERS_ALLOWED:
{', '.join(character_names)}

PILOT_EPISODE_1:
{pilot_section}

MANDATORY RULES:
1. Write exactly one Episode JSON object.
2. Use characters only from the allowed list. Primary duo: Fındık and Kestane.
3. Scenes: 5-6 scenes, each about 15 seconds, total around 90 seconds.
4. Keep all text in English except names and the episode title.
5. Simple dialogue for ages 5-8, warm and readable.
6. Include visual_prompt and video_prompt for every scene so it fits the 2.5D storybook style.
7. For every scene whose characters list contains Fındık and/or Kestane, the visual_prompt field must end with this exact string appended verbatim, with no paraphrase and no shortening: {CHARACTER_ANCHORS}
8. Write youtube_metadata.title, youtube_metadata.description, and youtube_metadata.tags in English, matching the dialogue language and target audience.
9. Fill copyright_check exactly as:
   - inspiration_type: "original"
   - skeleton_only: true
   - flagged_for_review: false
   - notes: "Original story built from the established Fındıkdere Mahallesi universe; no folklore or existing book plot used."
10. Return ONLY valid JSON, no Markdown, no extra commentary.

SCHEMA:
{{
  "episode_id": "ep001",
  "title": "",
  "logline": "",
  "target_age": "5-8",
  "characters": ["Fındık", "Kestane"],
  "copyright_check": {{
    "inspiration_type": "original",
    "skeleton_only": true,
    "flagged_for_review": false,
    "notes": "Original story built from the established Fındıkdere Mahallesi universe; no folklore or existing book plot used."
  }},
  "scenes": [
    {{
      "scene_id": "s1",
      "duration_seconds": 15,
      "location": "Fındıkdere Mahallesi",
      "characters": ["Fındık", "Kestane"],
      "action": "",
      "dialogue": [{{"character": "Fındık", "line": ""}}],
      "narration": "",
      "visual_prompt": "",
      "video_prompt": "",
      "audio_notes": "",
      "status": "PENDING"
    }}
  ],
  "status": "DRAFT_PENDING_REVIEW",
  "estimated_cost_usd": 0.0,
  "quality_score": null,
  "youtube_metadata": {{
    "title": "",
    "description": "",
    "tags": []
  }}
}}
""".strip()
    return prompt


def extract_json_from_text(raw_text: str) -> dict:
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```\s*$", "", text, flags=re.IGNORECASE)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
    return json.loads(text)


def main() -> None:
    project_bible = read_project_text(ROOT / "docs" / "project_bible.md")
    world_bible = read_project_text(ROOT / "docs" / "world_bible.md")
    characters_yaml = read_project_text(ROOT / "config" / "characters.yaml")
    pilot_markdown = read_project_text(ROOT / "projects" / "episodes" / "season1_pilot.md")
    pilot_section = extract_pilot_episode(pilot_markdown, "Fındık'ın Kayıp Fıstığı")

    prompt = build_prompt(project_bible, world_bible, characters_yaml, pilot_section)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Missing GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=api_key)

    last_error = None
    for attempt in range(4):
        try:
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            break
        except ServerError as exc:
            last_error = exc
            if getattr(exc, "code", None) == 503 and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise
    else:
        raise last_error

    raw_text = getattr(response, "text", str(response))
    try:
        payload = extract_json_from_text(raw_text)
        episode = Episode.model_validate(payload)
    except (json.JSONDecodeError, ValidationError, ValueError) as exc:
        print("Raw Gemini response:")
        print(raw_text)
        print("\nValidation error:")
        print(exc)
        raise SystemExit(1) from exc

    output_path = ROOT / "projects" / "episodes" / "ep001_findik_kayip_fistik.yaml"
    output_data = episode.model_dump(mode="json")
    output_path.write_text(
        yaml.safe_dump(output_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    total_duration = sum(scene.duration_seconds for scene in episode.scenes)
    print(
        f"Episode: {episode.title} | Scenes: {len(episode.scenes)} | "
        f"Total duration: {total_duration}s | Copyright: {episode.copyright_check['inspiration_type']}"
    )


if __name__ == "__main__":
    main()
