# Implementation Plan: Content Factory Integration (India Niche)

## Goal
Integrate the newly created Indian Gambling content plan (`data/content_plan_india.json`) into the main publishing bot (`core/publish_post.py`). The bot should prioritize topics from this plan when generating content.

## User Review Required
> [!IMPORTANT]
> This change will make the bot select topics from the pre-defined JSON list instead of only using the topics configured in `sites_data.json`. This ensures content relevance for the chosen niche.

## Proposed Changes

### Core Logic (`core/publish_post.py`)
- [x] **Add `load_content_plan` function**: Reads `data/content_plan_india.json`.
- [x] **Add `get_next_topic_from_plan` function**: Selects a random topic from the plan.
- [ ] **Modify `main` loop**:
    - Check if a site has a hardcoded topic.
    - If not, fetch a topic from the Content Plan.
    - Inject the specific "Keywords" and "Intent" from the plan into the prompt generation.

### Data
- [x] **`data/content_plan_india.json`**: Created with 20+ high-traffic game topics.

## Verification Plan

### Automated Tests
- Run `python3 core/publish_post.py --dry-run` (we need to implement a dry-run flag or just test with a dummy site).
- Verify that the log output shows a topic being picked from the JSON file.

### Manual Verification
1. Run the script locally.
2. Check the logs to see if it picked a topic like "Aviator Game Predictor" instead of a generic one.
3. Verify the generated HTML artifact to ensure it addresses the specific intent (e.g., "download" intent includes download buttons).
