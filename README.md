# Cocktails analysis
# Podsumowanie analizy
Jest umieszczone w ```cocktails_analysis.pdf``` - plik został opracowany za pomocą LaTeX.

# Powtórzenie eksperymentów
Dla powtórzenia eksperymentów stworzyłem pliki ```.py``` które są umieszczone w root folderze repositoria, są oni wykorzystae w ```cocktails_clean.ipynb``` gdize owszem można poeksperementować ze wszystkim, i równocześnie zejrzeć w zawartość pomocniczych plików ```.py```.
Jeżeli jest chęć zanurkować w przebieg preprocessingu, augmentacji, analizy i klasteringu, można zejrzeć w ```cocktails_draft.ipynb``` który leży w folderze ```Source```, z którego później zostali wyekstraktowane pliki ```.py``` i utworzony ```cocktails_clean.ipynb```

# Tworzenie conda environment
Jeżeli chcesz powtórzyć eksperymenty lokalnie: 
```conda create --name <env> --file requirements.txt``` - aby utworzyć conda env dla uruchomienia ```cocktails_clean.ipynb``` lub ```cocktails_draft.ipynb``` (zakomentować ```!pip install pulp```, biblioteka była instalowana podczas pracy w colab).
