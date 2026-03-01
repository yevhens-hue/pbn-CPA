---
name: frontend-design
description: Provide UI/UX design patterns and guidance focused on modern, premium aesthetics. Use when building frontend components, designing layouts, or improving the visual look of the application.
---
# Frontend Design & UX

This skill ensures that all UI development meets high aesthetic and usability standards.

## Instructions

When designing or building frontend components, apply these principles:

### 1. Typography
- **Primary Font**: Use `Inter`, `Roboto`, or `Outfit`. Prefer `Inter` for its balance of readability and modern feel.
- **Hierarchy**: Use clear weight and size distinctions (e.g., Bold H1, Medium Body, Regular Captions).
- **Leading & Kerning**: Keep letter-spacing tight for headers and line-height comfortable (1.5-1.6) for body text.

### 2. Modern Aesthetics (Next.js Look)
- **Glassmorphism**: Use `backdrop-filter: blur(10px)` with semi-transparent backgrounds and subtle borders.
- **Gradients**: Use smooth, curated gradients (e.g., dark blue to deep purple) rather than flat colors.
- **Card-based Layouts**: Group related information in clean, shadowed cards with rounded corners (12px to 20px).

### 3. Micro-animations
- **Hover Effects**: Add subtle scale (1.02) or color transitions to interactive elements.
- **Loading States**: Use skeleton loaders or smooth fade-ins instead of sudden appearances.

### 4. Accessibility
- Ensure contrast ratios meet WCAG standards.
- All interactive elements must have clear focus states.
- Use semantic HTML (e.g., `<button>` for actions, `<a>` for navigation).

## UI Component Checklist
- [ ] Responsive across all screen sizes (Mobile-first).
- [ ] Consistent color palette.
- [ ] No layout shifts during load.
- [ ] Intuitive navigation paths.
