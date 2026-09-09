"""Safe filesystem utility nodes."""

import fnmatch
from pathlib import Path


class FWFileCount:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "directory_path": ("STRING", {"default": ""}),
            "file_types": ("STRING", {"default": "*.png,*.jpg,*.jpeg"}),
            "recursive": ("BOOLEAN", {"default": False}),
            "case_sensitive": ("BOOLEAN", {"default": False}),
        }}

    RETURN_TYPES = ("INT", "STRING", "BOOLEAN")
    RETURN_NAMES = ("file_count", "status", "exists")
    FUNCTION = "execute"
    CATEGORY = "Fearnworks/Filesystem"

    def execute(self, directory_path, file_types, recursive, case_sensitive):
        path = Path(directory_path).expanduser()
        if not path.exists():
            return (0, "Directory does not exist", False)
        if not path.is_dir():
            return (0, "Path is not a directory", False)

        patterns = [p.strip() for p in file_types.split(",") if p.strip()]
        iterator = path.rglob("*") if recursive else path.iterdir()
        count = 0
        try:
            for candidate in iterator:
                if not candidate.is_file():
                    continue
                name = candidate.name if case_sensitive else candidate.name.lower()
                for pattern in patterns:
                    pattern = pattern if case_sensitive else pattern.lower()
                    if fnmatch.fnmatchcase(name, pattern):
                        count += 1
                        break
        except OSError as exc:
            return (count, f"Filesystem error: {exc}", True)
        return (count, f"Matched {count} file(s)", True)
