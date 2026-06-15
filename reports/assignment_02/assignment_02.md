# Wprowadzenie do sztucznej inteligencji

**Cwiczenie 02 - Algorytmy genetyczne i ewolucyjne**

Raport z badan

Semestr letni, rok akademicki 2025/2026

Autor: Wiktor Sosnowski
Numer albumu: 348 561

Warszawa, czerwiec 2026

---

## 1. Tresc zadania

Cel zadania polega na implementacji algorytmu genetycznego z mutacja, selekcja ruletkowa, krzyzowaniem jednopunktowym oraz sukcesja generacyjna. Zaimplementowany algorytm ma nastepnie posluzyc do optymalizacji klasycznego, symetrycznego problemu komiwojazera.

Kroki do wykonania:

1. Implementacja algorytmu genetycznego.
2. Zastosowanie algorytmu do rozwiazania problemu komiwojazera. Eksperymentalne dobranie zestawu parametrow, dla ktorego algorytm daje dobry wynik.
3. Zbadanie, w jaki sposob nastepujace zmiany wplyna na rezultaty osiagane przez algorytm:
   - zwiekszenie prawdopodobienstwa mutacji,
   - zmiana sposobu selekcji na turniejowa.

---

## 2. Interpretacja zadania

Problem komiwojazera (TSP) polega na znalezieniu najkrotszej trasy odwiedzajacej kazde miasto dokladnie raz i wracajacej do punktu startowego. Jest to klasyczny problem optymalizacji kombinatorycznej klasy NP-trudnej.

Algorytm genetyczny nasliaduje mechanizmy ewolucji biologicznej. Populacja osobnikow (permutacji miast) podlega kolejnym generacjom selekcji, krzyzowania i mutacji. Funkcja przystosowania jest odwrotnoscia dlugosci trasy - im krotsza trasa, tym wyzsze przystosowanie.

Selekcja ruletkowa przydziela kazdemu osobnikowi prawdopodobienstwo wyboru proporcjonalne do jego przystosowania. Selekcja turniejowa losuje k osobnikow i wybiera najlepszego - parametr k kontroluje sile presji selekcyjnej.

Krzyzowanie jednopunktowe dla permutacji: czesc trasy jednego rodzica (do losowo wybranego punktu) jest kopiowana do potomka, a pozostale miasta sa uzupelniane w kolejnosci wystepowania u drugiego rodzica, pomijajac juz umieszczone. Gwarantuje to poprawnosc permutacji.

Mutacja swap: z zadanym prawdopodobienstwem zamieniane sa pozycje dwoch losowo wybranych miast w trasie.

Sukcesja generacyjna oznacza, ze cala populacja jest zastepowana nowym pokoleniem potomkow w kazdej generacji.

---

## 3. Zbior danych

Uzyto instancji berlin52 z biblioteki TSPLIB. Instancja zawiera 52 miasta o wspolrzednych euklidesowych. Odleglosci obliczano jako odleglosci euklidesowe zaokraglone do najblizszej liczby calkowitej, zgodnie ze standardem TSPLIB. Znane optymalne rozwiazanie wynosi 7542.

---

## 4. Opis implementacji

Implementacja sklada sie z dwoch modulow:

`tsp_utils.py` - wczytywanie plikow TSPLIB, budowanie macierzy odleglosci, obliczanie dlugosci trasy i funkcji przystosowania.

`genetic_algorithm.py` - klasa `GeneticAlgorithm` przyjmujaca macierz odleglosci, rozmiar populacji, prawdopodobienstwo mutacji, liczbe generacji, metode selekcji i rozmiar turnieju. Implementuje inicjalizacje populacji losowymi permutacjami, selekcje ruletkowa i turniejowa, krzyzowanie jednopunktowe z naprawa permutacji, mutacje swap oraz sukcesje generacyjna.

Kazdy wariant parametrow byl uruchamiany 25 razy z roznym ziarnem generatora (seed 0-24). Wyniki zapisano do plikow `results.json` i `raw_lengths.csv`.

---

## 5. Konfiguracja bazowa (Baseline)

Parametry: pop_size = 100, mutation_prob = 0,01, n_generations = 500, selection = roulette.

| Wariant  | min       | srednia   | std     | max       |
|----------|-----------|-----------|---------|-----------|
| baseline | 17876,00  | 20937,24  | 1048,06 | 22481,00  |

Uzyskane wyniki sa znacznie powyzej optymalnego rozwiazania (7542), co jest oczekiwanym zachowaniem algorytmu bez elityzmu przy ograniczonej liczbie generacji. Wyniki stanowia punkt odniesienia dla kolejnych eksperymentow.

![Krzywa zbieznosci baseline](baseline_convergence.png)

---

## 6. Eksperyment 1 - Rozmiar populacji

Stale parametry: mutation_prob = 0,01, n_generations = 500, selection = roulette.
Badany zakres: pop_size in {20, 50, 100, 200, 500, 1000, 2000}.

| Wariant          | min       | srednia   | std     | max       |
|------------------|-----------|-----------|---------|-----------|
| pop_size = 20    | 22158,00  | 24580,00  | 956,84  | 26262,00  |
| pop_size = 50    | 19776,00  | 22290,64  | 1080,27 | 25053,00  |
| pop_size = 100   | 17876,00  | 20937,24  | 1048,06 | 22481,00  |
| pop_size = 200   | 17963,00  | 19702,44  | 1001,07 | 21496,00  |
| pop_size = 500   | 16920,00  | 19629,24  | 920,07  | 21084,00  |
| pop_size = 1000  | 17693,00  | 19247,20  | 781,75  | 20612,00  |
| pop_size = 2000  | 15097,00  | 18710,24  | 1080,44 | 20118,00  |

Srednia dlugosc trasy maleje wraz ze wzrostem rozmiaru populacji - od 24580,00 dla pop_size = 20 do 18710,24 dla pop_size = 2000. Poprawa jest wyrazna w zakresie 20-200, natomiast od 500 wzwyz tempo poprawy spowalnia (roznica srednich miedzy pop_size = 500 a 1000 wynosi 382, miedzy 1000 a 2000 wynosi 537). Najnizsze odchylenie standardowe osiagnieto dla pop_size = 1000 (781,75). Przy pop_size = 2000 odchylenie standardowe wzrasta do 1080,44 - porownywalne z mniejszymi populacjami - co wskazuje na niewystarczajaca liczbe generacji do zbieznosci tak duzej populacji.

![Srednia krzywa zbieznosci - rozmiar populacji](exp1_convergence.png)

Wnioski: Wiekszy rozmiar populacji poprawia srednia jakosc wynikow, jednak zysk maleje przy duzych wartosciach. Wzrost odchylenia standardowego przy pop_size = 2000 sugeruje, ze przy stalej liczbie generacji (500) bardzo duze populacje nie zdazaja sie zbiegac. Nie oznacza to, ze duza populacja jest ogolnie niekorzystna - przy wiekszej liczbie generacji efekt moze byc inny.

---

## 7. Eksperyment 2 - Prawdopodobienstwo mutacji

Stale parametry: pop_size = 100, n_generations = 500, selection = roulette.
Badany zakres: mutation_prob in {0,001, 0,003, 0,005, 0,007, 0,01, 0,05, 0,1, 0,3}.

| Wariant                   | min       | srednia   | std     | max       |
|---------------------------|-----------|-----------|---------|-----------|
| mutation_prob = 0,001     | 20871,00  | 22498,12  | 961,11  | 24610,00  |
| mutation_prob = 0,003     | 19303,00  | 21660,84  | 1385,32 | 24203,00  |
| mutation_prob = 0,005     | 18653,00  | 21823,20  | 1244,03 | 23962,00  |
| mutation_prob = 0,007     | 18986,00  | 21403,84  | 1278,96 | 23646,00  |
| mutation_prob = 0,01      | 17876,00  | 20937,24  | 1048,06 | 22481,00  |
| mutation_prob = 0,05      | 20111,00  | 21446,00  | 799,25  | 23299,00  |
| mutation_prob = 0,1       | 19843,00  | 21354,32  | 821,29  | 22897,00  |
| mutation_prob = 0,3       | 19387,00  | 21738,32  | 750,77  | 23199,00  |

Najlepsza srednia dlugosc trasy uzyskano dla mutation_prob = 0,01 (20937,24). Nizsze wartosci daja gorsze wyniki - przy 0,001 srednia wynosi 22498,12, co wskazuje na zbyt slaba eksploracje przestrzeni. Powyzej 0,01 srednia rosnie i stabilizuje sie w przedziale 21354-21823, co sugeruje ze zbyt czesta mutacja zaburza wzorce wypracowane przez krzyzowanie. Zaleznosc nie jest monotoniczna - w przedziale 0,001-0,01 obserwujemy nieregularny trend z lokalnym pogorszeniem przy 0,005, natomiast od 0,01 wzwyz srednie sa do siebie zblizone. Odchylenie standardowe maleje wraz ze wzrostem mutation_prob (od 961 do 751), co oznacza wieksza stabilnosc wynikow kosztem gorszej srednicy.

![Srednia krzywa zbieznosci - prawdopodobienstwo mutacji](exp2_convergence.png)

Wnioski: Dla instancji berlin52 przy podanych parametrach bazowych optymalne prawdopodobienstwo mutacji wynosi 0,01. Zbyt mala mutacja ogranicza eksploracje, zbyt duza zaburza dziedziczenie dobrych cech. Znalezione optimum jest specyficzne dla tej konfiguracji - przy innych parametrach optymalna wartosc moze sie roznic.

---

## 8. Eksperyment 3 - Metoda selekcji

Stale parametry: pop_size = 100, mutation_prob = 0,01, n_generations = 500.
Badane warianty: selekcja ruletkowa oraz selekcja turniejowa z rozmiarem turnieju k in {2, 3, 5, 10}.

| Wariant              | min       | srednia   | std    | max       |
|----------------------|-----------|-----------|--------|-----------|
| roulette             | 17876,00  | 20937,24  | 1048,06| 22481,00  |
| turniej (k = 2)      | 13034,00  | 14443,84  | 949,16 | 16322,00  |
| turniej (k = 3)      | 12028,00  | 13655,16  | 860,98 | 15168,00  |
| turniej (k = 5)      | 11781,00  | 13632,20  | 792,04 | 15078,00  |
| turniej (k = 10)     | 12447,00  | 13831,16  | 704,40 | 15659,00  |

Selekcja turniejowa przewyzsza ruletkowa we wszystkich badanych wariantach. Srednia dla roulette wynosi 20937,24, natomiast najlepszy wariant turniejowy (k = 5) osiaga srednia 13632,20 - poprawa o okolo 35%. Najlepszy wynik absolutny (min = 11781) rowniez nalezy do k = 5. Wsrod wariantow turniejowych najlepsza srednia osiagaja k = 5 (13632,20) i k = 3 (13655,16) - roznica jest niewielka. Przy k = 10 srednia rosnie do 13831,16, a minimum do 12447, co wskazuje na nadmierna presje selekcyjna i utrate roznorodnosci populacji. Odchylenie standardowe maleje monotonicznie wraz ze wzrostem k (od 949 do 704).

![Srednia krzywa zbieznosci - metoda selekcji](exp3_convergence.png)

Wnioski: Selekcja turniejowa daje wyraznie lepsze wyniki niz ruletkowa dla problemu komiwojazera w badanej konfiguracji. Optymalna wartosc rozmiaru turnieju lezy w okolicach k = 3-5. Zbyt maly turniej (k = 2) nie wywiera wystarczajacej presji selekcyjnej, zbyt duzy (k = 10) prowadzi do przedwczesnej zbieznosci.

---

## 9. Wnioski koncowe

Najlepsze parametry uzyskane w eksperymentach (przy n_generations = 500):

| Parametr        | Najlepsza badana wartosc | Srednia dlugosci trasy |
|-----------------|--------------------------|------------------------|
| pop_size        | 2000                     | 18710,24               |
| mutation_prob   | 0,01                     | 20937,24               |
| metoda selekcji | turniej k = 5            | 13632,20               |

Najwyzszy wplyw na jakosc wynikow miala zmiana metody selekcji z ruletkowej na turniejowa - poprawa sredniego wyniku o okolo 35% przy k = 5. Rozmiar populacji ma istotny wplyw, jednak zysk maleje przy duzych wartosciach, a przy stalej liczbie generacji bardzo duze populacje wykazuja wzrost wariancji. Prawdopodobienstwo mutacji ma umiarkowany wplyw z wyraznym minimum w okolicach 0,01.

Wszystkie uzyskane wyniki sa powyzej optymalnego rozwiazania instancji berlin52 (7542), co wynika z zastosowania sukcesji generacyjnej bez elityzmu oraz ograniczonej liczby generacji.
