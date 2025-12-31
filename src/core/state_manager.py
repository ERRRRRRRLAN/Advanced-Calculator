import json
import os

class StateManager:
    """Mengelola riwayat perhitungan dengan fitur Save/Load ke JSON."""
    
    def __init__(self, storage_file="history.json"):
        self.storage_file = storage_file
        self._history = self._load_from_disk()

    def _load_from_disk(self):
        """Memuat data dari file jika tersedia."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_to_disk(self):
        """Menyimpan state saat ini ke file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self._history, f, indent=4)
        except IOError as e:
            print(f"Failed to save history: {e}")

    def add_to_history(self, expression: str, result: str):
        entry = {"expression": expression, "result": result}
        self._history.append(entry)
        if len(self._history) > 50:
            self._history.pop(0)
        self._save_to_disk() # Simpan setiap ada perubahan

    def get_history(self):
        return self._history

    def clear_history(self):
        self._history = []
        self._save_to_disk()