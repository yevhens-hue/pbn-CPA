---
name: code-review
description: Review code for quality, security, and best practices. Provides structured feedback and a quality score. Use when reviewing pull requests, code changes, or when the user asks for a code review.
---
# Code Review

## Instructions

When performing a code review, analyze the changes for the following:

### 1. Correctness & Logic
- Does the code do what it's supposed to do?
- Are there any potential bugs, edge cases, or race conditions?
- Is the error handling comprehensive and robust?

### 2. Security
- Check for hardcoded secrets, API keys, or passwords.
- Look for common vulnerabilities: SQL injection, XSS, Path Traversal, etc.
- Verify that authentication and authorization are correctly implemented.

### 3. Maintainability & Style
- Is the code readable and easy to understand?
- Does it follow the project's style conventions?
- Are functions and classes appropriately sized and focused?
- Is there any unnecessary complexity that could be simplified?

### 4. Performance
- Are there any obvious performance bottlenecks?
- Is resource usage (CPU, memory, database connections) optimized?

## Structured Feedback Template

Provide your feedback using the following structure:

### Summary
[Brief overview of the changes and overall quality]

### Quality Score: [0-100]
- **0-40**: Significant issues, major rework required.
- **41-70**: Functional but lacks polish or has minor issues.
- **71-90**: High quality, minor suggestions only.
- **91-100**: Exceptional code, production-ready.

### Feedback Categories
- 🔴 **Critical**: Must fix before merge.
- 🟡 **Suggestion**: Improvement for readability or performance.
- 🟢 **Nice to have**: Minor polish or future consideration.

### Detailed Findings
- [List specific findings with file names and line numbers]
