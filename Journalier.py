import pandas as pd

# 1. Chargement des données
# Assurez-vous que ce fichier est dans le même dossier que votre script
nom_fichier_entree = r'c:\Users\manue\Documents\SAE 15 Traiter les données\Projet\Analyse_Journaliere_Complete_V2.xlsx'
nom_fichier_sortie = 'Analyse_Jours_Affluence_Source.xlsx'

try:
    df = pd.read_excel(nom_fichier_entree)
    print(f"Fichier chargé avec succès : {nom_fichier_entree}")
except FileNotFoundError:
    print(f"ERREUR : Le fichier '{nom_fichier_entree}' est introuvable.")
    exit()

# 2. Traitement des Dates
# On convertit la colonne 'Jour' en format date pour que Python comprenne
df['Jour'] = pd.to_datetime(df['Jour'], dayfirst=True)

# On extrait le nom du jour (Monday, Tuesday...)
df['Nom_Jour_Anglais'] = df['Jour'].dt.day_name()

# On traduit en Français pour que ce soit propre dans le rapport
traduction = {
    'Monday': 'Lundi', 
    'Tuesday': 'Mardi', 
    'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi', 
    'Friday': 'Vendredi', 
    'Saturday': 'Samedi', 
    'Sunday': 'Dimanche'
}
df['Jour_Semaine'] = df['Nom_Jour_Anglais'].map(traduction)

# 3. Calcul des Moyennes (Le Classement)
# On regroupe par jour de la semaine et on fait la moyenne du taux de remplissage
classement = df.groupby('Jour_Semaine')['Moyenne Remplissage (%)'].mean().reset_index()

# On trie du plus rempli au moins rempli
classement = classement.sort_values(by='Moyenne Remplissage (%)', ascending=False)

# 4. Création du Fichier Excel
# On crée un fichier Excel avec deux onglets
with pd.ExcelWriter(nom_fichier_sortie, engine='openpyxl') as writer:
    # Onglet 1 : Le Résumé (Votre classement)
    classement.to_excel(writer, sheet_name='Classement_Resumé', index=False)
    
    # Onglet 2 : Les Détails (Pour vérifier les dates des Jeudis)
    # On garde juste les colonnes utiles pour la vérification
    colonnes_utiles = ['Jour', 'Jour_Semaine', 'Nom', 'Moyenne Remplissage (%)']
    details = df[colonnes_utiles].sort_values(by='Jour')
    details.to_excel(writer, sheet_name='Données_Détaillées', index=False)

print("-" * 30)
print(f"SUCCÈS ! Le fichier '{nom_fichier_sortie}' a été créé.")
print("Vous y trouverez l'onglet 'Classement_Resumé' avec les moyennes par jour.")
print("-" * 30)