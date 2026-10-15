import os
import json
import re
from mechanisms.base import BaseMechanism

GRAPH_FILE = "synapses/knowledge_graph.json"

class KnowledgeGraphMechanism(BaseMechanism):
    name = "knowledge_graph"
    priority = 32

    def extract_triplets(self, text):
        triplets = []
        for s in re.split(r'[.\n]', text):
            words = [w.strip() for w in s.split() if len(w.strip()) > 2]
            if len(words) >= 3:
                triplets.append({"subject": words[0].capitalize(), "predicate": words[1].lower(), "object": " ".join(words[2:4])})
        return triplets[:5]

    def execute(self, context):
        wisdom = context.get("wisdom_text", "")
        triplets = self.extract_triplets(wisdom)
        
        graph = {"nodes": [], "edges": []}
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f: graph = json.load(f)
            except Exception: pass

        for t in triplets:
            if t["subject"] not in graph["nodes"]: graph["nodes"].append(t["subject"])
            if t["object"] not in graph["nodes"]: graph["nodes"].append(t["object"])
            edge = f"{t['subject']} --[{t['predicate']}]--> {t['object']}"
            if edge not in graph["edges"]: graph["edges"].append(edge)

        graph["nodes"] = graph["nodes"][-100:]
        graph["edges"] = graph["edges"][-150:]

        os.makedirs("synapses", exist_ok=True)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4, ensure_ascii=False)

        context["knowledge_graph_summary"] = f"Entities:{len(graph['nodes'])}, Edges:{len(graph['edges'])}"
