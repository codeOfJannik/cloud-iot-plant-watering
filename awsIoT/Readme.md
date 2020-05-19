# AWS IoT einrichten
## Manuelles Setup

Suche in der AWS Konsole den Service *IoT Core*.

**1. Ein Objekt (Thing) anlegen**

Auswahl des Menüpunkts *Integrieren* im Menü und anschließend *Erste Schritte* startet den Assistenten zum Anlegen neuer Objekte.
Klicke dich durch den Assistenten, wähle eine Platform und ein SDK aus (Linux & Python) und gebe einen Namen für dein Objekt ein.
Änderungen in der optionalen Konfiguration werden nicht benötigt.

**2. Download der Schlüssel und Zertfikate**

Um den Assistenten abzuschließen müssen privater und öffentlicher Schlüssel, sowie ein generiertes Zertifikat, in einem ZIP-Ordner
heruntergeladen werden.

**3. Objekt, Zertifikat und Richtlinie angelegt**

Nach dem Download ist das Setup in der AWS Konsole abgeschlossen. Nun sollte unter *Verwalten > Objekte* das angelegte Objekt sichtbar sein.
Außerdem sollte unter *Sicher > Zertifikate* ein neues Zertifikat und unter *Sicher > Richtlinien* eine neue Richtline sichtbar sein.

**4. Heruntergeladene Dateien entpacken**

Um die Software des angelegten Geräts zu simulieren, muss ein Ordner für das Objekt neben dem Dockerfile angelegt werden. In diesem Ordner wird ein Ordner *aws* erstellt.
Im Ordner *aws* wird die heruntergeladene ZIP Datei entpackt. Die Dateistruktur sollte dann wie folgt aussehen:

\- Dockefile
\- your_object_directory
\-- aws
\--- your_object.cert.pem
\--- your_object.private.key
\--- your_object_public.key
\--- start.sh

**5. start.sh und test.sh vorbereiten**

Öffne die entpackte Datei *start.sh* und kommentiere die letzten beiden Zeilen aus:

''' sh
# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e your-endpoint.amazonaws.com -r root-CA.crt -c your-cert.cert.pem -k your_key.private.key
'''

wird zu 

''' sh
# run pub/sub sample app using certificates downloaded in package
#printf "\nRunning pub/sub sample application...\n"
#python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e your-endpoint.amazonaws.com -r root-CA.crt -c your-cert.cert.pem -k your_key.private.key
'''

Alternativ kann die entpackte *start.sh*-Datei auch durch die *start.sh*-Datei des Repos (*/soil_moisture_1/aws/start.sh*) ersetzt werden.

Anschließend muss die eine neue Datei *test.sh* mit folgendem Inhalt erstellt werden:

''' sh
printf "\nRunning pub/sub sample application...\n"
python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e <YOUR-ENDPOINT>.amazonaws.com -r root-CA.crt -c <YOUR-CERTIFICATE>.cert.pem -k <YOUR-PRIVATEKEY>.private.key
'''
Der AWS-Endpoint, sowie die Dateinamen für Zertifikat und privaten Schlüssel müssen mit den korrekten Werten ersetzt werden. Der korrekte benutzerdefinierte Endpunkt ist in der AWS Konsole
in den Einstellungen des IoT-Core Service zu finden.

**6. docker build ausführen**

Führe im erstellten Objektordner (im Repo bspw. /soil_moisture_1) folgenden docker build Befehl aus. Wähle einen Name für das Docker Image.

'docker build -t <YOUR-DOCKER-IMAGE-NAME> -f ../Dockerfile .'

**7. Teste das Objekt**

Starte nach dem Build das erstellte Docker Image mit 'docker run <YOUR-DOCKER-IMAGE-NAME>'.

In der AWS Konsole kann nun unter dem Menüpunkt *Test* die Funktionalität geprüft werden. Mit einem Abbonement auf das Thema *#*, sollten alle vom Objekt gepublishten
Testnachrichten angezeigt werden und ein Publishen auf das Topic *sdk/test/Python* sollte die Nachrichten im Log des Docker Containers anzeigen.

