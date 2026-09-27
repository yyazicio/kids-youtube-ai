# Architecture Decisions Log

## Initial project scaffold
- Decision: Initial project scaffold created per project bible v1.
- Alternatives considered: none yet (first decision).
- Reason: establish clean structure before writing pipeline code.
- Cost: $0.
- Date: 2026-09-27.
- Reversible: Yes.

## Portable FFmpeg and stable project location
- Decision: Moved project from Copilot chat-cache path to C:\Personal_Projects\kids-youtube-ai; added portable FFmpeg under tools/ffmpeg/ instead of system install (avoids admin rights / install restrictions).
- Alternatives considered: system-wide FFmpeg install (rejected — requires admin rights not available on this machine).
- Reason: stable project location; FFmpeg needed for video assembly stage without violating no-install policy.
- Cost: $0.
- Date: 2026-09-27.
- Reversible: Yes.

## Dedicated Conda environment
- Decision: Use a dedicated conda environment (kidsyoutube-ai, Python 3.11 or as available) instead of a venv on system Python 3.14, since Anaconda was already installed on this machine and offers a more stable/compatible Python version.
- Alternatives considered: venv on system Python 3.14 (rejected — newer Python version risks missing prebuilt wheels for some packages later, e.g. moviepy/audio libs).
- Reason: avoid dependency install failures down the line; use already-permitted software instead of anything new.
- Cost: $0.
- Date: 2026-09-27.
- Reversible: Yes.
- Implementation status: Environment provisioning is blocked by Conda's SSL certificate and configured-proxy failures; no project environment or dependencies have been installed yet.

## Codespaces migration
- Decision: Moved project execution from local Windows machine to GitHub Codespaces, using a standard .venv instead of conda, and apt-installed FFmpeg instead of a portable Windows binary.
- Alternatives considered: fixing local corporate proxy/SSL trust for pip and conda (rejected — required inspecting/modifying system security configuration outside the scope of a personal project on a company machine).
- Reason: Codespaces provides unrestricted internet access and a clean Linux environment with no corporate network interference.
- Cost: $0 (within GitHub Codespaces free monthly quota — 120 core-hours/month on personal accounts).
- Date: 2026-09-27.
- Reversible: Yes.

## Original style-inspired content model
- Decision: Adopted "style-inspired, fully original" content model — analyze general stylistic tendencies of established Turkish children's authors (kept as an internal-only reference, never public-facing) without copying any specific plot/character/text; created 10 original characters in a shared universe (Fındıkdere Mahallesi) and 12 pilot episode concepts.
- Alternatives considered: adapting existing Turkish children's books directly (rejected — copyright risk under Turkish Law No. 5846, life+70 years protection); pure public-domain folklore only (kept as a secondary option, not primary).
- Reason: legally clean path that still captures the tone/warmth/humor the user wanted, with full creative control and no licensing dependency.
- Cost: $0.
- Date: 2026-09-27.
- Reversible: Yes.
