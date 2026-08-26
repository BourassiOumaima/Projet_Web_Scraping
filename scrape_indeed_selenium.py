from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

def parse_date_indeed(date_str):
    """Convertit les dates relatives Indeed en dates réelles"""
    if not date_str or date_str == "—":
        return "Non spécifiée"
    
    date_str = date_str.lower().strip()
    aujourdhui = datetime.now()
    
    # Aujourd'hui / Today
    if "aujourd'hui" in date_str or "today" in date_str or "auj" in date_str:
        return aujourdhui.strftime("%d/%m/%Y")
    
    # Hier / Yesterday
    if "hier" in date_str or "yesterday" in date_str:
        return (aujourdhui - timedelta(days=1)).strftime("%d/%m/%Y")
    
    # Il y a X jours / X days ago
    if "jour" in date_str or "day" in date_str:
        try:
            num = int(''.join(filter(str.isdigit, date_str)))
            return (aujourdhui - timedelta(days=num)).strftime("%d/%m/%Y")
        except:
            pass
    
    # Il y a X heures / X hours ago
    if "heure" in date_str or "hour" in date_str:
        return aujourdhui.strftime("%d/%m/%Y")
    
    # Plus de 30 jours / 30+ days
    if "30+" in date_str or "30 +" in date_str:
        return "Il y a 30+ jours"
    
    return date_str

def scrape_indeed_selenium(mot_cle, pays="fr", pages=1):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    base_url = f"https://{pays}.indeed.com/jobs?q={mot_cle.replace(' ', '+')}"
    driver.get(base_url)

    offres = []
    liens_vus = set()

    for page in range(pages):
        try:
            job_selector = "div.slider_container div" if pays == "ma" else "div.job_seen_beacon"
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_selector))
            )
        except:
            print("⚠️ Aucune offre trouvée sur cette page.")
            break

        jobs = driver.find_elements(By.CSS_SELECTOR, job_selector)

        for job in jobs:
            # ---- Titre ----
            try:
                titre = job.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text.strip()
            except:
                titre = "—"

            # ---- Entreprise ----
            entreprise = "—"
            for sel in ["span[data-testid='company-name']", "span.companyName", "div.company_location > span"]:
                try:
                    entreprise = job.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if entreprise:
                        break
                except:
                    continue

            # ---- Lieu ----
            lieu = "—"
            for sel in ["div[data-testid='text-location']", "div.companyLocation", "div.company_location"]:
                try:
                    lieu = job.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if lieu:
                        break
                except:
                    continue

            # ---- Date (améliorée) ----
            date = "—"
            for sel in ["span.date", "span[data-testid='myJobsStateDate']", "table.jobCardShelfContainer span.date"]:
                try:
                    date = job.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if date:
                        break
                except:
                    continue
            
            # Convertir la date relative en date formatée
            date = parse_date_indeed(date)

            # ---- Salaire (nouveau) ----
            salaire = "Non spécifié"
            for sel in ["div.salary-snippet-container", "div.metadata.salary-snippet-container"]:
                try:
                    salaire = job.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if salaire:
                        break
                except:
                    continue

            # ---- Type de contrat (nouveau) ----
            type_contrat = "Non spécifié"
            for sel in ["div.metadata div", "div.attribute_snippet"]:
                try:
                    type_contrat = job.find_element(By.CSS_SELECTOR, sel).text.strip()
                    if type_contrat and ("temps" in type_contrat.lower() or "time" in type_contrat.lower() or "stage" in type_contrat.lower()):
                        break
                except:
                    continue

            # ---- Lien ----
            try:
                lien_elem = job.find_element(By.CSS_SELECTOR, "a[data-jk], a.tapItem")
                job_id = lien_elem.get_attribute("data-jk")
                lien = f"https://{pays}.indeed.com/viewjob?jk={job_id}" if job_id else lien_elem.get_attribute("href")
            except:
                lien = "#"

            # Ignorer les offres trop incomplètes
            if (titre == "—") or (entreprise == "—" and lieu == "—"):
                continue

            # Éviter les doublons via l'URL
            if lien in liens_vus:
                continue
            liens_vus.add(lien)

            offres.append({
                "titre": titre,
                "entreprise": entreprise,
                "lieu": lieu,
                "date": date,
                "salaire": salaire,
                "type_contrat": type_contrat,
                "categorie": mot_cle,
                "pays": pays.upper(),
                "lien": lien
            })

        # ---- Page suivante ----
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
            href = next_btn.get_attribute("href")
            if href:
                driver.get(href)
                time.sleep(3)
            else:
                break
        except:
            break

    driver.quit()
    print(f"{len(offres)} offres extraites ✅ (après nettoyage)")
    return offres