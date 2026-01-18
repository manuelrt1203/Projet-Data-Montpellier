import pandas as pd
import os
import zipfile
import warnings

# On ignore les alertes pour avoir une console propre
warnings.filterwarnings("ignore")

print("--- DÉCOUPAGE DES DONNÉES BRUTES (PAR PARKING & PAR JOUR) ---")

# 1. Chargement du fichier source
fichier_source = "Grand_Fichier_Complet_Final.txt"
nom_zip_sortie = "Donnees_Brutes_Separees.zip"

try:
    df = pd.read_csv(fichier_source, sep=";", encoding="utf-8")
except:
    df = pd.read_csv(fichier_source, sep=";", encoding="latin1")

# 2. Préparation (Colonnes temporaires pour le tri)
# On crée une colonne date pour savoir comment nommer les onglets (ex: 2025-12-24)
df['TEMP_DATETIME'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'], format='%d/%m/%Y %H:%M:%S')
df['TEMP_JOUR_STR'] = df['TEMP_DATETIME'].dt.strftime('%Y-%m-%d')

# On identifie les colonnes originales pour ne garder qu'elles à la fin
cols_a_garder = [c for c in df.columns if c not in ['TEMP_DATETIME', 'TEMP_JOUR_STR']]

print(f"Création de l'archive {nom_zip_sortie}...")

# 3. Création des fichiers Excel et du ZIP
with zipfile.ZipFile(nom_zip_sortie, 'w', zipfile.ZIP_DEFLATED) as zf:
    
    # On récupère la liste unique des parkings
    liste_parkings = df[['Type', 'Nom']].drop_duplicates().values
    
    for type_p, nom_p in liste_parkings:
        # 1. On isole les données de ce parking
        df_parking = df[(df['Type'] == type_p) & (df['Nom'] == nom_p)]
        
        # 2. On définit le nom du fichier Excel (ex: Voiture_Antigone.xlsx)
        nom_clean = str(nom_p).replace("/", "-").replace("\\", "-").replace(":", "-")
        nom_fichier = f"{type_p}_{nom_clean}.xlsx"
        
        # 3. On crée le fichier Excel avec un onglet par jour
        with pd.ExcelWriter(nom_fichier, engine='openpyxl') as writer:
            # On récupère les jours présents pour ce parking
            jours_dispos = sorted(df_parking['TEMP_JOUR_STR'].unique())
            
            for jour in jours_dispos:
                # On isole les données de ce jour précis
                df_jour = df_parking[df_parking['TEMP_JOUR_STR'] == jour]
                
                # On écrit l'onglet (avec SEULEMENT les colonnes originales)
                if not df_jour.empty:
                    df_jour[cols_a_garder].to_excel(writer, sheet_name=jour, index=False)
        
        # 4. On ajoute le fichier au ZIP et on supprime l'original
        zf.write(nom_fichier)
        os.remove(nom_fichier)

print("Terminé ! Toutes les données sont découpées dans le fichier ZIP.")