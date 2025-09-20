import csv
import os
from typing import Dict, Iterable, List, Optional


class BooksRepository:
    def __init__(self, csv_path: str) -> None:
        self.csv_path = csv_path
        self._data: Optional[List[Dict[str, str]]] = None

    def ensure_loaded(self) -> None:
        if self._data is not None:
            return
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Books CSV not found: {self.csv_path}")
        rows: List[Dict[str, str]] = []
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()})
        # Synthesize an ID if not present
        headers = rows[0].keys() if rows else []
        has_id = any(str(h).strip().lower() in ("id", "book_id") for h in headers)
        if not has_id:
            for i, r in enumerate(rows, start=1):
                r["id"] = str(i)
        self._data = rows

    @property
    def headers(self) -> List[str]:
        self.ensure_loaded()
        assert self._data is not None
        return list(self._data[0].keys()) if self._data else []

    def list_all(self) -> List[Dict[str, str]]:
        self.ensure_loaded()
        assert self._data is not None
        return list(self._data)

    def get_by_id(self, book_id: str) -> Optional[Dict[str, str]]:
        self.ensure_loaded()
        assert self._data is not None
        key_candidates = [k for k in self.headers if k.lower() in ("id", "book_id")] or [self.headers[0]]
        key = key_candidates[0]
        for row in self._data:
            if str(row.get(key, "")).strip() == str(book_id).strip():
                return row
        return None

    def filter(self,
               genre: Optional[str] = None,
               year: Optional[str] = None,
               author: Optional[str] = None,
               title_contains: Optional[str] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None) -> List[Dict[str, str]]:
        self.ensure_loaded()
        assert self._data is not None

        def matches(row: Dict[str, str]) -> bool:
            if genre is not None:
                genre_col = _find_col(self.headers, "genre")
                genre_val = str(row.get(genre_col, ""))
                # Check if genre is contained in the category string (case insensitive)
                if genre.lower() not in genre_val.lower():
                    return False
            if year is not None and str(row.get(_find_col(self.headers, "year"), "")).strip() != str(year).strip():
                return False
            if author is not None and not _eq_ci(row.get(_find_col(self.headers, "author"), ""), author):
                return False
            if title_contains is not None:
                title_val = str(row.get(_find_col(self.headers, "title"), ""))
                if title_contains.lower() not in title_val.lower():
                    return False
            return True

        filtered: List[Dict[str, str]] = [row for row in self._data if matches(row)]
        if offset is not None:
            filtered = filtered[offset:]
        if limit is not None:
            filtered = filtered[:limit]
        return filtered


def _find_col(headers: Iterable[str], target: str) -> str:
    target_l = target.lower()
    for h in headers:
        if h.lower() == target_l:
            return h
    # Best-effort aliases
    aliases = {
        "title": {"book_title", "name"},
        "author": {"authors", "writer"},
        "year": {"publication_year", "year_published", "publish date (year)"},
        "genre": {"category", "genres"},
    }
    if target in aliases:
        for h in headers:
            if h.lower() in aliases[target]:
                return h
    return target


def _eq_ci(a: str, b: str) -> bool:
    return str(a).strip().lower() == str(b).strip().lower()
