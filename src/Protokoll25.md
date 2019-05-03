Protokoll
========

> Ist Restconf auf dem Router verfügbar?

Ja, wenn das Mgmt Package installiert wird, 
dann sollte Restconf vorhanden sein auf dem Router.
Einen Http Server ist nicht nötig.

> Warum bekomme ich bei Oper Anfragen und Openconfig lehre Daten zurück?

Bei Oper Modellen muss zuerst `streaming-telemetry` aktiviert werden und
dann sollte man Daten bekommen.

Von Openconfig sollten wir die Finger lassen, die Swisscom hat keine
guten Erfahrungen mit Openconfig gemacht. Cisco garantiert, dass die
proprietären Modelle implementiert sind. Diese sind nach Kundenwünschen
implementiert. Da müsen wir das Gegebene akzeptieren.

> Gibt es weitere Dokumentation zum YDK und Netconf bei XR Router Software?

Marcel schaut bei Cisco Intern nach.