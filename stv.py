#!/usr/bin/env python3

NOMBRO_DE_SEĜOJ = 3

class Frakcio:
    FRAKCIOJ = {
        (1, 4): "¼",
        (1, 2): "½",
        (3, 4): "¾",
        (1, 3): "⅓",
        (2, 3): "⅔",
        (1, 5): "⅕",
        (2, 5): "⅖",
        (3, 5): "⅗",
        (4, 5): "⅘",
        (1, 6): "⅙",
        (5, 6): "⅚",
        (1, 8): "⅛",
        (3, 8): "⅜",
        (5, 8): "⅝",
        (7, 8): "⅞"
    }
    def __init__(mem, supro, subo = None):
        if subo == None:
            subo = 1
        minimumo = min(supro, subo)
        for i in range(max(minimumo, 1), 0, -1):
            if supro % i == 0 and subo % i == 0:
                mem.supro = supro // i
                mem.subo = subo // i
                break
        else:
            raise(ValueError("Nevalida frakcio"))

    def __str__(mem):
        if mem.supro % mem.subo == 0:
            return str(mem.supro // mem.subo)
        if mem.supro > mem.subo:
            return (str(mem.supro // mem.subo) + " " +
                    str(Frakcio(mem.supro % mem.subo, mem.subo)))
        if (mem.supro, mem.subo) in Frakcio.FRAKCIOJ:
            return Frakcio.FRAKCIOJ[(mem.supro, mem.subo)]
        return "{}/{}".format(mem.supro, mem.subo)

    def adiciu(mem, alia):
        return Frakcio(mem.supro * alia.subo +
                       alia.supro * mem.subo,
                       mem.subo * alia.subo)

    def subtrahu(mem, alia):
        return Frakcio(mem.supro * alia.subo -
                       alia.supro * mem.subo,
                       mem.subo * alia.subo)

    def dividu(mem, alia):
        return mem.multipliku(Frakcio(alia.subo, alia.supro))

    def multipliku(mem, alia):
        return Frakcio(mem.supro * alia.supro,
                       mem.subo * alia.subo)

    def __ge__(mem, alia):
        return mem.supro * alia.subo >= alia.supro * mem.subo

    def __lt__(mem, alia):
        return mem.supro * alia.subo < alia.supro * mem.subo

class Voĉdono:
    def __init__(mem, ordo, valoro = 1):
        mem.valoro = Frakcio(valoro)
        mem.ordo = ordo

class Kandidato:
    def __init__(mem, nomo):
        mem.poentoj = Frakcio(0)
        mem.nomo = nomo
        mem.voĉdonoj = []
        mem.elektebla = True

    def aldonu_voĉdonon(mem, voĉdono):
        mem.voĉdonoj.append(voĉdono)
        mem.poentoj = mem.poentoj.adiciu(voĉdono.valoro)

def aldonu_voĉdonon(voĉdono):
    for elekto in voĉdono.ordo:
        kandidato = kandidatoj[elekto]
        if kandidato.elektebla:
            kandidato.aldonu_voĉdonon(voĉdono)
            break

def eligu_rezultojn(kandidatoj):
    plej_longa_nomo = 0
    for kandidato in kandidatoj:
        if len(kandidato.nomo) > plej_longa_nomo:
            plej_longa_nomo = len(kandidato.nomo)

    for kandidato in kandidatoj:
        if not kandidato.elektebla:
            continue
        poentoj = kandidato.poentoj
        print("{nomo:{larĝo}} : {poentoj}".format(nomo = kandidato.nomo,
                                                  larĝo = plej_longa_nomo,
                                                  poentoj = poentoj))

kandidatoj = [
    Kandidato("voldemort"),
    Kandidato("malfoy"),
    Kandidato("lestrange"),

    Kandidato("flitwick"),
    Kandidato("sybill"),
    Kandidato("gilderoy"),

    Kandidato("dumbledore"),
    Kandidato("weasley"),
    Kandidato("mcgonagall")
]

nombro_de_voĉdonoj = 0

for voĉdono in [Voĉdono([ 0, 1, 2 ], 9),
                Voĉdono([ 0, 2, 1 ], 45),
                Voĉdono([ 3, 4, 6, 7, 8 ], 18),
                Voĉdono([ 4, 3, 6, 7, 8 ], 18),
                Voĉdono([ 5, 3, 4, 6, 7, 8 ], 4),
                Voĉdono([ 6, 7, 8, 3, 4, 5 ], 30),
                Voĉdono([ 7, 6, 8, 3, 4, 5 ], 15),
                Voĉdono([ 8, 6, 7, 3, 4, 5 ], 5)]:
    aldonu_voĉdonon(voĉdono)
    nombro_de_voĉdonoj += voĉdono.valoro.supro

kvoto = (nombro_de_voĉdonoj + NOMBRO_DE_SEĜOJ) // (NOMBRO_DE_SEĜOJ + 1)
kvoto_frakcio = Frakcio(kvoto)

print("Kvoto = {}\n".format(kvoto))

elektitoj = []

while True:
    eligu_rezultojn(kandidatoj)
    print()

    if len(elektitoj) >= NOMBRO_DE_SEĜOJ:
        break

    for kandidato in kandidatoj:
        if not kandidato.elektebla:
            continue
        if kandidato.poentoj >= kvoto_frakcio:
            superfluaj_voĉdonoj = kandidato.poentoj.subtrahu(kvoto_frakcio)
            frakcio = superfluaj_voĉdonoj.dividu(kandidato.poentoj)

            print("Elektiĝas:           {}\n"
                  "Superfluaj voĉdonoj: {}\n"
                  "Frakcio:             {}\n".
                  format(kandidato.nomo,
                         superfluaj_voĉdonoj,
                         frakcio))

            kandidato.elektebla = False
            elektitoj.append(kandidato)
            
            for voĉdono in kandidato.voĉdonoj:
                voĉdono.valoro = voĉdono.valoro.multipliku(frakcio)
                aldonu_voĉdonon(voĉdono)
            break
    else:
        malplej_da_poentoj = Frakcio(nombro_de_voĉdonoj)
        malplej_bona_kandidato = None

        for kandidato in kandidatoj:
            if not kandidato.elektebla:
                continue
            if kandidato.poentoj < malplej_da_poentoj:
                malplej_da_poentoj = kandidato.poentoj
                malplej_bona_kandidato = kandidato

        if malplej_bona_kandidato == None:
            print("Nenio fareblas!")
            break

        kandidato = malplej_bona_kandidato

        print("Foriĝas: {}\n".format(kandidato.nomo))
        kandidato.elektebla = False
        for voĉdono in kandidato.voĉdonoj:
            aldonu_voĉdonon(voĉdono)

print("Elektitoj: {}".format(", ".join(map(lambda e: e.nomo, elektitoj))))
