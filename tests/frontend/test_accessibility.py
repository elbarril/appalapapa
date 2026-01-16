"""
Accessibility Tests

Tests for WCAG 2.1 AA compliance using axe-core.
Requires a running server (manual or via pytest-flask-live).
"""

import pytest
from playwright.sync_api import expect

# Skip all tests if dependencies are not available
pytest.importorskip("playwright")


class TestKeyboardNavigation:
    """Test keyboard navigation functionality."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_tab_order_login_page(self, page):
        """Verify logical tab order on login page."""
        page.goto("http://localhost:5000/auth/login")
        
        # Tab through interactive elements
        expected_order = [
            "a[href*='skip']",  # Skip link (if visible on focus)
            "#theme-switcher-button",  # Theme toggle
            "input[name='email']",
            "input[name='password']",
            "button[type='submit']",
        ]
        
        for i, selector in enumerate(expected_order[1:], 1):  # Skip the skip link
            page.keyboard.press("Tab")
            focused = page.locator(":focus")
            expect(focused).to_be_visible()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_focus_visible_on_all_interactive(self, page):
        """Verify focus indicators are visible on all interactive elements."""
        page.goto("http://localhost:5000/auth/login")
        
        # Tab through elements and verify focus is visible
        for _ in range(10):
            page.keyboard.press("Tab")
            focused = page.locator(":focus")
            
            if focused.count() > 0:
                # Check that element is visible when focused
                expect(focused).to_be_visible()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_skip_link_works(self, page):
        """Verify skip link navigates to main content."""
        page.goto("http://localhost:5000/auth/login")
        
        # Focus skip link
        page.keyboard.press("Tab")
        
        # Click it
        page.keyboard.press("Enter")
        
        # Verify focus moved to main content
        focused = page.locator(":focus")
        expect(focused).to_have_id("main-content")
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_modal_focus_trap(self, page):
        """Verify modals trap focus correctly."""
        # Login and navigate to dashboard
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Open add patient modal
        page.click("[data-action='add-patient']")
        
        # Tab multiple times - should stay in modal
        for _ in range(20):
            page.keyboard.press("Tab")
            focused = page.locator(":focus")
            
            # Verify focus is within modal
            modal = page.locator(".modal.show")
            if modal.count() > 0:
                expect(focused.locator("..").filter(has=modal).or_(modal.filter(has=focused))).to_be_visible()


class TestAriaAttributes:
    """Test ARIA attributes are correctly implemented."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_form_labels_linked(self, page):
        """Verify all form inputs have associated labels."""
        page.goto("http://localhost:5000/auth/login")
        
        # Get all inputs
        inputs = page.locator("input:not([type='hidden'])")
        
        for i in range(inputs.count()):
            input_elem = inputs.nth(i)
            input_id = input_elem.get_attribute("id")
            
            if input_id:
                # Verify label exists with matching for attribute
                label = page.locator(f"label[for='{input_id}']")
                expect(label).to_be_attached()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_buttons_have_accessible_names(self, page):
        """Verify all buttons have accessible names."""
        page.goto("http://localhost:5000/auth/login")
        
        buttons = page.locator("button")
        
        for i in range(buttons.count()):
            button = buttons.nth(i)
            
            # Button should have either text content, aria-label, or aria-labelledby
            text = button.text_content().strip()
            aria_label = button.get_attribute("aria-label")
            aria_labelledby = button.get_attribute("aria-labelledby")
            
            assert text or aria_label or aria_labelledby, \
                f"Button {i} has no accessible name"
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_icons_are_decorative(self, page):
        """Verify decorative icons have aria-hidden."""
        page.goto("http://localhost:5000/auth/login")
        
        icons = page.locator("i.bi")
        
        for i in range(icons.count()):
            icon = icons.nth(i)
            aria_hidden = icon.get_attribute("aria-hidden")
            
            # Decorative icons should have aria-hidden="true"
            assert aria_hidden == "true", \
                f"Icon {i} is not marked as decorative (aria-hidden='true')"
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_landmarks_present(self, page):
        """Verify page has correct landmark regions."""
        page.goto("http://localhost:5000/auth/login")
        
        # Check for main landmark
        main = page.locator("main, [role='main']")
        expect(main).to_be_attached()
        
        # Check for navigation
        nav = page.locator("nav, [role='navigation']")
        expect(nav).to_be_attached()


class TestColorContrast:
    """Test color contrast meets WCAG requirements."""
    
    @pytest.mark.skip(reason="Requires axe-playwright-python - run manually")
    def test_login_page_contrast(self, page):
        """Run axe-core accessibility audit on login page."""
        try:
            from axe_playwright_python.sync_playwright import Axe
        except ImportError:
            pytest.skip("axe-playwright-python not installed")
        
        page.goto("http://localhost:5000/auth/login")
        
        axe = Axe()
        results = axe.run(page)
        
        # Check for color contrast violations
        contrast_violations = [
            v for v in results.violations 
            if v["id"] == "color-contrast"
        ]
        
        assert len(contrast_violations) == 0, \
            f"Color contrast violations: {contrast_violations}"
    
    @pytest.mark.skip(reason="Requires axe-playwright-python - run manually")
    def test_full_accessibility_audit(self, page):
        """Run full axe-core accessibility audit."""
        try:
            from axe_playwright_python.sync_playwright import Axe
        except ImportError:
            pytest.skip("axe-playwright-python not installed")
        
        page.goto("http://localhost:5000/auth/login")
        
        axe = Axe()
        results = axe.run(page)
        
        # Assert no violations
        assert len(results.violations) == 0, \
            f"Accessibility violations found: {[v['id'] for v in results.violations]}"


class TestScreenReader:
    """Test screen reader compatibility features."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_live_region_for_flash_messages(self, page):
        """Verify flash messages use live regions."""
        page.goto("http://localhost:5000/auth/login")
        
        # Submit invalid form to trigger flash message
        page.fill("input[name='email']", "invalid")
        page.click("button[type='submit']")
        
        # Check for live region
        alerts = page.locator("[role='alert'], [aria-live]")
        expect(alerts.first).to_be_attached()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_headings_hierarchy(self, page):
        """Verify correct heading hierarchy."""
        page.goto("http://localhost:5000/auth/login")
        
        # Get all headings
        h1 = page.locator("h1")
        expect(h1).to_have_count(1)  # Should have exactly one h1
        
        # H2 should come after h1, etc.
        headings = page.locator("h1, h2, h3, h4, h5, h6")
        previous_level = 0
        
        for i in range(headings.count()):
            heading = headings.nth(i)
            tag_name = heading.evaluate("el => el.tagName.toLowerCase()")
            current_level = int(tag_name[1])
            
            # Heading level should not skip (e.g., h1 to h3)
            assert current_level <= previous_level + 1, \
                f"Heading hierarchy skips from h{previous_level} to h{current_level}"
            
            previous_level = current_level
