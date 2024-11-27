# WP2 Starter 

Dit is de starter repository voor WP2 2024. Deze bevat: 
- De [casus](CASUS.md)
- Een uitleg over hoe [ChatGPT te gebruiken in Python code](CHATGPT.md)
- Een lijst met [voorbeeld vragen](questions_extract.json) die we willen categoriseren
- Een SQLite [database](databases%2Fdatabase.db) met tabellen voor gebruikers, vragen en AI prompts.
- De [database tool](lib%2Fdatabase%2Fdatabase_generator.py) om een nieuwe database mee te genereren. Deze is vrij aan te passen.

Afspraken jinja template inheritance:
- Gebruik een block voor de navigation bar.
- Gebruik een block voor de footer.
- Gebruik een block voor de sidebar.

Folder structuur
```python
.
├── database/  # sqlite database bestand(en)
├── docs/      # documentatie van het project
├── lib/       # libraries (database generator en gpt module)
├── src/       # source code voor test-correct taxonomie programma
├── static/    # Statische bestanden (PNG, JPG, JS, CSS, Ect.)
└── templates/  # Jinja/HTML bestanden
```
