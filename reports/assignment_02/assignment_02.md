# Wprowadzenie do sztucznej inteligencji

**Ćwiczenie 02 - Algorytmy genetyczne i ewolucyjne**

Raport z badań

Semestr letni, rok akademicki 2025/2026

Autor: Wiktor Sosnowski
Numer albumu: 348 561

Warszawa, czerwiec 2026

---

## 1. Treść zadania

Cel zadania polega na implementacji algorytmu genetycznego z mutacją, selekcją ruletkową, krzyżowaniem jednopunktowym oraz sukcesją generacyjną. Zaimplementowany algorytm ma następnie posłużyć do optymalizacji klasycznego, symetrycznego problemu komiwojażera.

Kroki do wykonania:

1. Implementacja algorytmu genetycznego.
2. Zastosowanie algorytmu do rozwiązania problemu komiwojażera. Eksperymentalne dobranie zestawu parametrów, dla którego algorytm daje dobry wynik.
3. Zbadanie, w jaki sposób następujące zmiany wpłyną na rezultaty osiągane przez algorytm:
   - zwiększenie prawdopodobieństwa mutacji,
   - zmiana sposobu selekcji na turniejową.

---

## 2. Interpretacja zadania

Problem komiwojażera (TSP) polega na znalezieniu najkrótszej trasy odwiedzającej każde miasto dokładnie raz i wracającej do punktu startowego. Jest to klasyczny problem optymalizacji kombinatorycznej klasy NP-trudnej.

Algorytm genetyczny naśladuje mechanizmy ewolucji biologicznej. Populacja osobników (permutacji miast) podlega kolejnym generacjom selekcji, krzyżowania i mutacji. Funkcja przystosowania jest odwrotnością długości trasy - im krótsza trasa, tym wyższe przystosowanie.

Selekcja ruletkowa przydziela każdemu osobnikowi prawdopodobieństwo wyboru proporcjonalne do jego przystosowania. Selekcja turniejowa losuje k osobników i wybiera najlepszego - parametr k kontroluje siłę presji selekcyjnej.

Krzyżowanie jednopunktowe dla permutacji: część trasy jednego rodzica (do losowo wybranego punktu) jest kopiowana do potomka, a pozostałe miasta są uzupełniane w kolejności występowania u drugiego rodzica, pomijając już umieszczone. Gwarantuje to poprawność permutacji.

Mutacja swap: z zadanym prawdopodobieństwem zamieniane są pozycje dwóch losowo wybranych miast w trasie.

Sukcesja generacyjna oznacza, że cała populacja jest zastępowana nowym pokoleniem potomków w każdej generacji.

---

## 3. Zbiór danych

Użyto instancji berlin52 z biblioteki TSPLIB. Instancja zawiera 52 miasta o współrzędnych euklidesowych. Odległości obliczano jako odległości euklidesowe zaokrąglone do najbliższej liczby całkowitej, zgodnie ze standardem TSPLIB. Znane optymalne rozwiązanie wynosi 7542.

---

## 4. Opis implementacji

Implementacja składa się z dwóch modułów:

`tsp_utils.py` - wczytywanie plików TSPLIB, budowanie macierzy odległości, obliczanie długości trasy i funkcji przystosowania.

`genetic_algorithm.py` - klasa `GeneticAlgorithm` przyjmująca macierz odległości, rozmiar populacji, prawdopodobieństwo mutacji, liczbę generacji, metodę selekcji i rozmiar turnieju. Implementuje inicjalizację populacji losowymi permutacjami, selekcję ruletkową i turniejową, krzyżowanie jednopunktowe z naprawą permutacji, mutację swap oraz sukcesję generacyjną.

Każdy wariant parametrów był uruchamiany 25 razy z różnym ziarnem generatora (seed 0-24). Wyniki zapisano do plików `results.json` i `raw_lengths.csv`.

---

## 5. Konfiguracja bazowa (Baseline)

Parametry: pop_size = 100, mutation_prob = 0,01, n_generations = 500, selection = roulette.

| Wariant  | min      | średnia  | std     | max      |
|----------|----------|----------|---------|----------|
| baseline | 17876,00 | 20937,24 | 1048,06 | 22481,00 |

Uzyskane wyniki są znacznie powyżej optymalnego rozwiązania (7542), co jest oczekiwanym zachowaniem algorytmu bez elityzmu przy ograniczonej liczbie generacji. Wyniki stanowią punkt odniesienia dla kolejnych eksperymentów.

![Krzywa zbieżności baseline](baseline_convergence.png)

---

## 6. Eksperyment 1 - Rozmiar populacji

Stałe parametry: mutation_prob = 0,01, n_generations = 500, selection = roulette.
Badany zakres: pop_size in {20, 50, 100, 200, 500, 1000, 2000}.

| Wariant         | min      | średnia  | std     | max      |
|-----------------|----------|----------|---------|----------|
| pop_size = 20   | 22158,00 | 24580,00 | 956,84  | 26262,00 |
| pop_size = 50   | 19776,00 | 22290,64 | 1080,27 | 25053,00 |
| pop_size = 100  | 17876,00 | 20937,24 | 1048,06 | 22481,00 |
| pop_size = 200  | 17963,00 | 19702,44 | 1001,07 | 21496,00 |
| pop_size = 500  | 16920,00 | 19629,24 | 920,07  | 21084,00 |
| pop_size = 1000 | 17693,00 | 19247,20 | 781,75  | 20612,00 |
| pop_size = 2000 | 15097,00 | 18710,24 | 1080,44 | 20118,00 |

Średnia długość trasy maleje wraz ze wzrostem rozmiaru populacji - od 24580,00 dla pop_size = 20 do 18710,24 dla pop_size = 2000. Poprawa jest wyraźna w zakresie 20-200, natomiast od 500 wzwyż tempo poprawy spowalnia (różnica średnich między pop_size = 500 a 1000 wynosi 382, między 1000 a 2000 wynosi 537). Najniższe odchylenie standardowe osiągnięto dla pop_size = 1000 (781,75). Przy pop_size = 2000 odchylenie standardowe wzrasta do 1080,44 - porównywalne z mniejszymi populacjami - co wskazuje na niewystarczającą liczbę generacji do zbieżności tak dużej populacji.

![Średnia krzywa zbieżności - rozmiar populacji](exp1_convergence.png)

Wnioski: Większy rozmiar populacji poprawia średnią jakość wyników, jednak zysk maleje przy dużych wartościach. Wzrost odchylenia standardowego przy pop_size = 2000 sugeruje, że przy stałej liczbie generacji (500) bardzo duże populacje nie zdążają się zbiec. Nie oznacza to, że duża populacja jest ogólnie niekorzystna - przy większej liczbie generacji efekt może być inny.

---

## 7. Eksperyment 2 - Prawdopodobieństwo mutacji

Stałe parametry: pop_size = 100, n_generations = 500, selection = roulette.
Badany zakres: mutation_prob in {0,001, 0,003, 0,005, 0,007, 0,01, 0,05, 0,1, 0,3}.

| Wariant               | min      | średnia  | std     | max      |
|-----------------------|----------|----------|---------|----------|
| mutation_prob = 0,001 | 20871,00 | 22498,12 | 961,11  | 24610,00 |
| mutation_prob = 0,003 | 19303,00 | 21660,84 | 1385,32 | 24203,00 |
| mutation_prob = 0,005 | 18653,00 | 21823,20 | 1244,03 | 23962,00 |
| mutation_prob = 0,007 | 18986,00 | 21403,84 | 1278,96 | 23646,00 |
| mutation_prob = 0,01  | 17876,00 | 20937,24 | 1048,06 | 22481,00 |
| mutation_prob = 0,05  | 20111,00 | 21446,00 | 799,25  | 23299,00 |
| mutation_prob = 0,1   | 19843,00 | 21354,32 | 821,29  | 22897,00 |
| mutation_prob = 0,3   | 19387,00 | 21738,32 | 750,77  | 23199,00 |

Najlepsza średnia długość trasy uzyskano dla mutation_prob = 0,01 (20937,24). Niższe wartości dają gorsze wyniki - przy 0,001 średnia wynosi 22498,12, co wskazuje na zbyt słabą eksplorację przestrzeni. Powyżej 0,01 średnia rośnie i stabilizuje się w przedziale 21354-21823, co sugeruje, że zbyt częsta mutacja zaburza wzorce wypracowane przez krzyżowanie. Zależność nie jest monotoniczna - w przedziale 0,001-0,01 obserwujemy nieregularny trend z lokalnym pogorszeniem przy 0,005. Odchylenie standardowe maleje wraz ze wzrostem mutation_prob (od 961 do 751), co oznacza większą stabilność wyników kosztem gorszej średniej.

![Średnia krzywa zbieżności - prawdopodobieństwo mutacji](exp2_convergence.png)

Wnioski: Dla instancji berlin52 przy podanych parametrach bazowych optymalne prawdopodobieństwo mutacji wynosi 0,01. Zbyt mała mutacja ogranicza eksplorację, zbyt duża zaburza dziedziczenie dobrych cech. Znalezione optimum jest specyficzne dla tej konfiguracji - przy innych parametrach optymalna wartość może się różnić.

---

## 8. Eksperyment 3 - Metoda selekcji

Stałe parametry: pop_size = 100, mutation_prob = 0,01, n_generations = 500.
Badane warianty: selekcja ruletkowa oraz selekcja turniejowa z rozmiarem turnieju k in {2, 3, 5, 10}.

| Wariant          | min      | średnia  | std     | max      |
|------------------|----------|----------|---------|----------|
| roulette         | 17876,00 | 20937,24 | 1048,06 | 22481,00 |
| turniej (k = 2)  | 13034,00 | 14443,84 | 949,16  | 16322,00 |
| turniej (k = 3)  | 12028,00 | 13655,16 | 860,98  | 15168,00 |
| turniej (k = 5)  | 11781,00 | 13632,20 | 792,04  | 15078,00 |
| turniej (k = 10) | 12447,00 | 13831,16 | 704,40  | 15659,00 |

Selekcja turniejowa przewyższa ruletkową we wszystkich badanych wariantach. Średnia dla roulette wynosi 20937,24, natomiast najlepszy wariant turniejowy (k = 5) osiąga średnią 13632,20 - poprawa o około 35%. Najlepszy wynik absolutny (min = 11781) również należy do k = 5. Wśród wariantów turniejowych najlepszą średnią osiągają k = 5 (13632,20) i k = 3 (13655,16) - różnica jest niewielka. Przy k = 10 średnia rośnie do 13831,16, a minimum do 12447, co wskazuje na nadmierną presję selekcyjną i utratę różnorodności populacji. Odchylenie standardowe maleje monotonicznie wraz ze wzrostem k (od 949 do 704).

![Średnia krzywa zbieżności - metoda selekcji](exp3_convergence.png)

Wnioski: Selekcja turniejowa daje wyraźnie lepsze wyniki niż ruletkowa dla problemu komiwojażera w badanej konfiguracji. Optymalna wartość rozmiaru turnieju leży w okolicach k = 3-5. Zbyt mały turniej (k = 2) nie wywiera wystarczającej presji selekcyjnej, zbyt duży (k = 10) prowadzi do przedwczesnej zbieżności.

---

## 9. Wnioski końcowe

Najlepsze parametry uzyskane w eksperymentach (przy n_generations = 500):

| Parametr        | Najlepsza badana wartość | Średnia długości trasy |
|-----------------|--------------------------|------------------------|
| pop_size        | 2000                     | 18710,24               |
| mutation_prob   | 0,01                     | 20937,24               |
| metoda selekcji | turniej k = 5            | 13632,20               |

Największy wpływ na jakość wyników miała zmiana metody selekcji z ruletkowej na turniejową - poprawa średniego wyniku o około 35% przy k = 5. Rozmiar populacji ma istotny wpływ, jednak zysk maleje przy dużych wartościach, a przy stałej liczbie generacji bardzo duże populacje wykazują wzrost wariancji. Prawdopodobieństwo mutacji ma umiarkowany wpływ z wyraźnym minimum w okolicach 0,01.

Wszystkie uzyskane wyniki są powyżej optymalnego rozwiązania instancji berlin52 (7542), co wynika z zastosowania sukcesji generacyjnej bez elityzmu oraz ograniczonej liczby generacji.
