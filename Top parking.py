import pandas as pd

print("--- CLASSEMENT DES TOPS PERFORMANCES ---")

# 1. Chargement
fichier = "Grand_Fichier_Complet_Final.txt"
try:
    df = pd.read_csv(fichier, sep=";", encoding="utf-8")
except:
    df = pd.read_csv(fichier, sep=";", encoding="latin1")

# 2. Calcul des Performances (Taux moyen)
df['Capacite'] = df['Capacite'].replace(0, 1)

def calculer_perf(row):
    if row['Type'] == 'Voiture':
        return (1 - (row['Disponibilite'] / row['Capacite'])) * 100
    else:
        return (row['Disponibilite'] / row['Capacite']) * 100

df['Performance'] = df.apply(calculer_perf, axis=1)

# 3. Classement
# On fait la moyenne de la performance sur toute la semaine pour chaque parking
classement = df.groupby(['Type', 'Nom'])['Performance'].mean().reset_index()

# 4. Extraction des Tops 5
top_voitures = classement[classement['Type'] == 'Voiture'].sort_values(by='Performance', ascending=False).head(5)
top_velos = classement[classement['Type'] == 'Vélo'].sort_values(by='Performance', ascending=False).head(5)

# 5. Export
print("Génération du fichier Excel...")
with pd.ExcelWriter("Top5_Performants.xlsx") as writer:
    top_voitures.to_excel(writer, sheet_name="Top_Voitures", index=False)
    top_velos.to_excel(writer, sheet_name="Top_Velos", index=False)

print("Terminé !")
print("Top 1 Voiture :", top_voitures.iloc[0]['Nom'])
print("Top 1 Vélo    :", top_velos.iloc[0]['Nom'])