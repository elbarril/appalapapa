# Skill: Screen Reader Testing

## Overview

This skill covers screen reader testing methodologies for the Therapy Session Management Application. Testing with actual screen readers is essential for ensuring accessibility.

---

## Screen Reader Options

### Primary Screen Readers

| Screen Reader | Platform | Cost | Testing Priority |
|---------------|----------|------|------------------|
| NVDA | Windows | Free | High |
| VoiceOver | macOS/iOS | Built-in | High |
| JAWS | Windows | Commercial | Medium |
| TalkBack | Android | Built-in | Medium |
| Narrator | Windows | Built-in | Low |

### Recommended Setup

1. **Windows**: NVDA (primary) + Chrome
2. **macOS**: VoiceOver (built-in) + Safari
3. **Mobile**: TalkBack (Android) or VoiceOver (iOS)

---

## NVDA Setup (Windows)

### Installation

1. Download from [nvaccess.org](https://www.nvaccess.org/download/)
2. Install with default settings
3. Enable "Speak typed characters" for testing

### Essential Keyboard Commands

| Command | Action |
|---------|--------|
| `Insert + Q` | Stop speaking |
| `Insert + Space` | Toggle focus/browse mode |
| `Insert + Down` | Read from cursor |
| `Insert + Tab` | Report current focus |
| `Tab` | Move to next focusable element |
| `Shift + Tab` | Move to previous focusable element |
| `H` | Next heading |
| `Shift + H` | Previous heading |
| `D` | Next landmark |
| `Shift + D` | Previous landmark |
| `K` | Next link |
| `F` | Next form field |
| `B` | Next button |
| `T` | Next table |

### NVDA Speech Viewer

Enable "Tools → Speech Viewer" to see what NVDA announces without audio.

---

## VoiceOver Setup (macOS)

### Enabling VoiceOver

- Press `Cmd + F5` to toggle on/off
- Or: System Preferences → Accessibility → VoiceOver

### Essential Keyboard Commands

| Command | Action |
|---------|--------|
| `VO` = `Ctrl + Option` | VoiceOver modifier key |
| `VO + A` | Read from cursor |
| `Ctrl` | Stop speaking |
| `VO + Right` | Move to next element |
| `VO + Left` | Move to previous element |
| `VO + Space` | Activate element |
| `VO + U` | Open rotor |
| `VO + Cmd + H` | Next heading |

### VoiceOver Rotor

Press `VO + U` to open rotor, then use arrow keys to navigate by:
- Headings
- Links
- Form Controls
- Landmarks
- Tables

---

## Testing Protocol

### 1. Pre-Testing Preparation

```markdown
## Test Environment Checklist
- [ ] Screen reader installed and updated
- [ ] Browser updated (Chrome or Firefox for NVDA, Safari for VoiceOver)
- [ ] Application running locally (http://localhost:5000)
- [ ] Test user logged in
- [ ] Speech viewer enabled (for recording)
```

### 2. Page Load Announcements

**Test:** Navigate to page and verify announcements.

```markdown
## Expected Announcements on Page Load

1. **Page Title**: "Panel de Pacientes - Terapia App"
2. **Main Landmark**: "main" region announced
3. **First Heading**: "Panel de Pacientes, heading level 1"

## Test Steps:
1. Open browser
2. Start screen reader
3. Navigate to http://localhost:5000/
4. Wait for page to load
5. Record announcements

## Pass Criteria:
- [ ] Page title announced
- [ ] Main content region found
- [ ] Heading structure logical
```

### 3. Navigation Structure Testing

**Test:** Verify landmark regions and heading hierarchy.

```markdown
## Landmark Region Test

Press 'D' repeatedly to cycle through landmarks:

Expected:
1. "banner" - Header/navbar
2. "navigation" - Main navigation
3. "main" - Main content
4. "contentinfo" - Footer (if present)

## Heading Hierarchy Test

Press 'H' repeatedly to cycle through headings:

Expected:
1. H1: "Panel de Pacientes"
2. H2: Patient names (e.g., "Juan García")
3. H3: Session sections (if applicable)

## Pass Criteria:
- [ ] All landmarks present
- [ ] Heading hierarchy logical (H1 → H2 → H3)
- [ ] No skipped heading levels
```

### 4. Form Testing

**Test:** Navigate and complete a form.

```markdown
## Login Form Test

Steps:
1. Navigate to login page
2. Press 'F' to jump to first form field
3. Verify label announced: "Email, edit text"
4. Type email address
5. Press Tab to password field
6. Verify label announced: "Contraseña, edit text, protected"
7. Type password
8. Press Tab to submit button
9. Verify button announced: "Iniciar sesión, button"
10. Press Enter to submit

## Pass Criteria:
- [ ] All form fields have labels announced
- [ ] Required fields indicated
- [ ] Error messages announced (test invalid submission)
- [ ] Success/error feedback announced
```

### 5. Interactive Element Testing

**Test:** Buttons, links, and controls.

```markdown
## Button Test

1. Navigate to buttons using 'B' key
2. Verify each button has accessible name
3. Press Enter/Space to activate
4. Verify action result announced

## Expected Button Announcements:
- "Editar, button" (not just icon)
- "Eliminar, button"
- "Agregar sesión, button"
- "Pagado, button" (payment toggle)

## Pass Criteria:
- [ ] All buttons have descriptive names
- [ ] Icons have aria-label or visually-hidden text
- [ ] Button state changes announced
```

### 6. Modal Testing

**Test:** Modal dialog accessibility.

```markdown
## Modal Dialog Test

Steps:
1. Activate button that opens modal
2. Verify "dialog" role announced
3. Verify modal title announced
4. Press Tab to cycle through focusable elements
5. Verify focus stays within modal
6. Press Escape to close
7. Verify focus returns to trigger button

## Pass Criteria:
- [ ] "Dialog" role announced
- [ ] Modal title announced (aria-labelledby)
- [ ] Focus trapped within modal
- [ ] Escape key closes modal
- [ ] Focus restored to trigger
```

### 7. Dynamic Content Testing

**Test:** Toast notifications and live regions.

```markdown
## Toast Notification Test

Steps:
1. Trigger an action that shows toast (e.g., save patient)
2. Verify toast message announced
3. Verify aria-live="polite" working

## Error Message Test

Steps:
1. Submit form with invalid data
2. Verify error announced immediately
3. Verify aria-live="assertive" for errors

## Pass Criteria:
- [ ] Success messages announced (polite)
- [ ] Error messages announced (assertive)
- [ ] Announcements happen automatically (no user action needed)
```

### 8. Carousel Testing

**Test:** Session carousel accessibility.

```markdown
## Carousel Test

Steps:
1. Navigate to patient card with sessions
2. Find carousel navigation controls
3. Verify controls announced with labels
4. Use arrow keys to navigate slides
5. Verify slide change announced

## Expected Announcements:
- "Sesiones de [Patient Name], carousel"
- "Sesión 1 de 3, [date]"
- "Previous slide, button"
- "Next slide, button"

## Pass Criteria:
- [ ] Carousel labeled with patient name
- [ ] Slide count announced
- [ ] Navigation controls accessible
- [ ] Slide changes announced via live region
```

---

## Common Issues and Fixes

### Issue: Button Without Accessible Name

**Screen Reader Announces:** "Button" (no description)

**Cause:** Icon-only button without aria-label

```html
<!-- ❌ Problem -->
<button><i class="bi bi-trash"></i></button>

<!-- ✅ Fix -->
<button aria-label="Eliminar paciente">
    <i class="bi bi-trash" aria-hidden="true"></i>
</button>
```

### Issue: Form Field Without Label

**Screen Reader Announces:** "Edit text" (no field name)

**Cause:** Missing label association

```html
<!-- ❌ Problem -->
<input type="text" placeholder="Nombre">

<!-- ✅ Fix -->
<label for="name">Nombre</label>
<input type="text" id="name" placeholder="Nombre">
```

### Issue: Dynamic Content Not Announced

**Screen Reader Announces:** Nothing when toast appears

**Cause:** Missing live region

```html
<!-- ❌ Problem -->
<div id="toast">Guardado</div>

<!-- ✅ Fix -->
<div id="toast" role="status" aria-live="polite">Guardado</div>
```

### Issue: Modal Focus Not Managed

**Screen Reader:** Can tab outside modal

**Cause:** Focus not trapped

```javascript
// ✅ Fix: Use Bootstrap's built-in focus trapping
const modal = document.getElementById('myModal');
modal.addEventListener('shown.bs.modal', () => {
    modal.querySelector('input, button')?.focus();
});
```

### Issue: Heading Hierarchy Broken

**Screen Reader Navigation:** H1 → H3 (skipped H2)

**Cause:** Improper heading structure

```html
<!-- ❌ Problem -->
<h1>Panel</h1>
<h3>Sesiones</h3>

<!-- ✅ Fix -->
<h1>Panel</h1>
<h2>Juan García</h2>
<h3>Sesiones</h3>
```

---

## Screen Reader Testing Checklist

### Before Release

```markdown
## Full Accessibility Test Checklist

### Page Structure
- [ ] Page title is descriptive
- [ ] Skip link works
- [ ] Landmarks present (banner, nav, main)
- [ ] Heading hierarchy correct

### Navigation
- [ ] All links have descriptive text
- [ ] Current page indicated in nav
- [ ] Keyboard-only navigation works

### Forms
- [ ] All fields have labels
- [ ] Required fields indicated
- [ ] Error messages announced
- [ ] Validation feedback accessible

### Interactive Components
- [ ] All buttons have names
- [ ] Modals are accessible
- [ ] Focus managed correctly
- [ ] State changes announced

### Dynamic Content
- [ ] Toasts announced
- [ ] Errors announced immediately
- [ ] Loading states communicated
- [ ] Content updates announced

### Media
- [ ] Images have alt text
- [ ] Decorative images hidden
- [ ] Icons have descriptions
```

---

## Recording Test Results

### Test Report Template

```markdown
# Screen Reader Test Report

**Date:** [Date]
**Tester:** [Name]
**Screen Reader:** NVDA 2024.1 / VoiceOver 15.0
**Browser:** Chrome 121 / Safari 17
**Page Tested:** [URL]

## Summary
- **Pass:** X tests
- **Fail:** Y tests
- **Warnings:** Z issues

## Detailed Results

### 1. Page Load
- Status: PASS/FAIL
- Notes: [Description]

### 2. Navigation
- Status: PASS/FAIL
- Notes: [Description]

### 3. Forms
- Status: PASS/FAIL
- Notes: [Description]

### 4. Modals
- Status: PASS/FAIL
- Notes: [Description]

### 5. Dynamic Content
- Status: PASS/FAIL
- Notes: [Description]

## Issues Found

| ID | Severity | Description | WCAG | Fix |
|----|----------|-------------|------|-----|
| 1 | High | Button missing label | 1.1.1 | Add aria-label |

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

---

## Resources

- [NVDA User Guide](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [VoiceOver Guide](https://support.apple.com/guide/voiceover/welcome/mac)
- [WebAIM Screen Reader Survey](https://webaim.org/projects/screenreadersurvey/)
- [Deque Screen Reader Testing Guide](https://dequeuniversity.com/screenreaders/)

---

*Last Updated: January 15, 2026*
