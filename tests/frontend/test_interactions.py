"""
Interaction Tests

Tests for user interactions and UI behavior.
Requires a running server (manual or via pytest-flask-live).
"""

import pytest
from playwright.sync_api import expect

# Skip all tests if Playwright is not available
pytest.importorskip("playwright")


class TestAuthInteractions:
    """Test authentication flow interactions."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_login_flow(self, page):
        """Test complete login flow."""
        page.goto("http://localhost:5000/auth/login")
        
        # Fill in credentials
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        
        # Submit form
        page.click("button[type='submit']")
        
        # Should redirect to dashboard
        page.wait_for_url("**/patients/")
        expect(page).to_have_url("http://localhost:5000/patients/")
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_login_validation(self, page):
        """Test login form validation."""
        page.goto("http://localhost:5000/auth/login")
        
        # Submit empty form
        page.click("button[type='submit']")
        
        # Should show validation errors
        # Either HTML5 validation or custom error messages
        email_input = page.locator("input[name='email']")
        
        # Check for invalid state
        is_invalid = email_input.evaluate(
            "el => el.validity && !el.validity.valid"
        )
        assert is_invalid or page.locator(".invalid-feedback, .alert-danger").count() > 0
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_logout_flow(self, page):
        """Test logout functionality."""
        # First login
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Click logout
        page.click("a[href*='logout']")
        
        # Should redirect to login
        expect(page).to_have_url("http://localhost:5000/auth/login")


class TestDashboardInteractions:
    """Test dashboard interactions."""
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_filter_buttons(self, page):
        """Test filter button functionality."""
        # Login first
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Click pending filter
        pending_btn = page.locator("[data-filter='pending']")
        pending_btn.click()
        
        # Verify URL updated
        expect(page).to_have_url("http://localhost:5000/patients/?show=pending")
        
        # Verify button is active
        expect(pending_btn).to_have_class(/active/)
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_add_patient_modal_opens(self, page):
        """Test add patient modal opens correctly."""
        # Login first
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Click add patient button
        page.click("[data-bs-toggle='modal'][data-bs-target*='addPatient']")
        
        # Modal should be visible
        modal = page.locator("#addPatientModal, .modal.show")
        expect(modal).to_be_visible()
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_patient_card_edit_button(self, page):
        """Test edit button on patient card."""
        # Login and navigate to dashboard
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Find first patient card with edit button
        edit_buttons = page.locator("[data-patient-action='edit']")
        
        if edit_buttons.count() > 0:
            edit_buttons.first.click()
            
            # Should open edit modal or navigate to edit page
            # Check for modal or URL change
            modal = page.locator(".modal.show")
            if modal.count() == 0:
                # Navigated to edit page
                expect(page).to_have_url(match=".*edit.*")


class TestModalInteractions:
    """Test modal dialog interactions."""
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_modal_close_on_escape(self, page):
        """Test modal closes on Escape key."""
        page.goto("http://localhost:5000/auth/login")
        
        # Trigger a modal (if available on page)
        modals = page.locator("[data-bs-toggle='modal']")
        
        if modals.count() > 0:
            modals.first.click()
            
            modal = page.locator(".modal.show")
            expect(modal).to_be_visible()
            
            # Press Escape
            page.keyboard.press("Escape")
            
            # Modal should be hidden
            expect(modal).to_be_hidden()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_modal_close_on_backdrop_click(self, page):
        """Test modal closes on backdrop click."""
        page.goto("http://localhost:5000/auth/login")
        
        modals = page.locator("[data-bs-toggle='modal']")
        
        if modals.count() > 0:
            modals.first.click()
            
            modal = page.locator(".modal.show")
            expect(modal).to_be_visible()
            
            # Click backdrop (outside modal dialog)
            page.locator(".modal.show").click(position={"x": 10, "y": 10})
            
            # Modal should be hidden
            expect(modal).to_be_hidden()


class TestToastNotifications:
    """Test toast notification behavior."""
    
    @pytest.mark.skip(reason="Requires live server with API action - run manually")
    def test_toast_appears_on_action(self, page):
        """Test toast appears after successful action."""
        # Login first
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Perform an action that shows toast (e.g., toggle payment)
        toggle_buttons = page.locator("[data-session-action='toggle']")
        
        if toggle_buttons.count() > 0:
            toggle_buttons.first.click()
            
            # Toast should appear
            toast = page.locator(".toast")
            expect(toast).to_be_visible()
    
    @pytest.mark.skip(reason="Requires live server - run manually")
    def test_toast_auto_dismisses(self, page):
        """Test toast auto-dismisses after timeout."""
        # This test requires triggering a toast and waiting
        # Implementation depends on toast duration setting
        pass


class TestCarouselInteractions:
    """Test carousel navigation."""
    
    @pytest.mark.skip(reason="Requires live server with sessions - run manually")
    def test_carousel_next_button(self, page):
        """Test carousel next button works."""
        # Login and navigate to dashboard with sessions
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Find carousel
        carousel = page.locator(".carousel")
        
        if carousel.count() > 0:
            # Get current active item
            active_item = carousel.locator(".carousel-item.active").first
            
            # Click next
            carousel.locator("[data-bs-slide='next']").click()
            
            # Wait for animation
            page.wait_for_timeout(500)
            
            # Active item should have changed
            new_active = carousel.locator(".carousel-item.active").first
            # They should be different elements
    
    @pytest.mark.skip(reason="Requires live server with sessions - run manually")
    def test_carousel_keyboard_navigation(self, page):
        """Test carousel responds to keyboard."""
        # Login and navigate to dashboard
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        carousel = page.locator(".carousel")
        
        if carousel.count() > 0:
            # Focus carousel
            carousel.first.focus()
            
            # Press arrow right
            page.keyboard.press("ArrowRight")
            
            # Wait for animation
            page.wait_for_timeout(500)


class TestFormInteractions:
    """Test form submission and validation."""
    
    @pytest.mark.skip(reason="Requires live server with auth - run manually")
    def test_add_patient_form_submission(self, page):
        """Test adding a new patient."""
        # Login first
        page.goto("http://localhost:5000/auth/login")
        page.fill("input[name='email']", "test@example.com")
        page.fill("input[name='password']", "test123")
        page.click("button[type='submit']")
        page.wait_for_url("**/patients/")
        
        # Open add patient modal
        page.click("[data-bs-toggle='modal'][data-bs-target*='addPatient']")
        
        # Fill in patient name
        page.fill("#addPatientModal input[name='name']", "Nuevo Paciente Test")
        
        # Submit form
        page.click("#addPatientModal button[type='submit']")
        
        # Should see success toast or new patient in list
        toast = page.locator(".toast")
        patient_card = page.locator("[data-patient-id]")
        
        # Either toast appears or patient is added
        expect(toast.or_(patient_card.filter(has_text="Nuevo Paciente Test"))).to_be_visible()
