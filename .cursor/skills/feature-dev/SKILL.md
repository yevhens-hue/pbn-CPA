---
name: feature-dev
description: Structures the development of new features into 4 phases: Requirements, Design, Implementation, and Testing. Use when the user asks to "build a new feature" or "add a new functionality".
---
# Feature Development Workflow

This skill provides a structured approach to building new features, ensuring completeness and quality at every step.

## Instructions

Follow these four phases for every new feature request:

### Phase 1: Requirements Gathering
- **Goal**: Understand exactly WHAT the user needs.
- **Action**: Ask clarifying questions about edge cases, user roles, and success criteria.
- **Artifact**: Update `task.md` with the feature breakdown.

### Phase 2: Technical Design
- **Goal**: Decide HOW to build it before writing code.
- **Action**: Create or update the `implementation_plan.md`.
- **Considerations**: Architecture, database changes, security, and performance.

### Phase 3: Implementation
- **Goal**: Write the code.
- **Action**: Perform the changes in iterative steps.
- **Standard**: Follow `code-review` practices throughout implementation.

### Phase 4: Verification & Testing
- **Goal**: Ensure it works as intended.
- **Action**: Perform automated tests and manual walkthroughs.
- **Artifact**: Create or update `walkthrough.md` with results and recordings.

## Feedback Loop

If during Implementation you discover a design flaw, return to Phase 2 (Technical Design) to refine the approach before proceeding. Always keep the user informed of significant changes to the plan.
