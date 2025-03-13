import webbrowser, subprocess, shadowpc as sdp, blackjack as bj # Implementer
# soon ready:

class Menu:
    def __init__(self):
        self.choices = {
            "1": "1 - Open",
            "2": "2 - Game",
            "3": "3 - Exit"
        }
        self.conditions = [self.open_menu, self.game_menu, self.exit]
    
    def open_menu(self):
        def open_google():
            webbrowser.open("https://www.google.com")
        def open_youtube():
            webbrowser.open("https://www.youtube.com")
        def open_discord():
            webbrowser.open("https://discord.com")
        print("Open menu ->")
        input("Initialisation...")
        print()
        print("Open menu <-")
        print("Open Google ->")
        print("Open YouTube ->")
        print("Open Discord ->")
        print("Shadow Pc ->")
        print("Open menu <-")
        o_m = input("#-> ")
        match o_m:
            case "1" | "g" | "G" | "google" | "Google":
                print("Opening Google...")
                # Ajouter ici le code pour ouvrir Google
                open_google()
            case "2" | "y" | "Y" | "youtube" | "Youtube":
                print("Opening YouTube...")
                # Ajouter ici le code pour ouvrir YouTube
                open_youtube()
            case "3" | "d" | "D" | "discord" | "Discord":
                print("Opening Discord...")
                # Ajouter ici le code pour ouvrir Discord
                open_discord()
            case "4" | "s" | "S" | "shadow" | "Shadow":
                print("Opening Shadow PC...")
                # Ajouter ici le code pour ouvrir Shadow PC
                sdp.shadowpc()
            case _:
                print("Invalid choice")
                self.open_menu()
    
    def game_menu(self):
        print("Game menu ->")
        input("Initialisation...")
        print()
        print("Game menu <-")
        print("Shadow Pc ->")
        print("Black Jack ->")
        print("Pendu ->")
        print("Game menu <-")
        g_m = input("#-> ")
        match g_m:
            case "1" | "s" | "S" | "shadow" | "Shadow":
                print("Opening Shadow PC...")
                # Ajouter ici le code pour ouvrir Shadow PC
                sdp.shadowpc()
            case "2" | "b" | "B" | "blackjack" | "Blackjack":
                print("Starting Black Jack...")
                # Ajouter ici le code pour démarrer Black Jack
                bj.menu_principal()
            case "3" | "p" | "P" | "pendu" | "Pendu":
                print("Starting Pendu...")
                # Ajouter ici le code pour démarrer Pendu
                import pendu
                pendu.Pendu().menu()
            case _:
                print("Invalid choice")
                self.game_menu()
    
    def exit(self):
        print("Exit ->")
        exit()
    
    def menu(self):
        print("*"*10,"MENU","*"*10)
        print(self.choices["1"],"\n",self.choices["2"],"\n",self.choices["3"])
        condition = input("Enter your choice: ")
        match condition:
            case "1":
                self.conditions[0]() # Appel de la méthode open_menu
            case "2":
                self.conditions[1]() # Appel de la méthode game_menu
            case "3":
                self.conditions[2]() # Appel de la méthode exit
            case _:
                print("Invalid choice")
                self.menu()

# Créer une instance de Menu et appeler la méthode menu
Menu().menu()