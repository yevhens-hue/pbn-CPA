---
name: web-automation
description: Leverage the browser subagent for E2E testing, web scraping, and browser-based workflows. Use when the user asks to "test the website", "scrape data", or "verify UI in browser".
---
# Web Automation & E2E Testing

This skill allows the agent to interact with live web pages to verify functionality and design.

## Instructions

When performing web automation tasks, use the `browser_subagent` tool with clear, actionable tasks.

### 1. E2E Testing Workflow
- **Navigate**: Open the target URL.
- **Interact**: Use `click`, `type`, and `select` to simulate user actions (e.g., login, form submission).
- **Verify**: Check for specific elements, text, or visual states to confirm success.
- **Capture**: Always take a screenshot or recording of critical steps or failures for the `walkthrough.md`.

### 2. UI Verification
- Compare the rendered page against the requirements in `frontend-design`.
- Check for responsive behavior by resizing the browser window.
- Verify that micro-animations and hover effects are functional.

### 3. Data Extraction
- Use `read_browser_page` to extract clean markdown/text from pages.
- Handle dynamic content (SPA) by waiting for specific selectors to appear.

## Browser Task Guidelines
- Be specific about what to do and when to stop.
- Define a clear "Success Condition" for the subagent.
- Require the subagent to return a detailed report of its actions.

## Example Browser Task
"Navigate to https://example.com/login, fill in the username 'testuser' and password 'password', and click 'Submit'. Stop once the dashboard header 'Welcome, testuser' is visible. Return a screenshot of the dashboard."
