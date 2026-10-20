# 🤖 Entwicklung eines autonomen, reflexiven Web-Research-Agenten mit LangGraph und Obsidian-Integration

> **Ein autonomes, agentenbasiertes Web-Research-System zur eigenständigen Informationsbeschaffung, iterativen Reflexion und direkten Integration in ein lokales Personal Knowledge Management (PKM) System.**

---

## 🚀 Executive Summary

Um das volle Potenzial intelligenter Automatisierung auszuschöpfen, wurde in diesem Projekt ein autonomes, agentenbasiertes Web-Research-System als eigene Architektur umgesetzt. Der Agent recherchiert eigenständig im Web, evaluiert die Ergebnisqualität über eine dynamische Reflexionsschleife mit LangGraph und speichert die aufbereiteten Markdown-Reports direkt in einem lokalen Obsidian-Vault. Die Pipeline minimiert den manuellen Rechercheaufwand drastisch und verknüpft fortschrittliche LLM-Orchestrierung direkt mit strukturiertem Wissensmanagement.

---

## 🛠️ Tech Stack & Architecture

* **Programmiersprache:** Python 3.10+
* **LLM-Orchestrierung:** OpenAI `GPT-4o-mini` (über LangChain Core & ChatOpenAI)
* **Agenten-Framework:** LangGraph (für zustandsbasierte Graphen und bedingte Schleifen)
* **Web-Suche:** DuckDuckGo Search (`duckduckgo-search` / `ddgs`) – kostenfrei und ohne API-Key-Hürden
* **Persistenz & Wissensmanagement:** Obsidian-Vault via native Python-Dateisystemoperationen (`pathlib`)

---

## ⚙️ Ausgangsbasis: Der lineare Research-Agent (MVP)

In der ersten Entwicklungsstufe wurde ein sequenzielles, lineares Python-Skript implementiert, um die Kernfunktionalität zu validieren. Der Ablauf gestaltete sich strikt von oben nach unten:

1. **Initialisierung:** Laden der Umgebungsvariablen (`.env`) und Bereitstellung des Such-Tools sowie des LLMs.
2. **Web-Suche:** Ausführen einer einmaligen, fest definierten Suchabfrage über DuckDuckGo zum übergebenen Thema.
3. **Synthese:** Übergeben der gesammelten Rohdaten an das LLM via System- und User-Prompt, um einen strukturierten Report zu generieren.
4. **Persistenz:** Automatisches Generieren von YAML-Frontmatter (Metadaten wie Datum, Tags und Aliase) und Speichern der `.md`-Datei im Verzeichnis `03_Web_Research` des Obsidian-Vaults.

> **Limitierung:** Der lineare Agent lieferte zwar hervorragende Ergebnisse, konnte jedoch die Qualität der Suchergebnisse zur Laufzeit weder hinterfragen noch iterativ verbessern, wenn Informationen unvollständig waren.

---

## 🔄 Weiterentwicklung: Autonome Reflexionsarchitektur (LangGraph)

Um die Limitierungen des linearen Ansatzes zu überwinden, wurde das System zu einer zustandsbasierten State Machine weiterentwickelt:

* **State Management (`ResearchState`):** Ein zentrales Dictionary verwaltet Thema, Suchabfragen, gesammelte Rohdaten, Evaluierungsstatus und einen Schleifenzähler (`loop_count`).

![LangGraph Agent Workflow Code](langgraph-agent-workflow-code.png)

* **Reflexionsschleife & Guardrails:** Nach dem ersten Suchlauf bewertet das LLM eigenständig, ob die Daten ausreichen (`"READY"`) oder eine Verfeinerung nötig ist (`"REFINE"`). Um Endlosschleifen zu verhindern, greift eine harte Obergrenze von maximal 2 Durchläufen (`loop_count >= 2`).
* **Bedingte Kanten (Conditional Routing):** Der Graph verzweigt dynamisch – bei unvollständigen Daten springt das System zurück zum Such-Knoten, andernfalls wird der Schreib-Knoten für den Obsidian-Export angesteuert.

![Agent Execution Terminal Log](agent-execution-terminal-log.png)

---

## 📝 Obsidian-Integration & Ergebnis-Preview

Der finale Markdown-Report wird vollautomatisch mit sauberem YAML-Frontmatter und strukturierter Typografie direkt in den lokalen Obsidian-Vault exportiert, sodass die Rechercheergebnisse nahtlos in das persönliche Wissensmanagement (PKM) einfließen[cite: 4].

![Obsidian Vault Generated Report](obsidian-vault-generated-report.png)[cite: 4]

---

## 📈 Key Learnings & Fazit

* **MVP-First-Ansatz:** Die Validierung über einen linearen Agenten schuf ein stabiles Fundament, bevor die Komplexität durch LangGraph erhöht wurde.
* **Echte Autonomie durch Zyklen:** Erst durch zustandsbasierte Graphen und bedingte Rücksprünge wird ein Agent zu einem selbstkorrigierenden System.
* **Sicherheitsnetze sind essenziell:** Ohne harte Schleifenlimits neigen reflexive Agenten zu unnötigen API-Schleifen.
* **Nahtlose PKM-Verknüpfung:** Die automatisierte Formatierung für Obsidian verwandelt das Web-Research in eine direkt nutzbare, durchsuchbare Wissensbasis.

---

## 📂 Repository-Struktur

```text
├── 🐍 web_research_agent.py       # Hauptskript für den reflexiven Agenten (LangGraph)
├── 🐍 linear_research_mvp.py      # Ursprüngliches sequenzielles Skript (Baseline)
├── 📄 .env                        # Konfiguration der OpenAI API-Schlüssel
├── 📁 03_Web_Research/            # Zielordner im lokalen Obsidian-Vault
│   └── 📝 *.md                    # Generierte Markdown-Reports mit YAML-Frontmatter
├── 🖼️ langgraph-agent-workflow-code.png # Workflow-Code-Architektur
├── 🖼️ agent-execution-terminal-log.png   # Konsolen-Ausführungsprotokoll
└── 🖼️ obsidian-vault-generated-report.png # Obsidian Ansicht des Reports[cite: 4]
