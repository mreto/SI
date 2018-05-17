Aby przygotować interpreter dla pythona należy sciągnąć anaconde, stworzyć środowisko dla pliku environment.yml i aktywować 'source activate si'. Plik script.py generuje z artykułów w folderze article/ dane w formacie odpowiednim dla skryptu w octave som.m. Python generuje następujące dane 
 - ./data/basic_data/
   - zsumowane wyniki dla osobno artykułów sugerujących katastrofę i zamach
   - zsumowane dane razem (katastrofa + zamach)
   - dane na podstawie artykułów z Wikipedii, które można uznać za neutralne
 - ./data/biased_assasination/
 - ./data/biased_catastrophy/
   W obu folderach znajdują się foldery part i multiply.
   W folderach part znajdują się dane zsumowane z danych netruralnych + (i/30) * biased, czyli 29 stadiów pośrednich pomiędzy artykułami stronniczymi i neutralnymi uzyskanych poprzez dodawanie stopniowo do zbioru artykułów neutralnych coraz większych porcji artykułów stronniczych.
   Dane te powinny pokazywać, jak poglądy neutralne stopniowo zbliżają się do stronniczych.
   W folderach multiply znajdują się zsumowane dane neutral + i * biased, czyli 29 stadiów pośrednich pomiędzy artykułami stronniczymi i neutralnymi uzyskanych poprzez dodawanie do zbioru artykułów neutralnych kolejnych wielokrotności zbioru artykułów stronniczych, tak aby zmienić proporcje liczności zbioru artykułów stronniczych względem neutralnych.
 - ./data/single_articles_data/
   Dane dla pojedynczych artykułów z articles/. Na ich podstawie można sprawdzać, czy rzeczywiście pojedyncze artykuły są bliżej danych zsumowanych w ./data/basic_data/.
   
Skrypt w octavie generuje odpowiednie mapy (SOM) w formacie .jpg do folderu som_maps/ oraz porównuje numerycznie 
wektory w SOM-ach. Na ich podstawie można sprawdzać, czy są one podobne czy nie. Wyniki porównań znajdują się w ./numerical_compare/.

