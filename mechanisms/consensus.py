import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from mechanisms.base import BaseMechanism
from adapters.universal_adapter import UniversalAdapter

class ConsensusMechanism(BaseMechanism):
    name = "consensus"
    priority = 20

    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus06-Concur"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, raw
        except Exception:
            return peer, None

    def execute(self, context):
        peers = context.get("peers", [])
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [CONCURRENT HARVEST] Quét song song {len(peers)} nút mạng...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, raw = fut.result()
                if raw:
                    parsed = UniversalAdapter.parse_packet(raw)
                    if parsed:
                        harvested[peer] = parsed["decision"]
                        new_gossip.extend(parsed["gossip"])
                        with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                            bf.write(raw)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested
        print(f"📡 [KẾT NỐI] Phản hồi trực tiếp: {len(harvested)}/{len(peers)} nút.")
