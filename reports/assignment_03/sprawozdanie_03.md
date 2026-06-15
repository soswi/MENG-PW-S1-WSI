# Wprowadzenie do sztucznej inteligencji

**Cwiczenie 3 - Dwuosobowe gry deterministyczne**

Raport z badan

---

Semestr letni 2025/2026

Autor: Wiktor Sosnowski

Numer albumu: 348 561

Data: 15.06.2026

---

## Tresc zadania

Cel zadania polega na implementacji algorytmu min-max z przycinaniem alfa-beta i zastosowaniu go do gry w kolko i krzyzyk (tic-tac-toe). Do rozwiazania zadania mozna wykorzystac gotowa implementacje gry w kolko i krzyzyk, dostepna pod adresem: [moja strona domowa]/WSI/ttt.zip. Gra ta posiada prosty interfejs tekstowy, zaimplementowanego gracza "ludzkiego" i losowego, jak rowniez "zaslepke" dla gracza wykorzystujacego algorytm min-max.

Kroki do wykonania:

1. Uruchomienie gry dla gracza losowego i ludzkiego (w celu zapoznania sie ze sposobem dzialania gry).
2. Implementacja algorytmu min-max z przycinaniem alfa-beta. Ocena gracza min-max (porownanie jego zachowania w starciu z graczem ludzkim w stosunku do gracza losowego).
3. Rozszerzenie gry o mozliwosc konfiguracji roznych poziomow glebokosci drzewa przeszukiwan dla dwoch graczy min-max. Uruchomienie gry dla dwoch graczy min-max o roznej glebokosci drzewa przeszukiwan (dla kilku wartosci tego parametru) i skomentowanie wplywu glebokosci przeszukiwania drzewa gry na jakosc wynikow uzyskiwanych przez graczy.

Punkty 2 i 3 nalezy wykonac dla standardowego rozmiaru planszy (3x3), jak rowniez dla jednego wybranego wiekszego rozmiaru.

---

## Interpretacja zadania

Celem zadania jest implementacja algorytmu min-max z przycinaniem alfa-beta jako gracza w grze w kolko i krzyzyk. Algorytm min-max przeszukuje drzewo mozliwych stanow gry: gracz maksymalizujacy (MAX) wybiera ruch dajacy najwyzsza ocene, gracz minimalizujacy (MIN) - najnizsza. Przycinanie alfa-beta eliminuje galecie drzewa, ktore nie moga wplynac na wynik - dzieki temu liczba sprawdzanych stanow jest istotnie mniejsza niz przy pelnym przeszukaniu.

Przy ograniczonej glebokosci przeszukiwania stany nieterminalne ocenia funkcja heurystyczna. Zastosowana heurystyka liczy linie (rzedy, kolumny, przekatne) otwarte dla danego gracza - tj. takie, w ktorych przeciwnik nie postawil jeszcze zadnego znaku - i zwraca roznice tych liczb znormalizowana do przedzialu (-1, 1).

Jakosc gracza oceniana jest przez porownanie wynikow meczow z graczem losowym oraz przez mecze MinMax przeciwko MinMax przy roznych glebokosciach przeszukiwania.

---

## Opis implementacji

Implementacja opiera sie na dostarczonej strukturze kodu. Wypelniona zostala zaslepka `MinMaxPlayer` w pliku `p_minmax.py`. Plik `ttt.py` zostal rozszerzony o osobne parametry glebokosci dla obu graczy oraz o konfigurowalny rozmiar planszy przez argumenty wiersza polecen.

Metoda `minimax` przyjmuje perspektywe gracza MAX (przekazana przez `make_move` jako `side`), parametry alfa-beta z wartosciami domyslnymi `-inf`/`inf` oraz flage `maximizing`. Na kazdym poziomie rekurencji klonuje plansze, rejestruje ruch i wywoluje sie rekurencyjnie z zamieniona flaga. Przycinanie alfa-beta nastepuje po aktualizacji odpowiedniego ograniczenia: jesli `beta <= alpha`, galaz jest odcinana.

Wywolanie z wiersza polecen:

```
python ttt.py <typ_gracza1> <typ_gracza2> <rozmiar_planszy> <glebokoscz1> <glebokoscz2>
```

Przyklad - MinMax (glebokoscz 3) jako 'o' vs MinMax (glebokoscz 6) jako 'x' na planszy 4x4:

```
python ttt.py minmax minmax 4 3 6
```

---

## Obserwacje z gry z czlowiekiem

### Gracz ludzki vs gracz losowy (plansza 3x3)

Gra z graczem losowym jest latwa do wygrania. Gracz losowy nie reaguje na sytuacje na planszy - nie blokuje ruchow prowadzacych do wygranej przeciwnika i nie probuje samemu ukonczyc linii. W rozegrane partii gracz ludzki zajal srodek planszy (pole 4), a gracz losowy nie zablokował zadnego zagrozenia - gra zostala wygrana w 5 ruchach kompletujac kolumne srodkowa (pola 1, 4, 7).

### Gracz ludzki vs MinMax (plansza 3x3, glebokoscz = 9)

Zachowanie MinMax jest wyraznie odmienne od gracza losowego. Po zajeciu srodka przez czlowieka MinMax natychmiast zajal naroznik (pole 0), tworzac wlasne zagrozenie i jednoczesnie ograniczajac mozliwosci przeciwnika. W kolejnych ruchach MinMax konsekwentnie blokowal kazde zagrozenie ze strony ludzkiego gracza i zmuszal go do reagowania zamiast atakowania. Partia zakonczyla sie remisem po 9 ruchach - gracz ludzki nie byl w stanie wygrac mimo probowania roznych ruchow.

Roznica w stosunku do gracza losowego jest natychmiastowo widoczna: MinMax reaguje optymalnie na kazdy ruch, nigdy nie pomija zagrozenia i zawsze wybiera ruch zgodny z dlugookresowa strategia.

### Gracz ludzki vs MinMax (plansza 4x4, glebokoscz = 6)

Na planszy 4x4 MinMax rowniez okazal sie silniejszy od czlowieka. W rozegrane partii MinMax od poczatku budowal zagrozenia na przekatnej - po zajeciu pola 1 przez czlowieka MinMax zajal pole 0, a nastepnie systematycznie obsadzal pozycje tworzace zagrozenie ukosne (pola 0, 5, 10, 15). Gracz ludzki byl zmuszony do ciaglego reagowania na zagrozenia, nie mogac jednoczesnie realizowac wlasnej strategii. Partia zakonczyla sie wygrana MinMax po 12 ruchach przez uzupelnienie przekatnej.

Przy glebokosci 6 czas obliczen MinMax byl wyraznie odczuwalny - kazdy ruch trwal od ulamkow sekundy do kilku sekund w zaleznosci od etapu gry. Laczny czas obliczen MinMax wyniosl okolo 2,2 sekundy na cala partie, podczas gdy gracz ludzki spdezil na namysle okolo 35 sekund.

Wczesniej podjeta proba uruchomienia gry z glebokoscia 9 na planszy 4x4 zakonczyla sie niepowodzeniem - MinMax nie byl w stanie wykonac pierwszego ruchu w rozsdanym czasie (oczekiwanie rzedu kilku minut). Z tego powodu w eksperymentach na planszy 4x4 glebokoscz ograniczono do maksymalnie 6.

Z powodu ograniczonej głębokości możliwym jest wygranie rozgrywki przez człowieka w skończonej liczbie partii bez rozpoznaniu ograniczeń algorytmu.

---

## Eksperyment 1 - MinMax vs gracz losowy

Stale parametry: rozmiar planszy, glebokoscz MinMax.
Zmienna: strona MinMax (o - gra pierwszy, x - gra drugi).
Liczba powtorzen: 25 (gracz losowy jest niedeterministyczny).

### Plansza 3x3, glebokoscz = 9 (pelne drzewo)

| Strona MinMax | Wygrane | Remisy | Przegrane | Wygrane [%] | Remisy [%] | Przegrane [%] |
|---------------|---------|--------|-----------|-------------|------------|---------------|
| o (pierwszy)  | 25      | 0      | 0         | 100,00      | 0,00       | 0,00          |
| x (drugi)     | 22      | 3      | 0         | 88,00       | 12,00      | 0,00          |

MinMax z pelna glebokoscia na planszy 3x3 nigdy nie przegrywa z graczem losowym. Grajac jako pierwszy wygrywa wszystkie 25 meczow. Grajac jako drugi wygrywa 22 z 25, a pozostale 3 konczy remisem - wynika to z tego, ze gracz losowy moze przez przypadek zajac pola uniemozliwiajace MinMaxowi wygrana, co przy optymalnej grze obu stron na planszy 3x3 zawsze prowadzi do remisu.

### Plansza 4x4, glebokoscz = 6

| Strona MinMax | Wygrane | Remisy | Przegrane | Wygrane [%] | Remisy [%] | Przegrane [%] |
|---------------|---------|--------|-----------|-------------|------------|---------------|
| o (pierwszy)  | 17      | 8      | 0         | 68,00       | 32,00      | 0,00          |
| x (drugi)     | 16      | 9      | 0         | 64,00       | 36,00      | 0,00          |

Na planszy 4x4 przy glebokosci 6 MinMax rowniez nigdy nie przegrywa, ale czesciej konczy remisem - odpowiednio 32% i 36% meczow. Wynika to z ograniczonego horyzontu przeszukiwania: glebokoscz 6 nie pokrywa calego drzewa gry (plansza ma 16 pol), wiec heurystyka moze nie dostrzec wygranej lub przegranej odleglejszej niz 6 ruchow. Gracz losowy, dzialajac przypadkowo, moze zajmowac pola uniemozliwiajace MinMaxowi sfinalizowanie wygranej w zasiegu przeszukiwania.

![wykres](plots/exp1_minmax_vs_random.png)

### Wnioski z eksperymentu 1

MinMax z przycinaniem alfa-beta nie przegrywa z graczem losowym ani na planszy 3x3, ani na 4x4. Na planszy 3x3 przy pelnej glebokosci przewaga jest absolutna. Na planszy 4x4 przy ograniczonej glebokosci jakosc gracza jest nizsza - czesc meczow konczy remisem - co pokazuje, ze heurystyczna ocena stanow nieterminalnych jest slabszym substytutem pelnego przeszukiwania. Granie jako pierwszy daje niewielka przewage w obu przypadkach.

---

## Eksperyment 2 - MinMax vs MinMax przy roznych glebokosciach

Obaj gracze uzywaja MinMax z przycinaniem alfa-beta. Dla kazdej pary glebokosci (depth_o, depth_x) rozegrano jedna gre - mecze sa w pelni deterministyczne, wielokrotne powtarzanie nie zmienia wyniku.

Gracz 'o' gra pierwszy, gracz 'x' gra drugi.

Badane glebokosci na planszy 4x4 ograniczono do maksymalnie 6 ze wzgledu na czas obliczen - jak zaobserwowano przy uruchamianiu gry interaktywnie, glebokoscz 9 na planszy 4x4 powoduje czas oczekiwania rzedu kilku minut juz na pierwszym ruchu.

### Plansza 3x3 - macierz wynikow

Wiersze: glebokoscz gracza 'o'. Kolumny: glebokoscz gracza 'x'.

| depth\_o \ depth\_x | 1         | 2     | 3     | 4         | 9     |
|---------------------|-----------|-------|-------|-----------|-------|
| 1                   | o wygrywa | remis | remis | remis     | remis |
| 2                   | o wygrywa | remis | remis | remis     | remis |
| 3                   | o wygrywa | remis | remis | remis     | remis |
| 4                   | o wygrywa | remis | remis | remis     | remis |
| 9                   | remis     | remis | remis | o wygrywa | remis |

Przy niemal wszystkich kombinacjach glebokosci wynik to remis, co jest zgodne z teoria - kolko i krzyzyk na planszy 3x3 jest gra rozstrzygnieta i przy optymalnej grze obu stron zawsze konczy sie remisem.

Wyjatek stanowi kolumna depth_x = 1: gracz 'x' z glebokoscia 1 przegrywa niezaleznie od glebokosci przeciwnika. Gracz z glebokoscia 1 widzi tylko bezposrednie nastepstwa swojego ruchu i nie jest w stanie skutecznie bronic sie przed dlugookresowa strategia.

Drugi wyjatek to para (depth_o = 9, depth_x = 4), gdzie gracz 'o' wygrywa. Gracz o glebokosci 4 pomija pewne galecie drzewa, przez co wybiera ruch gorszy niz optymalny - gracz z pelnym przeszukiwaniem potrafi to wykorzystac. Przy symetrycznej parze (depth_o = 4, depth_x = 9) wynik to juz remis, co wskazuje ze efekt jest asymetryczny i zalezny od kolejnosci ruchow.

### Plansza 4x4 - macierz wynikow

Wiersze: glebokoscz gracza 'o'. Kolumny: glebokoscz gracza 'x'.

| depth\_o \ depth\_x | 1     | 2     | 3     | 4     | 6     |
|---------------------|-------|-------|-------|-------|-------|
| 1                   | remis | remis | remis | remis | remis |
| 2                   | remis | remis | remis | remis | remis |
| 3                   | remis | remis | remis | remis | remis |
| 4                   | remis | remis | remis | remis | remis |
| 6                   | remis | remis | remis | remis | remis |

Na planszy 4x4 wszystkie pary glebokosci daja remis. W przeciwienstwie do planszy 3x3 nawet minimalna glebokoscz 1 nie prowadzi do przegranej. Na wiekszej planszy przy ograniczonym horyzoncie przeszukiwania zadna ze stron nie jest w stanie zaplanowac wygrywajacych sekwencji ruchow - heurystyka odzwierciedla ogolny potencjal pozycji, ale nie wskazuje jednoznacznej sciezki do wygranej. Obaj gracze prowadza bezpieczna gre i doprowadzaja do remisow.

![wykres](plots/exp2_minmax_vs_minmax_heatmap.png)

### Czas obliczen w zaleznosci od glebokosci

Sredni czas obliczen gracza 'o' w calej grze (usredniony po wszystkich przeciwnikach).

**Plansza 3x3:**

| Glebokoscz | Sredni czas [ms] |
|------------|------------------|
| 1          | 0,28             |
| 2          | 0,81             |
| 3          | 2,87             |
| 4          | 6,51             |
| 9          | 98,12            |

**Plansza 4x4:**

| Glebokoscz | Sredni czas [ms] |
|------------|------------------|
| 1          | 1,10             |
| 2          | 4,68             |
| 3          | 29,91            |
| 4          | 107,58           |
| 6          | 1773,07          |

Czas obliczen rosnie wyraznie wraz z glebokoscia. Na planszy 4x4 przejscie z glebokosci 4 do 6 zwieksza czas ponad 16-krotnie - do niemal 1,8 sekundy na gre. Pelne przeszukanie planszy 4x4 jest praktycznie niewykonalne w rozsdanym czasie, co potwierdzily obserwacje z gry interaktywnej.

![wykres](plots/exp2_time_vs_depth.png)

### Wnioski z eksperymentu 2

Na planszy 3x3 gracz z glebokoscia 1 zawsze przegrywa, co potwierdza ze tak plytkie przeszukiwanie jest niewystarczajace. Przy glebokosciach 2 i wyzszych wynik to remis - zgodnie z teoria gry w kolko i krzyzyk 3x3 jest rozstrzygnieta. Jedynym odchyleniem jest para (9, 4), gdzie glebokie przeszukiwanie pozwala wykorzystac niepelnosc glebokosci 4.

Na planszy 4x4 zadna testowana glebokoscz nie pozwala zadnemu graczowi na wygrana. Oznacza to, ze przy ograniczonym horyzoncie przeszukiwania i zastosowanej heurystyce roznice miedzy graczami sa nieuchwytne - istotna role odgrywa tu jakosc heurystyki, a nie sama glebokoscz.

Czas obliczen rosnie szybko wraz z glebokoscia, co pokazuje ze wybor glebokosci jest kluczowym kompromisem miedzy jakoscia gracza a czasem obliczen.

---

## Wnioski koncowe

| Konfiguracja | Wynik MinMax | Uwagi |
|---|---|---|
| 3x3, MinMax vs losowy, depth=9 | 100% wygranych jako 'o', 88% jako 'x' | Pelne drzewo, gra optymalna |
| 4x4, MinMax vs losowy, depth=6 | 68% wygranych jako 'o', 64% jako 'x' | Heurystyka, czesc remisow |
| 3x3, MinMax vs MinMax | Remis (depth >= 2 vs depth >= 2) | Gra rozstrzygnieta - remis optymalny |
| 4x4, MinMax vs MinMax | Remis dla wszystkich par | Heurystyka niewystarczajaca do wygrania |

MinMax z przycinaniem alfa-beta jest znacznie silniejszym graczem niz gracz losowy - nigdy nie przegrywa z nim ani na planszy 3x3, ani na 4x4, co potwierdzily zarowno eksperymenty automatyczne, jak i obserwacje z gry z czlowiekiem. Na planszy 3x3 przy pelnej glebokosci gra optymalnie. Na wiekszej planszy koniecznosc ograniczenia glebokosci i uzycia heurystyki obniza jakosc gracza.

Glebokoscz przeszukiwania ma duzy wplyw na jakosc gracza na planszy 3x3 - roznica miedzy glebokoscia 1 a wyzszymi jest wyrazna i prowadzi do bezposredniej przegranej. Na planszy 4x4 przy badanych glebokosciach roznice w jakosci miedzy graczami MinMax sa nieuchwytne, co sugeruje ze przy wiekszych planszach istotniejsza role odgrywa jakosc heurystyki niz sama glebokoscz przeszukiwania.

Czas obliczen rosnie bardzo szybko wraz z rozmiarem planszy i glebokoscia - pelne przeszukanie drzewa gry na planszy 4x4 jest praktycznie niewykonalne, co czyni przycinanie alfa-beta i ograniczenie glebokosci niezbednym elementem implementacji dla wiekszych plansz.
