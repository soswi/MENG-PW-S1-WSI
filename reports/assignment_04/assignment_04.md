# Wprowadzenie do sztucznej inteligencji

**Ćwiczenie 4 - Regresja i klasyfikacja**
**Typ dokumentu:** Raport z badan
**Semestr:** letni 2025/2026
**Rok akademicki:** 2025/2026
**Autor:** Wiktor Sosnowski
**Numer albumu:** 348 561
**Data:** 15.06.2026

---

## Trescz zadania

Cel zadania polega na implementacji drzewa decyzyjnego tworzonego algorytmem ID3 z ograniczeniem maksymalnej glebokosci drzewa, jak rowniez na stworzeniu i zbadaniu jakosci klasyfikatora dla zbioru danych Tic-Tac-Toe Endgame.

Kroki do wykonania:

1. Zaimplementuj drzewo decyzyjne ID3 (z ograniczeniem jego maksymalnej glebokosci).
2. Zbadaj skutecznosc dzialania klasyfikatora dla zbioru danych Tic-Tac-Toe Endgame, obliczajac dokladnosc i macierz pomylek.

---

## Interpretacja zadania

Celem zadania jest implementacja algorytmu ID3 (Iterative Dichotomiser 3) sluzacego do budowy drzewa decyzyjnego dla problemow klasyfikacji. Algorytm wybiera w kazdym wezle atrybut o najwyzszym przyroscie informacji (information gain), definiowanym jako roznica entropii Shannona zbioru przed i po podziale. Parametr maksymalnej glebokosci drzewa ogranicza liczbe kolejnych podzialow, co pozwala kontrolowac zlozonosc modelu i zapobiegac przeuczeniu.

Zbior danych Tic-Tac-Toe Endgame zawiera przykladowe koncowe stany planszy kolko-krzyzyk opisane wylacznie atrybutami kategorycznymi, co czyni go odpowiednim do zastosowania algorytmu ID3.

---

## Zbior danych

Zbior danych Tic-Tac-Toe Endgame pochodzi z repozytorium UCI Machine Learning Repository. Zawiera 958 przykladow opisujacych wszystkie mozliwe koncowe stany planszy 3x3 w grze kolko-krzyzyk, w ktorych gracz `x` wykonuje ruch jako pierwszy.

Kazdy przyklad sklada sie z 9 atrybutow kategorycznych odpowiadajacych polom planszy (wartosci: `x`, `o`, `b` - puste pole) oraz etykiety klasy:

- `positive` - gracz `x` wygral (626 przykladow)
- `negative` - gracz `x` nie wygral (332 przyklady)

Zbior jest niezbilansowany - klasa `positive` stanowi okolo 65% przykladow.

---

## Opis implementacji

Implementacja znajduje sie w pliku `src/assignment_04/id3.py` i sklada sie z nastepujacych elementow:

**Funkcje pomocnicze:**
- `entropy(labels)` - oblicza entropie Shannona tablicy etykiet
- `information_gain(labels, subsets)` - oblicza przyrost informacji dla danego podzialu
- `accuracy(y_true, y_pred)` - oblicza dokladnosc klasyfikacji
- `confusion_matrix(y_true, y_pred)` - buduje macierz pomylek

**Klasa `Node`** reprezentuje pojedynczy wezel drzewa. Wezel wewnetrzny przechowuje indeks atrybutu i slownik dzieci (wartosc atrybutu -> wezel), a lisc przechowuje etykiete klasy.

**Klasa `DecisionTreeID3`** implementuje algorytm ID3:
- `fit(X, y)` - buduje drzewo rekurencyjnie metodą `_build`, wybierajac w kazdym wezle atrybut o najwyzszym przyroscie informacji; rekurencja konczy sie gdy wszystkie przyklady naleza do jednej klasy, brak dostepnych atrybutow lub osiagnieto limit glebokosci - w ostatnich dwoch przypadkach tworzony jest lisc z etykieta wynikajaca z glosu wiekszosci
- `predict(X)` - klasyfikuje przyklad przechodzac od korzenia do liscia wedlug wartosci atrybutow; dla wartosci niewidzianych w treningu zwraca etykiete najczesciej wystepujaca w poddrzewie

Implementacja jest uniwersalna - nie zawiera zadnych zaleznosci od konkretnego zbioru danych.

---

## Eksperymenty

W kazdym eksperymencie algorytm ID3 jest z natury deterministyczny - przy ustalonych danych treningowych buduje zawsze to samo drzewo. Zrodlem losowosci jest podzial danych na zbiory treningowy, walidacyjny i testowy. Dlatego kazda konfiguracja parametrow zostala przetestowana w 25 losowych podziałach (ziarna 0-24), a wyniki agregowano statystycznie.

### Eksperyment 1 - wplyw maksymalnej glebokosci drzewa

**Stale parametry:** podzial train/val/test = 70/15/15, 25 powtorzen

**Badany parametr:** max_depth ∈ {1, 2, 3, 4, 5, 6, 7, 8, 9, None}

#### Dokladnosc na zbiorze walidacyjnym

| max_depth | min | srednia | std | max |
|-----------|-----|---------|-----|-----|
| 1 | 0,66 | 0,71 | 0,04 | 0,79 |
| 2 | 0,60 | 0,67 | 0,04 | 0,74 |
| 3 | 0,69 | 0,74 | 0,03 | 0,82 |
| 4 | 0,73 | 0,79 | 0,03 | 0,85 |
| 5 | 0,77 | 0,85 | 0,03 | 0,91 |
| 6 | 0,78 | 0,86 | 0,04 | 0,94 |
| 7 | 0,80 | 0,86 | 0,04 | 0,94 |
| 8 | 0,80 | 0,86 | 0,04 | 0,94 |
| 9 | 0,80 | 0,86 | 0,04 | 0,94 |
| None | 0,80 | 0,86 | 0,04 | 0,94 |

#### Dokladnosc na zbiorze testowym

| max_depth | min | srednia | std | max |
|-----------|-----|---------|-----|-----|
| 1 | 0,65 | 0,69 | 0,03 | 0,75 |
| 2 | 0,61 | 0,68 | 0,03 | 0,73 |
| 3 | 0,68 | 0,74 | 0,03 | 0,79 |
| 4 | 0,70 | 0,78 | 0,04 | 0,86 |
| 5 | 0,78 | 0,84 | 0,03 | 0,92 |
| 6 | 0,79 | 0,86 | 0,03 | 0,90 |
| 7 | 0,79 | 0,86 | 0,03 | 0,91 |
| 8 | 0,79 | 0,86 | 0,03 | 0,91 |
| 9 | 0,79 | 0,86 | 0,03 | 0,91 |
| None | 0,79 | 0,86 | 0,03 | 0,91 |

![Wykres eksperymentu 1](exp1_depth_accuracy.png)

Wyniki na zbiorze walidacyjnym i testowym rosna wraz z glebokoscia do poziomu max_depth = 7, po czym pozostaja niezmienione dla wartosci 8, 9 i None. Oznacza to, ze drzewo budowane na tym zbiorze danych nie przekracza glebokosci 7 nawet bez ograniczen - dalsze zwiekszanie parametru nie ma juz wplywu. Najnizsza dokladnosc uzyskano dla max_depth = 2, co jest efektem zbyt duzej redukcji przestrzeni hipotez przy jednoczesnym braku wystarczajacej reprezentacji danych przy depth = 1. Wzrost dokladnosci miedzy depth = 4 a 5 jest najwyrazniejszy (okolo 6 punktow procentowych na zbiorze testowym), co sugeruje ze na tym poziomie glebokosci drzewo zaczyna uchwycic najistotniejsze zaleznosci w danych.

Nie zaobserwowano oznaki przeuczenia - dokladnosc na zbiorze testowym jest zblizona do walidacyjnej na kazdym poziomie glebokosci.

**Najlepsza wartosc parametru: max_depth = 7** (dalsze zwiekszanie nie przynosi poprawy, mniejsze wartosci daja gorsze wyniki).

---

### Eksperyment 2 - wplyw proporcji zbioru treningowego

**Stale parametry:** max_depth = 7, 25 powtorzen; zbior walidacyjny i testowy dziela po rowno pozostala czesz danych

**Badany parametr:** train_ratio ∈ {0,50, 0,60, 0,70, 0,80, 0,90}

#### Dokladnosc na zbiorze testowym

| train_ratio | min | srednia | std | max |
|-------------|-----|---------|-----|-----|
| 0,50 | 0,76 | 0,83 | 0,03 | 0,88 |
| 0,60 | 0,78 | 0,85 | 0,02 | 0,89 |
| 0,70 | 0,79 | 0,86 | 0,03 | 0,91 |
| 0,80 | 0,78 | 0,86 | 0,03 | 0,91 |
| 0,90 | 0,73 | 0,85 | 0,05 | 0,94 |

![Wykres eksperymentu 2](exp2_split_accuracy.png)

Srednia dokladnosc na zbiorze testowym rosnie od train_ratio = 0,50 do 0,70, po czym utrzymuje sie na tym samym poziomie dla 0,80 (0,8590 w obu przypadkach). Przy train_ratio = 0,90 srednia nieznacznie spada, a odchylenie standardowe wyraznie rosnie do 0,05 - wynik staje sie niestabilny, co jest efektem malego rozmiaru zbioru testowego (tylko 10% danych, czyli okolo 96 przykladow). Przy train_ratio = 0,70 model osiaga dokladnosc rowna tej dla 0,80, ale przy nizszym odchyleniu standardowym (0,03 vs 0,03 - identyczne), jednak przy wiekszym zbiorze testowym, co daje bardziej wiarygodna ocene.

**Najlepsza wartosc parametru: train_ratio = 0,70** - zapewnia dobry kompromis miedzy rozmiarem zbioru treningowego a wiarygodnoscia oceny na zbiorze testowym.

---

## Macierz pomylek - najlepszy model

**Parametry:** max_depth = 7, train_ratio = 0,70 (val/test = 0,15/0,15), seed = 0

**Dokladnosc na zbiorze testowym:** 0,8069

|  | Przewidziano: negative | Przewidziano: positive |
|--|------------------------|------------------------|
| **Rzeczywiste: negative** | 36 | 18 |
| **Rzeczywiste: positive** | 10 | 81 |

![Macierz pomylek](confusion_matrix.png)

Model poprawnie sklasyfikowal 117 z 145 przykladow w zbiorze testowym. Liczba falszywie ujemnych (FN = 18, klasa positive sklasyfikowana jako negative) jest wyzsza niz falszywie dodatnich (FP = 10, klasa negative sklasyfikowana jako positive). Wynika to ze struktury zbioru - klasa positive jest liczniejsza, dlatego model lepiej uczy sie jej wzorcow. Dokladnosc w tym konkretnym podziale (0,81) jest nieznacznie nizsza od sredniej z 25 powtorzen (0,86), co miesci sie w typowej zmiennosci wynikow.

---

## Wnioski koncowe

| Parametr | Badany zakres | Najlepsza wartosc |
|----------|---------------|-------------------|
| max_depth | 1, 2, 3, 4, 5, 6, 7, 8, 9, None | 7 |
| train_ratio | 0,50 - 0,90 | 0,70 |

Zaimplementowany algorytm ID3 osiaga srednia dokladnosc okolo 0,86 na zbiorze testowym przy optymalnych parametrach. Najwazniejszym parametrem okazala sie maksymalna glebokosci drzewa - zbyt mala (1-4) wyraznie obniza jakosc klasyfikacji, natomiast powyzej 7 nie przynosi dalszej poprawy, poniewaz drzewo budowane na tym zbiorze nie przekracza tej glebokosci. Brak objawow przeuczenia - wyniki na zbiorach walidacyjnym i testowym sa zblizone na wszystkich poziomach glebokosci.

Proporcja podzialu danych ma mniejszy wplyw na srednia dokladnosc niz glebokosci drzewa - roznica miedzy najgorszym (0,50) a najlepszym (0,70) wynikiem wynosi okolo 3 punkty procentowe. Zbyt duzy zbior treningowy (0,90) skutkuje wzrostem niestabilnosci wynikow z powodu malego rozmiaru zbioru testowego.
