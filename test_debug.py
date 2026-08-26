from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug_indeed_structure(mot_cle="design", pays="ma"):
    """
    Script de diagnostic pour voir la vraie structure HTML d'Indeed
    """
    options = Options()
    # ❌ PAS DE HEADLESS pour voir ce qui se passe
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://{pays}.indeed.com/jobs?q={mot_cle.replace(' ', '+')}"
    
    print(f"🌐 Accès à : {url}")
    driver.get(url)
    
    # Attendre le chargement
    print("⏳ Attente du chargement de la page (8 secondes)...")
    time.sleep(8)
    
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC DE LA PAGE")
    print("="*60)
    
    # 1. Vérifier le titre de la page
    print(f"\n✅ Titre de la page : {driver.title}")
    
    # 2. Sauvegarder le HTML
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("✅ HTML sauvegardé dans 'debug_page.html'")
    
    # 3. Chercher tous les sélecteurs possibles
    selectors_to_test = [
        "div.job_seen_beacon",
        "li.job_seen_beacon",
        "div.resultContent",
        "div.cardOutline",
        "div.job_card",
        "article",
        "div[data-testid='job-card']",
        "li[data-testid='job-card']",
        "div.slider_container div",
        "ul.jobsearch-ResultsList li",
        "div.mosaic-zone div.slider_item",
        "li.css-5lfssm",
        "div[data-testid='jobCard']"
    ]
    
    print("\n🔍 Test des sélecteurs de cartes d'offres :")
    best_selector = None
    max_elements = 0
    
    for selector in selectors_to_test:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            count = len(elements)
            if count > 0:
                print(f"  ✅ '{selector}' -> {count} éléments trouvés")
                if count > max_elements:
                    max_elements = count
                    best_selector = selector
            else:
                print(f"  ❌ '{selector}' -> 0 éléments")
        except Exception as e:
            print(f"  ⚠️ '{selector}' -> Erreur: {e}")
    
    if not best_selector:
        print("\n❌ AUCUN sélecteur n'a trouvé d'offres !")
        print("⚠️ Possible problème : captcha, blocage, ou structure HTML différente")
        print("\nAppuyez sur Entrée pour fermer le navigateur...")
        input()
        driver.quit()
        return
    
    # 4. Essayer d'extraire les données de la première offre
    print(f"\n📋 Meilleur sélecteur trouvé : '{best_selector}' ({max_elements} éléments)")
    print("\n🔍 Extraction de la première offre :")
    
    jobs = driver.find_elements(By.CSS_SELECTOR, best_selector)
    job = jobs[0]
    
    # Afficher le HTML de la première offre
    print("\n📄 HTML de la première offre (premiers 800 caractères):")
    html_snippet = job.get_attribute('outerHTML')[:800]
    print(html_snippet)
    print("...")
    
    # Tester différents sélecteurs pour chaque champ
    print("\n" + "="*60)
    print("🔍 TEST DES SÉLECTEURS DE TITRE :")
    print("="*60)
    titre_selectors = [
        "h2.jobTitle span",
        "h2.jobTitle a",
        "h2 a span",
        "a span[title]",
        "h2 span",
        "a[data-jk] span",
        "span[title]",
        "h2.jobTitle"
    ]
    
    titre_trouve = False
    for sel in titre_selectors:
        try:
            elem = job.find_element(By.CSS_SELECTOR, sel)
            texte = elem.text.strip() or elem.get_attribute("title") or ""
            if texte:
                print(f"  ✅ '{sel}' -> '{texte}'")
                titre_trouve = True
            else:
                print(f"  ⚠️ '{sel}' -> Trouvé mais vide")
        except:
            print(f"  ❌ '{sel}' -> Non trouvé")
    
    if not titre_trouve:
        print("  ⚠️ Aucun titre trouvé avec les sélecteurs testés")
    
    print("\n" + "="*60)
    print("🔍 TEST DES SÉLECTEURS D'ENTREPRISE :")
    print("="*60)
    entreprise_selectors = [
        "span[data-testid='company-name']",
        "span.companyName",
        "div.company_location span",
        "span.css-1h7lukg",
        "div[data-testid='company-name']",
        "a[data-testid='company-name']",
        "span[class*='company']"
    ]
    
    entreprise_trouve = False
    for sel in entreprise_selectors:
        try:
            elem = job.find_element(By.CSS_SELECTOR, sel)
            texte = elem.text.strip()
            if texte:
                print(f"  ✅ '{sel}' -> '{texte}'")
                entreprise_trouve = True
            else:
                print(f"  ⚠️ '{sel}' -> Trouvé mais vide")
        except:
            print(f"  ❌ '{sel}' -> Non trouvé")
    
    if not entreprise_trouve:
        print("  ⚠️ Aucune entreprise trouvée avec les sélecteurs testés")
    
    print("\n" + "="*60)
    print("🔍 TEST DES SÉLECTEURS DE LIEU :")
    print("="*60)
    lieu_selectors = [
        "div[data-testid='text-location']",
        "span[data-testid='text-location']",
        "div.companyLocation",
        "div.company_location div",
        "span.css-1p0sjhy",
        "div[class*='location']",
        "span[class*='location']"
    ]
    
    lieu_trouve = False
    for sel in lieu_selectors:
        try:
            elem = job.find_element(By.CSS_SELECTOR, sel)
            texte = elem.text.strip()
            if texte:
                print(f"  ✅ '{sel}' -> '{texte}'")
                lieu_trouve = True
            else:
                print(f"  ⚠️ '{sel}' -> Trouvé mais vide")
        except:
            print(f"  ❌ '{sel}' -> Non trouvé")
    
    if not lieu_trouve:
        print("  ⚠️ Aucun lieu trouvé avec les sélecteurs testés")
    
    print("\n" + "="*60)
    print("🔍 TEST DES SÉLECTEURS DE DATE :")
    print("="*60)
    date_selectors = [
        "span[data-testid='myJobsStateDate']",
        "span.date",
        "span.css-qvloho",
        "span[class*='date']",
        "div[class*='date']"
    ]
    
    date_trouve = False
    for sel in date_selectors:
        try:
            elem = job.find_element(By.CSS_SELECTOR, sel)
            texte = elem.text.strip()
            if texte:
                print(f"  ✅ '{sel}' -> '{texte}'")
                date_trouve = True
            else:
                print(f"  ⚠️ '{sel}' -> Trouvé mais vide")
        except:
            print(f"  ❌ '{sel}' -> Non trouvé")
    
    if not date_trouve:
        print("  ⚠️ Aucune date trouvée avec les sélecteurs testés")
    
    print("\n" + "="*60)
    print("🔍 TEST DES SÉLECTEURS DE LIEN :")
    print("="*60)
    lien_selectors = [
        "a[data-jk]",
        "h2.jobTitle a",
        "a[id^='job_']",
        "a[href*='viewjob']"
    ]
    
    lien_trouve = False
    for sel in lien_selectors:
        try:
            elem = job.find_element(By.CSS_SELECTOR, sel)
            job_id = elem.get_attribute("data-jk") or elem.get_attribute("id") or ""
            href = elem.get_attribute("href") or ""
            if job_id or href:
                print(f"  ✅ '{sel}' -> job_id: '{job_id}' | href: '{href[:50]}...'")
                lien_trouve = True
            else:
                print(f"  ⚠️ '{sel}' -> Trouvé mais pas d'ID/href")
        except:
            print(f"  ❌ '{sel}' -> Non trouvé")
    
    if not lien_trouve:
        print("  ⚠️ Aucun lien trouvé avec les sélecteurs testés")
    
    print("\n" + "="*60)
    print("📝 RÉSUMÉ DU DIAGNOSTIC")
    print("="*60)
    print(f"✅ Meilleur sélecteur de carte : '{best_selector}'")
    print(f"✅ Nombre d'offres détectées : {max_elements}")
    print(f"{'✅' if titre_trouve else '❌'} Titre : {'Trouvé' if titre_trouve else 'NON trouvé'}")
    print(f"{'✅' if entreprise_trouve else '❌'} Entreprise : {'Trouvé' if entreprise_trouve else 'NON trouvé'}")
    print(f"{'✅' if lieu_trouve else '❌'} Lieu : {'Trouvé' if lieu_trouve else 'NON trouvé'}")
    print(f"{'✅' if date_trouve else '❌'} Date : {'Trouvé' if date_trouve else 'NON trouvé'}")
    print(f"{'✅' if lien_trouve else '❌'} Lien : {'Trouvé' if lien_trouve else 'NON trouvé'}")
    
    print("\n" + "="*60)
    print("🔍 Le navigateur reste ouvert pour inspection manuelle.")
    print("💡 Vous pouvez inspecter la page pour trouver les bons sélecteurs.")
    print("📄 Le HTML complet a été sauvegardé dans 'debug_page.html'")
    print("\nAppuyez sur Entrée pour fermer le navigateur...")
    print("="*60)
    input()
    
    driver.quit()

if __name__ == "__main__":
    print("\n🚀 DÉMARRAGE DU DIAGNOSTIC INDEED\n")
    debug_indeed_structure(mot_cle="design", pays="ma")