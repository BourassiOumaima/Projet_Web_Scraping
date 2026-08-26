import schedule, time
from scraper import scraper_exemple

def job():
    df = scraper_exemple()
    df = ajout_filtrage_contrat(df)
    df = ajout_filtrage_domaine(df)
    df.to_csv("offres_filtrees.csv", index=False)
    print("Données mises à jour ✅")

schedule.every(2).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
