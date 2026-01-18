import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Chargement des données
# Remplacez le nom du fichier si nécessaire
nom_fichier = r'c:\Users\manue\Documents\SAE 15 Traiter les données\Projet\Analyse_Journaliere_Complete_V2.xlsx'

try:
    # On essaie de lire le fichier Excel
    df = pd.read_excel(nom_fichier)
except FileNotFoundError:
    print(f"Erreur : Le fichier '{nom_fichier}' est introuvable. Vérifiez le chemin.")
    # Si vous utilisez le CSV exporté par le chat, décommentez la ligne suivante :
    # df = pd.read_csv('Synthese_Parfaite_Par_Heure.xlsx - Sheet1.csv')

# 2. Filtrage des données
# On ne garde que les "Voitures" pour comparer ce qui est comparable
df_voitures = df[df['Type'] == 'Voiture']

# 3. Préparation de la matrice (Pivot)
# L'objectif est d'avoir une colonne par parking et les heures en lignes
# On utilise le 'Taux_Occupation' pour voir si les parkings se remplissent en même temps
df_pivot = df_voitures.pivot_table(
    index='Datetime', 
    columns='Nom', 
    values='Taux_Occupation'
)

# 4. Calcul de la Corrélation
# La méthode .corr() calcule le coefficient de Pearson (de -1 à 1)
matrice_correlation = df_pivot.corr()

# 5. Création de la Heatmap
plt.figure(figsize=(16, 14)) # Grande taille pour que les noms soient lisibles

sns.heatmap(
    matrice_correlation, 
    annot=True,         # Affiche les chiffres dans les cases
    fmt=".2f",          # 2 chiffres après la virgule
    cmap='coolwarm',    # Rouge = Corrélation forte, Bleu = Inverse
    center=0,           # Le blanc/neutre est à 0
    square=True,        # Cases carrées
    linewidths=.5,      # Petites lignes blanches pour séparer
    cbar_kws={"shrink": .7, "label": "Coefficient de Corrélation"}
)

plt.title('Matrice de Corrélation : Synchronisation des Parkings Voitures', fontsize=18)
plt.xticks(rotation=45, ha='right', fontsize=10) # Rotation des noms en bas
plt.yticks(fontsize=10)
plt.tight_layout()

# 6. Affichage et Sauvegarde
plt.savefig('Heatmap_Parkings_Voitures.png', dpi=300) # Sauvegarde en haute qualité
plt.show()