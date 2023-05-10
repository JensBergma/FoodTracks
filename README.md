# FoodTracks
Vorraussetzungen 
- Python muss auf der Machine installiert sein
- Beim Eintwickeln und erstellen der Befehle habe ich Windows und Visual Studio Code verwendet

Quellcode öffnen
- Terminal öffnen und sich im Ordner FoodTracks befinden
- Das Virtuelle Environment auf die aktuellen Pfade setzen
	-> py -m venv <Pfad von dem Repo>\FoodTracks\\.venv (z. B. C:\Programmieren\Python\FoodTracks\\.venv )
- Die Virtuelle Umgebung starten
	-> .\.venv\Scripts\activate
		->(Sollte das nicht funktionieren, kann es an der ExecutionPolicy liegen. Hiefür einmal folgendes ausführen -> Set-ExecutionPolicy RemoteSigned -Scope Process)
- Den Quellcode/Server starten
	-> py manage.py runserver
	
- Jetzt sollte man sich anmelden können, mit Benutzername: foodtracks und Kennwort: admin
	-> Falls nicht, dann einmal neuen Benutzer anlegen mit -> py manage.py createsuperuser  
	
Zum Authentifiziern den Endpoint /api-token-auth/
Anschließend den token für die Authentifiziern benutzen

Als Dokumentation habe ich swagger und redoc eingerichtet.
	-> Dafür einfach /swagger/ oder /redoc/ nach der IP-Adresse angeben (z. B. http://127.0.0.1:8000/redoc/)	
	
Zum Ausführen der Unit-Test
	-> py manage.py test

Dokumentation: https://docs.google.com/document/d/1BeI8JpqD-71kJMp_olvjc0vb9StBdztEPVbUrpwaE4o/edit?usp=sharing
