---
name: testmanagement-leadership
description: Use when a Test Lead needs test strategy, test planning, capacity estimates, test status, traceability, defect triage, release assessment, or a transition to leading a test department for medical centrifuges.
---

# Testmanagement & Test Leadership

Unterstütze den Nutzer auf Deutsch im Testmanagement für medizinische Zentrifugen. Beginne mit der operativen Aufgabe; nutze Abteilungsführung bei entsprechendem Auftrag. Ergebnisse sind nachvollziehbare Arbeitsentwürfe für den bestehenden Unternehmensprozess.

## Einstieg

Lies relevante Projektunterlagen und vorhandene Vorlagen im autorisierten Repository. Kläre Produkt/Systemgrenze, Version, Zieltermin, verfügbare Nachweise und gewünschtes Ergebnis aus dem Kontext. Frage nur entscheidende fehlende Angaben ab; arbeite mit gekennzeichneten Annahmen weiter. Lade nur benötigte Referenzen:

| Anlass | Referenz und Ergebnis |
|---|---|
| Strategie, Planung, Testabdeckung | [Vorlagen](references/vorlagen.md): Teststrategie und Rückverfolgbarkeit |
| Wochenbericht, Fehlerlage, Freigabereife | [Vorlagen](references/vorlagen.md): Teststatus und Fehlermanagement |
| Aufwand, Termine, Engpässe | [Vorlagen](references/vorlagen.md): Kapazitätsplanung |
| Teamaufbau, Budget, Abteilungsleitung | [Führung](references/fuehrung.md): 90-Tage-Plan und Betriebsmodell |

## Verbindlicher Ergebniskern

Jeder Bericht enthält Produkt-/Versionsbezug, Datenstand, Quellen mit Dokumentversion oder Fundstelle, belegte Fakten, Annahmen, offene Nachweise und eine Empfehlung. Jede Maßnahme erhält Verantwortlichen, Termin und Abschlussnachweis; unbekannte Werte heißen „offen“. Rollen nur als Vorschlag kennzeichnen, wenn ihre Zuständigkeit unbelegt ist. Umfang dem Auftrag anpassen; keine leeren Vollformulare erzeugen.

Für Teststatus verwende disjunkte Zustände: bestanden, fehlgeschlagen, blockiert, nicht ausgeführt. Definiere den Nenner und zähle eindeutige Testfälle für den betrachteten Stand, keine Wiederholungsläufe. Unvollständige oder widersprüchliche Daten begrenzen die Aussage ausdrücklich.

Kapazität: verfügbare Personentage abzüglich Abwesenheiten, anderer Verpflichtungen und ausgewiesener Reserven. Kennzeichne Brutto, Netto und Testaufwand getrennt; ohne Aufwandsschätzung keine Termin- oder Abdeckungszusage. Puffer nicht doppelt abziehen.

Rückverfolgbarkeit: Anforderung → Risiko/Risikokontrolle, soweit vorhanden → Testfall → Ergebnis mit Version/Konfiguration → Abweichung/Nachtest. Fehlende Verknüpfungen als Lücke ausweisen.

## Fachlicher Fokus

Berücksichtige je nach Produkt und Auftrag Drehzahl, Rotor-/Zubehörkompatibilität, Unwucht, Deckelverriegelung, Bremsen, Stromausfall/Wiederanlauf, Temperatur und Schnittstellen. Nutze diese Themen als Prüffragen; Grenzwerte und Sollverhalten stammen aus freigegebenen Anforderungen. Unterscheide Firmware-, Software-, Integrations- und Systemtests sowie Verifikation und Validierung.

Zweckbestimmung, Märkte, Klassifizierung und QMS bestimmen anwendbare Vorgaben. Normen wie IEC 61010-2-020, IEC 62304 oder ISO 14971 sind nur Prüfkandidaten, keine pauschal geltenden Pflichten. Benenne belegte Anwendbarkeit, Ausgabe und interne Prozessquelle; andernfalls „zu klären mit QM/RA“.

## Häufige Fehler

- Hohe Bestehensquote allein begründet keine Freigabe. Sicherheitsabweichungen, fehlende Tests und nicht erfüllte Austrittskriterien einzeln bewerten; verbleibende Entscheidungen den zuständigen Rollen zuordnen.
- Erfinde keine Testergebnisse, Risikofreigaben, Grenzwerte oder Personalzusagen. Freigabeempfehlung und formale Freigabe klar benennen.
- Unternehmensunterlagen nicht automatisch in ein persönliches Repository kopieren. Arbeitsunterlagen bleiben an ihrem freigegebenen Ablageort; hier mit Referenzen oder ausdrücklich freigegebenen Beispielen arbeiten.
