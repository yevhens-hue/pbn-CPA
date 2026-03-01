---
name: code-simplifier
description: Identify and refactor overly complex code into simpler, more maintainable versions. Use when you encounter deeply nested conditions, long functions, or redundant logic.
---
# Code Simplifier

## Instructions

When the user asks to simplify code, or when you encounter complex logic during development, follow this process:

### 1. Identify Complexity
- **Deep Nesting**: More than 3 levels of indentation.
- **Long Functions**: Functions longer than 30-50 lines.
- **Redundant Logic**: Code that performs the same operation multiple times.
- **Complex Conditionals**: Logical expressions that are hard to parse mentally.

### 2. Refactoring Techniques
- **Guard Clauses**: Use early returns to eliminate `else` blocks and reduce nesting.
- **Extract Function**: Break large functions into smaller, descriptive sub-functions.
- **Simplify Expressions**: Use boolean identity and clear variable names to simplify logical checks.
- **Use Modern Language Features**: Leverage map/filter/reduce, destructuring, or other higher-level constructs where appropriate.

### 3. Verification
- Ensure that the refactored code retains the exact same functionality as the original (Unit Tests are highly recommended).
- Compare the before and after to demonstrate the improvement in readability.

## Example Refactorings

### Before (Nested):
```python
def process_data(data):
    if data:
        if 'items' in data:
            for item in data['items']:
                if item.get('active'):
                    # Do something
                    pass
```

### After (Simplified):
```python
def process_data(data):
    if not data or 'items' not in data:
        return
        
    for item in data['items']:
        if not item.get('active'):
            continue
        # Do something
```
