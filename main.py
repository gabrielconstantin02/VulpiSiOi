import pygame
import sys
import math
import copy
import time


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        print("A castigat " + final)
        return True

    return False


def coliniare(p, q, r):
    p1, p2 = p[0], p[1]
    q1, q2 = q[0], q[1]
    r1, r2 = r[0], r[1]
    det = q1 * r2 + p1 * q2 + p2 * r1 - p2 * q1 - q2 * r1 - p1 * r2
    if det == 0:
        return True
    return False

def exista_oi_de_capturat(stare):
    for x in stare.tabla_joc.pieseVulpi:
        vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
        index_punct_vulpe = Graph.noduri.index(vulpe)
        for muchie in Graph.muchii:
            nod = None
            if muchie[0] == index_punct_vulpe:
                nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                       Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
            elif muchie[1] == index_punct_vulpe:
                nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                       Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
            if nod is not None and nod in stare.tabla_joc.pieseOi:
                # print("OAIE")
                oaie = (
                    (nod[0] - Graph.translatie) // Graph.scalare, (nod[1] - Graph.translatie) // Graph.scalare)
                index_punct_oaie = Graph.noduri.index(oaie)
                for muchie2 in Graph.muchii:
                    nod2 = None
                    if muchie2[0] == index_punct_oaie:
                        nod2 = [Graph.noduri[muchie2[1]][0] * Graph.scalare + Graph.translatie,
                                Graph.noduri[muchie2[1]][1] * Graph.scalare + Graph.translatie]
                    elif muchie2[1] == index_punct_oaie:
                        nod2 = [Graph.noduri[muchie2[0]][0] * Graph.scalare + Graph.translatie,
                                Graph.noduri[muchie2[0]][1] * Graph.scalare + Graph.translatie]
                    if nod2 is not None and nod2 not in stare.tabla_joc.pieseOi + stare.tabla_joc.pieseVulpi and coliniare(x, nod, nod2):
                        return True
    return False


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
    JMIN = None
    JMAX = None

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

    def __init__(self, pieseOi=None, pieseVulpi=None):
        self.pieseOi = pieseOi or [[x * Graph.scalare + Graph.translatie, y * Graph.scalare + Graph.translatie] for
                                   (x, y) in
                                   Graph.noduri[13:]]
        self.pieseVulpi = pieseVulpi or [[220, 20], [420, 20]]

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        rez = False
        if len(self.pieseOi) < 9:
            rez = "v"
        if numara_oi_in_patrat(self.pieseOi) == 9:
            rez = "o"
        if rez:
            return rez
        else:
            return False

    # TODO: testeaza functia de mutari
    def mutari(self, jucator_opus):
        # l_mutari_oi = []
        # l_mutari_vulpi = []
        l_mutari = []
        if jucator_opus == 'o':
            for x in self.pieseOi:
                oaie = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                index_punct_oaie = Graph.noduri.index(oaie)
                for muchie in Graph.muchii:
                    if muchie[0] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                        if muchie[1] - 2 < muchie[0] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            # l_mutari_oi.append(lista_oi_noua)
                            l_mutari.append(Joc(lista_oi_noua, self.pieseVulpi))
                    elif muchie[1] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                        if muchie[0] - 2 < muchie[1] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            # l_mutari_oi.append(lista_oi_noua)
                            l_mutari.append(Joc(lista_oi_noua, self.pieseVulpi))
        elif jucator_opus == 'v':
            # presupunem ca nu putem captura oi
            ok = False
            for x in self.pieseVulpi:
                vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                index_punct_vulpe = Graph.noduri.index(vulpe)
                for muchie in Graph.muchii:
                    nod = None
                    if muchie[0] == index_punct_vulpe:
                        nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                    elif muchie[1] == index_punct_vulpe:
                        nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                    if nod is not None and nod not in self.pieseOi + self.pieseVulpi and not ok:
                        lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                        lista_vulpi_noua.remove(x)
                        lista_vulpi_noua.append(nod)
                        # l_mutari_vulpi.append(lista_vulpi_noua)
                        l_mutari.append(Joc(self.pieseOi, lista_vulpi_noua))
                    elif nod is not None and nod in self.pieseOi:
                        # print("OAIE")
                        oaie = (
                        (nod[0] - Graph.translatie) // Graph.scalare, (nod[1] - Graph.translatie) // Graph.scalare)
                        index_punct_oaie = Graph.noduri.index(oaie)
                        for muchie2 in Graph.muchii:
                            nod2 = None
                            if muchie2[0] == index_punct_oaie:
                                nod2 = [Graph.noduri[muchie2[1]][0] * Graph.scalare + Graph.translatie,
                                        Graph.noduri[muchie2[1]][1] * Graph.scalare + Graph.translatie]
                            elif muchie2[1] == index_punct_oaie:
                                nod2 = [Graph.noduri[muchie2[0]][0] * Graph.scalare + Graph.translatie,
                                        Graph.noduri[muchie2[0]][1] * Graph.scalare + Graph.translatie]
                            if nod2 is not None and nod2 not in self.pieseOi + self.pieseVulpi and coliniare(x, nod, nod2):
                                # print(nod2)
                                if not ok:
                                    # l_mutari_vulpi = []
                                    l_mutari = []
                                    ok = True

                                lista_oi_noua = copy.deepcopy(self.pieseOi)
                                lista_oi_noua.remove(nod)
                                # l_mutari_oi.append(lista_oi_noua)
                                lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                                lista_vulpi_noua.remove(x)
                                lista_vulpi_noua.append(nod2)
                                # l_mutari_vulpi.append(lista_vulpi_noua)
                                l_mutari.append(Joc(lista_oi_noua, lista_vulpi_noua))

        return l_mutari

    def estimeaza_scor(self, adancime, j_curent):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif j_curent == 'v':
            return 20 - len(self.pieseOi) - numara_oi_in_patrat(self.pieseOi)
        else:
            return len(self.pieseOi) + numara_oi_in_patrat(self.pieseOi)

    def __str__(self):
        sir = "  "
        sir += self.display_line(0, 3) + "  "
        sir += self.display_line(3, 6)
        sir += self.display_line(6, 13)
        sir += self.display_line(13, 20)
        sir += self.display_line(20, 27) + "  "
        sir += self.display_line(27, 30) + "  "
        sir += self.display_line(30, 33)

        return sir

    def display_line(self, i, j):
        sir = ""
        for x in Graph.noduri[i:j]:
            nod = [x[0] * Graph.scalare + Graph.translatie, x[1] * Graph.scalare + Graph.translatie]
            if nod in self.pieseOi:
                sir += "o"
            elif nod in self.pieseVulpi:
                sir += "v"
            else:
                sir += "#"
        sir += "\n"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


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
              (20, 21), (21, 22), (22, 23), (22, 28), (22, 27), (23, 24), (23, 28), (24, 25), (24, 29), (24, 28),
              (25, 26),
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
nodOaieSelectata = False
coordonateNoduri = [[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]
# pieseOi = [[x * Graph.scalare + Graph.translatie, y * Graph.scalare + Graph.translatie] for (x, y) in Graph.noduri[13:]]
nodPiesaSelectata = None
nodOaieSelectata = None
# pieseVulpi = [[220, 20], [420, 20]]

ADANCIME_MAX = 6


def deseneazaEcranJoc():
    ecran.fill(culoareEcran)
    for nod in coordonateNoduri:
        pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                           width=0)  # width=0 face un cerc plin

    for muchie in Graph.muchii:
        p0 = coordonateNoduri[muchie[0]]
        p1 = coordonateNoduri[muchie[1]]
        pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
    for nod in stare_curenta.tabla_joc.pieseOi:
        ecran.blit(piesaOaie, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    for nod in stare_curenta.tabla_joc.pieseVulpi:
        ecran.blit(piesaVulpe, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    if nodPiesaSelectata:
        ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
    pygame.display.update()


raspuns_valid = False
while not raspuns_valid:
    tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
    if tip_algoritm in ['1', '2']:
        raspuns_valid = True
    else:
        print("Nu ati ales o varianta corecta.")
# initializare jucatori
raspuns_valid = False
while not raspuns_valid:
    Joc.JMIN = input("Doriti sa jucati cu V sau cu O? ").lower()
    if (Joc.JMIN in ['v', 'o']):
        raspuns_valid = True
    else:
        print("Raspunsul trebuie sa fie V sau O.")
Joc.JMAX = 'o' if Joc.JMIN == 'v' else 'v'

# initializare tabla
tabla_curenta = Joc()
print("Tabla initiala")
print(str(tabla_curenta))

# creare stare initiala
stare_curenta = Stare(tabla_curenta, 'v', ADANCIME_MAX)

deseneazaEcranJoc()
rand = 0

# print(len(tabla_curenta.mutari("v")))
# print(len(joc.mutari("O")))
# print(numara_oi_in_patrat([ [320, 20], [220, 120], [220, 20], [420, 20], [320, 120], [220, 220], [420, 120], [420, 220], [320, 220]]))

# joc.pieseOi = [ [320, 20], [220, 120], [220, 20], [420, 20], [320, 120], [220, 220], [420, 120], [420, 220], [320, 220]]
# print(joc.final())

# print("Muta " + ("vulpe" if rand else "oaie"))
while True:
    # if verifica_oi(joc.pieseOi) == True:
    # print(True)
    if stare_curenta.j_curent == Joc.JMIN:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for nod in coordonateNoduri:
                    if distEuclid(pos, nod) <= Graph.razaPct:
                        # print(len(stare_curenta.tabla_joc.mutari("V")))
                        if stare_curenta.j_curent == 'v':
                            piesa = piesaVulpe
                            pieseCurente = stare_curenta.tabla_joc.pieseVulpi
                        else:
                            piesa = piesaOaie
                            pieseCurente = stare_curenta.tabla_joc.pieseOi
                            # print(pieseCurente)

                        if nod not in stare_curenta.tabla_joc.pieseOi + stare_curenta.tabla_joc.pieseVulpi:

                            if nodPiesaSelectata:
                                n0 = coordonateNoduri.index(nod)
                                n1 = coordonateNoduri.index(nodPiesaSelectata)
                                if stare_curenta.j_curent == 'o' and ((n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii) and n1 > n0 - 2:
                                    pieseCurente.remove(nodPiesaSelectata)
                                    pieseCurente.append(nod)
                                    # rand = 1 - rand
                                    # print("Muta " + ("vulpe" if rand else "oaie"))
                                    nodPiesaSelectata = False
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                elif not nodOaieSelectata and ((n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii) and not exista_oi_de_capturat(stare_curenta) and stare_curenta.j_curent == 'v':
                                    pieseCurente.remove(nodPiesaSelectata)
                                    pieseCurente.append(nod)
                                    # rand = 1 - rand
                                    # print("Muta " + ("vulpe" if rand else "oaie"))
                                    nodPiesaSelectata = False
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                elif nodOaieSelectata:
                                    n2 = coordonateNoduri.index(nodOaieSelectata)
                                    if ((n0, n2) in Graph.muchii or (n2, n0) in Graph.muchii) and ((n2, n1) in Graph.muchii or (n1, n2) in Graph.muchii) and coliniare(nod, nodPiesaSelectata, nodOaieSelectata):
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        stare_curenta.tabla_joc.pieseOi.remove(nodOaieSelectata)
                                        nodPiesaSelectata = False
                                        nodOaieSelectata = False
                                        if not exista_oi_de_capturat(stare_curenta):
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
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
                                    nodOaieSelectata = False
                                else:
                                    nodPiesaSelectata = nod
                            elif stare_curenta.j_curent == 'v' and nodPiesaSelectata:
                                if nod in stare_curenta.tabla_joc.pieseOi:
                                    if nodOaieSelectata == nod:
                                        nodOaieSelectata = False
                                    else:
                                        nodOaieSelectata = nod
                        # print(tabla_curenta)
                        print("Tabla dupa mutarea jucatorului")
                        print(str(stare_curenta))
                        deseneazaEcranJoc()
                        break

    else:  # jucatorul e JMAX (calculatorul)
        # Mutare calculator

        # preiau timpul in milisecunde de dinainte de mutare
        t_inainte = int(round(time.time() * 1000))
        nr_oi_inainte = len(stare_curenta.tabla_joc.pieseOi)
        if tip_algoritm == '1':
            stare_actualizata = min_max(stare_curenta)
        else:  # tip_algoritm==2
            stare_actualizata = alpha_beta(-500, 500, stare_curenta)
        stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
        nr_oi_curent = len(stare_curenta.tabla_joc.pieseOi)
        print("Tabla dupa mutarea calculatorului")
        print(str(stare_curenta))

        deseneazaEcranJoc()
        # preiau timpul in milisecunde de dupa mutare
        t_dupa = int(round(time.time() * 1000))
        print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

        if afis_daca_final(stare_curenta):
            break

        # S-a realizat o mutare. Schimb jucatorul cu cel opus
        if not (exista_oi_de_capturat(stare_curenta) and nr_oi_inainte != nr_oi_curent) or stare_curenta.j_curent == 'o':
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
