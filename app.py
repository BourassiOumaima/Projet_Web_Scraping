from flask import Flask, render_template, request, jsonify
from scrape_indeed_selenium import scrape_indeed_selenium
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from datetime import datetime

app = Flask(__name__)

# Variable globale pour stocker les offres
offres_cache = []
mot_cle_defaut = ""
pays_defaut = "fr"
derniere_maj = None

# Fonction de mise à jour automatique
def mise_a_jour_offres():
    global offres_cache, derniere_maj
    print("⏳ Mise à jour automatique en cours...")
    nouvelles_offres = scrape_indeed_selenium(mot_cle_defaut, pays=pays_defaut, pages=1)
    if nouvelles_offres:
        offres_cache = nouvelles_offres
        derniere_maj = datetime.now()
        print(f"✅ {len(offres_cache)} offres mises à jour automatiquement.")
    else:
        print("⚠️ Aucune nouvelle offre trouvée lors de la mise à jour.")

# Planificateur (toutes les 2 heures)
scheduler = BackgroundScheduler()
scheduler.add_job(func=mise_a_jour_offres, trigger="interval", hours=2)
scheduler.start()

# Route principale
@app.route("/", methods=["GET", "POST"])
def index():
    global offres_cache, derniere_maj

    mot_cle = mot_cle_defaut
    pays = pays_defaut

    if request.method == "POST":
        mot_cle = request.form.get("mot_cle", "").strip()
        pays = request.form.get("pays", "fr")
        if mot_cle:
            print(f"🔎 Recherche manuelle de '{mot_cle}' sur Indeed {pays.upper()} ...")
            offres_cache = scrape_indeed_selenium(mot_cle, pays=pays, pages=1)
            derniere_maj = datetime.now()

    total = len(offres_cache)
    france = sum(1 for o in offres_cache if o["pays"] == "FR")
    maroc = sum(1 for o in offres_cache if o["pays"] == "MA")
    
    # Formater la date de dernière mise à jour
    maj_str = derniere_maj.strftime("%d/%m/%Y à %H:%M") if derniere_maj else "Jamais"

    return render_template(
        "index.html", 
        offres=offres_cache, 
        total=total, 
        france=france, 
        maroc=maroc, 
        mot_cle=mot_cle,
        derniere_maj=maj_str
    )

# Route API pour filtrer les offres
@app.route("/api/filter", methods=["POST"])
def filter_offres():
    data = request.json
    filtre_pays = data.get("pays", "all")
    filtre_date = data.get("date", "all")
    
    offres_filtrees = offres_cache
    
    # Filtre par pays
    if filtre_pays != "all":
        offres_filtrees = [o for o in offres_filtrees if o["pays"] == filtre_pays.upper()]
    
    # Filtre par date (optionnel - peut être étendu)
    if filtre_date == "recent":
        offres_filtrees = [o for o in offres_filtrees if "jour" in o.get("date", "").lower() or "aujourd'hui" in o.get("date", "").lower() or "/" in o.get("date", "")]
    
    return jsonify({"offres": offres_filtrees, "count": len(offres_filtrees)})

if __name__ == "__main__":
    # Lancer une première mise à jour au démarrage
    threading.Thread(target=mise_a_jour_offres).start()
    app.run(debug=True, use_reloader=False)