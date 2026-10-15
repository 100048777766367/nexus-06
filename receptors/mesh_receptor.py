import json
import urllib.request

class MeshReceptor:
    """NẤC 2: Anten bắt sóng mạng lưới nơ-ron sợi nấm toàn cầu"""
    @staticmethod
    def capture_pulse(peer_url, timeout=3.5):
        try:
            req = urllib.request.Request(peer_url, headers={"User-Agent": "Nexus06-MeshReceptor"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode('utf-8'))
        except Exception:
            return None
        return None
