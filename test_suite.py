import re
import random
import string
import time
from datetime import date, timedelta
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
    id_unic = str(int(time.time()))
    camp_id = page.locator(".oxd-input-group").filter(has_text="Employee Id").locator("input")
    camp_id.fill(id_unic)
    page.get_by_role("button", name="Save").click()
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)
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

# ---------------------------------------------------------
# TEST 6: Delogare (Logout)
# ---------------------------------------------------------
def test_logout(page: Page):
    # Logare inițială
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator(".oxd-topbar-header-breadcrumb")).to_be_visible(timeout=15000)

    # Deschidem meniul userului și dăm click pe Logout
    page.locator(".oxd-userdropdown-tab").click()
    page.get_by_role("menuitem", name="Logout").click()

    # Verificăm că am revenit pe pagina de login
    expect(page.get_by_placeholder("Username")).to_be_visible(timeout=15000)
    expect(page).to_have_url(re.compile(r".*/auth/login"))


# ---------------------------------------------------------
# TEST 7: Claims - Event nou, Claim nou, Expense si verificare in My Claims
# ---------------------------------------------------------
def test_claims_create_event_claim_expense(page: Page):
    # Logare
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator(".oxd-topbar-header-breadcrumb")).to_be_visible(timeout=15000)

    # Date aleatorii (reținute pentru verificările de la final)
    litere = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 9)))
    nume_event = f"{litere} test"
    descriere_event = f"{''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 9)))} test description"
    tip_cheltuiala = None
    data_cheltuiala = (date.today() - timedelta(days=random.randint(1, 90))).strftime("%Y-%d-%m")
    suma = random.randint(1, 999)

    # Claims -> Configuration -> Events
    page.get_by_role("link", name="Claim").click()
    page.get_by_role("listitem").filter(has_text="Configuration").click()
    page.get_by_role("menuitem", name="Events").click()
    expect(page.get_by_role("heading", name="Events")).to_be_visible(timeout=15000)

    # Add Event
    page.get_by_role("button", name="Add").click()
    page.locator(".oxd-input-group").filter(has_text="Event Name").locator("input").fill(nume_event)
    page.locator(".oxd-input-group").filter(has_text="Description").locator("textarea").fill(descriere_event)
    page.get_by_role("button", name="Save").click()
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)

    # Submit Claim
    page.get_by_role("link", name="Submit Claim").click()
    expect(page.get_by_role("heading", name="Create Claim Request")).to_be_visible(timeout=15000)
    alege_dropdown(page, "Event", nume_event)
    alege_dropdown(page, "Currency")
    page.locator(".oxd-input-group").filter(has_text="Remarks").locator("textarea").fill("claim test 1")
    page.get_by_role("button", name="Create").click()
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)

    # Adăugare Expense
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Add").first.click()
    dialog = page.locator(".oxd-dialog-container-default--inner")
    expect(dialog).to_be_visible(timeout=10000)
    tip_cheltuiala = alege_dropdown(page, "Expense Type", scope=dialog)
    dialog.locator(".oxd-input-group").filter(has_text="Date").locator("input").fill(data_cheltuiala)
    dialog.locator(".oxd-input-group").filter(has_text="Amount").locator("input").fill(str(suma))
    dialog.get_by_role("button", name="Save").click()
    expect(page.locator(".oxd-toast-content--success")).to_be_visible(timeout=10000)

    # Verificare expense în claim
    rand_expense = page.locator(".oxd-table-card").filter(has_text=tip_cheltuiala).first
    expect(rand_expense).to_contain_text(data_cheltuiala)
    expect(rand_expense).to_contain_text(str(suma))

    # My Claims
    page.get_by_role("link", name="My Claims").click()
    expect(page.locator(".oxd-table-body")).to_be_visible(timeout=15000)
    rand_claim = page.locator(".oxd-table-card").filter(has_text=nume_event).first
    expect(rand_claim).to_be_visible(timeout=10000)
    expect(rand_claim).to_contain_text(nume_event)
    expect(rand_claim).to_contain_text(str(suma))


def alege_dropdown(page: Page, eticheta: str, optiune: str = None, scope=None) -> str:
    """Deschide dropdown-ul cu eticheta dată și alege opțiunea dată (sau una aleatorie). Returnează textul ales."""
    zona = scope if scope is not None else page
    zona.locator(".oxd-input-group").filter(has_text=eticheta).locator(".oxd-select-text").click()
    optiuni = page.locator(".oxd-select-dropdown .oxd-select-option")
    optiuni.nth(1).wait_for(timeout=10000)
    if optiune is None:
        texte = [t.strip() for t in optiuni.all_inner_texts() if t.strip() and not t.startswith("-- Select")]
        optiune = random.choice(texte)
    page.locator(".oxd-select-dropdown .oxd-select-option").filter(has_text=optiune).first.click()
    expect(zona.locator(".oxd-input-group").filter(has_text=eticheta).locator(".oxd-select-text-input")).to_have_text(optiune)
    return optiune
