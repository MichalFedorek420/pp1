"""To jest szablon do stworzenia rozwiazania"""

import time, numpy as np
import sortowania, wykresy, uklad
import gauss, gaussjordan, cholesky, banachiewicz
import iteracjaprosta, iteracjaseidela

class Zadanie:
    def __init__(self, n = 200, M = 5, N = 24):
        """Konstruktor okreslajacy parametry eksperymentu"""
        self.n = n                          # maksymalny rozmiar macierzy
        self.M = M                          # liczba pomiarow
        self.N = N                          # liczba rozmiarow
        self.rozmiary = []                  # lista rozmiarow ukladow
        self.czasy = [[], []]   # lista czasow rozwiazywania
        
    def mierz_czas(self, metoda, k):
        """Metoda mierzaca czas sortowan losowych list o dlugosci k"""
        uklad1=uklad.Uklad(k)
        if k is None:
            k = self.dlugosc
        self.lista = []
        czas = 0.0
        for _ in range(self.M):
            uklad1.losuj_uklad()
            iteracjapro = iteracjaprosta.IteracjaProsta(uklad1)
            banach = banachiewicz.Banachiewicz(uklad1)
            if metoda == 1:
                stoper = time.time()
                banach.rozklad()
                banach.rozwiaz_trojkatny_dolny()
                banach.rozwiaz_trojkatny_gorny()
                stoper = time.time() - stoper
            else:
                stoper = time.time()
                iteracjapro.przygotuj()
                iteracjapro.iteruj_roznica(1.0e-9,1)
                stoper = time.time() - stoper
            czas = czas + stoper
        
        return czas/self.M
    
    def badaj_zlozonosc(self, metoda, opis):
        # okreslamy krok zmiany rozmiaru ukladu
        krok = self.n / self.N
        self.rozmiary = []
        self.czasy[metoda-1] = []
        for i in range(self.N):
            self.rozmiary.append(int((i+1)*krok))   
            self.czasy[metoda-1].append(
                self.mierz_czas(metoda, self.rozmiary[i])
            )
            print(self.rozmiary[i], self.czasy[metoda-1][i])
        wykres = wykresy.Wykresy(self.n)
        wykres.badaj_zlozonosc(
            rozmiary = self.rozmiary,
            czasy = self.czasy[metoda-1],
            nazwa = opis
        )
    
    def porownaj_metody(self, nazwa_metody1, nazwa_metody2):
        krok = self.n / self.N
        for i in range(self.N):
            k = int((i+1)*krok)
            self.rozmiary.append(k)
            t1 = self.mierz_czas(1, k)
            t2 = self.mierz_czas(2, k)
            self.czasy[0].append(t1)
            self.czasy[1].append(t2)
            print(f"{k} \t {t1:10.8f} \t {t2:10.8f}")
        wykres = wykresy.Wykresy(self.n)
        wykres.porownaj_algorytmy(
            self.rozmiary,
            self.czasy,
            nazwa_metody1,
            nazwa_metody2
        )