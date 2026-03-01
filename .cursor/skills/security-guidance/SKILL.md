---
name: security-guidance
description: Scan for common security vulnerabilities like hardcoded secrets, auth bypass patterns, and injection risks. Use when reviewing code, deploying updates, or when the user asks for a security check.
---
# Security Guidance & Scanning

This skill protects the codebase from common security threats and vulnerabilities.

## Instructions

When the user asks for a security check, or as part of a `code-review`, focus on:

### 1. Secret Detection
- **Action**: Scan for hardcoded API keys, database credentials, passwords, or tokens.
- **Pattern**: Look for variables named `API_KEY`, `PASSWORD`, `SECRET`, `AUTH_TOKEN`, etc.
- **Remediation**: Instruct the user to move secrets to an `.env` file and add it to `.gitignore`.

### 2. Injection Risks
- **SQL Injection**: Ensure all database queries use parameterized statements or ORMs.
- **XSS (Cross-Site Scripting)**: Verify that all user-supplied data is properly sanitized and encoded before being rendered in HTML.
- **Command Injection**: Check for unsafe execution of shell commands using user input.

### 3. Dependency Vulnerabilities
- Scan `package.json`, `requirements.txt`, or other dependency files for known vulnerable versions.
- Recommend updates or patches for critical security issues.

### 4. Authentication & Authorization
- **Broken Auth**: Look for weak password policies, lack of MFA, or insecure session handling.
- **Insecure Direct Object References (IDOR)**: Ensure that users can only access data they are authorized to see.

## Security Report Structure
For every scan, provide a prioritized report:
- 🔴 **High**: Immediate risk (e.g., exposed DB credentials).
- 🟡 **Medium**: Potential vulnerability (e.g., missing XSS sanitation).
- 🔵 **Low**: Best practice improvement (e.g., set secure cookie flags).
