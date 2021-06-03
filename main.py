import pygame
import sys
import math
import copy
import time
import statistics

from pygame import K_SPACE, K_ESCAPE


def marcheaza_oi():
    """
    functie care marcheaza oile daca au castigat
    :return:
    """
    for nod in stare_curenta.tabla_joc.pieseOi:
        ecran.blit(piesaSelectata, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    pygame.display.update()


def marcheaza_vulpi():
    """
    functie care marcheaza vulpile daca au castigat
    :return:
    """
    for nod in stare_curenta.tabla_joc.pieseVulpi:
        ecran.blit(piesaSelectata, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    pygame.display.update()


def afis_daca_final(stare_curenta):
    """
    functie de verificare a starii finale
    :param stare_curenta: starea in care ne aflam
    :return: True daca este o sare finala
    """
    final = stare_curenta.tabla_joc.final()
    if final:
        print("A castigat " + final)
        if final == "v":
            marcheaza_vulpi()
        else:
            marcheaza_oi()
        return True

    return False


def coliniare(p, q, r):
    """
    functie care verifica daca 3 puncte sunt coliniare prin calcularea determinantului
    :param p: primul punct de coordonate
    :param q: al doilea punct
    :param r: al treailea punct
    :return: True daca determinantul este 0
    """
    p1, p2 = p[0], p[1]
    q1, q2 = q[0], q[1]
    r1, r2 = r[0], r[1]
    det = q1 * r2 + p1 * q2 + p2 * r1 - p2 * q1 - q2 * r1 - p1 * r2
    if det == 0 and not(p1 == q1 and p2 == q2) and not(r1 == q1 and r2 == q2) and not(p1 == r1 and p2 == r2):
        return True
    return False


def exista_oi_de_capturat(stare, x=None):
    """
    functie care verifica daca exista oi de capturat
    :param stare: starea pentru care calculam
    :return: True daca exista oi ce pot fi capturate
    """
    if x is not None:
        vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
        index_punct_vulpe = Graph.noduri.index(vulpe)
        # pentru fiecare muchie
        for muchie in Graph.muchii:
            nod = None
            if muchie[0] == index_punct_vulpe:
                nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                       Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
            elif muchie[1] == index_punct_vulpe:
                nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                       Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
            #aca gasim un nod care e in legatura directa cu vulpea si e oaie
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
                    # daca dupa oaie avem spatiu in linie dreapta astfel incat sa putem sari cu vulpea
                    if nod2 is not None and nod2 not in stare.tabla_joc.pieseOi + stare.tabla_joc.pieseVulpi and coliniare(
                            x, nod, nod2):
                        return True
        return False
    else:
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
                        if nod2 is not None and nod2 not in stare.tabla_joc.pieseOi + stare.tabla_joc.pieseVulpi and coliniare(
                                x, nod, nod2):
                            return True
        return False


def nr_oi_in_pericol(pieseOi, pieseVulpi):
    """
    functie care calculeaza cate oi sunt in pericol de capturare
    :param pieseOi: lista de pozitii cu oi
    :param pieseVulpi: lista de pozitii cu vulpi
    :return: numarul de oi in pericol
    """
    nr = 0
    for x in pieseVulpi:
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
            if nod is not None and nod in pieseOi:
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
                    if nod2 is not None and nod2 not in pieseOi + pieseVulpi and coliniare(
                            x, nod, nod2):
                        nr += 1
    return nr


def numara_piese_in_patrat(listaOi, listaVulpi):
    """
    functie care numara cate piese au ajuns in patratul de sus
    :param listaOi: lista de pozitii pt piesele oi
    :param listaVulpi: lista de pozitii pt piesele vulpe
    :return: nr de piese din patratul de sus
    """
    nr = 0
    for x in listaOi:
        oaie = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
        if oaie in Graph.noduri[:6] + Graph.noduri[8:11]:
            nr += 1
    for x in listaVulpi:
        vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
        if vulpe in Graph.noduri[:6] + Graph.noduri[8:11]:
            nr += 1
    return nr


class Joc:
    """
    Clasa care defineste jocul.
    """
    JMIN = None
    JMAX = None

    def __init__(self, pieseOi=None, pieseVulpi=None):
        self.pieseOi = pieseOi or [[x * Graph.scalare + Graph.translatie, y * Graph.scalare + Graph.translatie] for
                                   (x, y) in
                                   Graph.noduri[13:]]
        self.pieseVulpi = pieseVulpi or [[220, 20], [420, 20]]

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        """
        functie care testeaza daca am ajuns la finalul jocului
        :return: v - au castigat vulpile | o - au castigat oilea | False - nu s-a ajuns intr-o stare finala
        """
        rez = False
        # daca au ramas oi mai putine de 9
        if len(self.pieseOi) < 9:
            rez = "v"
        # daca am umplut patratul de sus
        if numara_piese_in_patrat(self.pieseOi, self.pieseVulpi) == 9:
            posibilitate_captura = False
            for x in self.pieseVulpi:
                vulpe = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                if vulpe in Graph.noduri[:6] + Graph.noduri[8:11] and exista_oi_de_capturat(stare_curenta, x):
                    posibilitate_captura = True
            # daca in patratul de sus nu exista vulpi care sa ne poate captura oile
            if not posibilitate_captura:
                rez = "o"
        if rez:
            return rez
        else:
            return False

    def mutari(self, jucator_opus):
        """
        functie pentru generarea mutarilor posibile
        :param jucator_opus: id-ul jucatorului opus
        :return: lista de mutari posibile
        """

        l_mutari = []
        # daca jucatorul opus e oaie
        if jucator_opus == 'o':
            # pentru fiecare oaie existenta pe tabla generam toate mutarile posibile
            for x in self.pieseOi:
                oaie = ((x[0] - Graph.translatie) // Graph.scalare, (x[1] - Graph.translatie) // Graph.scalare)
                index_punct_oaie = Graph.noduri.index(oaie)
                # pentru toate muchiile din graf
                for muchie in Graph.muchii:
                    # verificam e o muchie pe care putem merge
                    if muchie[0] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[1]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[1]][1] * Graph.scalare + Graph.translatie]
                        # verificam daca e liber si ne deplasam in orice directie, dar nu in jos
                        if muchie[1] - 2 < muchie[0] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            l_mutari.append(Joc(lista_oi_noua, self.pieseVulpi))
                    elif muchie[1] == index_punct_oaie:
                        nod = [Graph.noduri[muchie[0]][0] * Graph.scalare + Graph.translatie,
                               Graph.noduri[muchie[0]][1] * Graph.scalare + Graph.translatie]
                        # verificam daca e liber si ne deplasam in orice directie, dar nu in jos
                        if muchie[0] - 2 < muchie[1] and nod not in self.pieseOi + self.pieseVulpi:
                            lista_oi_noua = copy.deepcopy(self.pieseOi)
                            lista_oi_noua.remove(x)
                            lista_oi_noua.append(nod)
                            l_mutari.append(Joc(lista_oi_noua, self.pieseVulpi))
        # daca jucatorul opus e vulpe
        elif jucator_opus == 'v':
            # presupunem ca nu putem captura oi
            ok = False
            # pentru fiecare vulpe
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
                    # daca e spatiu liber si putem muta pe linie
                    if nod is not None and nod not in self.pieseOi + self.pieseVulpi and not ok:
                        lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                        lista_vulpi_noua.remove(x)
                        lista_vulpi_noua.append(nod)
                        l_mutari.append(Joc(self.pieseOi, lista_vulpi_noua))
                    # daca la acea pozitie exista o oaie
                    elif nod is not None and nod in self.pieseOi:
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
                            # daca exista spatiu in linie dreapta astfel incat sa putem sa sarim peste acea oaie (capturam)
                            if nod2 is not None and nod2 not in self.pieseOi + self.pieseVulpi and coliniare(x, nod,
                                                                                                             nod2):
                                if not ok:
                                    l_mutari = []
                                    ok = True

                                lista_oi_noua = copy.deepcopy(self.pieseOi)
                                lista_oi_noua.remove(nod)
                                lista_vulpi_noua = copy.deepcopy(self.pieseVulpi)
                                lista_vulpi_noua.remove(x)
                                lista_vulpi_noua.append(nod2)
                                l_mutari.append(Joc(lista_oi_noua, lista_vulpi_noua))

        return l_mutari

    def estimeaza_scor(self, adancime, mod):
        """
        functie de estimare a scorului
        :param adancime: adancimea din arbore
        :param mod: modul de calculare al estimarii (1 sau 2)
        :return: scorul estimat
        """
        t_final = self.final()
        # daca am castigat
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        # daca a castigat oponentul
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif mod == "1":
            # daca e vulple, atunci trebuie sa prioritizam instantele in care reducem numarul de oi si numarul de piese ce au intrat in patratul de sus
            if self.JMAX == 'v':
                # scadeam din numarul de oi capturate numarul de piese ce au intrat in patratul de sus
                # astfel vom incuraja capturarea de oi si blocare lor in incercarea de a intra in patrat
                return 20 - len(self.pieseOi) - numara_piese_in_patrat(self.pieseOi, self.pieseVulpi)
            else:
                # daca e oaie, prioritisam dupa numarul de oi intrate in patrat si ramase in viata, deci le adunam intre ele
                # astfel vom incuraja mentinerea numarului de oi si intrarea lor in patrat
                return len(self.pieseOi) + numara_piese_in_patrat(self.pieseOi, self.pieseVulpi)
        else:
            if self.JMAX == 'v':
                # din numarul de oi capturate scadem numarul de piese din patrat, dar adunam numarul de oi aflate in pericol deoarece le putem captura reducand astfel sansele oponentului
                return 20 - len(self.pieseOi) + nr_oi_in_pericol(self.pieseOi, self.pieseVulpi) - numara_piese_in_patrat(self.pieseOi, self.pieseVulpi)
            else:
                # adunam numarul de oi ramase in viata cu numarul de piese din patrat, dar scadem numarul de oi aflate in pericol deoarece disparitia lor ne reduce sansa de a castiga
                # in plus fata de estimarea precedenta, penalizam deoarece exista oi aflate in pericol de capturare
                return len(self.pieseOi) + numara_piese_in_patrat(self.pieseOi, self.pieseVulpi) - nr_oi_in_pericol(self.pieseOi, self.pieseVulpi)

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
        """
        functie de afisare a unei linii din tabla
        :param i: indicele de pornire
        :param j: capatul
        :return: string-ul format pt afisare
        """
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
    """
    algoritmul min-max
    :param stare: primeste starea pentru care calculam
    :return: starea modificata (noua stare)
    """
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, estimare)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    global noduri_generate
    # crestem numarul de noduri generate
    noduri_generate += len(stare.mutari_posibile)
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
    """
    algoritmul alpha-beta
    :param alpha: capatul din stanga al intervalului
    :param beta: capatul din dreapta al intervalului
    :param stare: starea pentru care calculam
    :return: noua stare
    """
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, estimare)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    global noduri_generate
    # crestem numarul de noduri generate
    noduri_generate += len(stare.mutari_posibile)
    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        # sortare descrescatoare dupa scor
        stare.mutari_posibile = sorted(stare.mutari_posibile, key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime, estimare), reverse=True)

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:

        # sortare crescatoare dupa scor
        stare.mutari_posibile = sorted(stare.mutari_posibile, key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime, estimare))

        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def distEuclid(p0, p1):
    """
    functie de calculat distanta dintre 2 puncte
    :param p0: primul punct de coordonate
    :param p1: al doilea punct
    :return:
    """
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
    razaPct = 9
    razaPiesa = 15


pygame.init()
pygame.display.set_caption("Constantin Gabriel-Adrian --- Vulpi si oi ")
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
# pieseVulpi = [[220, 20], [420, 20]]


def deseneazaEcranJoc():
    """
    functia care deseneaza exrtanul jocului
    :return:
    """
    ecran.fill(culoareEcran)
    for nod in coordonateNoduri:
        pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                           width=0)

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


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


def deseneaza_alegeri(display):
    """
    functie de desenare a butoanelor pentru ca utilizatorul sa aleaga
    :param display: ecranul din pygame (fereastra)
    :return: alegerile facute de utilizator
    """
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="1"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="2")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="vulpi", valoare="v"),
            Buton(display=display, w=35, h=30, text="oi", valoare="o")
        ],
        indiceSelectat=0)
    btn_fst = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=175, h=30, text="Primul jucator: vulpi", valoare="v"),
            Buton(display=display, w=175, h=30, text="Primul jucator: oi", valoare="o")
        ],
        indiceSelectat=1)
    btn_dif = GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=125, h=30, text="Incepator", valoare="1"),
            Buton(display=display, w=125, h=30, text="Mediu", valoare="3"),
            Buton(display=display, w=125, h=30, text="Avansat", valoare="4"),
        ],
        indiceSelectat=1)
    btn_est = GrupButoane(
        top=30,
        left=300,
        listaButoane=[
            Buton(display=display, w=125, h=30, text="Estimare 1", valoare="1"),
            Buton(display=display, w=125, h=30, text="Estimare 2", valoare="2"),
        ],
        indiceSelectat=1)
    btn_mod = GrupButoane(
        top=310,
        left=30,
        listaButoane=[
            Buton(display=display, w=125, h=30, text="PvP", valoare="1"),
            Buton(display=display, w=125, h=30, text="Player vs PC", valoare="2"),
            Buton(display=display, w=125, h=30, text="PC vs PC", valoare="3"),
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=410, left=30, w=40, h=30, text="PLAY", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_fst.deseneaza()
    btn_dif.deseneaza()
    btn_est.deseneaza()
    btn_mod.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_fst.selecteazaDupacoord(pos):
                            if not btn_dif.selecteazaDupacoord(pos):
                                if not btn_est.selecteazaDupacoord(pos):
                                    if not btn_mod.selecteazaDupacoord(pos):
                                        if ok.selecteazaDupacoord(pos):
                                            display.fill((0, 0, 0))  # stergere ecran
                                            # deseneazaEcranJoc()
                                            return btn_juc.getValoare(), btn_alg.getValoare(), btn_fst.getValoare(), btn_dif.getValoare(), btn_est.getValoare(), btn_mod.getValoare()
        pygame.display.update()


Joc.JMIN, tip_algoritm, primul_jucator, nivel, estimare, game_mod = deseneaza_alegeri(ecran)
Joc.JMAX = 'o' if Joc.JMIN == 'v' else 'v'
# initializare tabla
tabla_curenta = Joc()
print("Tabla initiala")
print(str(tabla_curenta))
# creare stare initiala
ADANCIME_MAX = int(nivel)
# print(ADANCIME_MAX)
stare_curenta = Stare(tabla_curenta, primul_jucator, ADANCIME_MAX)

deseneazaEcranJoc()
rand = 0
time_arr = []
nod_arr = []
noduri_generate = 0
nr_mutari_pc = 0
nr_mutari_juc = 0
t_inainte_joc = int(round(time.time() * 1000))

afisare = False
t_inainte_jucator = None
# Player vs PC
if game_mod == "2":
    while True:
        pressed_keys = pygame.key.get_pressed()
        # daca s-a apasat escape ca sa se iasa din joc
        if pressed_keys[K_ESCAPE]:
            t_dupa_joc = int(round(time.time() * 1000))
            print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
            print("Numar de mutari calculator: " + str(nr_mutari_pc))
            print("Numar de mutari jucator: " + str(nr_mutari_juc))
            pygame.quit()
            sys.exit()
        # daca e randul jucatorului
        if stare_curenta.j_curent == Joc.JMIN:
            if t_inainte_jucator is None:
                t_inainte_jucator = int(round(time.time() * 1000))
            if not afisare:
                print("\nMuta " + ("vulpe" if Joc.JMIN == 'v' else "oaie") + "\n")
                afisare = True
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if stare_curenta.j_curent == 'v':
                                piesa = piesaVulpe
                                pieseCurente = stare_curenta.tabla_joc.pieseVulpi
                            else:
                                piesa = piesaOaie
                                pieseCurente = stare_curenta.tabla_joc.pieseOi

                            if nod not in stare_curenta.tabla_joc.pieseOi + stare_curenta.tabla_joc.pieseVulpi:

                                if nodPiesaSelectata:
                                    n0 = coordonateNoduri.index(nod)
                                    n1 = coordonateNoduri.index(nodPiesaSelectata)
                                    # daca e oaie si face o mutare valida
                                    if stare_curenta.j_curent == 'o' and (
                                            (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii) and n1 > n0 - 2:
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                                        nr_mutari_juc += 1
                                    # daca e vulpe si nu exista oi de capturat
                                    elif not nodOaieSelectata and ((n0, n1) in Graph.muchii or (
                                    n1, n0) in Graph.muchii) and not exista_oi_de_capturat(
                                            stare_curenta) and stare_curenta.j_curent == 'v':
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                                        nr_mutari_juc += 1
                                    # daca vrea sa captureze o oaie
                                    elif nodOaieSelectata:
                                        n2 = coordonateNoduri.index(nodOaieSelectata)
                                        # daca poate sari peste ea in linie dreapta
                                        if ((n0, n2) in Graph.muchii or (n2, n0) in Graph.muchii) and (
                                                (n2, n1) in Graph.muchii or (n1, n2) in Graph.muchii) and coliniare(nod,
                                                                                                                    nodPiesaSelectata,
                                                                                                                    nodOaieSelectata):
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            stare_curenta.tabla_joc.pieseOi.remove(nodOaieSelectata)
                                            nodPiesaSelectata = False
                                            nodOaieSelectata = False
                                            # daca nu mai exista alte oi de capturat cu aceasta piesa
                                            nr_mutari_juc += 1
                                            if not exista_oi_de_capturat(stare_curenta, nod):
                                                print("Tabla dupa mutarea jucatorului")
                                                print(str(stare_curenta))
                                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                                afisare = False
                                                t_dupa_jucator = int(round(time.time() * 1000))
                                                print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                            else:
                                if nod in pieseCurente:
                                    # daca deselectam piesa
                                    if nodPiesaSelectata == nod:
                                        nodPiesaSelectata = False
                                        nodOaieSelectata = False
                                    else: # selectam piesa
                                        nodPiesaSelectata = nod
                                elif stare_curenta.j_curent == 'v' and nodPiesaSelectata:
                                    if nod in stare_curenta.tabla_joc.pieseOi:
                                        # deselectam oaie
                                        if nodOaieSelectata == nod:
                                            nodOaieSelectata = False
                                        else: # selectam oaie de capturat
                                            nodOaieSelectata = nod
                            deseneazaEcranJoc()
                            break
            # daca am ajuns la finalul jocului
            if afis_daca_final(stare_curenta):
                break
        else:  # jucatorul e JMAX (calculatorul)
            t_inainte_jucator = None
            noduri_generate = 0
            # Mutare calculator
            print("\nMuta " + ("vulpe" if stare_curenta.j_curent == 'v' else "oaie") + "\n")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_oi_inainte = len(stare_curenta.tabla_joc.pieseOi)
            vulpi_inainte = stare_curenta.tabla_joc.pieseVulpi
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
            time_arr.append(t_dupa - t_inainte)
            nod_arr.append(noduri_generate)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            print("Timp minim: " + str(min(time_arr)))
            print("Timp maxim: " + str(max(time_arr)))
            print("Timp mediu: " + str(sum(time_arr)/len(time_arr)))
            print("Timp median: " + str(statistics.median(time_arr)))
            print("\nEstimare algoritm: " + str(stare_curenta.tabla_joc.estimeaza_scor(ADANCIME_MAX, estimare)))
            print("\nNumar noduri generate: " + str(noduri_generate))
            print("Noduri minim: " + str(min(nod_arr)))
            print("Noduri maxim: " + str(max(nod_arr)))
            print("Noduri mediu: " + str(sum(nod_arr)/len(nod_arr)))
            print("Noduri median: " + str(statistics.median(nod_arr)))

            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus daca nu sunt vulpe si am capturi de facut
            vulpe = None
            for x in stare_curenta.tabla_joc.pieseVulpi:
                if x not in vulpi_inainte:
                    vulpe = x
            if not (vulpe is not None and exista_oi_de_capturat(
                    stare_curenta, vulpe) and nr_oi_inainte != nr_oi_curent) or stare_curenta.j_curent == 'o':
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            nr_mutari_pc += 1

    t_dupa_joc = int(round(time.time() * 1000))

    print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
    print("Numar de mutari calculator: " + str(nr_mutari_pc))
    print("Numar de mutari jucator: " + str(nr_mutari_juc))

# PvP
elif game_mod == "1":
    t_inainte_jucator2 = None
    nr_mutari_juc2 = 0
    while True:
        pressed_keys = pygame.key.get_pressed()
        # daca s-a apasat escape ca sa se iasa din joc
        if pressed_keys[K_ESCAPE]:
            t_dupa_joc = int(round(time.time() * 1000))
            print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
            print("Numar de mutari jucator2: " + str(nr_mutari_juc2))
            print("Numar de mutari jucator: " + str(nr_mutari_juc))
            pygame.quit()
            sys.exit()
        # daca e randul jucatorului
        if stare_curenta.j_curent == Joc.JMIN:
            if t_inainte_jucator is None:
                t_inainte_jucator = int(round(time.time() * 1000))
            if not afisare:
                print("\nMuta " + ("vulpe" if Joc.JMIN == 'v' else "oaie") + "\n")
                afisare = True
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if stare_curenta.j_curent == 'v':
                                piesa = piesaVulpe
                                pieseCurente = stare_curenta.tabla_joc.pieseVulpi
                            else:
                                piesa = piesaOaie
                                pieseCurente = stare_curenta.tabla_joc.pieseOi

                            if nod not in stare_curenta.tabla_joc.pieseOi + stare_curenta.tabla_joc.pieseVulpi:

                                if nodPiesaSelectata:
                                    n0 = coordonateNoduri.index(nod)
                                    n1 = coordonateNoduri.index(nodPiesaSelectata)
                                    # daca e oaie si face o mutare valida
                                    if stare_curenta.j_curent == 'o' and (
                                            (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii) and n1 > n0 - 2:
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                                        nr_mutari_juc += 1
                                    # daca e vulpe si nu exista oi de capturat
                                    elif not nodOaieSelectata and ((n0, n1) in Graph.muchii or (
                                    n1, n0) in Graph.muchii) and not exista_oi_de_capturat(
                                            stare_curenta) and stare_curenta.j_curent == 'v':
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                                        nr_mutari_juc += 1
                                    # daca vrea sa captureze o oaie
                                    elif nodOaieSelectata:
                                        n2 = coordonateNoduri.index(nodOaieSelectata)
                                        # daca poate sari peste ea in linie dreapta
                                        if ((n0, n2) in Graph.muchii or (n2, n0) in Graph.muchii) and (
                                                (n2, n1) in Graph.muchii or (n1, n2) in Graph.muchii) and coliniare(nod,
                                                                                                                    nodPiesaSelectata,
                                                                                                                    nodOaieSelectata):
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            stare_curenta.tabla_joc.pieseOi.remove(nodOaieSelectata)
                                            nodPiesaSelectata = False
                                            nodOaieSelectata = False
                                            # daca nu mai exista alte oi de capturat cu aceasta piesa
                                            nr_mutari_juc += 1
                                            if not exista_oi_de_capturat(stare_curenta, nod):
                                                print("Tabla dupa mutarea jucatorului")
                                                print(str(stare_curenta))
                                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                                afisare = False
                                                t_dupa_jucator = int(round(time.time() * 1000))
                                                print("Jucatorul a gandit timp de " + str(t_dupa_jucator - t_inainte_jucator) + " milisecunde.")
                            else:
                                if nod in pieseCurente:
                                    # daca deselectam piesa
                                    if nodPiesaSelectata == nod:
                                        nodPiesaSelectata = False
                                        nodOaieSelectata = False
                                    else: # selectam piesa
                                        nodPiesaSelectata = nod
                                elif stare_curenta.j_curent == 'v' and nodPiesaSelectata:
                                    if nod in stare_curenta.tabla_joc.pieseOi:
                                        # deselectam oaie
                                        if nodOaieSelectata == nod:
                                            nodOaieSelectata = False
                                        else: # selectam oaie de capturat
                                            nodOaieSelectata = nod
                            deseneazaEcranJoc()
                            break
            # daca am ajuns la finalul jocului
            if afis_daca_final(stare_curenta):
                break
        else:  # jucatorul e JMAX (calculatorul)
            if t_inainte_jucator2 is None:
                t_inainte_jucator2 = int(round(time.time() * 1000))
            if not afisare:
                print("\nMuta " + ("oaie" if Joc.JMIN == 'v' else "vulpe") + "\n")
                afisare = True
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if stare_curenta.j_curent == 'v':
                                piesa = piesaVulpe
                                pieseCurente = stare_curenta.tabla_joc.pieseVulpi
                            else:
                                piesa = piesaOaie
                                pieseCurente = stare_curenta.tabla_joc.pieseOi

                            if nod not in stare_curenta.tabla_joc.pieseOi + stare_curenta.tabla_joc.pieseVulpi:

                                if nodPiesaSelectata:
                                    n0 = coordonateNoduri.index(nod)
                                    n1 = coordonateNoduri.index(nodPiesaSelectata)
                                    # daca e oaie si face o mutare valida
                                    if stare_curenta.j_curent == 'o' and (
                                            (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii) and n1 > n0 - 2:
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator2 = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(
                                            t_dupa_jucator2 - t_inainte_jucator2) + " milisecunde.")
                                        nr_mutari_juc2 += 1
                                    # daca e vulpe si nu exista oi de capturat
                                    elif not nodOaieSelectata and ((n0, n1) in Graph.muchii or (
                                            n1, n0) in Graph.muchii) and not exista_oi_de_capturat(
                                        stare_curenta) and stare_curenta.j_curent == 'v':
                                        pieseCurente.remove(nodPiesaSelectata)
                                        pieseCurente.append(nod)
                                        nodPiesaSelectata = False
                                        print("Tabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        afisare = False
                                        t_dupa_jucator2 = int(round(time.time() * 1000))
                                        print("Jucatorul a gandit timp de " + str(
                                            t_dupa_jucator2 - t_inainte_jucator2) + " milisecunde.")
                                        nr_mutari_juc2 += 1
                                    # daca vrea sa captureze o oaie
                                    elif nodOaieSelectata:
                                        n2 = coordonateNoduri.index(nodOaieSelectata)
                                        # daca poate sari peste ea in linie dreapta
                                        if ((n0, n2) in Graph.muchii or (n2, n0) in Graph.muchii) and (
                                                (n2, n1) in Graph.muchii or (n1, n2) in Graph.muchii) and coliniare(nod,
                                                                                                                    nodPiesaSelectata,
                                                                                                                    nodOaieSelectata):
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            stare_curenta.tabla_joc.pieseOi.remove(nodOaieSelectata)
                                            nodPiesaSelectata = False
                                            nodOaieSelectata = False
                                            # daca nu mai exista alte oi de capturat cu aceasta piesa
                                            nr_mutari_juc2 += 1
                                            if not exista_oi_de_capturat(stare_curenta, nod):
                                                print("Tabla dupa mutarea jucatorului")
                                                print(str(stare_curenta))
                                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                                afisare = False
                                                t_dupa_jucator2 = int(round(time.time() * 1000))
                                                print("Jucatorul a gandit timp de " + str(
                                                    t_dupa_jucator2 - t_inainte_jucator2) + " milisecunde.")
                            else:
                                if nod in pieseCurente:
                                    # daca deselectam piesa
                                    if nodPiesaSelectata == nod:
                                        nodPiesaSelectata = False
                                        nodOaieSelectata = False
                                    else:  # selectam piesa
                                        nodPiesaSelectata = nod
                                elif stare_curenta.j_curent == 'v' and nodPiesaSelectata:
                                    if nod in stare_curenta.tabla_joc.pieseOi:
                                        # deselectam oaie
                                        if nodOaieSelectata == nod:
                                            nodOaieSelectata = False
                                        else:  # selectam oaie de capturat
                                            nodOaieSelectata = nod
                            deseneazaEcranJoc()
                            break
            # daca am ajuns la finalul jocului
            if afis_daca_final(stare_curenta):
                break

    t_dupa_joc = int(round(time.time() * 1000))

    print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
    print("Numar de mutari jucator2: " + str(nr_mutari_juc2))
    print("Numar de mutari jucator: " + str(nr_mutari_juc))

# PC vs PC
else:

    # initializare tabla
    tabla_curenta2 = Joc()
    tabla_curenta2.JMAX = 'v' if Joc.JMIN == 'v' else 'o'
    tabla_curenta2.JMIN = 'o' if tabla_curenta2.JMAX == 'v' else 'o'
    stare_curenta2 = Stare(tabla_curenta2, primul_jucator, ADANCIME_MAX)

    time_arr2 = []
    nod_arr2 = []
    nr_mutari_pc2 = 0
    print(tabla_curenta.JMAX, tabla_curenta2.JMAX)
    print(stare_curenta.j_curent, stare_curenta2.j_curent)
    while True:
        pressed_keys = pygame.key.get_pressed()
        # daca s-a apasat escape ca sa se iasa din joc
        if pressed_keys[K_ESCAPE]:
            t_dupa_joc = int(round(time.time() * 1000))
            print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
            print("Numar de mutari calculator: " + str(nr_mutari_pc))
            print("Numar de mutari calculator2: " + str(nr_mutari_pc2))
            pygame.quit()
            sys.exit()
        # daca e randul jucatorului
        if stare_curenta2.j_curent == tabla_curenta2.JMAX:
            noduri_generate = 0
            # Mutare calculator"
            print("\nMuta " + ("vulpe" if stare_curenta2.j_curent == 'v' else "oaie") + "\n")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_oi_inainte = len(stare_curenta2.tabla_joc.pieseOi)
            vulpi_inainte = stare_curenta2.tabla_joc.pieseVulpi
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta2)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta2)
            stare_curenta2.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            nr_oi_curent = len(stare_curenta2.tabla_joc.pieseOi)
            print("Tabla dupa mutarea calculatorului2")
            print(str(stare_curenta2))

            deseneazaEcranJoc()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            time_arr2.append(t_dupa - t_inainte)
            nod_arr2.append(noduri_generate)
            print("Calculatorul2 a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            print("Timp minim: " + str(min(time_arr2)))
            print("Timp maxim: " + str(max(time_arr2)))
            print("Timp mediu: " + str(sum(time_arr2) / len(time_arr2)))
            print("Timp median: " + str(statistics.median(time_arr2)))
            print("\nEstimare algoritm: " + str(stare_curenta2.tabla_joc.estimeaza_scor(ADANCIME_MAX, estimare)))
            print("\nNumar noduri generate: " + str(noduri_generate))
            print("Noduri minim: " + str(min(nod_arr2)))
            print("Noduri maxim: " + str(max(nod_arr2)))
            print("Noduri mediu: " + str(sum(nod_arr2) / len(nod_arr2)))
            print("Noduri median: " + str(statistics.median(nod_arr2)))

            if afis_daca_final(stare_curenta2):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus daca nu sunt vulpe si am capturi de facut
            vulpe = None
            for x in stare_curenta2.tabla_joc.pieseVulpi:
                if x not in vulpi_inainte:
                    vulpe = x
            if not (vulpe is not None and exista_oi_de_capturat(
                    stare_curenta2, vulpe) and nr_oi_inainte != nr_oi_curent) or stare_curenta2.j_curent == 'o':
                stare_curenta2.j_curent = Joc.jucator_opus(stare_curenta2.j_curent)
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                estimare = "2" if estimare == "1" else "1"
            nr_mutari_pc2 += 1
        else:
            t_inainte_jucator = None
            noduri_generate = 0
            # Mutare calculator
            print("\nMuta " + ("vulpe" if stare_curenta.j_curent == 'v' else "oaie") + "\n")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_oi_inainte = len(stare_curenta.tabla_joc.pieseOi)
            vulpi_inainte = stare_curenta.tabla_joc.pieseVulpi
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            stare_curenta2.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            nr_oi_curent = len(stare_curenta.tabla_joc.pieseOi)
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            deseneazaEcranJoc()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            time_arr.append(t_dupa - t_inainte)
            nod_arr.append(noduri_generate)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            print("Timp minim: " + str(min(time_arr)))
            print("Timp maxim: " + str(max(time_arr)))
            print("Timp mediu: " + str(sum(time_arr)/len(time_arr)))
            print("Timp median: " + str(statistics.median(time_arr)))
            print("\nEstimare algoritm: " + str(stare_curenta.tabla_joc.estimeaza_scor(ADANCIME_MAX, estimare)))
            print("\nNumar noduri generate: " + str(noduri_generate))
            print("Noduri minim: " + str(min(nod_arr)))
            print("Noduri maxim: " + str(max(nod_arr)))
            print("Noduri mediu: " + str(sum(nod_arr)/len(nod_arr)))
            print("Noduri median: " + str(statistics.median(nod_arr)))

            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus daca nu sunt vulpe si am capturi de facut
            vulpe = None
            for x in stare_curenta.tabla_joc.pieseVulpi:
                if x not in vulpi_inainte:
                    vulpe = x
            if not (vulpe is not None and exista_oi_de_capturat(
                    stare_curenta, vulpe) and nr_oi_inainte != nr_oi_curent) or stare_curenta.j_curent == 'o':
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                stare_curenta2.j_curent = Joc.jucator_opus(stare_curenta2.j_curent)
                estimare = "2" if estimare == "1" else "1"
            nr_mutari_pc += 1

    t_dupa_joc = int(round(time.time() * 1000))

    print("Jocul a durat " + str(t_dupa_joc - t_inainte_joc) + " milisecunde.")
    print("Numar de mutari calculator: " + str(nr_mutari_pc))
    print("Numar de mutari calculator2: " + str(nr_mutari_pc2))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
