# Automatic Taxonomy using LLMs

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db) met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.

# Installatie requirements

#### Stap 1: Installeer Python 3.12 (indien nog niet geïnstalleerd).
Ga naar de officiële Python-website en download de installer voor Python 3.12:
https://www.python.org/downloads/release/python-3120/

Zorg ervoor dat je de optie 'Add Python to PATH' aanvinkt tijdens de installatie, zodat je Python vanuit de commandoregel kunt gebruiken.

#### Stap 2: Maak een locale kloon van de repository aan.
```shell
git clone https://github.com/Rac-Software-Development/wp2-2024-mvc-1b4-04_notfound.git
```

#### Stap 3: Navigeer naar de map van de gekloonde repository.
```shell
cd wp2-2024-mvc-1b4-04_notfound
```

#### Stap 4: Maak een virtuele omgeving aan om de benodigde Python-pakketten geïsoleerd te installeren.
```shell
python -m venv .venv
```

#### Stap 5: Activeer de virtuele omgeving.
```shell
.\.venv\Scripts\activate
```

#### Stap 6: Installeer flask (3.1.0), cryptography (44.0.0), openai (1.57.4) en ollama (0.4.4)
```shell
pip install -r requirements.txt
```

# Applicatie opstarten
Als je in de virtual environment zit kan je applicatie start op met het volgende commando:
```shell
flask run
```

# Ontwerpdocumentatie
## Visuele ontwerpdocumentatie:
Aan het begin van WP2 hebben we wireframes gemaakt met Balsamiq o.b.v. de voorbeelden uit de casus. We hebben daarna deze gebruikt om 'bare-bones' HTML pagina's te maken. Toen we begonnen met het stijlen van de pagina's liepen we al snel tegen problemen aan. We gebruikten namelijk CSS en dit veroorzaakte verschillende problemen. We hebben daarom beslist om over te stappen op Bootstrap; Een flexibele en krachtige frontend library. Hiermee ging het stijlen van de pagina's een stuk sneller en zag het er een stuk beter uit. 

Omdat we merkten dat de front-end nog niet helemaal gelijk was op elke pagina zijn we aan het eind van sprint 3 begonnen met het maken van een reference page met Bootstrap. Hier hebben we alle veel gebruikte HTML elementen uitgewerkt en met bootstrap gestyled naar de website van Test-correct.

## Technische ontwerpdocumentatie
We hebben bij ons project gebruik gemaakt van de CRUD-model om het opslaan, aanmaken, wijzigen en verwijderen van data te faciliteren. We hebben die functies als volgt verdeelt:
- Templates/static: Hier staan alle HTML, CSS en overige bestanden die voor het uiterlijke van de pagina's zorgen (frontend). Variabelen en de vaste layout (d.m.v. inheritance/templating) zijn met Jinja in de HTML files verwerkt.
- src: In deze map staan alle models die de verbinding leggen tussen de app.py en de database. Deze models zijn met python geschreven en maken gebruik van de SQLite3 package. Deze maakt verbinding met de database (in /lib) en stuurt queries (o.b.v. data van app.py) naar de database en stuurt de data daarna weer terug.

In de app.py file komen al deze verschillende onderdelen samen. We hebben hier routes gemaakt voor alle pagina's/functies. Ook hebben we hier alle functies van de models staan die van hieruit de data versturen naar de models of weergeven op de pagina's. We maken hierbij gebruik van de Flask module die ons handige functies biedt zoals render_template, request en url_for.

# Coding standerds/conventions:
Afspraken jinja template inheritance/bootstrap/css:
- Gebruik op elke pagina de layout.html.jinja file uit de templates folder. Voeg deze toe met de {% extends .... %}-functie
- Houd je op elke pagina aan de HTML code standards/conventions:
     - Schrijf je CSS in aparte bestanden (niet in het HTML element zelf)
     - Gebruik geen/zo min mogelijk JS
     - Schrijf alle HTML binnen de {% block content %}-functie van Jinja
 

# Folder structuur
```python
.
├── database/  # sqlite database bestand(en)
├── docs/      # documentatie van het project
├── lib/       # libraries (database generator en gpt module)
├── src/       # source code voor test-correct taxonomie programma
├── static/    # Statische bestanden (PNG, JPG, JS, CSS, Ect.)
└── templates/  # Jinja/HTML bestanden
```

# Navigatie:
De gebruiker begint altijd op de homepagina. Van hieruit kan de gebruiker naar drie verschillende pagina's navigeren:
- Het vragenoverzicht. Hier kan je alle vragen zien en filters toepassen. Van hieruit kan de gebruiker:
     - Vragen importeren
     - Nieuwe vraag toevoegen
     - Vragen exporteren
     - Een vraag aanpassen
- Het promptsoverzicht. Hier kan je een lijst van alle prompts zien. Van hieruit kan de gebruiker:
     - Een nieuw prompt toevoegen
     - Een prompt verwijderen
     - De details van een prompt bekijken
- Het redacteurenoverzicht. Hier ziet de gebruiker een overzicht van alle redacteuren. Van hieruit kan de gebruiker:
     - (eigen) Gegevens aanpassen
     - Een nieuwe redacteur aanmaken

# Bronnenlijst:
- (Bootstrap, Background, 2025)
- (Bootstrap, Flex, 2025)
- (Bootstrap, Floating labels, 2025)
- (Bootstrap, Form controls - file input, 2025)
- (Bootstrap, Forms, 2025)
- (Bootstrap, Layout, 2025)
- (Bootstrap, Tables, 2025)
- (Bootstrap, Text, 2025)
- (GeeksforGeeks, Flask HTTP methods, handle GET & POST requests., 2023)
- (GeeksforGeeks, How to Center a Flex Container but Left-Align Flex Items?, 2024)
- (docs, 2025)
- (Jibin, 2017)
- (kasperhj, 2013)
- (Kimmy, 2013)
- (Sheldon, 2021)
- (Barclay, 2024)
- (Tagliaferri, 2021)
- (Flask, 2010)
- Readonly checkboxes: ​(GeeksForGeeks, 2024)​
- Input types: ​(developer.mozilla, 2024)​
- (Balsamiq, 2025) 
- (Haim, 2024)
- (Bootstrap, Tables, 2025)
- (w3schools, 2025)
- (Bootstrap, Tooltips - Overflow auto and scroll, 2025)
- (w3schools.com, 2025)
- (Bootstrap, Checks and radios, 2025)

P.S. Voor uitgebreide bronnenlijst/APA 7-vermelding zie bibliografie.

# Bibliografie
- Balsamiq. (2025). Editing controls - The data grid (table) control. Retrieved from Balsamiq.com: https://balsamiq.com/wireframes/desktop/docs/datagrids/
- Barclay, G. (2024, Maart 1). Argon2 vs bcrypt vs. scrypt: which hashing algorithm is right for you? Retrieved from Stytch: https://stytch.com/blog/argon2-vs-bcrypt-vs-scrypt/
- Bootstrap. (2025). Background. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/5.0/utilities/background/
- Bootstrap. (2025). Checks and radios. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/5.1/forms/checks-radios/
- Bootstrap. (2025). Flex. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/4.0/utilities/flex/
- Bootstrap. (2025). Floating labels. Retrieved from getbootstrap: https://getbootstrap.com/docs/5.0/forms/floating-labels/
- Bootstrap. (2025). Form controls - file input. Retrieved from Bootstrap: https://getbootstrap.com/docs/5.0/forms/form-control/#file-input
- Bootstrap. (2025). Forms. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/5.0/forms/overview/
- Bootstrap. (2025). Layout. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/5.0/forms/layout/
- Bootstrap. (2025). Tables. Retrieved from Getbootstrap.com: https://getbootstrap.com/docs/4.0/content/tables/
- Bootstrap. (2025). Text. Retrieved from Getbootstrap.com: https://getbootstrap.com/docs/5.0/utilities/text/
- developer.mozilla. (2024, november 1). <input>: The HTML Input element. Retrieved from www.developer.mozilla.org: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input
- docs, M. w. (2025). Aligning items in a flex container. Retrieved from MDN web docs: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Aligning_items_in_a_flex_container
- Flask. (2010). Uploading Files. Retrieved from Flask: https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
- GeeksforGeeks. (2023, Februari 2). Flask HTTP methods, handle GET & POST requests. Retrieved from GeeksforGeeks.org: https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/
- GeeksforGeeks. (2024, Juli 31). How to Center a Flex Container but Left-Align Flex Items? Retrieved from GeeksforGeeks.org: https://www.geeksforgeeks.org/how-to-center-a-flex-container-but-left-align-flex-items/#using-margin-auto-on-the-flex-container
- GeeksForGeeks. (2024, januari 5). How to Set Checkboxes Readonly in HTML ? Retrieved from www.geeksforgeeks.org: https://www.geeksforgeeks.org/how-to-set-checkboxes-readonly-in-html/
- Haim, I. (2024, mei 14). How To Center A Table In CSS / HTML. Retrieved from elementor.com: https://elementor.com/blog/how-to-center-a-table-in-css/#:~:text=Method%201%3A%20margin%3A%200%20auto%3B,-This%20is%20the&text=Set%20Margins%20to%20Auto%3A%20By,the%20table%20into%20the%20center. 
- Jibin. (2017, Juni 2). select required not working. Retrieved from Stackoverflow: https://stackoverflow.com/questions/44322824/select-required-not-working
- kasperhj. (2013, Januari 19). Common folder/file structure in Flask app [closed]. Retrieved from Stackoverflow: https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app
- Kimmy. (2013, Juni 26). How to debug a Flask app. Retrieved from Stackoverflow: https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app
- Sheldon. (2021, November 9). How do I determine if the row has been inserted? Retrieved from Stackoverflow: https://stackoverflow.com/questions/13313694/how-do-i-determine-if-the-row-has-been-inserted
- Tagliaferri, L. (2021, Augustus 20). How To Use *args and **kwargs in Python 3. Retrieved from digitalocean.com: https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
- w3schools. (2025). CSS Layout - The position Property. Retrieved from w3schools.com: https://www.w3schools.com/css/css_positioning.asp
- w3schools.com. (2025). How TO - Custom Scrollbar. Retrieved from w3schools.com: https://www.w3schools.com/howto/howto_css_custom_scrollbar.asp
