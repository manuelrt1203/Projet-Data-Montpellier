import pandas as pd

# Noms des fichiers
fichier_historique = "comparaison_finale.txt"      # Votre gros fichier du 24 déc au 1er janv
fichier_reference = "gps_et_capa_totale.txt"       # Le petit fichier avec les coordonnées
fichier_sortie = "Grand_Fichier_Complet_Final.txt" # Le résultat final

print("Chargement des fichiers...")

# 1. Chargement des données
# On gère l'encodage pour éviter les erreurs
try:
    df_main = pd.read_csv(fichier_historique, sep=";", encoding="utf-8")
    df_ref = pd.read_csv(fichier_reference, sep=";", encoding="utf-8")
except:
    df_main = pd.read_csv(fichier_historique, sep=";", encoding="latin1")
    df_ref = pd.read_csv(fichier_reference, sep=";", encoding="latin1")

print(f"- Lignes dans l'historique : {len(df_main)}")
print(f"- Lignes dans la référence : {len(df_ref)}")

# 2. Préparation de la table de référence (Dictionnaire des parkings)
# On ne garde que les colonnes utiles (clés + nouvelles infos)
# On supprime les doublons (au cas où le fichier ref contient plusieurs mesures du même parking)
cols_utiles = ['Type', 'Nom', 'Capacite', 'Latitude', 'Longitude']
df_infos_parkings = df_ref[cols_utiles].drop_duplicates(subset=['Type', 'Nom'])

print(f"- Parkings uniques identifiés pour la fusion : {len(df_infos_parkings)}")

# 3. La Fusion (Merge)
# On ajoute les infos au fichier principal en faisant correspondre 'Type' et 'Nom'
# how='left' signifie : on garde tout l'historique, et on ajoute les infos si on les trouve.
df_final = pd.merge(df_main, df_infos_parkings, on=['Type', 'Nom'], how='left')

# 4. Réorganisation des colonnes (Optionnel, pour faire joli)
# Ordre souhaité : Date, Heure, Type, Nom, Dispo, Capacite, Statut, Lat, Lon
cols_ordre = ['Date', 'Heure', 'Type', 'Nom', 'Disponibilite', 'Capacite', 'Statut', 'Latitude', 'Longitude']

# Vérification que toutes les colonnes existent avant de réordonner
cols_finales = [c for c in cols_ordre if c in df_final.columns]
df_final = df_final[cols_finales]

# 5. Sauvegarde
df_final.to_csv(fichier_sortie, sep=";", index=False, encoding="utf-8")

print("\nOpération terminée !")
print(f"Le fichier '{fichier_sortie}' a été créé avec succès.")
print("Vous pouvez maintenant l'utiliser pour vos cartes et calculs de taux de remplissage.")