# Wprowadzenie do sztucznej inteligencji

**Numer cwiczenia:** 06  
**Temat:** Uczenie sie ze wzmocnieniem - Q-Learning  
**Typ dokumentu:** Raport z badan  
**Semestr:** letni 2025/2026  
**Autor:** Wiktor Sosnowski  
**Numer albumu:** 348 561  
**Data:** 15.06.2026

---

## Tresc zadania

Cel zadania polega na implementacji algorytmu Q-learning oraz zastosowaniu go do rozwiazania problemu Cliff Walking. Srodowisko to jest dostepne w pakiecie gymnasium (`gym.make('CliffWalking-v0')`).

Kroki do wykonania:

1. Implementacja algorytmu Q-learning.
2. Zbadanie skutecznosci dzialania algorytmu dla problemu Cliff Walking dla roznych wartosci wspolczynnika uczenia i roznej liczby epizodow (w procesie trenowania).

Uwagi: Implementacja algorytmu powinna byc uniwersalna, tzn. mozliwa do wykorzystania dla roznych srodowisk o dyskretnej przestrzeni stanow i akcji.

---

## Interpretacja zadania

Q-learning jest algorytmem uczenia sie ze wzmocnieniem (ang. reinforcement learning). Agent dziala w srodowisku, ktore po kazdej akcji zwraca nagrode i nowy stan. Celem agenta jest maksymalizacja sumarycznej nagrody w epizodzie.

Algorytm utrzymuje tablice Q o wymiarach liczba_stanow x liczba_akcji. Kazdy wpis Q(s, a) przybliza oczekiwana sumaryczna nagrode, jaka agent uzyska, bedac w stanie s i wykonujac akcje a, a nastepnie postepujac optymalnie. Aktualizacja po kazdym kroku odbywa sie wedlug wzoru:

```
Q(s, a) <- Q(s, a) + alpha * (r + gamma * max_a' Q(s', a') - Q(s, a))
```

gdzie alpha to wspolczynnik uczenia, gamma to wspolczynnik dyskontowania nagrod przyszlych, r to otrzymana nagroda, a s' to nastepny stan.

Do wyboru akcji stosowana jest strategia epsilon-zachlanna: z prawdopodobienstwem epsilon agent wybiera losowa akcje (eksploracja), a z prawdopodobienstwem 1-epsilon wybiera akcje o najwyzszej wartosci Q (eksploatacja).

Srodowisko Cliff Walking to siatka 4x12. Agent startuje w lewym dolnym rogu i musi dotrzec do prawego dolnego rogu. Dolny rzad (oprocz startu i celu) to klif - wejscie na niego konczy epizod z kara -100. Kazdy krok kosztuje -1. Optymalna sciezka prowadzi wzdluz klifu i ma dlugosc 12 krokow (nagroda -12), jednak agent uczacy sie ze wzmocnieniem - ze wzgledu na ryzyko wpadniecia na klif podczas eksploracji - typowo uczy sie bezpieczniejszej sciezki gornym skrajem siatki o dlugosci 13 krokow (nagroda -13).

Skutecznosc po treningu oceniana jest jednym epizodzie greedy (epsilon=0): mierzona jest suma nagrod (reward) i liczba krokow (steps).

---

## Opis implementacji

Zaimplementowano klase `QLearningAgent` z metoda `update` realizujaca krok TD (ang. temporal difference) zgodnie z powyzszym wzorem. Tablica Q inicjalizowana jest zerami. Wybor akcji realizuje metoda `select_action` z parametrem `greedy` - przy `greedy=True` agent zawsze wybiera akcje o najwyzszej wartosci Q (ewaluacja po treningu).

Funkcja `train` przeprowadza trening przez zadana liczbe epizodow. Funkcja `evaluate` uruchamia jeden epizod greedy z limitem 200 krokow - limit ten zapobiega nieskonczonej petli dla nienauczonego agenta (nienauczony agent krazy w miejscu, poniewaz wszystkie wartosci Q sa rowne zeru i argmax zawsze zwraca akcje o indeksie 0).

Funkcja `run_experiment` powtarza pelny cykl trening+ewaluacja 25 razy z niezalezna tablica Q i innym ziarnem generatora liczb pseudolosowych w kazdym uruchomieniu.

Implementacja jest uniwersalna - przyjmuje jako parametry liczbe stanow i akcji, wiec moze byc uzyty dla dowolnego srodowiska o dyskretnej przestrzeni stanow i akcji.

---

## Srodowisko

Uzyto srodowiska `CliffWalking-v1` z pakietu gymnasium z domyslnym parametrem `is_slippery=False`, co jest rownowazne z opisanym w tresci zadania `CliffWalking-v0` (wersja v0 zostala wycofana w aktualnej wersji biblioteki). Srodowisko ma 48 stanow (siatka 4x12) i 4 akcje (gora, prawo, dol, lewo).

---

## Konfiguracja bazowa (Baseline)

**Parametry:** alpha=0,5, gamma=0,99, epsilon=0,1, num_episodes=500, n_runs=25

| metryka | min | srednia | std | max |
|---------|-----|---------|-----|-----|
| nagroda | -13,00 | -13,00 | 0,00 | -13,00 |
| liczba krokow | 13,00 | 13,00 | 0,00 | 13,00 |

Przy konfiguracji bazowej we wszystkich 25 uruchomieniach agent osiaga wynik -13 (13 krokow) - min, srednia, max i std sa identyczne. Jest to oczekiwany wynik dla Q-learning w tym srodowisku - agent uczy sie bezpiecznej sciezki gornym skrajem siatki, unikajac klifu.

![Krzywa uczenia baseline](plots/assignment_06/baseline_learning_curve.png)

Krzywa uczenia pokazuje szybkie osiagniecie stabilnego wyniku okolo -13. Wahania we wczesnych epizodach wynikaja z eksploracji - agent wpada na klif, co generuje duze kary. Po okolo 50-100 epizodach algorytm stabilizuje sie na optymalnej sciezce.

---

## Eksperyment 1 - wplyw wspolczynnika uczenia (alpha)

**Stale parametry:** gamma=0,99, epsilon=0,1, num_episodes=100  
**Badany zakres:** alpha w {0,1; 0,3; 0,5; 0,7; 0,9}

Liczba epizodow ustawiona na 100, poniewaz przy tej wartosci roznice miedzy wartosciami alpha sa wyraznie widoczne - wiecej epizodow prowadzi do zbiagniecia wszystkich wariantow.

### Tabela 1a - nagroda ewaluacyjna vs alpha

| alpha | min | srednia | std | max |
|-------|-----|---------|-----|-----|
| 0,1 | -200,00 | -200,00 | 0,00 | -200,00 |
| 0,3 | -200,00 | -20,56 | 36,63 | -13,00 |
| 0,5 | -13,00 | -13,00 | 0,00 | -13,00 |
| 0,7 | -13,00 | -13,00 | 0,00 | -13,00 |
| 0,9 | -13,00 | -13,00 | 0,00 | -13,00 |

### Tabela 1b - liczba krokow ewaluacyjnych vs alpha

| alpha | min | srednia | std | max |
|-------|-----|---------|-----|-----|
| 0,1 | 200,00 | 200,00 | 0,00 | 200,00 |
| 0,3 | 13,00 | 20,56 | 36,63 | 200,00 |
| 0,5 | 13,00 | 13,00 | 0,00 | 13,00 |
| 0,7 | 13,00 | 13,00 | 0,00 | 13,00 |
| 0,9 | 13,00 | 13,00 | 0,00 | 13,00 |

![Eksperyment 1 - alpha](plots/assignment_06/experiment1_alpha.png)

![Eksperyment 1 - alpha, liczba krokow](plots/assignment_06/experiment1_alpha_steps.png)

Przy alpha=0,1 agent w zadnym z 25 uruchomien nie zdolal nauczyc sie wlasciwej polityki w ciagu 100 epizodow - wynik -200 odpowiada limitowi 200 krokow, co oznacza brak zbieznosci. Maly wspolczynnik uczenia powoduje, ze wartosci Q aktualizowane sa bardzo wolno i 100 epizodow to za malo, by zgromadzic wystarczajaca wiedze.

Przy alpha=0,3 wyniki sa niejednorodne: srednia -20,56 ze standardowym odchyleniem 36,63 wskazuje, ze czesc uruchomien zbiega do optimum (-13), a czesc nie - co potwierdza max=-13 i min=-200. Wspolczynnik jest juz wystarczajacy do zbieznosci, ale nie w sposob pewny.

Od alpha=0,5 wyzej we wszystkich 25 uruchomieniach wynik ewaluacyjny wynosi -13, a std=0 - brak jakiejkolwiek zmiennosci miedzy uruchomieniami. Wieksze wartosci alpha przyspieszaja uczenie, przez co 100 epizodow jest wystarczajace.

**Wniosek:** Zbyt maly wspolczynnik uczenia (alpha=0,1) uniemozliwia zbieznosc przy 100 epizodach - zadne z 25 uruchomien nie osiaga celu (std=0, mean=-200). Wartosci alpha od 0,5 wzwyz daja wynik -13 we wszystkich 25 uruchomieniach (std=0). W tym srodowisku optymalny zakres to alpha >= 0,5 przy 100 epizodach treningowych.

---

## Eksperyment 2 - wplyw liczby epizodow treningowych

**Stale parametry:** alpha=0,5, gamma=0,99, epsilon=0,1  
**Badany zakres:** num_episodes w {10; 20; 30; 50; 75; 100; 200; 500}

### Tabela 2a - nagroda ewaluacyjna vs liczba epizodow

| liczba epizodow | min | srednia | std | max |
|----------------|-----|---------|-----|-----|
| 10 | -200,00 | -200,00 | 0,00 | -200,00 |
| 20 | -200,00 | -200,00 | 0,00 | -200,00 |
| 30 | -200,00 | -200,00 | 0,00 | -200,00 |
| 50 | -200,00 | -95,28 | 92,82 | -13,00 |
| 75 | -13,00 | -13,00 | 0,00 | -13,00 |
| 100 | -13,00 | -13,00 | 0,00 | -13,00 |
| 200 | -13,00 | -13,00 | 0,00 | -13,00 |
| 500 | -13,00 | -13,00 | 0,00 | -13,00 |

### Tabela 2b - liczba krokow ewaluacyjnych vs liczba epizodow

| liczba epizodow | min | srednia | std | max |
|----------------|-----|---------|-----|-----|
| 10 | 200,00 | 200,00 | 0,00 | 200,00 |
| 20 | 200,00 | 200,00 | 0,00 | 200,00 |
| 30 | 200,00 | 200,00 | 0,00 | 200,00 |
| 50 | 13,00 | 95,28 | 92,82 | 200,00 |
| 75 | 13,00 | 13,00 | 0,00 | 13,00 |
| 100 | 13,00 | 13,00 | 0,00 | 13,00 |
| 200 | 13,00 | 13,00 | 0,00 | 13,00 |
| 500 | 13,00 | 13,00 | 0,00 | 13,00 |

![Eksperyment 2 - liczba epizodow](plots/assignment_06/experiment2_episodes.png)

Przy 10-30 epizodach agent nie zbiega w zadnym z 25 uruchomien - tablica Q nie zostaje wystarczajaco wypelniona, by polityka greedy prowadzila do celu. Wynik -200 oznacza osiagniecie limitu krokow.

Przy 50 epizodach widoczna jest niejednorodnosc wynikow: srednia -95,28 ze standardowym odchyleniem 92,82 wskazuje, ze czesc uruchomien osiaga optimum, a czesc nie. Jest to punkt przejscia, w ktorym zbieznosc jest mozliwa, ale niestabilna.

Od 75 epizodow agent zbiega do optymalnego wyniku -13 we wszystkich 25 uruchomieniach. Zwiekszanie liczby epizodow powyzej 75 nie poprawia juz wyniku ewaluacyjnego - algorytm osiaga optimum, ktorego nie mozna przekroczyc bez zmiany epsilon lub gamma.

**Wniosek:** Przy alpha=0,5 juz 75 epizodow treningowych wystarczy, by we wszystkich 25 uruchomieniach uzyskac wynik -13 (std=0). Dalsze zwiekszanie liczby epizodow nie przynosi poprawy wyniku ewaluacyjnego.

---

## Wnioski koncowe

| parametr | badany zakres | najlepsze wartosci |
|----------|--------------|-------------------|
| alpha | 0,1 - 0,9 | >= 0,5 (przy 100 epizodach) |
| num_episodes | 10 - 500 | >= 75 (przy alpha=0,5) |

Q-learning skutecznie rozwiazuje problem Cliff Walking. Algorytm uczy sie bezpiecznej polityki gornym skrajem siatki (nagroda -13, 13 krokow), a nie optymalnej w sensie teorii (-12, 12 krokow wzdluz klifu). Jest to typowe zachowanie Q-learning: podczas eksploracji agent wpada na klif, co penalizuje sciezke krawedzia na tyle, ze preferowana staje sie dluzsza, ale bezpieczniejsza trasa.

Wspolczynnik uczenia alpha ma istotny wplyw na szybkosc zbieznosci. Przy alpha=0,1 zadne z 25 uruchomien nie osiaga celu w ciagu 100 epizodow. Przy alpha=0,5 i wyzej wszystkie 25 uruchomien daje identyczny wynik -13 (std=0).

Liczba epizodow treningowych wyznacza, czy agent zdazy zebrac wystarczajaca liczbe obserwacji. Przy alpha=0,5 i 10-30 epizodach zadne z 25 uruchomien nie osiaga celu. Przy 75 epizodach wszystkie 25 uruchomien daje wynik -13 (std=0) i dalsze zwiekszanie liczby epizodow nie zmienia tego wyniku.

Oba parametry wplywaja na zbieznosc w podobny sposob: niewystarczajace wartosci uniemozliwiaja nauke, a po przekroczeniu progu wynik stabilizuje sie na optimum i nie mozna go dalej poprawic przez same zwiekszanie alpha lub liczby epizodow.
