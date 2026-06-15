# Wprowadzenie do sztucznej inteligencji

Cwiczenie 7 - Modele bayesowskie

Raport z badan

Semestr letni 2025/2026

Autor: Wiktor Sosnowski

Numer albumu: 348 561

Data: 15.06.2026

---

## Tesc zadania

Cel zadania polega na skonstruowaniu sieci Bayesowskiej oraz zbadaniu wplywu informacji o statusie w MS Teams na prawdopodobienstwo swiecenia sie swiatla w pokoju doktorantki K.

Scenariusz: Doktorantka K. spedza 40% czasu pracy w swoim pokoju na uczelni. Pozostale 60% czasu pracuje zdalnie. Kiedy K. jest w swoim pokoju, polowe czasu ma wylaczone swiatlo (kiedy probuje ukryc sie przed studentami i pracowac nad doktoratem). Gdy nie ma jej w pokoju, zostawia wlaczone swiatlo tylko w 5% przypadkow. W 80% czasu, gdy jest w swoim biurze, K. jest zalogowana w MS Teams. Poniewaz czasami loguje sie do Teamsow z domu, w 5% przypadkow, gdy nie ma jej na uczelni, nadal jest zalogowana w MS Teams.

Kroki do wykonania:

1. Skonstruuj siec Bayesowska, aby przedstawic opisany scenariusz.
2. Zakladajac, ze student sprawdza status K. w MS Teams i widzi, ze jest ona zalogowana - jaki wplyw ma to na przekonanie studenta, ze swiatlo w pokoju K. jest wlaczone?

---

## Interpretacja zadania

Siec Bayesowska to probabilistyczny model graficzny, w ktorym wezly reprezentuja zmienne losowe, a krawedzie skierowane oznaczaja zaleznosci przyczynowe miedzy nimi. Kazdy wezel posiada tablice warunkowego rozkladu prawdopodobienstwa (CPD - Conditional Probability Distribution), ktora opisuje prawdopodobienstwo przyjecia danej wartosci w zaleznosci od wartosci wezlow rodzicielskich.

W tym zadaniu modelujemy zaleznosc miedzy lokalizacja doktorantki K. (w biurze lub zdalnie) a dwoma obserwowalnymi zjawiskami: stanem oswietlenia jej pokoju oraz jej statusem w komunikatorze MS Teams. Lokalizacja jest zmienna ukryta (nie jest bezposrednio obserwowalna), podczas gdy stan swiatla i status w Teams moga byc sprawdzone przez studenta.

Wnioskowanie bayesowskie pozwala na aktualizacje przekonan o zmiennej ukrytej (Lokalizacja) na podstawie obserwacji (Teams=zalogowana), a nastepnie wyznaczenie zaktualizowanego prawdopodobienstwa dla innej zmiennej (Swiatlo=wlaczone).

---

## Opis implementacji

Siec zbudowano przy uzyciu biblioteki `pgmpy` (klasa `DiscreteBayesianNetwork`). Model zawiera trzy dyskretne zmienne dwustanowe:

- Location: 0 = w biurze, 1 = zdalnie
- Light: 0 = wlaczone, 1 = wylaczone
- Teams: 0 = zalogowana, 1 = wylogowana

Struktura sieci: Location -> Light, Location -> Teams.

Zmienne Light i Teams sa warunkowo niezalezne przy znajomosci Location - Teams nie jest bezposrednim dowodem na stan swiatla, lecz dostarcza informacji o lokalizacji, ktora z kolei wplywa na oswietlenie.

Tablice CPD wyznaczono bezposrednio z tresci zadania. Do wnioskowania uzyto algorytmu eliminacji zmiennych (Variable Elimination).

---

## Konfiguracja bazowa

Parametry wynikajace z tresci zadania:

| Parametr | Wartosc |
|---|---|
| P(Lokalizacja = w biurze) | 0,40 |
| P(Swiatlo = wlaczone / w biurze) | 0,50 |
| P(Swiatlo = wlaczone / zdalnie) | 0,05 |
| P(Teams = zalogowana / w biurze) | 0,80 |
| P(Teams = zalogowana / zdalnie) | 0,05 |

Wyniki zapytania dla konfiguracji bazowej:

| Zapytanie | Wartosc |
|---|---|
| P(Swiatlo = wlaczone) | 0,23 |
| P(Swiatlo = wlaczone / Teams = zalogowana) | 0,46 |

Bez zadnej obserwacji prawdopodobienstwo, ze swiatlo jest wlaczone, wynosi 0,23. Po zaobserwowaniu, ze doktorantka K. jest zalogowana w MS Teams, prawdopodobienstwo to wzrasta do 0,46 - niemal dwukrotnie. Wynika to z faktu, ze status zalogowania w Teams jest silnym wskaznikiem obecnosci K. w biurze, a obecnosc w biurze wiaze sie z P(Swiatlo=wlaczone) = 0,50.

---

## Eksperymenty

### Eksperyment 1 - wplyw P(Lokalizacja = w biurze)

Stale parametry: P(Swiatlo=wl. / w biurze) = 0,50, P(Swiatlo=wl. / zdalnie) = 0,05, P(Teams=zalog. / w biurze) = 0,80, P(Teams=zalog. / zdalnie) = 0,05.

Badany zakres: P(w biurze) in {0,10; 0,20; 0,40; 0,60; 0,80}.

| P(w biurze) | P(Swiatlo=wl.) | P(Swiatlo=wl. / Teams=zalog.) | Roznica |
|---|---|---|---|
| 0,10 | 0,10 | 0,34 | 0,24 |
| 0,20 | 0,14 | 0,41 | 0,27 |
| 0,40 | 0,23 | 0,46 | 0,23 |
| 0,60 | 0,32 | 0,48 | 0,16 |
| 0,80 | 0,41 | 0,49 | 0,08 |

![wykres eksperymentu 1](plots/exp1_p_in_office.png)

Oba prawdopodobienstwa rosna wraz ze wzrostem P(w biurze), co jest zgodne z intuicja - im czesciej K. bywa w biurze, tym wieksze a priori prawdopodobienstwo, ze swiatlo jest wlaczone. Wartosc P(Swiatlo=wl. / Teams=zalog.) szybciej osiaga nasycenie i dla P(w biurze) = 0,80 wynosi 0,49, podczas gdy prior wynosi juz 0,41 - roznica spada do 0,08.

Wnioski: Im rzadziej K. bywa w biurze (male P(w biurze)), tym wiekszy przyrost informacyjny daje obserwacja statusu Teams. Kiedy K. prawie zawsze jest w biurze, informacja o Teams niewiele zmienia, bo i tak spodziewamy sie wysokiego prawdopodobienstwa wlaczonego swiatla.

---

### Eksperyment 2 - wplyw P(Swiatlo = wlaczone / w biurze)

Stale parametry: P(w biurze) = 0,40, P(Swiatlo=wl. / zdalnie) = 0,05, P(Teams=zalog. / w biurze) = 0,80, P(Teams=zalog. / zdalnie) = 0,05.

Badany zakres: P(Swiatlo=wl. / w biurze) in {0,10; 0,25; 0,50; 0,75; 0,90}.

| P(Swiatlo=wl. / w biurze) | P(Swiatlo=wl.) | P(Swiatlo=wl. / Teams=zalog.) | Roznica |
|---|---|---|---|
| 0,10 | 0,07 | 0,10 | 0,03 |
| 0,25 | 0,13 | 0,23 | 0,10 |
| 0,50 | 0,23 | 0,46 | 0,23 |
| 0,75 | 0,33 | 0,69 | 0,36 |
| 0,90 | 0,39 | 0,83 | 0,44 |

![wykres eksperymentu 2](plots/exp2_p_light_given_in.png)

Wraz ze wzrostem P(Swiatlo=wl. / w biurze) rosnie zarowno prior, jak i prawdopodobienstwo warunkowe. Roznica miedzy nimi takze rosnie - dla wartosci 0,90 wynosi az 0,44. Obserwacja Teams jest tym bardziej wartosciowa, im czesciej K. zostawia swiatlo wlaczone bedac w biurze.

Wnioski: Parametr ten bezposrednio kontroluje, jak mocno obecnosc K. w biurze przekklada sie na stan swiatla. Gdy P(Swiatlo=wl. / w biurze) jest male, informacja o Teams nie pomaga - nawet jesli wiemy, ze K. jest w biurze, swiatlo i tak rzadko bywa wlaczone.

---

### Eksperyment 3 - wplyw P(Teams = zalogowana / w biurze)

Stale parametry: P(w biurze) = 0,40, P(Swiatlo=wl. / w biurze) = 0,50, P(Swiatlo=wl. / zdalnie) = 0,05, P(Teams=zalog. / zdalnie) = 0,05.

Badany zakres: P(Teams=zalog. / w biurze) in {0,20; 0,40; 0,60; 0,80; 0,95}.

| P(Teams=zalog. / w biurze) | P(Swiatlo=wl.) | P(Swiatlo=wl. / Teams=zalog.) | Roznica |
|---|---|---|---|
| 0,20 | 0,23 | 0,38 | 0,15 |
| 0,40 | 0,23 | 0,43 | 0,20 |
| 0,60 | 0,23 | 0,45 | 0,22 |
| 0,80 | 0,23 | 0,46 | 0,23 |
| 0,95 | 0,23 | 0,47 | 0,24 |

![wykres eksperymentu 3](plots/exp3_p_teams_given_in.png)

Prior P(Swiatlo=wl.) pozostaje stalY dla wszystkich wartosci parametru - co jest poprawne, poniewaz zmiana wiarygodnosci Teams nie wplywa na brzegowe prawdopodobienstwo swiatla. Wzrost P(Teams=zalog. / w biurze) powoduje wzrost P(Swiatlo=wl. / Teams=zalog.), jednak efekt jest stosunkowo niewielki - miedzy wartoscia 0,20 a 0,95 roznica wynosi tylko 0,09.

Wnioski: Wiarygodnosc Teams jako wskaznika obecnosci w biurze ma umiarkowany wplyw na wynik wnioskowania. Nawet przy niskiej wiarygodnosci (0,20) informacja o logowaniu nadal podnosi prawdopodobienstwo wlaczonego swiatla. Efekt nasycenia jest widoczny juz powyzej wartosci 0,60.

---

### Eksperyment 4 - wplyw P(Teams = zalogowana / zdalnie)

Stale parametry: P(w biurze) = 0,40, P(Swiatlo=wl. / w biurze) = 0,50, P(Swiatlo=wl. / zdalnie) = 0,05, P(Teams=zalog. / w biurze) = 0,80.

Badany zakres: P(Teams=zalog. / zdalnie) in {0,01; 0,05; 0,15; 0,30; 0,50}.

| P(Teams=zalog. / zdalnie) | P(Swiatlo=wl.) | P(Swiatlo=wl. / Teams=zalog.) | Roznica |
|---|---|---|---|
| 0,01 | 0,23 | 0,49 | 0,26 |
| 0,05 | 0,23 | 0,46 | 0,23 |
| 0,15 | 0,23 | 0,40 | 0,17 |
| 0,30 | 0,23 | 0,34 | 0,11 |
| 0,50 | 0,23 | 0,28 | 0,05 |

![wykres eksperymentu 4](plots/exp4_p_teams_given_out.png)

Prior pozostaje staly, natomiast P(Swiatlo=wl. / Teams=zalog.) wyraznie maleje wraz ze wzrostem P(Teams=zalog. / zdalnie). Przy wartosci 0,50 informacja o zalogowaniu w Teams jest prawie bezuzyteczna - prawdopodobienstwo wzrasta jedynie o 0,05 w stosunku do prioru.

Wnioski: Jest to parametr o najwiekszym wplywie na uzytecznosc obserwacji Teams. Im czesciej K. loguje sie do Teams z domu, tym slabszym dowodem na jej obecnosc w biurze jest status zalogowania. W skrajnym przypadku (P = 0,50), gdy K. loguje sie zdalnie rownie czesto co z biura, obserwacja Teams niemal nie zmienia przekonania o stanie swiatla.

---

## Wnioski koncowe

| Parametr | Zakres badan | Wplyw na P(Swiatlo=wl. / Teams=zalog.) |
|---|---|---|
| P(w biurze) | 0,10 - 0,80 | Rosnie, efekt informacyjny Teams maleje |
| P(Swiatlo=wl. / w biurze) | 0,10 - 0,90 | Silny wzrost liniowy |
| P(Teams=zalog. / w biurze) | 0,20 - 0,95 | Slaby wzrost, szybkie nasycenie |
| P(Teams=zalog. / zdalnie) | 0,01 - 0,50 | Silny spadek - parametr krytyczny |

Konfiguracja bazowa z tresci zadania daje P(Swiatlo=wl.) = 0,23 oraz P(Swiatlo=wl. / Teams=zalog.) = 0,46. Zaobserwowanie statusu zalogowania w Teams niemal podwaja prawdopodobienstwo wlaczonego swiatla w tym scenariuszu.

Eksperymenty pokazuja, ze uzytecznosc informacji o statusie Teams jako dowodu na wlaczone swiatlo zalezy w najwiekszym stopniu od dwoch parametrow: P(Swiatlo=wl. / w biurze) oraz P(Teams=zalog. / zdalnie). Pierwszy z nich kontroluje, jak mocno obecnosc w biurze przekklada sie na stan swiatla - im wyzszy, tym bardziej warto wiedziec, czy K. jest w biurze. Drugi parametr decyduje o diagnostycznosci samego Teams jako wskaznika lokalizacji - gdy K. loguje sie zdalnie rownie czesto co z biura, status Teams przestaje byc uzytecznym dowodem.

Parametr P(Teams=zalog. / w biurze) ma zaskakujaco maly wplyw w porownaniu z pozostalymi - efekt nasycenia pojawia sie juz przy wartosci okolo 0,60, a dalszy wzrost do 0,95 zmienia wynik jedynie o 0,02. Wynika to z tego, ze przy stosunkowo niskim P(Teams=zalog. / zdalnie) = 0,05 juz srednia wiarygodnosc Teams z biura wystarcza do uzyskania silnego sygnalu.
