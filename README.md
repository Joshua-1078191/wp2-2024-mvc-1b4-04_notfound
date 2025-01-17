# Automatic Taxonomy using LLMs

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db) met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.

# Installatie requirements
Installeer python (3.12), flask (3.1.0), cryptography (44.0.0), openai (1.57.4) en ollama (0.4.4)
```shell
pip install -r requirements.txt
```

# applicatie opstarten
De applicatie start op met het volgende commando:
```shell
flask run
```

# coding standerds/conventions:
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

P.S. Voor uitgebreide bronnenlijst/APA 7-vermelding zie bibliografie.

# Bibliografie
- Barclay, G. (2024, Maart 1). Argon2 vs bcrypt vs. scrypt: which hashing algorithm is right for you? Retrieved from Stytch: https://stytch.com/blog/argon2-vs-bcrypt-vs-scrypt/

- Bootstrap. (2025). Background. Retrieved from getbootstrap.com: https://getbootstrap.com/docs/5.0/utilities/background/
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

- Jibin. (2017, Juni 2). <select> required not working. Retrieved from Stackoverflow: https://stackoverflow.com/questions/44322824/select-required-not-working
- kasperhj. (2013, Januari 19). Common folder/file structure in Flask app [closed]. Retrieved from Stackoverflow: https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app
- Kimmy. (2013, Juni 26). How to debug a Flask app. Retrieved from Stackoverflow: https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app
- Sheldon. (2021, November 9). How do I determine if the row has been inserted? Retrieved from Stackoverflow: https://stackoverflow.com/questions/13313694/how-do-i-determine-if-the-row-has-been-inserted

- Tagliaferri, L. (2021, Augustus 20). How To Use *args and **kwargs in Python 3. Retrieved from digitalocean.com: https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
