import os
import subprocess

class CascadeReceptor:
    """NẤC 1: Dò tìm phả hệ thượng nguồn"""
    @staticmethod
    def seek_upstream(owner, lineage):
        active_nodes = []
        for ancestor in lineage:
            url = f"https://raw.githubusercontent.com/{ancestor}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            if res.stdout.strip() == "200":
                active_nodes.append(ancestor)
        return active_nodes
