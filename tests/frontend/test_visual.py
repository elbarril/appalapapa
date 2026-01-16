"""
Visual Regression Tests

Tests for visual appearance and theme switching.
Requires a running server (manual or via pytest-flask-live).
"""

import pytest
from playwright.sync_api import expect

# Skip all tests if Playwright is not available
pytest.importorskip("playwright")


class TestThemeSwitching:
    """Test theme switching functionality."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_default_theme_is_dark(self, page, screenshots_dir):
        """Verify default theme is dark mode."""
        page.goto("http://localhost:5000/auth/login")
        
        html = page.locator("html")
        expect(html).to_have_attribute("data-bs-theme", "dark")
        
        page.screenshot(path=f"{screenshots_dir}/login-dark.png")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_theme_toggle_to_light(self, page, screenshots_dir):
        """Verify theme can be switched to light mode."""
        page.goto("http://localhost:5000/auth/login")
        
        # Click theme toggle
        page.locator("#theme-switcher-button").click()
        
        # Verify theme changed
        html = page.locator("html")
        expect(html).to_have_attribute("data-bs-theme", "light")
        
        page.screenshot(path=f"{screenshots_dir}/login-light.png")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_theme_persists_across_pages(self, page, screenshots_dir):
        """Verify theme preference persists."""
        page.goto("http://localhost:5000/auth/login")
        
        # Switch to light mode
        page.locator("#theme-switcher-button").click()
        
        # Navigate to register page
        page.click("a[href*='register']")
        
        # Verify theme is still light
        html = page.locator("html")
        expect(html).to_have_attribute("data-bs-theme", "light")


class TestResponsiveDesign:
    """Test responsive design at different viewports."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_mobile_viewport(self, page, screenshots_dir):
        """Test layout on mobile viewport (375x667)."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto("http://localhost:5000/auth/login")
        
        # Navbar should be collapsed
        expect(page.locator(".navbar-toggler")).to_be_visible()
        
        page.screenshot(path=f"{screenshots_dir}/login-mobile.png")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_tablet_viewport(self, page, screenshots_dir):
        """Test layout on tablet viewport (768x1024)."""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto("http://localhost:5000/auth/login")
        
        page.screenshot(path=f"{screenshots_dir}/login-tablet.png")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_desktop_viewport(self, page, screenshots_dir):
        """Test layout on desktop viewport (1280x720)."""
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto("http://localhost:5000/auth/login")
        
        page.screenshot(path=f"{screenshots_dir}/login-desktop.png")


class TestDashboardVisual:
    """Visual tests for dashboard page."""
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_dashboard_dark_mode(self, page, screenshots_dir):
        """Verify dashboard renders correctly in dark mode."""
        # Login first (assumes test user exists)
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Verify theme is dark
        html = page.locator("html")
        expect(html).to_have_attribute("data-bs-theme", "dark")
        
        page.screenshot(path=f"{screenshots_dir}/dashboard-dark.png")
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_dashboard_light_mode(self, page, screenshots_dir):
        """Verify dashboard renders correctly in light mode."""
        # Login first
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Switch to light mode
        page.locator("#theme-switcher-button").click()
        
        # Verify theme changed
        html = page.locator("html")
        expect(html).to_have_attribute("data-bs-theme", "light")
        
        page.screenshot(path=f"{screenshots_dir}/dashboard-light.png")
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_patient_card_structure(self, page):
        """Verify patient card has correct structure."""
        # Login and navigate to dashboard
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Check if there are any patient cards
        cards = page.locator("[data-patient-id]")
        if cards.count() > 0:
            card = cards.first
            
            # Verify card structure
            expect(card.locator(".patient-card__name, .card-header")).to_be_visible()


class TestFormVisual:
    """Visual tests for form elements."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_login_form_validation_visual(self, page, screenshots_dir):
        """Verify form validation styles."""
        page.goto("http://localhost:5000/auth/login")
        
        # Submit empty form
        page.click("button[type='submit']")
        
        # Take screenshot showing validation states
        page.screenshot(path=f"{screenshots_dir}/login-validation.png")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_form_focus_indicators(self, page, screenshots_dir):
        """Verify focus indicators are visible."""
        page.goto("http://localhost:5000/auth/login")
        
        # Focus the email input
        page.focus("input[name='email']")
        
        # Take screenshot
        page.screenshot(path=f"{screenshots_dir}/login-focus.png")
