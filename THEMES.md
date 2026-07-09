# 🎨 Sea Battle Game - Color Palettes

## Overview
Added selectable color palettes to the Sea Battle game using CSS custom properties (variables) and localStorage persistence.

## Palettes

### 1. 🌊 Ocean (Default)
- **Primary Accent:** `#4fc3f7` (Cyan)
- **Background:** `#0a1628` (Dark Blue)
- **Board Background:** `#0d1f3c` (Navy)
- **Border Color:** `#1a3a5c` (Blue-Gray)
- **Ship Color:** `#2e7d32` (Green)
- **Hit Color:** `#c62828` (Red)
- **Warning Color:** `#ffd54f` (Yellow)
- **Theme Name:** `ocean`

### 2. 🌲 Forest
- **Primary Accent:** `#00d084` (Bright Green)
- **Background:** `#0d1117` (Very Dark)
- **Board Background:** `#1a1a2e` (Dark Navy)
- **Border Color:** `#0f3460` (Dark Teal)
- **Ship Color:** `#2d5a3d` (Forest Green)
- **Hit Color:** `#ff4757` (Coral Red)
- **Warning Color:** `#ffa502` (Orange)
- **Theme Name:** `forest`


## Implementation Details

### CSS Variables
All colors are defined as CSS custom properties under `body.palette-{name}` selectors:
- 20+ color variables per palette
- Smooth 0.3s transition between themes
- Automatically applied to all UI elements

### JavaScript Functions
1. `setTheme(themeName)` - Switch to a specific palette
2. `initTheme()` - Load saved theme or default to 'ocean'

### Storage
- Theme preference saved to `localStorage` with key `sb_theme`
- Persists across browser sessions
- Defaults to 'ocean' if not set

### UI
- **Theme Selector:** Located in the main menu
- **Buttons:** 🌊 Ocean, 🌲 Forest
- **Active State:** Selected theme button highlighted
- **Position:** Below the game board, above action buttons

## How to Use

### For Players
1. Go to the main menu
2. Click the theme button (🌊 / 🌲)
3. Your choice is automatically saved
4. Theme applies immediately with smooth transition

### For Developers
Add a new theme by:
1. Define new CSS variables in `body.palette-{name} :root { ... }`
2. Add a button in the theme selector HTML
3. Add theme name to `validThemes` array in `setTheme()` function

## Colors Used

### CSS Variables Structure
```
--bg-dark              # Main background
--bg-board             # Game board background
--bg-board-alt         # Alternative board color
--border-color         # Borders and dividers
--accent-primary       # Main accent color
--accent-primary-light # Light accent
--accent-primary-alt   # Alternative accent
--text-muted           # Muted text
--text-secondary       # Secondary text
--text-tertiary        # Tertiary text
--text-hint            # Hint text
--color-ship           # Ship cells
--color-hit            # Hit cells
--color-sunk-dark      # Sunk ship color
--color-btn-primary-1  # Button gradient start
--color-btn-primary-2  # Button gradient end
--color-btn-success-1  # Success button start
--color-btn-success-2  # Success button end
--color-btn-outline-border # Outline button border
--color-warning        # Warning color
--color-header-grad-1  # Header gradient start
--color-header-grad-2  # Header gradient end
```

## Features

✅ Smooth theme transitions (0.3s CSS animations)
✅ Persistent storage using localStorage
✅ Three pre-designed palettes
✅ Easy to add more themes
✅ Works with all game components (boards, buttons, modals, etc.)
✅ Maintains contrast and readability across all themes
✅ Mobile-friendly theme selector

## Browser Compatibility

- CSS Variables (Custom Properties) supported in all modern browsers
- localStorage supported in all modern browsers
- Fallback: Defaults to Ocean palette if localStorage unavailable
