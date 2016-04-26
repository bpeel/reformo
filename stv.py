#!/usr/bin/env python3

NOMBRO_DE_SEĜOJ = 3

class Voĉdono:
    def __init__(mem, ordo):
        mem.valoro = 1.0
        mem.ordo = ordo

class Kandidato:
    def __init__(mem, nomo):
        mem.poentoj = 0
        mem.nomo = nomo
        mem.voĉdonoj = []
        mem.elektebla = True

    def aldonu_voĉdonon(mem, voĉdono):
        mem.voĉdonoj.append(voĉdono)
        mem.poentoj += voĉdono.valoro

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

for voĉdono in ([ [ 0, 1, 2 ] ] * 9 +
                [ [ 0, 2, 1 ] ] * 45 +
                [ [ 3, 6 ] ] * 18 +
                [ [ 4, 3, 6 ] ] * 18 +
                [ [ 5, 3, 6 ] ] * 4 +
                [ [ 6, 7, 8 ] ] * 30 +
                [ [ 7, 6, 8 ] ] * 15 +
                [ [ 8, 6, 7 ] ] * 5):
    aldonu_voĉdonon(Voĉdono(voĉdono))
    nombro_de_voĉdonoj += 1

kvoto = (nombro_de_voĉdonoj + NOMBRO_DE_SEĜOJ) // (NOMBRO_DE_SEĜOJ + 1)

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
        if kandidato.poentoj >= kvoto:
            print("Elektiĝas: {}".format(kandidato.nomo))
            kandidato.elektebla = False
            elektitoj.append(kandidato)
            frakcio = (kandidato.poentoj - kvoto) / kandidato.poentoj
            
            for voĉdono in kandidato.voĉdonoj:
                voĉdono.valoro *= frakcio
                aldonu_voĉdonon(voĉdono)
            break
    else:
        malplej_da_poentoj = nombro_de_voĉdonoj
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

        print("Foriĝas: {}".format(kandidato.nomo))
        kandidato.elektebla = False
        for voĉdono in kandidato.voĉdonoj:
            aldonu_voĉdonon(voĉdono)

print("Elektitoj: {}".format(", ".join(map(lambda e: e.nomo, elektitoj))))
