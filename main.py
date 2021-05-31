import pygame
import sys
import math


def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


class Graph:
    # coordonatele nodurilor ()
    noduri = [
        (2, 0),
        (3, 0),
        (4, 0),
        (2, 1),
        (3, 1),
        (4, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (2, 5),
        (3, 5),
        (4, 5),
        (2, 6),
        (3, 6),
        (4, 6)
    ]
    muchii = [(0, 1), (0, 4), (0, 3), (1, 2), (1, 4), (2, 5), (2, 4),
              (3, 4), (3, 8), (4, 5), (4, 10), (4, 9), (4, 8), (5, 10),
              (6, 7), (6, 14), (6, 13), (7, 8), (7, 14), (8, 9), (8, 16), (8, 15), (8, 14),
              (9, 10), (9, 16), (10, 11), (10, 18), (10, 17), (10, 16), (11, 12), (11, 18), (12, 19), (12, 18),
              (13, 14), (13, 20), (14, 15), (14, 22), (14, 21), (14, 20), (15, 16), (15, 22), (16, 17),
              (16, 24), (16, 23), (16, 22), (17, 18), (17, 24), (18, 19), (18, 26), (18, 25), (18, 24), (19, 26),
              (20, 21), (21, 22), (22, 23), (22, 28), (22, 27), (23, 24), (23, 28), (24, 25), (24, 29), (24, 28), (25, 26),
              (27, 28), (27, 30), (28, 29), (28, 32), (28, 31), (28, 30), (29, 32),
              (30, 31), (31, 32)

              ]
    scalare = 100
    translatie = 20
    razaPct = 8
    razaPiesa = 15


pygame.init()
culoareEcran = (255, 255, 255)
culoareLinii = (0, 0, 0)

ecran = pygame.display.set_mode(size=(700, 700))

piesaOaie = pygame.image.load('piesa-alba.png')
diametruPiesa = 2 * Graph.razaPiesa
piesaOaie = pygame.transform.scale(piesaOaie, (diametruPiesa, diametruPiesa))
piesaVulpe = pygame.image.load('piesa-rosie.png')
piesaVulpe = pygame.transform.scale(piesaVulpe, (diametruPiesa, diametruPiesa))
piesaSelectata = pygame.image.load('piesa-neagra.png')
piesaSelectata = pygame.transform.scale(piesaSelectata, (diametruPiesa, diametruPiesa))
nodPiesaSelectata = False
coordonateNoduri = [[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]
pieseOi = [[x * 100 + 20, y * 100 + 20] for (x, y) in Graph.noduri[13:]]
nodPiesaSelectata = None
pieseVulpi = [[220, 20], [420, 20]]


def deseneazaEcranJoc():
    ecran.fill(culoareEcran)
    for nod in coordonateNoduri:
        pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                           width=0)  # width=0 face un cerc plin

    for muchie in Graph.muchii:
        p0 = coordonateNoduri[muchie[0]]
        p1 = coordonateNoduri[muchie[1]]
        pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
    for nod in pieseOi:
        ecran.blit(piesaOaie, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    for nod in pieseVulpi:
        ecran.blit(piesaVulpe, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    if nodPiesaSelectata:
        ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
    pygame.display.update()


deseneazaEcranJoc()
rand = 0

print("Muta " + ("vulpe" if rand else "oaie"))
while True:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for nod in coordonateNoduri:
                if distEuclid(pos, nod) <= Graph.razaPct:
                    if rand == 1:
                        piesa = piesaVulpe
                        pieseCurente = pieseVulpi
                    else:
                        piesa = piesaOaie
                        pieseCurente = pieseOi

                    if nod not in pieseOi + pieseVulpi:

                        if nodPiesaSelectata:
                            n0 = coordonateNoduri.index(nod)
                            n1 = coordonateNoduri.index(nodPiesaSelectata)
                            if ((n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii):
                                pieseCurente.remove(nodPiesaSelectata)
                                pieseCurente.append(nod)
                                rand = 1 - rand
                                print("Muta " + ("vulpe" if rand else "oaie"))
                                nodPiesaSelectata = False
                        '''
                        else:
                            pieseCurente.append(nod)
                            rand = 1 - rand
                            print(nod)
                            print(pieseCurente)
                            print("Muta " + ("negru" if rand else "alb"))
                        '''
                    else:
                        if nod in pieseCurente:
                            if nodPiesaSelectata == nod:
                                nodPiesaSelectata = False
                            else:
                                nodPiesaSelectata = nod

                    deseneazaEcranJoc()
                    break


