import os
import subprocess

user = os.getlogin()
racine = r"C:\Users\+\AppData\Local\Programs\shadow\Shadow PC.exe"
r = racine.replace("+", user)

def shadowpc():
    print("ShadowPC en cours d'éxécution !")
    try:
        subprocess.Popen(r)
    except FileNotFoundError:
        print("Le fichier Shadow PC.exe n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    input("Appuyez sur Entrée pour quitter...")
if __name__ == "__main__":
    shadowpc()