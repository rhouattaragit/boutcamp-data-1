import pandas as pd
import os

# Définir les colonnes du CSV
colonnes = ["Etablissement", "Filière", "Mode_d_entree", "BAC_recommandé", "Matières", "Métiers/Débouchés"]

# Créer une liste vide pour stocker les données
donnees = []

# Fonction pour extraire les informations à partir d'un fichier texte
def extraire_informations(fichier):
    # Essayer de lire le fichier avec encodage utf-8, sinon essayer d'autres encodages
    try:
        with open(fichier, 'r', encoding='utf-8', errors='replace') as f:
            lignes = f.readlines()
    except UnicodeDecodeError:
        # Si l'UTF-8 échoue, essayer avec ISO-8859-1 (latin1)
        with open(fichier, 'r', encoding='ISO-8859-1', errors='replace') as f:
            lignes = f.readlines()

    # Initialisation des variables d'extraction
    etablissement = ""
    filiere, mode_entree, bac, matieres, debouches = "", "", "", "", ""

    # Parcours des lignes pour extraire les informations
    for ligne in lignes:
        if "Établissement" in ligne or "Etablissement" in ligne:
            etablissement = ligne.split(":")[1].strip()
        elif "Filière" in ligne:
            filiere = ligne.split(":")[1].strip()
        elif "Mode_d_entree" in ligne:
            mode_entree = ligne.split(":")[1].strip()
        elif "BAC_recommandé" in ligne:
            bac = ligne.split(":")[1].strip() or "Non spécifié"
        elif "Matières" in ligne:
            matieres = ligne.split(":")[1].strip()
        elif "Métiers/Débouchés" in ligne:
            debouches = ligne.split(":")[1].strip()

    # Si l'établissement n'a pas été trouvé dans le fichier, tu peux mettre "non spécifié"
    if not etablissement:
        etablissement = "Non spécifié"

    # Ajouter les informations dans une liste de données
    donnees.append([etablissement, filiere, mode_entree, bac, matieres, debouches])

# Traitement des fichiers texte dans le répertoire
repertoire = "./data"  # Remplace par le chemin du répertoire contenant tes fichiers

# Parcours de tous les fichiers .txt dans le répertoire
for fichier in os.listdir(repertoire):
    if fichier.endswith(".txt"):  # S'assurer de traiter uniquement les fichiers .txt
        chemin_fichier = os.path.join(repertoire, fichier)
        extraire_informations(chemin_fichier)

# Créer un DataFrame pandas à partir des données extraites
df = pd.DataFrame(donnees, columns=colonnes)

# Sauvegarder les données dans un fichier CSV avec gestion d'encodage
df.to_csv("resultat_final.csv", index=False, encoding='utf-8-sig')  # Utiliser 'utf-8-sig' pour inclure BOM

print("Données sauvegardées avec succès dans resultat_final.csv")
