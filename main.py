import pygame
import sys
import math
import copy


def numara_oi_in_patrat(listaOi):
    """
    functie care verifica daca 9 oi au ajuns in patratul de sus
    :param listaOi:
    :return:
    """
    nr = 0
    for x in listaOi:
        oaie = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
        if oaie in Graph.noduri[:6] + Graph.noduri[8:11]:
            nr += 1
    return nr


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 3
    JMIN = None
    JMAX = None
    GOL = '#'

    '''
    @classmethod
    def initializeaza(cls, display, NR_COLOANE=3, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie = ind // 3  # // inseamna div
            coloana = ind % 3

            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

    # pygame.display.update()
'''
    def __init__(self, pieseOi = None, pieseVulpi = None):
        self.pieseOi = pieseOi or [[x * Graph.scalare + Graph.translatie, y * Graph.scalare + Graph.translatie] for (x, y) in
                   Graph.noduri[13:]]
        self.pieseVulpi = pieseVulpi or [[220, 20], [420, 20]]


    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        rez = len(self.pieseOi) < 9 or numara_oi_in_patrat(self.pieseOi) == 9
        if rez:
            return rez
        else:
            return False

    #TODO: testeaza functia de mutari
    def mutari(self, jucator_opus):
        l_mutari_oi = []
        l_mutari_vulpi = []
        if jucator_opus == 'O':
            for x in self.pieseOi:
                oaie = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                index_punct_oaie = Graph.noduri.index(oaie)
                for muchie in Graph.muchii:
                    if muchie[0] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie, Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                        if muchie[1] - 2 < muchie[0] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            l_mutari_oi.append(lista_oi_noua)
                    elif muchie[1] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie, Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                        if muchie[0] - 2 < muchie[1] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            l_mutari_oi.append(lista_oi_noua)
        elif jucator_opus == 'V':
            for x in self.pieseVulpi:
                vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                index_punct_vulpe = Graph.noduri.index(vulpe)
                for muchie in Graph.muchii:
                    nod = None
                    if muchie[0] == index_punct_vulpe:
                        nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie, Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                    elif muchie[1] == index_punct_vulpe:
                        nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie, Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                    if nod is not None and nod not in self.pieseOi + self.pieseVulpi:
                        lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                        lista_vulpi_noua.remove(x)
                        lista_vulpi_noua.append(nod)
                        l_mutari_vulpi.append(lista_vulpi_noua)
                    elif nod is not None and nod in self.pieseOi:
                        oaie = ((nod[0] - Graph.translatie) // Graph.scalare, (nod[1] - Graph.translatie) // Graph.scalare)
                        index_punct_oaie = Graph.noduri.index(oaie)
                        for muchie2 in Graph.muchii:
                            if muchie2[0] == index_punct_oaie:
                                nod2 = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                                       Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                            elif muchie2[1] == index_punct_oaie:
                                nod2 = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                                       Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                            if nod2 not in self.pieseOi + self.pieseVulpi:
                                lista_oi_noua = copy.deepcopy(self.pieseOi)
                                lista_oi_noua.remove(nod)
                                l_mutari_oi.append(lista_oi_noua)
                                lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                                lista_vulpi_noua.remove(x)
                                lista_vulpi_noua.append(nod2)
                                l_mutari_vulpi.append(lista_vulpi_noua)


        return l_mutari_oi, l_mutari_vulpi

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif t_final == 'remiza':
            return 0
        else:
            return 20 - len(self.pieseOi) - numara_oi_in_patrat(self.pieseOi)

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:3]]) + "\n" +
               " ".join([str(x) for x in self.matr[3:6]]) + "\n" +
               " ".join([str(x) for x in self.matr[6:9]]) + "\n")

        return sir


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
# pieseOi = [[x * Graph.scalare + Graph.translatie, y * Graph.scalare + Graph.translatie] for (x, y) in Graph.noduri[13:]]
nodPiesaSelectata = None
# pieseVulpi = [[220, 20], [420, 20]]


def deseneazaEcranJoc():
    ecran.fill(culoareEcran)
    for nod in coordonateNoduri:
        pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                           width=0)  # width=0 face un cerc plin

    for muchie in Graph.muchii:
        p0 = coordonateNoduri[muchie[0]]
        p1 = coordonateNoduri[muchie[1]]
        pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
    for nod in joc.pieseOi:
        ecran.blit(piesaOaie, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    for nod in joc.pieseVulpi:
        ecran.blit(piesaVulpe, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    if nodPiesaSelectata:
        ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
    pygame.display.update()


joc = Joc()
deseneazaEcranJoc()
rand = 0

print(len(joc.mutari("V")[1]))
# print(len(joc.mutari("O")))
# print(numara_oi_in_patrat([ [320, 20], [220, 120], [220, 20], [420, 20], [320, 120], [220, 220], [420, 120], [420, 220], [320, 220]]))

print("Muta " + ("vulpe" if rand else "oaie"))
while True:
    # if verifica_oi(joc.pieseOi) == True:
        # print(True)
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
                        pieseCurente = joc.pieseVulpi
                    else:
                        piesa = piesaOaie
                        pieseCurente = joc.pieseOi
                        # print(pieseCurente)

                    if nod not in joc.pieseOi + joc.pieseVulpi:

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


