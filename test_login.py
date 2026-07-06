from playwright.sync_api import sync_playwright

def testeaza_login():
    # Pornim motorul Playwright
    with sync_playwright() as p:
        # Lansăm browserul Chrome/Chromium. 
        # headless=False înseamnă că vom vedea fereastra (pe server va fi True)
        # slow_mo=500 încetinește fiecare acțiune cu jumătate de secundă ca să vedem ce face
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("1. Accesăm site-ul OrangeHRM...")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Playwright este inteligent și așteaptă automat ca pagina să se încarce
        print("2. Introducem credențialele...")
        page.locator("input[name='username']").fill("Admin")
        page.locator("input[name='password']").fill("admin123")

        print("3. Apăsăm butonul de Login...")
        page.locator("button[type='submit']").click()

        print("4. Verificăm dacă logarea a avut succes (căutăm titlul 'Dashboard')...")
        # Robotul va aștepta până apare textul "Dashboard" pe ecran
        page.wait_for_selector("text=Dashboard")
        
        print("✅ TEST TRECUT CU SUCCES! Robotul a intrat în cont.")

        # Pauză de 3 secunde ca să admiri rezultatul, apoi închide fereastra
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    testeaza_login()