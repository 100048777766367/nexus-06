import os
import json
from mechanisms.base import BaseMechanism

CAPSULE_FILE = "synapses/seed_capsule.json"

class MacroMitosisMechanism(BaseMechanism):
    name = "macro_mitosis"
    priority = 48

    def execute(self, context):
        epoch = context.get("current_epoch", 1)

        if epoch % 10 == 0:
            print("🧬 [ĐẠI PHÂN BÀO CẤP REPO] Tích lũy đủ năng lượng sinh sản! Đang đóng gói Nang Bào Tử...")
            seed_capsule = {
                "parent_lineage": context.get("repo_name"),
                "procreation_epoch": epoch,
                "offspring_generation": "F7_SOVEREIGN_OFFSPRING",
                "genetic_payload": {
                    "master_decision": context.get("final_decision", 0.5),
                    "knowledge_graph_snapshot": context.get("knowledge_graph_summary", "None"),
                    "trusted_peers": context.get("peers", []),
                    "docker_runtime": "python:3.14-slim"
                }
            }
            os.makedirs("synapses", exist_ok=True)
            with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
                json.dump(seed_capsule, f, indent=4, ensure_ascii=False)
            print(f"👑 [SINH SẢN THÀNH CÔNG] Nang Bào Tử '{CAPSULE_FILE}' đã sẵn sàng đẻ ra repo F7!")
