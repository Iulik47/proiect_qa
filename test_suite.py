import re
from playwright.sync_api import Page, expect

# ---------------------------------------------------------
# TEST 1: Login Valid (Pozitiv)
# ---------------------------------------------------------
def test_login_valid(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # expect() verifică automat dacă elementul apare pe ecran (Assertion)
    expect(page.locator(".oxd-topbar-header-breadcrumb")).to_be_visible(timeout=15000)

# ---------------------------------------------------------
# TEST 2: Login cu Date Invalide (Negativ)
# ---------------------------------------------------------
def test_login_invalid_credentials(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("AdminGresit")
    page.get_by_placeholder("Password").fill("Parola123!")
    page.get_by_role("button", name="Login").click()
    
    # Verificăm dacă apare textul roșu de eroare
    expect(page.locator(".oxd-alert-content-text")).to_have_text("Invalid credentials")

# ---------------------------------------------------------
# TEST 3: Mini Test de Securitate (SQL Injection Attempt)
# ---------------------------------------------------------
def test_login_sql_injection_attempt(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # Introducem un payload de SQLi în câmpul de user
    page.get_by_placeholder("Username").fill("Admin' OR '1'='1")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # Sistemul ar trebui să se apere și să respingă logarea
    expect(page.locator(".oxd-alert-content-text")).to_have_text("Invalid credentials")

# ---------------------------------------------------------
# TEST 4: Validarea Câmpurilor Goale (Empty Fields)
# ---------------------------------------------------------
def test_empty_fields_validation(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # Apăsăm Login direct, fără să completăm nimic
    page.get_by_role("button", name="Login").click()
    
    # Căutăm textele roșii "Required" sub căsuțe. Verificăm că apar fix 2 astfel de mesaje.
    mesaje_eroare = page.locator("span.oxd-text--span.oxd-input-field-error-message")
    expect(mesaje_eroare).to_have_count(2)

# ---------------------------------------------------------
# TEST 5: Scenariul E2E (CRUD) - Angajare, Modificare, Ștergere
# ---------------------------------------------------------
def test_e2e_employee_lifecycle(page: Page):
    # Logare
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator(".oxd-topbar-header-breadcrumb")).to_be_visible(timeout=15000)

    # Adăugare Angajat
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("link", name="Add Employee").click()
    page.get_by_placeholder("First Name").fill("Ion")
    page.get_by_placeholder("Last Name").fill("Popescu")
    page.get_by_role("button", name="Save").click()
    expect(page.locator("h6:has-text('Personal Details')")).to_be_visible(timeout=15000)

    # Modificare Date
    page.get_by_placeholder("Middle Name").fill("Vasile")
    page.locator("button[type='submit']").first.click()
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)

    # Ștergere Angajat (Metoda reparată anterior)
    page.get_by_role("link", name="Employee List").click()
    expect(page.locator(".oxd-table-body")).to_be_visible(timeout=15000)
    page.get_by_placeholder("Type for hints...").first.fill("Ion")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(2000) # Scurtă pauză pentru tabel
    
    rand_angajat = page.locator(".oxd-table-card").filter(has_text="Popescu").first
    rand_angajat.locator(".bi-trash").click()
    page.locator("button.oxd-button--label-danger").click()
    
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)