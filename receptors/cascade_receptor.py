import hashlib
import json
import os

class ContractReceptor:
    """NẤC 3: Màng kiểm dịch kháng lượng tử SHAKE & Bẫy năng lượng hacker"""
    @staticmethod
    def verify_and_absorb(raw_data, source_peer, immune_memory_path="synapses/immune_memory.json"):
        try:
            packet = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
            contract = packet.get("contract", "")
            
            if "bodhi" in contract or "nexus" in contract:
                return True, packet, None

            quarantine_energy = {
                "source": source_peer,
                "entropy_signature": hashlib.shake_256(str(raw_data).encode()).hexdigest(16),
                "absorbed_weight": round(len(str(raw_data)) / 1000.0, 4)
            }
            ContractReceptor.store_immune_memory(quarantine_energy, immune_memory_path)
            return False, None, quarantine_energy
        except Exception:
            return False, None, None

    @staticmethod
    def store_immune_memory(energy_data, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        memory = []
        if os.path.exists(path):
            try:
                with open(path, "r") as f: memory = json.load(f)
            except Exception: pass
        memory.append(energy_data)
        with open(path, "w") as f: json.dump(memory[-50:], f, indent=4)
        print(f"🛡️ [PHẢN MONG MANH] Đã nuốt trọn năng lượng bất thường từ {energy_data['source']} vào Túi Kháng Thể!")
