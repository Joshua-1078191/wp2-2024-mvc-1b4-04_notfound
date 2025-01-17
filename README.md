# Automatic Taxonomy using LLMs

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db) met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.

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
## Joshua
- 
## Roos
- 
## Jorik
- 
## Tobias
- Readonly checkboxes: ​(GeeksForGeeks, 2024)​
- Input types: ​(developer.mozilla, 2024)​

P.S. Voor uitgebreide bronnenlijst/APA 7-vermelding zie bibliografie.

# Bibliografie
- developer.mozilla. (2024, november 1). <input>: The HTML Input element. Opgehaald van www.developer.mozilla.org: https://developer.mozilla.org/en-     US/docs/Web/HTML/Element/input

- GeeksForGeeks. (2024, januari 5). How to Set Checkboxes Readonly in HTML ? Opgehaald van www.geeksforgeeks.org: https://www.geeksforgeeks.org/how-to-set-checkboxes-readonly-in-html/
