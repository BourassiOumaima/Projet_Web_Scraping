import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraper_exemple():
    data = []
    url = "https://www.indeed.com/jobs?q=stage+data+science&l="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for job in soup.select(".job_seen_beacon"):
        titre = job.select_one("h2 span").text if job.select_one("h2 span") else ""
        entreprise = job.select_one(".companyName").text if job.select_one(".companyName") else ""
        lieu = job.select_one(".companyLocation").text if job.select_one(".companyLocation") else ""
        desc = job.select_one(".job-snippet").text if job.select_one(".job-snippet") else ""
        data.append([titre, entreprise, lieu, desc])
    
    df = pd.DataFrame(data, columns=["titre", "entreprise", "lieu", "description"])
    df.to_csv("offres.csv", index=False)
    print("Scraping terminé ✅")
    return df

# Exemple d'exécution
df = scraper_exemple()
