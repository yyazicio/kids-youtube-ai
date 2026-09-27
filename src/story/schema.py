from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Scene(BaseModel):
    scene_id: str
    duration_seconds: int
    location: str
    characters: list[str]
    action: str
    dialogue: list[dict[str, str]]
    narration: str
    visual_prompt: str
    video_prompt: str
    audio_notes: str
    status: str = "PENDING"


class Episode(BaseModel):
    episode_id: str
    title: str
    logline: str
    target_age: str
    characters: list[str]
    copyright_check: dict[str, Any]
    scenes: list[Scene]
    status: str = "DRAFT_PENDING_REVIEW"
    estimated_cost_usd: float = 0.0
    quality_score: str | None = None
    youtube_metadata: dict[str, Any] = Field(
        default_factory=lambda: {"title": "", "description": "", "tags": []}
    )
