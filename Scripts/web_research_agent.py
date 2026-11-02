import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Umgebungsvariablen laden
load_dotenv()
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

if not VAULT_PATH:
    raise ValueError("OBSIDIAN_VAULT_PATH ist nicht in der .env definiert!")

# 2. LLM und Such-Tool initialisieren
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
search_tool = DuckDuckGoSearchRun()

def research_and_write(topic: str):
    print(f"Starte Recherche zum Thema: '{topic}'...")
    
    # Schritt A: Web-Suche durchführen
    search_query = f"{topic} latest trends developments 2026"
    print(f"Führe Websuche aus: '{search_query}'...")
    search_results = search_tool.run(search_query)
    
    # Schritt B: Prompts für das LLM definieren
    system_prompt = (
        "Du bist ein präziser AI Research Architekt. "
        "Analysiere die bereitgestellten Suchergebnisse und erstelle einen tiefgehenden, "
        "strukturierten Markdown-Report. Der Report muss professionell formatiert sein, "
        "Überschriften (H1, H2, H3), Stichpunkte und eine Zusammenfassung enthalten."
    )
    
    user_prompt = f"""
    Thema: {topic}
    
    Web-Suchergebnisse als Rohdaten:
    {search_results}
    
    Erstelle nun den vollständigen, finalen Report auf Basis dieser Daten.
    """
    
    print("Synthetisiere Report mit LLM...")
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    report_content = response.content
    
    # Schritt C: YAML-Frontmatter und Obsidian-konforme Formatierung vorbereiten
    current_date = datetime.now().strftime("%Y-%m-%d")
    safe_title = topic.replace(" ", "_").replace("/", "-")
    filename = f"{current_date}_{safe_title}.md"
    
    obsidian_file_path = Path(VAULT_PATH) / filename
    
    frontmatter = f"""---
aliases: [{topic}]
tags: [ai-lab, web-research, agent-generated]
date: {current_date}
topic: "{topic}"
---

# Web Research Report: {topic}

"""
    
    full_markdown = frontmatter + report_content
    
    # Schritt D: Speichern im Obsidian-Vault
    os.makedirs(VAULT_PATH, exist_ok=True)
    
    with open(obsidian_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
        
    print(f"Erfolgreich gespeichert in Obsidian unter: {obsidian_file_path}")

if __name__ == "__main__":
    # Test-Thema für den ersten Run
    thema = "State of the Art in Multi-Agent Systems 2026"
    research_and_write(thema)