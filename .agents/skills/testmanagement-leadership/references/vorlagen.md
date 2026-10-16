# Operative Arbeitsvorlagen

Nur benötigte Abschnitte verwenden. Platzhalter sind keine erhobenen Daten. Ergebnis als Entwurf kennzeichnen und vorhandene Unternehmensvorlagen vorrangig verwenden.

## Gemeinsamer Dokumentkopf

- Produkt/Systemgrenze, Hardware-/Firmware-/Softwarestand, relevante Konfiguration:
- Zweck, Betrachtungszeitraum und Datenstand:
- Autor, Dokumentversion und Reviewstatus:
- Quellen mit Dokumentversion/Fundstelle:
- Fakten / Annahmen / offene Angaben:

## Teststrategie und Testplan

1. Testziele, Umfang und begründete Ausschlüsse einschließlich Auswirkungen.
2. Priorisierung aus Anforderungen, Produktänderungen, Risikoanalyse und Fehlerhistorie.
3. Teststufen und Verfahren: Reviews, statische Prüfungen, manuelle/automatisierte Tests, Regression, Verifikation/Validierung entsprechend Prozess.
4. Testbasis mit Versionsbezug; Rückverfolgbarkeit und Konfigurationsmanagement.
5. Testobjekte, Umgebungen, Simulatoren, Prüfmittelstatus, Testdaten und Reproduzierbarkeit.
6. Ressourcen, Fähigkeiten, Aufwand, Abhängigkeiten und Meilensteine.
7. Eintritts-, Unterbrechungs-, Wiederaufnahme- und Austrittskriterien mit überprüfbaren Nachweisen; fehlende Kriterien als Vorschlag ausweisen.
8. Fehlerprozess, Berichtsrhythmus, Review- und Entscheidungsrollen.

| Arbeitspaket | Risiko/Priorität und Quelle | Ergebnis/Nachweis | Aufwand mit Unsicherheit | Verantwortlich | Termin | Abhängigkeit |
|---|---|---|---|---|---|---|
| offen | offen | offen | offen | offen | offen | offen |

## Teststatus und Entscheidungsvorlage

Beginne mit Bewertung und Begründung. Status ohne vereinbarte Ampelkriterien als begründete Einschätzung kennzeichnen.

| Feld | Inhalt |
|---|---|
| Produkt/Version, Datenstand, Quelle | siehe Dokumentkopf |
| Testumfang | eindeutige geplante Fälle für diesen Stand; Änderungen seit letztem Bericht |
| Ergebnisse | bestanden / fehlgeschlagen / blockiert / nicht ausgeführt |
| Abdeckung | Anforderungen und Risikokontrollen mit Beleg; offene oder veraltete Nachweise |
| Kritische Abweichungen | ID, Auswirkung, Einstufung mit Quelle, Status, fehlender Nachweis |
| Plan und Kapazität | nächste Meilensteine, Engpässe, Prognose mit Annahmen |
| Entscheidung | Empfehlung, offene Kriterien, zuständige Entscheidungsrolle |
| Nächste Maßnahmen | Maßnahme, Verantwortlicher, Termin, Abschlussnachweis |

Kennzahlen nur bei passender Datenbasis:

- Gesamt = bestanden + fehlgeschlagen + blockiert + nicht ausgeführt.
- Ausgeführt = bestanden + fehlgeschlagen. Ein begonnener, nicht bewertbarer Test bleibt blockiert.
- Ausführungsquote = ausgeführt / Gesamt.
- Bestehensquote der ausgeführten Fälle = bestanden / ausgeführt.
- Bestanden bezogen auf Gesamt = bestanden / Gesamt.
- Bei Nenner null: „nicht berechenbar“. Ergebnisquote ist keine Anforderungs-/Risikoabdeckung.

**Fiktives Rechenbeispiel:** 100 Fälle, davon 95 bestanden, 1 fehlgeschlagen, 0 blockiert und 4 nicht ausgeführt. Ausführungsquote 96/100 = 96 %, Bestehensquote der ausgeführten Fälle 95/96 ≈ 99,0 %, bestanden bezogen auf Gesamt 95/100 = 95 %. Ein fehlgeschlagener Deckelverriegelungstest erfordert Klärung und Nachweise vor einer positiven Empfehlung; die Quote entscheidet dies nicht.

## Kapazität und Aufwand

| Rolle/Person | Arbeitstage im Zeitraum | Verfügbarkeitsanteil | Abwesenheit in PT | Andere Aufgaben in PT | Reserve in PT | Netto für geplante Tests in PT |
|---|---|---|---|---|---|---|
| offen | offen | offen | offen | offen | offen | offen |

Brutto = Summe(Arbeitstage × Verfügbarkeitsanteil). Netto = Brutto − Abwesenheiten − andere Aufgaben − Reserve. Abzüge auf dieselbe verfügbare Arbeitszeit beziehen; Teilzeit und Urlaub nicht doppelt berücksichtigen. Feiertage im betrachteten Standortkalender berücksichtigen.

**Fiktives Beispiel:** 3 Vollzeitpersonen × 10 Arbeitstage = 30 PT brutto; 3 PT Urlaub, 5 PT andere Aufgaben, 4 PT Reserve ergeben 18 PT für geplante Tests. Die Reserve umfasst hier Nachtests/ungeplante Arbeit. Für diese Tätigkeiten keinen zweiten Aufwandsposten abziehen.

Vergleiche Netto mit geschätztem Testaufwand als Bandbreite. Ohne Schätzung bleiben machbarer Umfang und Fertigstellung offen. Engpässe durch Prüfstände, Spezialkenntnisse und Lieferstände gesondert erfassen.

## Rückverfolgbarkeit

| Anforderung-ID/Version | Risiko-/Kontroll-ID, falls vorhanden | Testfall-ID/Version | Testobjekt/Konfiguration | Ergebnis und Nachweis | Fehler/Nachtest | Lücke, Verantwortlicher, Termin |
|---|---|---|---|---|---|---|
| offen | offen | offen | offen | offen | offen | offen |

## Fehlermanagement und Triage

Erfasse ID, beobachtetes und erwartetes Verhalten mit Anforderungsquelle, Reproduktionsschritte, Testobjekt/Konfiguration, Nachweise und betroffene Varianten. Schweregrad beschreibt Auswirkungen, Priorität die Bearbeitungsreihenfolge; beide mit Begründung und nach internen Definitionen.

Triage dokumentiert Bewertung, Verantwortlichen, Zieltermin, nächste Entscheidung und betroffenen Testumfang. Abschluss benötigt Korrekturbezug, Nachtest und begründete Regression. Sicherheitsrelevante Befunde nach bestehendem Prozess an zuständige Entwicklung/QM/Risikomanagement eskalieren. Risikoakzeptanz bleibt bei den dafür autorisierten Rollen.
