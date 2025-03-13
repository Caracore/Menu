#Jeu du pendu en python
import random

#TODO: ALL IT's DONE but need try to make it better:
# - add a way to save the game
# - add a way to load the game
# - add a way to exit the game
# - and try 2 or more lettres in choix for found quickly the word.
# - print mot essayé
# - print vie restante
# - rajouter plus de mots dans le disctionnaire
# - ajouter un restart après 0 vie choice oui ou non

class Pendu:
    def __init__(self, mot=None, vie=None, lettre=None, mot_=None, letter_in_mot_=None):
        self.mot = ["python","code","programme","programmer","programmation","pendu","jeu","maman","papa"]
        self.vie = 10
        self.lettres_essayees = []
        self.mot_ = random.choice(self.mot)
        self.update_letter = ["_" for _ in self.mot_]
        self.letter_in_mot_ = " ".join(self.update_letter)


    def trouver_mot(self, mot_): # a voir si je mets mot_ ou + mot
        print("Trouvé" if mot_ == self.mot_ else "Pas encore trouvé")

    def afficher_vie(self, vie):
        print("Vie restante :", vie)
        return vie

    def afficher_mot(self, mot_):
        print("Le mot était :", mot_)
    
    def choisir_lettre(self):
        lettre = input("Choisissez une lettre : ")
        return lettre
         
    def menu(self):
        vie_str = "vies"
        print("Pendu ->")
        input("Initialisation...")
        print()
        print("Pendu <-")
        print("Trouver le mot avec des lettres en miniscule ->")
        print("Vous avez :", self.vie, "vies" if self.vie > 1 else "vie")
        print("Mot à trouver :", self.letter_in_mot_)
        print("Pendu <-")

        while self.vie > 0:
            choix = input("#-> ").lower()
            
            if len(choix) == 0:
                print("La lettre ne peut pas être vide")
                continue
                
            if len(choix) > 1:
                if choix == self.mot_:
                    print("Bravo ! Vous avez trouvé le mot :", self.mot_)
                    break
                else:
                    print("Ce n'est pas le bon mot")
                    self.vie -= 1
                    print("Il vous reste:", self.vie, "vies" if self.vie > 1 else "vie")
                continue
                
            if choix in self.lettres_essayees:
                print("Vous avez déjà essayé cette lettre")
                continue
                
            self.lettres_essayees.append(choix)
            
            if choix in self.mot_:
                print("Tu as trouvé la lettre", choix)
                # Mettre à jour les lettres trouvées
                for i in range(len(self.mot_)):
                    if self.mot_[i] == choix:
                        self.update_letter[i] = choix
                self.letter_in_mot_ = " ".join(self.update_letter)
                print("Mot à trouver :", self.letter_in_mot_)
                
                # Vérifier si le mot est complet
                if "_" not in self.update_letter:
                    print("Bravo ! Vous avez trouvé le mot :", self.mot_)
                    break
            else:
                print("La lettre n'est pas dans le mot")
                self.vie -= 1
                print("Il vous reste:", self.vie, "vies" if self.vie > 1 else "vie")
            
            if self.vie == 0:
                print("Vous avez perdu ! Le mot était :", self.mot_)
                break

# Créer une instance de Pendu et lancer le jeu
if __name__ == "__main__":
    jeu = Pendu()
    jeu.menu()