import pandas as pd
from neo4j import GraphDatabase

# Connexion à Neo4j
uri = "bolt://localhost:7687"  # L'URL par défaut de Neo4j
username = "neo4j"              # Remplace par ton nom d'utilisateur Neo4j
password = "123456789"          # Remplace par ton mot de passe Neo4j

# Initialisation de la connexion
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonction pour créer ou récupérer un nœud et établir une relation avec un autre nœud
def creer_relation(tx, filiere, etablissement, entite, mode_entree, bac, matieres, debouches):
    tx.run(
        """
        MERGE (f:Filiere {nom: $filiere})
        ON CREATE SET f.mode_entree = $mode_entree, f.bac_recommande = $bac, 
                      f.matieres = $matieres, f.debouches = $debouches
        ON MATCH SET f.mode_entree = $mode_entree, f.bac_recommande = $bac, 
                      f.matieres = $matieres, f.debouches = $debouches
        MERGE (e:Etablissement {nom: $etablissement})
        MERGE (ent:Entite {nom: $entite})
        MERGE (e)-[:APPARTIENT_A]->(ent)
        MERGE (e)-[:PROPOSE]->(f)
        """,
        filiere=filiere, etablissement=etablissement, entite=entite, 
        mode_entree=mode_entree, bac=bac, matieres=matieres, debouches=debouches
    )

# Lire le fichier Excel
df = pd.read_excel("Tempate_Extraction2.xlsx")

# Traitement des données et insertion dans Neo4j
with driver.session() as session:
    for index, row in df.iterrows():
        # Extraire les matières et débouchés séparés par des virgules
        matieres = ', '.join([m.strip() for m in row['Matières'].split(',')])
        debouches = ', '.join([d.strip() for d in row['Débouchés /Métiers'].split(',')])
        
        # Insérer les données dans Neo4j
        session.write_transaction(
            creer_relation,
            row['Filières de formation'],
            row['Etablissements'],
            row['Entité de formation'],
            row["Mode d'entrée"],  # Correction de "Mode Entrée" -> "Mode d'entrée"
            row['Baccalauréat recommandé'],
            matieres,
            debouches
        )

print("Données importées avec succès dans Neo4j !")

# Fermer la connexion
driver.close()
