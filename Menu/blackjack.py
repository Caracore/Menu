import random
import os
import time

class Carte:
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur
    
    def __str__(self):
        symboles = {"Coeur": "♥", "Carreau": "♦", "Trèfle": "♣", "Pique": "♠"}
        return f"{self.valeur}{symboles[self.couleur]}"
    
    def valeur_points(self):
        if self.valeur in ["J", "Q", "K"]:
            return 10
        elif self.valeur == "A":
            return 11  # L'As vaut 11 par défaut, mais peut valoir 1
        else:
            return int(self.valeur)

class Deck:
    def __init__(self):
        valeurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        couleurs = ["Coeur", "Carreau", "Trèfle", "Pique"]
        self.cartes = [Carte(valeur, couleur) for valeur in valeurs for couleur in couleurs]
        self.melanger()
    
    def melanger(self):
        random.shuffle(self.cartes)
    
    def tirer_carte(self):
        if len(self.cartes) > 0:
            return self.cartes.pop()
        else:
            print("Le deck est vide. Création d'un nouveau deck.")
            self.__init__()
            return self.cartes.pop()

class Main:
    def __init__(self):
        self.cartes = []
    
    def ajouter_carte(self, carte):
        self.cartes.append(carte)
    
    def calculer_points(self):
        points = sum(carte.valeur_points() for carte in self.cartes)
        # Ajustement pour les As
        nombre_as = sum(1 for carte in self.cartes if carte.valeur == "A")
        while points > 21 and nombre_as > 0:
            points -= 10  # Convertir un As de 11 à 1 point
            nombre_as -= 1
        return points
    
    def afficher(self, cacher_premiere=False):
        if cacher_premiere and len(self.cartes) > 0:
            return ["XX"] + [str(carte) for carte in self.cartes[1:]]
        else:
            return [str(carte) for carte in self.cartes]

class Joueur:
    def __init__(self, nom, argent=1000):
        self.nom = nom
        self.main = Main()
        self.argent = argent
        self.mise = 0
    
    def placer_mise(self, montant):
        if montant <= self.argent:
            self.mise = montant
            self.argent -= montant
            return True
        else:
            return False
    
    def gagner(self, multiplicateur=2):
        gain = self.mise * multiplicateur
        self.argent += gain
        self.mise = 0
        return gain
    
    def perdre(self):
        perte = self.mise
        self.mise = 0
        return perte
    
    def egalite(self):
        self.argent += self.mise
        self.mise = 0

class Croupier:
    def __init__(self):
        self.main = Main()
    
    def doit_tirer(self):
        return self.main.calculer_points() < 17

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.joueur = None
        self.croupier = Croupier()
    
    def effacer_ecran(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def afficher_table(self, cacher_carte_croupier=True):
        self.effacer_ecran()
        print("\n" + "=" * 50)
        print(f"{'BLACKJACK':^50}")
        print("=" * 50 + "\n")
        
        # Afficher les cartes du croupier
        cartes_croupier = self.croupier.main.afficher(cacher_carte_croupier)
        points_croupier = "?" if cacher_carte_croupier else self.croupier.main.calculer_points()
        print(f"Croupier: {' '.join(cartes_croupier)} ({points_croupier} points)")
        
        # Afficher les cartes du joueur
        cartes_joueur = self.joueur.main.afficher()
        points_joueur = self.joueur.main.calculer_points()
        print(f"\n{self.joueur.nom}: {' '.join(cartes_joueur)} ({points_joueur} points)")
        print(f"Argent: {self.joueur.argent}€ | Mise actuelle: {self.joueur.mise}€\n")
    
    def nouvelle_partie(self):
        self.effacer_ecran()
        print("\n" + "=" * 50)
        print(f"{'BIENVENUE AU BLACKJACK':^50}")
        print("=" * 50 + "\n")
        
        if self.joueur is None:
            nom = input("Entrez votre nom: ")
            argent_initial = 1000
            self.joueur = Joueur(nom, argent_initial)
        
        self.jouer_manche()
    
    def reinitialiser_mains(self):
        self.deck = Deck()
        self.joueur.main = Main()
        self.croupier.main = Main()
    
    def distribuer_cartes_initiales(self):
        # Distribuer 2 cartes à chaque joueur
        for _ in range(2):
            self.joueur.main.ajouter_carte(self.deck.tirer_carte())
            self.croupier.main.ajouter_carte(self.deck.tirer_carte())
    
    def tour_joueur(self):
        while True:
            self.afficher_table()
            
            # Vérifier si le joueur a un blackjack
            if len(self.joueur.main.cartes) == 2 and self.joueur.main.calculer_points() == 21:
                print("Blackjack!")
                time.sleep(2)
                return "blackjack"
            
            # Vérifier si le joueur a dépassé 21
            if self.joueur.main.calculer_points() > 21:
                print("Vous avez dépassé 21. Vous perdez.")
                time.sleep(2)
                return "perdu"
            
            # Demander au joueur ce qu'il veut faire
            choix = input("\nQue voulez-vous faire? (T)irer une carte, (R)ester: ").upper()
            
            if choix == 'T':
                self.joueur.main.ajouter_carte(self.deck.tirer_carte())
            elif choix == 'R':
                return "reste"
            else:
                print("Choix invalide. Veuillez réessayer.")
                time.sleep(1)
    
    def tour_croupier(self):
        self.afficher_table(cacher_carte_croupier=False)
        time.sleep(1)
        
        # Le croupier tire des cartes jusqu'à avoir au moins 17 points
        while self.croupier.doit_tirer():
            self.croupier.main.ajouter_carte(self.deck.tirer_carte())
            self.afficher_table(cacher_carte_croupier=False)
            time.sleep(1)
        
        points_croupier = self.croupier.main.calculer_points()
        
        if points_croupier > 21:
            print("Le croupier a dépassé 21. Vous gagnez!")
            return "gagne"
        
        return "termine"
    
    def determiner_gagnant(self):
        points_joueur = self.joueur.main.calculer_points()
        points_croupier = self.croupier.main.calculer_points()
        
        if points_joueur > points_croupier:
            print(f"Vous gagnez avec {points_joueur} points contre {points_croupier}!")
            return "gagne"
        elif points_joueur < points_croupier:
            print(f"Le croupier gagne avec {points_croupier} points contre {points_joueur}.")
            return "perdu"
        else:
            print(f"Égalité à {points_joueur} points.")
            return "egalite"
    
    def jouer_manche(self):
        # Réinitialiser les mains
        self.reinitialiser_mains()
        
        # Demander la mise
        while True:
            self.effacer_ecran()
            print(f"\nArgent disponible: {self.joueur.argent}€")
            try:
                mise = int(input("Placez votre mise (minimum 10€): "))
                if mise < 10:
                    print("La mise minimum est de 10€.")
                    time.sleep(1)
                    continue
                if not self.joueur.placer_mise(mise):
                    print("Vous n'avez pas assez d'argent.")
                    time.sleep(1)
                    continue
                break
            except ValueError:
                print("Veuillez entrer un nombre valide.")
                time.sleep(1)
        
        # Distribuer les cartes initiales
        self.distribuer_cartes_initiales()
        
        # Tour du joueur
        resultat_joueur = self.tour_joueur()
        
        if resultat_joueur == "blackjack":
            # Le joueur a un blackjack, il gagne 1.5x sa mise
            gain = self.joueur.gagner(2.5)
            print(f"Blackjack! Vous gagnez {gain}€!")
        elif resultat_joueur == "perdu":
            # Le joueur a dépassé 21, il perd sa mise
            perte = self.joueur.perdre()
            print(f"Vous avez perdu {perte}€.")
        else:  # resultat_joueur == "reste"
            # Tour du croupier
            resultat_croupier = self.tour_croupier()
            
            if resultat_croupier == "gagne":
                # Le croupier a dépassé 21, le joueur gagne
                gain = self.joueur.gagner()
                print(f"Vous gagnez {gain}€!")
            else:  # resultat_croupier == "termine"
                # Déterminer le gagnant
                resultat_final = self.determiner_gagnant()
                
                if resultat_final == "gagne":
                    gain = self.joueur.gagner()
                    print(f"Vous gagnez {gain}€!")
                elif resultat_final == "perdu":
                    perte = self.joueur.perdre()
                    print(f"Vous avez perdu {perte}€.")
                else:  # resultat_final == "egalite"
                    self.joueur.egalite()
                    print("Égalité. Votre mise vous est rendue.")
        
        time.sleep(2)
        
        # Vérifier si le joueur a encore de l'argent
        if self.joueur.argent <= 0:
            print("\nVous n'avez plus d'argent. Game over!")
            rejouer = input("\nVoulez-vous recommencer avec 1000€? (O/N): ").upper()
            if rejouer == 'O':
                self.joueur.argent = 1000
                self.jouer_manche()
            else:
                print("\nMerci d'avoir joué!")
                return
        
        # Demander si le joueur veut rejouer
        rejouer = input("\nVoulez-vous jouer une autre manche? (O/N): ").upper()
        if rejouer == 'O':
            self.jouer_manche()
        else:
            print(f"\nVous partez avec {self.joueur.argent}€. Merci d'avoir joué!")

def afficher_regles():
    print("\n" + "=" * 50)
    print(f"{'RÈGLES DU BLACKJACK':^50}")
    print("=" * 50 + "\n")
    print("Le but du jeu est d'avoir une main de cartes dont la valeur est")
    print("la plus proche possible de 21 sans dépasser ce nombre.")
    print("\nValeur des cartes:")
    print("- Les cartes numériques (2-10) valent leur valeur nominale.")
    print("- Les figures (Valet, Dame, Roi) valent 10 points.")
    print("- L'As vaut 11 points, ou 1 point si 11 ferait dépasser 21.")
    print("\nDéroulement du jeu:")
    print("1. Vous placez votre mise.")
    print("2. Le croupier distribue 2 cartes à chaque joueur.")
    print("   Une des cartes du croupier reste cachée.")
    print("3. Vous pouvez 'Tirer' pour recevoir une carte supplémentaire")
    print("   ou 'Rester' pour garder votre main actuelle.")
    print("4. Si vous dépassez 21, vous perdez immédiatement.")
    print("5. Quand vous décidez de rester, c'est au tour du croupier.")
    print("6. Le croupier tire des cartes jusqu'à avoir au moins 17 points.")
    print("7. Si le croupier dépasse 21, vous gagnez.")
    print("8. Sinon, le joueur avec la main la plus proche de 21 gagne.")
    print("\nGains:")
    print("- Victoire normale: vous récupérez 2x votre mise.")
    print("- Blackjack (21 avec 2 cartes): vous récupérez 2.5x votre mise.")
    print("- Égalité: votre mise vous est rendue.")
    print("- Défaite: vous perdez votre mise.")
    
    input("\nAppuyez sur Entrée pour revenir au menu principal...")

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 50)
        print(f"{'BLACKJACK':^50}")
        print("=" * 50 + "\n")
        print("1. Nouvelle partie")
        print("2. Règles du jeu")
        print("3. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            jeu = Blackjack()
            jeu.nouvelle_partie()
        elif choix == "2":
            afficher_regles()
        elif choix == "3":
            print("\nMerci d'avoir joué! Au revoir.")
            break
        else:
            print("\nChoix invalide. Veuillez réessayer.")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()
