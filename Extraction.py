# Configuration des noms de fichiers
fichier_entree = "Grand_Fichier_Complet_Final.txt"
fichier_sortie_voiture = "donnees_voitures.txt"
fichier_sortie_velo = "donnees_velos.txt"

print("Début du traitement...")

try:
    # On ouvre les 3 fichiers en même temps
    # 'r' pour lire l'entrée, 'w' pour écrire dans les sorties
    with open(fichier_entree, "r", encoding="utf-8") as f_in, \
         open(fichier_sortie_voiture, "w", encoding="utf-8") as f_voiture, \
         open(fichier_sortie_velo, "w", encoding="utf-8") as f_velo:

        # 1. Gestion de l'en-tête (la première ligne)
        entete = f_in.readline()
        
        # On écrit l'en-tête dans les deux nouveaux fichiers pour garder la structure
        f_voiture.write(entete)
        f_velo.write(entete)

        # 2. Traitement ligne par ligne (garde l'ordre chronologique)
        compteur_voiture = 0
        compteur_velo = 0

        for ligne in f_in:
            # On nettoie la ligne et on sépare les colonnes pour analyser le type
            # Structure : Date;Heure;Type;Nom;...
            colonnes = ligne.strip().split(";")

            # Sécurité : on vérifie que la ligne n'est pas vide
            if len(colonnes) > 2:
                type_vehicule = colonnes[2] # La 3ème colonne est le Type (index 2)

                if type_vehicule == "Voiture":
                    f_voiture.write(ligne)
                    compteur_voiture += 1
                elif type_vehicule == "Vélo":
                    f_velo.write(ligne)
                    compteur_velo += 1

    print("Terminé !")
    print(f"Lignes voitures extraites : {compteur_voiture}")
    print(f"Lignes vélos extraites : {compteur_velo}")
    print(f"Fichiers créés : {fichier_sortie_voiture} et {fichier_sortie_velo}")

except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_entree}' est introuvable. Vérifiez l'emplacement.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")