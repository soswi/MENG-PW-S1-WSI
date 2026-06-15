# Modyfikacje wzgledem oryginalnej wersji

## p_minmax.py

- Dodano `import math` - wymagany przez `math.inf` uzywane w alfa-beta.

- Zaimplementowano `make_move` - oryginalna zaslepka zwracala `None`, co powodowalo crash w `engine.py`. Metoda wywoluje `minimax` z perspektywy aktualnego gracza i zwraca indeks najlepszego pola.

- Zaimplementowano `minimax` - oryginalna zaslepka zwracala `(None, None)`. Dodano pelna implementacje algorytmu minimax z przycinaniem alfa-beta. Sygnatura rozszerzona o parametry `alpha`, `beta` z wartosciami domyslnymi `-inf`/`inf` oraz flage `maximizing` z wartoscia domyslna `True` - bez tych parametrow alfa-beta nie moze byc zaimplementowane. Wartosci domyslne zachowuja kompatybilnosc z oryginalnym wywolaniem `minimax(board, side, depth)`.

- Zaimplementowano `evaluate` - oryginalna zaslepka zwracala zawsze `0`, co przy ograniczonej glebokosci powodowalo ze gracz traktowal wszystkie stany nieterminalne jako rownowazne i gral de facto losowo. Metoda liczy linie otwarte dla danego gracza minus linie otwarte dla przeciwnika, znormalizowane do przedzialu (-1, 1).

## ttt.py

- Rozmiar planszy przeniesiony z hardkodowanej stalej `board_size = 3` do argumentu wiersza polecen `argv[3]` - umozliwia uruchomienie gry na planszy innego rozmiaru bez modyfikacji kodu, co jest wymagane przez zadanie (punkty 2 i 3 dla planszy 3x3 i wiekszej).

- Pojedynczy wspolny `depth_limit` zastapiony dwoma osobnymi zmiennymi `depth1` i `depth2` czytanymi z `argv[4]` i `argv[5]` - punkt 3 zadania wymaga wprost konfiguracji roznych poziomow glebokosci dla dwoch graczy min-max.

- Dodano funkcje pomocnicza `default_depth` zwracajaca domyslna glebokoscz gdy nie zostanie podana w argumentach: 9 dla planszy 3x3 (pelne drzewo), 6 dla plansz wiekszych. Ograniczenie do 6 dla plansz wiekszych niz 3x3 jest konieczne - jak zaobserwowano empirycznie, glebokoscz 9 na planszy 4x4 powoduje czas obliczen rzedu kilku minut juz na pierwszym ruchu.
