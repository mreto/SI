Aby przygotować interpreter dla pythona należy sciągnąć anaconde, stworzyć środowisko dla pliku environment.yml, i aktywować 'source activate si'. Plik script.py generuje z artykułów w folderze article/ dane w formacie odpowiednim dla skryptu w octave som.m. Python generuje następujące dane 
 - ./data/basic_data/
   - zsumowane wyniki dla osobno artykułów sugerujące katastrofę i zamach
   - zsumowane dane razem (katastrofa + zamach)
   - dane na podstawie artykułów z Wikipedii które teoretycznie powinny być neutralne
 - ./data/biased_assasination/
 - ./data/biased_catastrophy/
   W obu folderach znajdują się foldery part i multiply.
   W folderach part znajdują się dane zsumowane z danych netruralnych + (i/30) * biased.
   Teoretycznie dane te powinny pokazywać jak poglądy neutralne 
   powoli zmieniają się biased.
   W folderach multiply znajdują się zsumowane dane neutral + i * biased.
 - ./data/single_articles_data/
   Dane dla pojedynczych artykułów z articles/. Na ich podstawie można sprawdzać czy 
   rzeczywiście pojedyncze artykuły są bliżej danych zsumowanych w ./data/basic_data
Skrypt w octavie generuje odpowiednie mapy w formacie .jpg do folderu som_maps/ oraz porównuje numerycznie 
wektory w somach, na ich podstawie można sprawdzać czy somy są podobne czy nie. Wyniki porównań są w ./numerical_compare/

