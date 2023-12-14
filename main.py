import pygame
import random
import sys

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
white = (255, 255, 255)
black = (0, 0, 0)

with open("mots.txt", "r") as fichier:
    mots = fichier.readlines()


def choose_word():
    return random.choice(mots).strip()


def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_ "
    return mot_cache


def dessiner_pendu(erreurs):
    pendu_images = [
        pygame.image.load("image/1.png"),
        pygame.image.load("image/2.png"),
        pygame.image.load("image/3.png"),
        pygame.image.load("image/4.png"),
        pygame.image.load("image/5.png"),
        pygame.image.load("image/6.png"),
        pygame.image.load("image/7.png"),
    ]
    return pendu_images[erreurs]


def afficher_message(message, couleur):
    police = pygame.font.Font(None, 48)
    texte = police.render(message, True, couleur)
    screen.blit(texte, (width // 2 - texte.get_width() // 2, height // 2 - texte.get_height() // 2))
    pygame.display.flip()


def afficher_menu():
    screen.fill(white)
    police_menu = pygame.font.Font(None, 48)
    titre = police_menu.render("Menu", True, black)
    jouer_texte = police_menu.render("1. Jouer", True, black)
    inserer_texte = police_menu.render("2. Insérer un nouveau mot", True, black)
    quitter_texte = police_menu.render("3. Quitter", True, black)

    screen.blit(titre, (width // 2 - titre.get_width() // 2, 50))
    screen.blit(jouer_texte, (width // 2 - jouer_texte.get_width() // 2, 200))
    screen.blit(inserer_texte, (width // 2 - inserer_texte.get_width() // 2, 300))
    screen.blit(quitter_texte, (width // 2 - quitter_texte.get_width() // 2, 400))

    pygame.display.flip()


def jouer():
    mot_a_deviner = choose_word()
    lettres_trouvees = []
    erreurs = 0
    tentatives_max = 6
    police = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    proposition = chr(event.key).lower()
                    if proposition in lettres_trouvees:
                        print("Vous avez déjà proposé cette lettre.")
                    elif proposition in mot_a_deviner:
                        print("Bonne proposition !")
                        lettres_trouvees.append(proposition)
                    else:
                        print("Mauvaise proposition.")
                        erreurs += 1

        screen.fill(white)
        mot_affiche = afficher_mot_cache(mot_a_deviner, lettres_trouvees)
        mot_texte = police.render(mot_affiche, True, black)
        screen.blit(mot_texte, (20, 20))
        pendu_image = dessiner_pendu(erreurs)
        screen.blit(pendu_image, (400, 20))

        if set(mot_a_deviner) == set(lettres_trouvees):
            afficher_message("Vous avez gagné !", (0, 255, 0))
            pygame.time.delay(2000)
            return

        if erreurs >= tentatives_max:
            afficher_message("Vous avez perdu. Le mot était : {}".format(mot_a_deviner), (255, 0, 0))
            pygame.time.delay(2000)
            return

        pygame.display.flip()
        clock.tick(60)


def inserer_mot():
    nouveau_mot = input("Entrez un nouveau mot : ")
    with open("mots.txt", "a") as fichier:
        fichier.write(nouveau_mot + "\n")


if __name__ == "__main__":
    while True:
        afficher_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jouer()
                elif event.key == pygame.K_2:
                    inserer_mot()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()