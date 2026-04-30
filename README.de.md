# workingclass

[简体中文](README.md) · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · **Deutsch**

> KI-Werkzeuge auf der Seite der Arbeitenden.
> AI tools that stand on the side of workers.

Dieses Repository sammelt Agent Skills und Werkzeuge, die Arbeitenden dienen sollen. Das erste — und zentrale — ist **Laborer's Companion / 劳动者AI助手**: ein Werkzeug, mit dem du die Rhetorik der Arbeitswelt durchschaust und die Entscheidungen triffst, die für dich wirklich gut sind.

---

## Warum es dieses Projekt gibt

Im Beruf haben das Unternehmen, HR und deine Vorgesetzten enorme Ressourcen, um dich zu managen: HR-Beratungen, Manipulations-Playbooks, Performance-Management-Systeme, juristische Teams, Recruiting-Psychologinnen und -Psychologen. Jeder Satz ist sorgfältig entworfen — nicht zwangsläufig, damit du klar siehst, sondern damit du die Entscheidung triffst, die dem Unternehmen am meisten nützt.

Du hast nur dich selbst.

Die KI-Ära verschärft diese Asymmetrie — Unternehmen nutzen KI, um deine Arbeit zu destillieren, dich zu ersetzen, dich zu überwachen. Dieses Projekt dreht den Spieß um: **KI auf deiner Seite**.

---

## Was aktuell enthalten ist

### 1. `skills/laborer-companion/` — Laborer's Companion

9 Kernmodule + 4 Einstiegswerkzeuge, die das gesamte Arbeitsleben abdecken:

| Modul | Zweck |
|-------|-------|
| Werkzeug 0a · Triage | Leitet dich weiter, wenn du nicht weißt, welches Modul passt |
| Werkzeug 0b · Red-Flag-Scan | 60-Sekunden-Check, ob deine Lage gefährlich ist |
| Werkzeug 0c · Erste 72 h nach einer Kündigung | Was du tun — und nicht tun — solltest, direkt nach einer Kündigung |
| Werkzeug 0d · Privatsphäre und OPSEC | Wie du das Werkzeug sicher nutzt |
| Modul 1 · Rhetorik-Decoder | Übersetzt, was Vorgesetzte / HR *wirklich* sagen |
| Modul 2 · Überstunden-Entscheidung | Echte Kosten-Nutzen-Analyse |
| Modul 3 · Performance-Review-Decoder | Sichtbar machen, was hinter dem Review steht |
| Modul 4 · Bleiben oder Gehen | Entscheidung auf Basis deiner echten Interessen |
| Modul 5 · Historische Perspektive | Bezugspunkte aus 150 Jahren Arbeiterbewegung |
| Modul 6 · Karte des Arbeitsrechts | 8 Jurisdiktions-Einträge zu 9 benannten Jurisdiktionen/Regionen (keine Rechtsberatung) |
| Modul 7 · Gehaltsverhandlung | Vollständiges Playbook |
| Modul 8 · PIP-Survival | Vom Frühwarnsignal bis zur Abfindungsverhandlung |
| Modul 9 · Jobsuche und Vorstellungsgespräche | Gesamter Lebenszyklus |

Details: [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md).

---

## Installation

```bash
# Repository klonen
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Claude Code (legacy Claude skills)
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

Beschreibe danach deine Arbeitssituation im Agenten — die Skill aktiviert sich. Oder nutze die Slash-Befehle:

```
/triage      - Hier starten, wenn du nicht weißt, welches Modul passt
/scan        - Red-Flag-Scan (60 s)
/decode      - Rhetorik von Vorgesetzten/HR entschlüsseln
/overtime    - Entscheidung über Überstunden
/review      - Eine Performance-Beurteilung lesen
/jump        - Bleiben oder gehen
/history     - Historische Perspektive
/law         - Arbeitsrecht-Recherche
/salary      - Gehaltsverhandlung
/pip         - PIP-Survival
/jobsearch   - Jobsuche und Vorstellungsgespräche
```

---

## Abdeckung des Arbeitsrechts

Modul 6 enthält aktuell **8 Jurisdiktions-Einträge**, die **9 benannte Jurisdiktionen/Regionen** abdecken:

| Eintrag | Hinweise |
|---------|----------|
| Festland-China | Eigene Datei |
| Hongkong / Taiwan | Zwei Regionen/Jurisdiktionen in einer Datei; Regeln dürfen nicht vermischt werden; niemals als Länder bezeichnen |
| USA | Bundesebene + Schwerpunkt Kalifornien / New York |
| Kanada | Bundesebene + provinzielle Unterschiede markiert |
| Australien | Fair Work / Awards / unfair dismissal |
| Vereinigtes Königreich | UK employment / ACAS / Tribunal |
| Europäische Union | Regionale Übersicht mit Hinweisen zu Deutschland/Frankreich/Niederlande; keine Enzyklopädie pro Mitgliedstaat |
| Indien | Vier Labour Codes + IT-Branchen-FAQ |

Werden Hongkong und Taiwan separat gezählt, sind es **9 benannte Jurisdiktionen/Regionen**; nach Referenzdatei / Jurisdiktions-Eintrag sind es **8**. Hongkong und Taiwan müssen in diesem Projekt als **Regionen/Jurisdiktionen** bezeichnet werden, niemals als Länder.

---

## Unterstützte Sprachen

Aktuell:

- 简体中文 / Vereinfachtes Chinesisch
- 繁體中文 / Traditionelles Chinesisch
- English / Englisch
- Español / Spanisch
- Français / Französisch
- Português / Portugiesisch
- Deutsch

Standardregel: Die Skill antwortet in der unterstützten Sprache, in der die Person schreibt. Gesetzesnamen, Behörden und Vertragsklauseln bleiben im Original; bei Bedarf wird eine kurze Übersetzung ergänzt. Im traditionellen Chinesisch werden Termini aus Hongkong / Taiwan bevorzugt.

---

## Beispiele und Tutorials

Weitere Beispiele in [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md). Gute Einstiegspunkte:

```text
/triage
Meine Vorgesetzte ist in letzter Zeit distanziert und ich kann nicht klar benennen warum. Hilf mir zu entscheiden, welches Modul passt.
```

```text
/law
Ich arbeite Teilzeit in Hongkong, 17 Stunden pro Woche. Die HR sagt, der gesetzliche Mindestlohn gelte nur für bestimmte Branchen. Stimmt das?
```

```text
/review
Hier ist meine Performance-Beurteilung: [redigierten Inhalt einfügen]
Letztes Jahr "exceeds", dieses Jahr "meets". Ist das ein Warnsignal?
```

Wir freuen uns über weitere Tutorials und reale Fälle — besonders:

- Beispiele aus dem Arbeitsrecht verschiedener Jurisdiktionen/Regionen
- Walkthroughs zu PIP / Kündigung / Abfindungsverhandlung
- Skripte für Gehaltsverhandlungen
- Beispiele zur Anti-Manipulation in Bewerbungsgesprächen
- Anonymisierte E-Mail-Beispiele von HR / Vorgesetzten
- Reale Anwendungsfälle in Spanisch, Französisch, Portugiesisch und Deutsch

---

## Grundprinzipien

1. **Kein Aufruf zu kollektivem Handeln** — dies ist ein Klarheitswerkzeug für einzelne Arbeitende.
2. **Reale Restriktionen anerkennen** — keine leichtfertigen "Sofort kündigen"-Ratschläge.
3. **Intellektuelle Ehrlichkeit** — keine Anpassung der Empfehlungen an politische Bequemlichkeit.
4. **Privatsphäre zuerst** — siehe `skills/laborer-companion/references/privacy-and-opsec.md`.
5. **Kein Anwaltsersatz** — das Werkzeug liefert Rahmen und die richtigen Fragen, ersetzt aber keine professionelle Rechtsberatung.

---

## Datenschutzhinweis ⚠️

- Diese Skill lädt deine Konversationen nicht zu Dritten hoch.
- Aber der Dialog mit deinem KI-Anbieter kann je nach Konto- und Datenschutzeinstellungen von der Plattform protokolliert werden.
- **Nutze dieses Werkzeug nicht auf einem Firmengerät oder im Firmennetz.**
- **Füge keine vertraulichen Unternehmensdaten in die KI ein** — vorher anonymisieren.

Details: [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md).

---

## Inspiration

- Koki Xus Anti-Distillation-Skill (April 2026)
- Karl Marx zum Wert der Arbeit und zur Entfremdung
- E.P. Thompson, *Die Entstehung der englischen Arbeiterklasse*
- 150 Jahre konkrete Fälle aus der Arbeiterbewegung
- Zeitgenössische Arbeitsökonomie und Arbeitssoziologie

Dieses Werkzeug erfindet nichts Neues. Es übersetzt 150 Jahre kollektiver Arbeiterklassenweisheit in eine Form, die im Jahr 2026 in der KI-Ära nutzbar ist.

---

## Mitwirken

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Besonders willkommen:

- Neue Rhetorik-Fälle (damit Modul 1 vollständiger wird)
- Arbeitsrechtsergänzungen für dein Land/deine Region/Jurisdiktion
- Erfolgreiche Gehalts- / Abfindungsverhandlungen
- PIP-Erfahrungen (anonymisiert)
- Übersetzungen der nutzerorientierten READMEs

---

## Lizenz

Apache 2.0 — siehe [LICENSE](LICENSE).

Einzige Bitte: **die Kernmission des Werkzeugs erhalten — Arbeitenden zu dienen**.

---

## Ein Absatz

Die eigene Lage klar zu sehen verändert sie nicht. Aber Klarheit ist die Vorbedingung von Veränderung. Und oft ist es besser, die Realität mit offenen Augen zu akzeptieren (auch das "ich kann jetzt noch nicht weg") als sie mit geschlossenen Augen zu ertragen.

Wenigstens weißt du, was du tust.
