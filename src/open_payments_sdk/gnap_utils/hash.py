import base64
import hashlib


class HashManager:

    @staticmethod
    def verify_hash(client_nonce, interact_nonce, interact_ref, auth_server_url, received_hash)->bool:
        data = f"{client_nonce}\n{interact_nonce}\n{interact_ref}\n{auth_server_url}/"
        hash_bytes = hashlib.sha256(data.encode("utf-8")).digest()
        computed_hash = base64.b64encode(hash_bytes).decode("utf-8")
        return computed_hash == received_hash
