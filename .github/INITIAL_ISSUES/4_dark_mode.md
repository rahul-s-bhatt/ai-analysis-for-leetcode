[FEATURE] Add Dark Mode Support

## Feature Description
Implement a dark mode theme option to improve accessibility and user experience during night-time usage.

## Problem Statement
The application currently only supports a light theme, which can be straining on the eyes in low-light conditions. We need to add dark mode support to make the application more comfortable to use in different lighting conditions.

## Proposed Solution
1. Implement CSS variables for color theming
2. Add a theme toggle button
3. Persist user's theme preference

## Technical Details
Example implementation structure:

1. **CSS Variables**
```css
/* Light theme (default) */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #dee2e6;
    --accent-color: #007bff;
}

/* Dark theme */
[data-theme="dark"] {
    --bg-primary: #212529;
    --bg-secondary: #343a40;
    --text-primary: #f8f9fa;
    --text-secondary: #ced4da;
    --border-color: #495057;
    --accent-color: #3d8bfd;
}
```

2. **Theme Toggle Implementation**
```javascript
// Theme toggle functionality
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Theme initialization
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}
```

### Required Skills
- [x] HTML
- [x] CSS
- [x] Basic JavaScript
- [ ] Other: _____

### Difficulty Level
- [x] Beginner Friendly
- [ ] Intermediate
- [ ] Advanced

### Estimated Time
- [ ] Small (< 2 hours)
- [x] Medium (2-4 hours)
- [ ] Large (4-8 hours)
- [ ] Extra Large (> 8 hours)

## Implementation Checklist
- [ ] Define CSS variables for both themes
- [ ] Add data-theme attribute handling
- [ ] Create theme toggle button UI
- [ ] Implement theme toggle functionality
- [ ] Add local storage for theme persistence
- [ ] Test in different browsers
- [ ] Update documentation

## Getting Started
1. Locate the main CSS file in `api/templates/` directory
2. Add CSS variables for both themes
3. Create a theme toggle button in the navigation bar
4. Implement the JavaScript functions for theme switching
5. Test the implementation in different browsers

## Additional Context
- Consider using CSS variables for easy theme switching
- Ensure sufficient color contrast for accessibility
- Test with screen readers
- Consider adding a system theme detection option

This is a great first issue for beginners to learn about:
- CSS custom properties (variables)
- DOM manipulation
- Local Storage
- Media queries
- Accessibility considerations

Labels: good first issue, enhancement, frontend, accessibility
