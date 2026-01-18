import pandas as pd

# 1. Chargement du fichier spécifique
fichier = "velos_2025-12-24.csv"
try:
    df = pd.read_csv(fichier, sep=";", encoding="utf-8")
except:
    df = pd.read_csv(fichier, sep=";", encoding="latin1")

# 2. Préparation
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
df['Jour'] = df['Datetime'].dt.strftime('%d/%m/%Y')

# Taux de remplissage
df['Capacite'] = df['Capacite'].replace(0, 1)
df['Taux'] = round((df['Disponibilite'] / df['Capacite']) * 100, 2)

# 3. Agrégation Complète
def analyse_jour(groupe):
    # On récupère la capacité max (c'est une constante pour le parking)
    cap = groupe['Capacite'].max()
    
    return pd.Series({
        'Capacité Totale': int(cap),
        'Dispo Moyenne': round(groupe['Disponibilite'].mean(), 1),
        'Taux Moyen (%)': round(groupe['Taux'].mean(), 1),
        'Taux Max (%)': groupe['Taux'].max(),
        'Taux Min (%)': groupe['Taux'].min(),
        'Min Places Dispo': groupe['Disponibilite'].min(),
        'Max Places Dispo': groupe['Disponibilite'].max()
    })

# Groupement
df_synthese = df.groupby(['Nom', 'Jour']).apply(analyse_jour).reset_index()

# 4. Export
nom_fichier = "Synthese_Journaliere_Avec_Capacite.xlsx"
df_synthese.to_excel(nom_fichier, index=False)

print(f"Terminé ! Fichier généré : {nom_fichier}")