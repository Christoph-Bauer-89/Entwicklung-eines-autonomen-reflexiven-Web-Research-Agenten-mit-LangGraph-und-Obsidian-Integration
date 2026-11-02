# 🤖 Entwicklung eines autonomen, reflexiven Web-Research-Agenten mit LangGraph und Obsidian-Integration

Ein autonomes, agentenbasiertes Web-Research-System zur eigenständigen Informationsbeschaffung, iterativen Reflexion und direkten Integration in ein lokales Personal Knowledge Management (PKM) System.

---

## 🚀 Executive Summary & Projektziel

Um das volle Potenzial intelligenter Automatisierung auszuschöpfen, wurde in diesem Projekt ein autonomes, agentenbasiertes Web-Research-System als eigene Architektur umgesetzt. Der Agent recherchiert eigenständig im Web, evaluiert die Ergebnisqualität über eine dynamische Reflexionsschleife mit LangGraph und speichert die aufbereiteten Markdown-Reports direkt in einem lokalen Obsidian-Vault. Die Pipeline minimiert den manuellen Rechercheaufwand drastisch und verknüpft fortgeschrittene LLM-Orchestrierung direkt mit strukturiertem Wissensmanagement.

> **Transparenzhinweis & Entwicklungsansatz:** Dieses System wurde nach dem „AI-First-Builder“-Prinzip konzipiert und umgesetzt. Als Architekt des Workflows lag der Fokus auf der Konzeption des Datenflusses, der Systemlogik (zustandsbasierte Schleifen, Reflexion und Validierung) sowie der nahtlosen Integration von APIs und lokalen Dateisystemen. Der Einsatz moderner KI-Assistenten diente dabei als hocheffizienter Entwicklungshebel – ein Beweis dafür, wie man komplexe Agenten-Architekturen pragmatisch, schnell und mit klarem Blick für den echten Nutzwert realisiert.

*Hinweis zum Setup:* Die lokalen Systempfade und API-Keys sind sicher über eine `.env`-Datei (mittels `python-dotenv`) ausgelagert und werden im Repository nicht offengelegt.

---

## 🛠️ Tech Stack & Architektur

* **Programmiersprache:** Python 3.10+
* **LLM-Orchestrierung:** OpenAI `gpt-4o-mini` (über LangChain Core & ChatOpenAI)
* **Agenten-Framework:** LangGraph (für zustandsbasierte Graphen und bedingte Schleifen)
* **Web-Suche:** DuckDuckGo Search (`duckduckgo-search` / `ddgs`) – kostenfrei und ohne API-Key-Hürden
* **Persistenz & Wissensmanagement:** Obsidian-Vault via native Python-Dateisystemoperationen (`pathlib`)

---

## 🔍 Ausgangsbasis: Der lineare Research-Agent (MVP)

In der ersten Entwicklungsstufe wurde ein sequenzielles, lineares Python-Skript implementiert, um die Kernfunktionalität zu validieren. Der Ablauf gestaltete sich strikt von oben nach unten:

1. **Initialisierung:** Laden der Umgebungsvariablen (`.env`) und Bereitstellung des Such-Tools sowie des LLMs.
2. **Web-Suche:** Ausführen einer einmaligen, fest definierten Suchabfrage über DuckDuckGo zum übergebenen Thema.
3. **Synthese:** Übergeben der gesammelten Rohdaten an das LLM via System- und User-Prompt, um einen strukturierten Report zu generieren.
4. **Persistenz:** Automatisches Generieren von YAML-Frontmatter (Metadaten wie Datum, Tags und Aliase) und Speichern der `.md`-Datei im Zielverzeichnis des Obsidian-Vaults.

*Limitation:* Der lineare Agent lieferte zwar hervorragende Ergebnisse, konnte jedoch die Qualität der Suchergebnisse zur Laufzeit weder hinterfragen noch iterativ verbessern, wenn Informationen unvollständig waren.

---

## 🔄 Weiterentwicklung: Autonome Reflexionsarchitektur (LangGraph)

Um die Limitisierungen des linearen Ansatzes zu überwinden, wurde das System zu einer zustandsbasierten State Machine weiterentwickelt:

* **State Management (`ResearchState`):** Ein zentrales Dictionary verwaltet Thema, Suchabfragen, gesammelte Rohdaten, Evaluierungsstatus und einen Schleifenzähler (`loop_count`).
* **Reflexionsschleife & Guardrails:** Nach dem ersten Suchlauf bewertet das LLM eigenständig, ob die Daten ausreichen (`"READY"`) oder eine Verfeinerung nötig ist (`"REFINE"`). Um Endlosschleifen zu verhindern, greift eine harte Obergrenze von maximal 2 Durchläufen (`loop_count >= 2`).
* **Bedingte Kanten (Conditional Routing):** Der Graph verzweigt dynamisch – bei unvollständigen Daten springt das System zurück zum Such-Knoten, andernfalls wird der Schreib-Knoten für den Obsidian-Export angesteuert.

```text
[Websuche] ---> [Evaluere Rohdaten]
                      |
        ┌─────────────┴─────────────┐
   (Daten OK)                  (Mehr Info nötig)
        ▼                           ▼
[Schreibe Report]            [Such-Query verfeinern] ---> (zurück zu Websuche)

📂 Obsidian-Integration & Ergebnis-Preview
Der finale Markdown-Report wird vollautomatisch mit sauberem YAML-Frontmatter und strukturierter Typographie direkt in den lokalen Obsidian-Vault exportiert, sodass die Rechercheergebnisse nahtlos in das persönliche Wissensmanagement (PKM) einfließen.

💡 Key Learnings & Fazit
MVP-First-Ansatz: Die Validierung über einen linearen Agenten schuf ein stabiles Fundament, bevor die Komplexität durch LangGraph erhöht wurde.

Echte Autonomie durch Zyklen: Erst durch zustandsbasierte Graphen und bedingte Rücksprünge wird ein Agent zu einem selbstkorrigierenden System.

Sicherheitsnetze sind essenziell: Ohne harte Schleifenlimits neigen reflexive Agenten zu unnötigen API-Schleifen.

Nahtlose PKM-Verknüpfung: Die automatisierte Formatierung für Obsidian verwandelt das Web-Research in eine direkt nutzbare, durchsuchbare Wissensbasis.

📁 Repository-Struktur
```text
├── Scripts/
│   ├── web_research_agent.py       # Hauptskript für den reflexiven Agenten (LangGraph)
│   └── linear_research_mvp.py      # Ursprüngliches sequenzielles Skript (Baseline)
├── Pictures/
│   ├── langgraph-agent-workflow-code.png
│   ├── agent-execution-terminal-log.png
│   └── obsidian-vault-generated-report.png
├── .gitignore                      # Ausschluss für .env, __pycache__ etc.
├── requirements.txt                # Python-Abhängigkeiten
└── README.md                       # Projektdokumentation
