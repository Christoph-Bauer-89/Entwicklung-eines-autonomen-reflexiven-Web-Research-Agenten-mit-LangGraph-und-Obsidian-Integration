import os
from pathlib import Path
from datetime import datetime
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

if not VAULT_PATH:
    raise ValueError("OBSIDIAN_VAULT_PATH ist nicht in der .env definiert!")

# Das Datenmodell für den Agenten-Zustand
class ResearchState(TypedDict):
    topic: str                      # Das ursprüngliche Thema
    search_query: str               # Die aktuelle Suchanfrage
    raw_data: str                   # Gesammelte Suchergebnisse
    evaluation_status: str          # "needs_more_search" oder "ready"
    loop_count: int                 # Zähler, um Endlosschleifen zu verhindern
    final_report: str               # Der fertige Markdown-Text

# Tools und LLM initialisieren
search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Knoten 1: Suche
def search_node(state: ResearchState):
    print(f"\n[Agent-Schritt] Führe Websuche aus für: '{state['search_query']}' (Durchlauf: {state['loop_count'] + 1})")
    
    try:
        results = search_tool.run(state["search_query"])
    except Exception as e:
        results = f"Fehler bei der Suche: {str(e)}"
        
    updated_raw_data = state["raw_data"] + "\n\n" + results
    
    return {
        "raw_data": updated_raw_data,
        "loop_count": state["loop_count"] + 1
    }

# Knoten 2: Evaluierung / Reflexion
def evaluate_node(state: ResearchState):
    print("[Agent-Schritt] Evaluiere, ob die Daten ausreichen...")
    
    prompt = f"""
    Du bist ein kritischer Research-Evaluator.
    Thema: {state['topic']}
    
    Bisher gesammelte Rohdaten:
    {state['raw_data']}
    
    Analysiere das Material. Wenn die Daten ausreichen, antworte exakt mit dem Wort: "READY".
    Wenn wichtige Aspekte fehlen und unbedingt eine zweite gezielte Suche nötig ist, antworte exakt mit dem Wort: "REFINE".
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    decision = response.content.strip()
    
    # Schutz vor unendlichen Schleifen: Maximal 2 Such-Durchläufe
    if state["loop_count"] >= 2:
        decision = "READY"
        print("[Agent-Hinweis] Maximales Such-Limit erreicht. Erzwinge Report-Generierung.")
    
    if "REFINE" in decision:
        print("[Entscheidung] Informationen unvollständig. Starte Nachrecherche...")
        return {
            "evaluation_status": "needs_more_search",
            "search_query": f"{state['topic']} deep dive technical details architecture"
        }
    else:
        print("[Entscheidung] Daten ausreichend. Gehe zur Synthese über.")
        return {"evaluation_status": "ready"}

# Knoten 3: Schreiben & Vault-Export
def write_node(state: ResearchState):
    print("[Agent-Schritt] Synthetisiere finalen Markdown-Report...")
    
    system_prompt = (
        "Du bist ein präziser AI Research Architekt. "
        "Erstelle einen tiefgehenden, strukturierten Markdown-Report basierend auf den Rohdaten. "
        "Nutze H1, H2, H3, Stichpunkte und eine klare Zusammenfassung."
    )
    
    user_prompt = f"Thema: {state['topic']}\n\nRohdaten:\n{state['raw_data']}"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    report_content = response.content
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    safe_title = state["topic"].replace(" ", "_").replace("/", "-")
    filename = f"{current_date}_{safe_title}.md"
    obsidian_file_path = Path(VAULT_PATH) / filename
    
    frontmatter = f"""---
aliases: [{state['topic']}]
tags: [ai-lab, langgraph-agent, research]
date: {current_date}
topic: "{state['topic']}"
---

# Web Research Report (Autonomous Agent): {state['topic']}

"""
    full_markdown = frontmatter + report_content
    
    os.makedirs(VAULT_PATH, exist_ok=True)
    with open(obsidian_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
        
    print(f"[Erfolg] Report autonom im Obsidian-Vault gespeichert unter: {obsidian_file_path}")
    
    return {"final_report": full_markdown}

# Router für die bedingte Kante
def decide_next_step(state: ResearchState):
    if state["evaluation_status"] == "needs_more_search":
        return "search"
    return "write"

# Graph aufbauen
workflow = StateGraph(ResearchState)

workflow.add_node("search", search_node)
workflow.add_node("evaluate", evaluate_node)
workflow.add_node("write", write_node)

workflow.set_entry_point("search")
workflow.add_edge("search", "evaluate")

workflow.add_conditional_edges(
    "evaluate",
    decide_next_step,
    {
        "search": "search",
        "write": "write"
    }
)

workflow.add_edge("write", END)
app = workflow.compile()

if __name__ == "__main__":
    initial_topic = "Analysiere die Stärken und Schwächen der besten LLM-KI-Modelle auf dem Markt"
    
    initial_state = {
        "topic": initial_topic,
        "search_query": f"{initial_topic} latest trends developments",
        "raw_data": "",
        "evaluation_status": "",
        "loop_count": 0,
        "final_report": ""
    }
    
    print(f"=== Starte autonomen LangGraph Agenten für: '{initial_topic}' ===")
    app.invoke(initial_state)
    print("=== Agenten-Prozess erfolgreich abgeschlossen! ===")