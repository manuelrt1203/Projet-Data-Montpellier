import pandas as pd

print("--- GÉNÉRATION DE LA SYNTHÈSE PAR ONGLETS SÉPARÉS ---")

# 1. Chargement
fichier = "Grand_Fichier_Complet_Final.txt"
try:
    df = pd.read_csv(fichier, sep=";", encoding="utf-8")
except:
    df = pd.read_csv(fichier, sep=";", encoding="latin1")

# 2. Préparation
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
traduction = {
    'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
}
df['Date_Jour'] = df['Datetime'].dt.date
df['Nom_Jour'] = df['Datetime'].dt.day_name().map(traduction)

# 3. Calculs
df['Capacite'] = df['Capacite'].replace(0, 1)
df['Occupants'] = df.apply(lambda row: (row['Capacite'] - row['Disponibilite']) if row['Type'] == 'Voiture' else row['Disponibilite'], axis=1)

# 4. AGRÉGATION (Moyenne journalière de la charge de la ville)
# On calcule d'abord la somme par HEURE pour avoir la charge instantanée de la ville
df_horaire = df.groupby(['Datetime', 'Type']).agg({'Occupants': 'sum', 'Capacite': 'sum'}).reset_index()
df_horaire['Date_Jour'] = df_horaire['Datetime'].dt.date
df_horaire['Nom_Jour'] = df_horaire['Datetime'].dt.day_name().map(traduction)

# On moyenne ensuite par JOUR
df_synthese = df_horaire.groupby(['Date_Jour', 'Nom_Jour', 'Type']).agg({
    'Occupants': 'mean',
    'Capacite': 'mean'
}).reset_index()
df_synthese['Taux'] = round((df_synthese['Occupants'] / df_synthese['Capacite']) * 100, 2)

# SÉPARATION
df_voitures = df_synthese[df_synthese['Type'] == 'Voiture'].drop(columns=['Type'])
df_velos = df_synthese[df_synthese['Type'] == 'Vélo'].drop(columns=['Type'])

# 5. VILLE ENTIÈRE (Tout confondu)
df_horaire_ville = df.groupby(['Datetime']).agg({'Occupants': 'sum', 'Capacite': 'sum'}).reset_index()
df_horaire_ville['Date_Jour'] = df_horaire_ville['Datetime'].dt.date
df_horaire_ville['Nom_Jour'] = df_horaire_ville['Datetime'].dt.day_name().map(traduction)

df_ville = df_horaire_ville.groupby(['Date_Jour', 'Nom_Jour']).agg({'Occupants': 'mean', 'Capacite': 'mean'}).reset_index()
df_ville['Taux'] = round((df_ville['Occupants'] / df_ville['Capacite']) * 100, 2)

# 6. EXPORT
with pd.ExcelWriter("Synthese_Jours_Onglets_Separes.xlsx") as writer:
    df_voitures.to_excel(writer, sheet_name="Synthese_Voitures", index=False)
    df_velos.to_excel(writer, sheet_name="Synthese_Velos", index=False)
    df_ville.to_excel(writer, sheet_name="Synthese_Globale_Ville", index=False)

print("Fichier généré avec succès !")