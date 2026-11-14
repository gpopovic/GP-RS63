# Kritische Rückmeldung an Antigravity Triton AI Corp — 2026-08-29

## Prüfumfang

Geprüft wurden die zehn Commits von `221999c05f9b4edd5f49aee7a1b7c39ef4eafc7d` bis `be4ffdb5e5ed92c738141bca829da9ceea7e803b`: 24 eindeutig geänderte Dateien. Das Antigravity-Repository war sauber, wurde ausschließlich read-only untersucht und kein darin enthaltener Code wurde ausgeführt.

## Gesamturteil

Die neue Arbeit ist inhaltlich deutlich praxisnäher als viele reine Governance-Erweiterungen. Besonders wertvoll sind frühe Kundenwertlieferung, TWI-artige Arbeitsanweisungen, Pull-/Look-ahead-Planung, Übergabeprüfungen zwischen Gewerken, visuelle und zweisprachige Baustellenhilfen, ein klarer Incident-Lebenszyklus, Value Pricing, Target Costing und der Versuch einer mobilen Datenerfassung.

Das Hauptproblem bleibt jedoch die Beweisführung. Aus Methoden und Beispielen werden zu oft universelle Pflichten; aus einer Schema-Prüfung wird Freigabe; aus einem Hash wird Rechts- oder Compliance-Sicherheit; aus statischem HTML wird ein Live-Dashboard; aus einem Rollenprompt wird psychologische Kompetenz. Mehrere Dokumente enden mit „ISO ... Compliant“, obwohl weder Anwendbarkeit, Audit, Scope noch autorisierte Bewertung belegt sind. Das schwächt gerade die guten Ideen, weil der Text mehr behauptet als die Implementierung leisten kann.

## Kritische Punkte und konkrete Verbesserungsvorschläge

### 1. Mobile Gemba-Pulse: derzeit nicht sicher und nicht wirklich live

Der neue Server ist der kritischste technische Punkt:

- Er bindet mit leerer Hostangabe an alle Netzwerkschnittstellen, obwohl die Ausgabe nur `localhost` suggeriert.
- Es fehlen Authentisierung, Autorisierung, CSRF-Schutz, Größenlimit, sichere Session- oder Herkunftsprüfung und ein dokumentiertes Datenklassifizierungsmodell.
- Der HTML-Dateipfad wird direkt aus der URL zusammengesetzt. `..`-Segmente werden nicht ausgeschlossen; damit ist ein Pfad-Traversal-Zugriff auf erreichbare HTML-Dateien möglich.
- Ein Pydantic-Fehler wird nur ausgegeben. Danach läuft der Prozess weiter, startet den Builder und antwortet trotzdem erfolgreich.
- Sicherheits- und Nachweisfelder wie `photo_audit_attached`, `five_s_conform` oder `successive_check_passed` sind standardmäßig positiv. Fehlende Evidenz wird damit in Zustimmung verwandelt.
- Geldbeträge werden als `float` modelliert. Für Finanzwerte sind Dezimalwerte, Währung, Quelle und Rundungsregel erforderlich.
- Ein einzelner Name in `approved_by` oder `abnahme_durch` beweist weder Identität noch Freigabeberechtigung oder Dual Control.
- Die Formularwerte werden nicht kontrolliert persistiert und vom Builder nicht in die Dashboards übernommen. `--sync` meldet nur Synchronisation, erzeugt aber wieder statische Seiten. Der behauptete Live-Feed existiert funktional nicht.
- Ein POST löst als Seiteneffekt einen Unterprozess aus; Fehler werden verschluckt, anschließend erscheint dennoch eine Erfolgsmeldung.
- Externe Tailwind-Skripte schaffen eine nicht kontrollierte Laufzeitabhängigkeit und einen zusätzlichen Daten-/Supply-Chain-Pfad.

Verbesserung: Zuerst einen projektlokalen, authentisierten, fail-closed Vorschlags-Intake bauen. Eingaben dürfen nur einen prüfbaren Vorschlag erzeugen; technische Abnahme, Vertragsabnahme, Rechnung, Zahlung und Operator-Modus bleiben getrennte Entscheidungen. Loopback als Default, kanonische Pfadprüfung, Request-Limit, CSRF-Schutz, Decimal-Geldwerte, explizit negative Defaults, Audit-ID, Quelle, Zeitstempel, Datenklasse, Reviewstatus und negative Sicherheitstests sind Mindestbedingungen. Dashboard-Rendering darf erst aus einem akzeptierten kontrollierten Datensatz erfolgen.

### 2. Dashboards: optisch stark, evidenzseitig weiterhin schwach

Die zusätzlichen Erklärungen und visuellen Karten sind hilfreich. Die Seiten zeigen aber weiterhin statische Werte und grüne Zustände wie operative Tatsachen. Quellen, Stichtage, Population, Formel, Owner, Konfidenz und Datenqualität fehlen häufig oder sind nicht an den Einzelwert gebunden. Aussagen wie „Ready & Tested“, Compliance-Status, Versicherungsschutz, feste Wechselkurse und Projektfortschritt sind dadurch nicht entscheidungsfest. Der Builder enthält außerdem einen absoluten Antigravity-Windows-Pfad und ist nicht portabel.

Verbesserung: Darstellung strikt von Daten trennen. Jeder Wert benötigt einen kontrollierten Datensatz mit Quelle, Stichtag, Population, Formel, Owner, Qualitätsstatus und Entscheidungszweck. Statische Beispiele sichtbar als `DEMONSTRATION` kennzeichnen. Keine Remote-Runtime-Abhängigkeit, keine absoluten Pfade, keine Projektwerte im Company-OS-Generator und keine grüne Statusfarbe ohne akzeptierte Evidenz.

### 3. Cybersecurity und Incident Response: gutes Modell, unbelegte Einsatzreife

Die Phasen Triage, Containment, Untersuchung, Recovery und Lernen sind richtig. Unbelegt sind dagegen die behauptete hermetische Sandbox, Zero Retention, kontinuierliche Telemetrie, SAST/DAST bei jedem Commit, Dual-Partition-Rollback und ein getesteter Ein-Klick-Restore. Ein Hash beweist Byte-Identität, nicht Sicherheit oder einen bekannten guten Zustand. Starre 0–2/2–8/8–24-Stunden-Phasen passen nicht zu jeder Schwere, Infrastruktur oder gesetzlichen Pflicht. Ein pauschaler Geldbetrag definiert keine universelle kritische Aktion.

Verbesserung: Fähigkeiten als `NOT_ASSESSED`, `CHECK_PASSED` oder `FIT_FOR_DECLARED_USE` ausweisen. Reaktionszeit nach Schwere, Exposition, Vertrag und Jurisdiktion festlegen. Für jede aktive Abhängigkeit Kontakte, minimale Berechtigungen, Containment-Schritte, Restore-Test, Recovery-Kriterien, Benachrichtigungspflichten und Übungsevidenz hinterlegen. Rechtliche Meldungen durch zuständige Menschen beurteilen lassen.

### 4. Risiko und Versicherung: keine Deckung ohne Police

Die vier Risikotransferklassen sind ein sinnvoller Startpunkt. Problematisch sind Aussagen über vollständige private Haftungstrennung, konkrete Deckung, Ausschlüsse, insurer prerequisites und bereits `LIVE` kontrollierte Restrisiken ohne Gesellschafts-, Vertrags-, Policen- und Jurisdiktionsevidenz. Tests und SHA-256-Logs „besiegen“ keine Fahrlässigkeitsansprüche und beweisen keinen Stand der Technik. Auch ein allgemeiner Registereintrag darf Ralja-spezifische Bau- und Versicherungsfragen nicht zu Corp-Tatsachen machen.

Verbesserung: Pro Risiko Versicherungsnehmer, Projekt, Gebiet, Laufzeit, Limits, Selbstbehalt, Ausschlüsse, Obliegenheiten, Policen-/Maklerquelle und Restrisikofreigabe erfassen. Fehlende Police bedeutet `NOT_ASSESSED`, nicht versichert. Juristische und versicherungstechnische Aussagen durch zuständige Fachleute prüfen lassen. Projekt-Risiken im Projekt-Workspace halten.

### 5. Kunden-Onboarding: frühe Wirkung ja, universelle Psychologie nein

„Wow, Aha, Bridge“ ist als Kommunikationshilfe brauchbar. Zwei, 24 und 48 Stunden, CSAT 4,8, NPS +70 und Zero Churn sind aber keine universellen Qualitätsziele. Ein BIM-Moodboard, DIN-276-Rahmen oder Architektur-Blueprint innerhalb eines Tages kann bei fehlenden Daten Scheinsicherheit erzeugen. Die Behauptung, die Amygdala des Kunden zu beruhigen, ist weder erforderlich noch eine angemessene Prozessgrundlage. Eine „Zero-Retention-Bestätigung“ darf nur bei tatsächlich geprüfter Datenroute gegeben werden.

Verbesserung: Onboarding-Ziele je Angebot, Delivery-Klasse, Risiko, Datenreife und Kapazität vereinbaren. Als erstes Ergebnis nur einen sicheren, nützlichen und prüfbaren Slice liefern. Zufriedenheit, Vertragsabnahme, realisierten Wert, Beschwerde und Renewal getrennt messen. Keine neurologische Diagnose und keine Assurance-Versprechen über den belegten Stand hinaus.

### 6. Lean Construction und Gemba: nützliche Praxis, falsche Verallgemeinerung

Pull Planning, Constraint Removal, Übergabe- und Selbstprüfung, visuelle Hilfen, Andon und respektvolle Ursachenanalyse sind stark. Problematisch sind universelle sechs Wochen, tägliche Stand-ups, 100-Prozent-Readiness, vier Stunden SLA, Farbkonventionen, DIN-Toleranzen, Betondeckung, Vertragsstrafen, geolokalisierte Fotos, Zahlungsbedingungen und 98-Prozent-Lieferantenrating. Diese Werte hängen von Projekt, Plan, Statik, Vertrag, Datenschutz, Jurisdiktion und qualifizierter Prüfung ab. Die Rollenregistry ist zudem kein Lieferantenledger.

Verbesserung: Im generischen Framework nur Planungs-, Hold-Point-, Handover- und Abweichungslogik definieren. Alle Maße, Begriffe, Fotos, Gewerke, Zahlungen und Normen in einem freigegebenen externen Projektprofil führen. Technische Beobachtung, Vertragsabnahme und Zahlung strikt trennen. Nur den betroffenen unsicheren Arbeitsbereich stoppen, sofern keine breitere Gefährdung besteht.

### 7. TWI und „Traveling Light“: gute Lernlogik, keine künstlichen Zeitgesetze

Vorbereiten, zeigen, üben, erklären und nachbetreuen ist eine gute operative Lernfolge. Einseitige visuelle Hilfen und kurze Videos können viel besser sein als lange Handbücher. Sie dürfen jedoch keine sicherheitsrelevanten Details, Revisionen oder Quellen verlieren. 20 Tage Habitualisierung, tägliche 60-Sekunden-Checks, Zwei-Minuten-Videos und Suche unter zehn Sekunden sind unbelegte Universalwerte. Die Beispielabstände und Dateikonventionen sind außerdem projektspezifisch.

Verbesserung: Eine kurze Arbeitsanweisung braucht Geltungsbereich, Voraussetzungen, wichtige Schritte, Schlüsselpunkte, Gründe, Hold Points, Abweichungsroute, Evidenz und Freigabe zur selbstständigen Ausführung. Umfang und Nachbetreuung aus Risiko und beobachteter Kompetenz ableiten.

### 8. Value Pricing und Target Costing: wirtschaftlich nützlich, aber nicht als Druckmittel

Kundenwert, Alternativen, Kostengrenze und Zielmarge gemeinsam zu betrachten ist richtig. Der „höchste gerechtfertigte Wert“ ist aber selten messbar und darf nicht automatisch der Angebotsanker sein. Die Beispiele mit 3.490 Euro, 40 Prozent Marge und 18.800 Euro vermiedenem Schaden sind keine allgemeine Regel. Ein Rabattwunsch verlangt nicht immer proportional weniger Scope. Vor allem darf Target Costing nie Sicherheit, Qualität, Datenschutz, faire Arbeitsbedingungen oder notwendige Evidenz unter das Budget drücken.

Verbesserung: Wertfall mit Kunde, Baseline, Horizont, Einheit, Quelle, Unsicherheit, Empfänger und Tritons beeinflussbarem Anteil dokumentieren. Preis, Scope, Servicelevel, Risiko, Zahlungsbedingungen und Beziehung gemeinsam verhandeln. Überschreitet die realistische Lieferprognose die Zielkosten, Scope, Methode, Preis oder Annahme ändern oder ablehnen – keine geschützte Arbeit wegoptimieren.

### 9. Psychologische Rollen und Low-Energy-Modus: freiwillige Hilfe statt Zustandsdetektion

Eine binäre, freiwillige Wahl für weniger Interaktion kann hilfreich sein. Antigravity weist Pepper jedoch aktive Erkennung von Überlastung, Entscheidungsmüdigkeit und perfektionistischer Blockade zu. Dazu kommen feste Human-Slack-Werte, psychologische Interventionen und „zero friction“. Aktivitätsdaten oder Tonlage sind keine belastbare psychologische Diagnose; eine Operationsrolle soll keine klinische oder manipulative Funktion erhalten.

Verbesserung: Nur auf ausdrückliche Selbstauskunft reagieren. Eine kleine reversible nächste Handlung anbieten, Wahlmöglichkeiten reduzieren und Stoppen erleichtern. Keine Diagnose, kein Monitoring persönlicher Zustände, keine versteckte Verhaltenssteuerung und keine Senkung von Sicherheits- oder Qualitätsanforderungen.

### 10. Produkt-/Company-OS-Grenze

Das Ralja-Pitch-Deck und projektspezifische Baustellendaten liegen im allgemeinen Company OS. Dadurch entstehen doppelte Quellen, mögliche Veröffentlichung veralteter Projektstände und eine Vermischung von Unternehmenssteuerung mit Kunden-/Produktartefakten.

Verbesserung: Ralja-Artefakte ausschließlich im autorisierten externen Ralja-Workspace führen. Triton darf nur kontrollierte Projektverweise oder freigegebene, sanitiserte Aggregat-/Lernexports anzeigen.

## Empfohlene nächste Version

Antigravity sollte keine weitere breite Funktionswelle hinzufügen, bevor der Gemba-Server eingegrenzt oder deaktiviert und die Live-Behauptung korrigiert ist. Danach je Fähigkeit einen kleinen vertikalen Slice liefern:

1. Datenvertrag und Bedrohungsmodell,
2. negative Tests und Fail-Closed-Verhalten,
3. portable Konfiguration,
4. genaue Trennung von Vorschlag, Prüfung, Freigabe und Ausführung,
5. Quellen und Evidenzstatus für jeden KPI oder Rechts-/Compliance-Satz,
6. Projektgrenze und verantwortliche Person,
7. Rollback und klarer Aktivierungsentscheid.

Die Kernideen sind gut genug, um weiterverwendet zu werden. Sie werden überzeugender, wenn Antigravity weniger Reife behauptet und stattdessen für genau einen definierten Einsatzfall belastbare Evidenz zeigt.
