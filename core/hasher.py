import hashlib

class Hasher:
    @staticmethod
    def calculate_sha256(filepath):
        """Computes SHA-256 and safely extracts text content from a file."""
        sha256_hash = hashlib.sha256()
        content = ""
        try:
            # Read block chunks for large files securely
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            # Read human-readable text safely for diff analysis
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            return sha256_hash.hexdigest(), content
        except (OSError, PermissionError, FileNotFoundError):
            return None, ""
