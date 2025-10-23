#!/usr/bin/env python3
"""
Detection result caching system for Adaptive Claude Agents.

Implements filesystem-based cache with mtime-based invalidation,
file locking for thread safety, and TTL-based expiration.

Usage:
    from detection_cache import DetectionCache
    from detect_stack import DetectionResult

    cache = DetectionCache()
    result = cache.get(Path("/path/to/project"))
    if not result:
        # Cache miss - run detection
        result = detect_project()
        cache.set(Path("/path/to/project"), result)
"""

import fcntl
import hashlib
import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Version for cache invalidation
VERSION = "0.7.0-beta"

# Default TTL: 24 hours
DEFAULT_TTL_SECONDS = 24 * 60 * 60


class DetectionCache:
    """
    Filesystem-based cache for detection results.

    Provides O(1) cache lookups with mtime-based invalidation.
    Thread-safe via file locking (fcntl).

    Cache structure:
        ~/.cache/adaptive-claude-agents/
            detection_cache.json    # Main cache file
            metadata.json           # Cache metadata (hit count, etc.)
            .lock                   # Lock file for thread safety
    """

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = DEFAULT_TTL_SECONDS):
        """
        Initialize detection cache.

        Args:
            cache_dir: Base cache directory (default: ~/.cache)
            ttl: Time-to-live in seconds (default: 24h)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache"

        self.cache_dir = cache_dir / "adaptive-claude-agents"
        self.cache_file = self.cache_dir / "detection_cache.json"
        self.metadata_file = self.cache_dir / "metadata.json"
        self.lock_file = self.cache_dir / ".lock"
        self.ttl = ttl

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.debug(f"Initialized cache at: {self.cache_dir}")

    def generate_key(self, project_path: Path) -> str:
        """
        Generate unique cache key for project.

        Key format: "{path_hash}:{mtime_hash}:{version}"

        Args:
            project_path: Absolute path to project

        Returns:
            Cache key string

        Example:
            "a1b2c3d4e5f6g7h8:12345678:0.7.0-beta"
        """
        # 1. Resolve to absolute path
        abs_path = project_path.resolve()

        # 2. Get mtime of key indicator files
        key_files = self._get_key_indicator_files(abs_path)

        # 3. Compute mtime hash
        mtime_hash = self._compute_mtime_hash(key_files)

        # 4. Hash the path (avoid long path issues)
        path_hash = hashlib.sha256(str(abs_path).encode()).hexdigest()[:16]

        # 5. Combine components
        return f"{path_hash}:{mtime_hash}:{VERSION}"

    def _get_key_indicator_files(self, project_path: Path) -> List[Path]:
        """
        Get list of files that indicate project type.

        Changes to these files should invalidate cache.

        Args:
            project_path: Project root path

        Returns:
            List of existing indicator files
        """
        indicators = [
            # JavaScript/TypeScript
            project_path / "package.json",
            project_path / "package-lock.json",
            project_path / "yarn.lock",
            project_path / "pnpm-lock.yaml",
            # Python
            project_path / "requirements.txt",
            project_path / "pyproject.toml",
            project_path / "Pipfile",
            project_path / "setup.py",
            # Go
            project_path / "go.mod",
            project_path / "go.sum",
            # Flutter/Dart
            project_path / "pubspec.yaml",
            project_path / "pubspec.lock",
            # iOS
            project_path / "Podfile",
            project_path / "Podfile.lock",
            # PHP
            project_path / "composer.json",
            project_path / "composer.lock",
            # Configuration
            project_path / "next.config.js",
            project_path / "next.config.ts",
            project_path / "next.config.mjs",
            project_path / "vite.config.js",
            project_path / "vite.config.ts",
        ]

        # Return only files that exist
        return [f for f in indicators if f.exists()]

    def _compute_mtime_hash(self, files: List[Path]) -> str:
        """
        Compute hash of modification times.

        Args:
            files: List of files to check

        Returns:
            16-character hex hash of sorted mtimes
        """
        if not files:
            # No indicator files - use timestamp as fallback
            return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

        # Get sorted mtimes
        mtimes = sorted([f.stat().st_mtime for f in files])

        # Hash the concatenated mtimes
        mtime_str = ",".join(str(int(m)) for m in mtimes)
        return hashlib.sha256(mtime_str.encode()).hexdigest()[:16]

    def get(self, project_path: Path) -> Optional[Dict]:
        """
        Get cached detection result.

        Args:
            project_path: Project root path

        Returns:
            Cached DetectionResult dict if valid, None if cache miss

        Cache miss scenarios:
        - Key not in cache
        - Entry expired (TTL exceeded)
        - Entry version mismatch
        """
        key = self.generate_key(project_path)

        # Acquire lock for reading
        with self._lock():
            # Load cache
            cache_data = self._load_cache()

            # Check if key exists
            if key not in cache_data:
                logger.debug(f"Cache miss: key not found ({key[:16]}...)")
                self._increment_miss()
                return None

            entry = cache_data[key]

            # Check TTL
            age = time.time() - entry.get("cached_at", 0)
            if age > self.ttl:
                logger.debug(f"Cache miss: expired ({age:.0f}s > {self.ttl}s)")
                self._increment_miss()
                # Remove expired entry
                del cache_data[key]
                self._save_cache(cache_data)
                return None

            # Cache hit!
            logger.info(f"✓ Cache hit: {entry['result']['framework']} (age: {age:.0f}s)")
            self._increment_hit()
            return entry["result"]

    def set(self, project_path: Path, result: Dict):
        """
        Store detection result in cache.

        Args:
            project_path: Project root path
            result: DetectionResult dict to cache
        """
        key = self.generate_key(project_path)

        # Create cache entry
        entry = {
            "result": result,
            "cached_at": time.time(),
            "version": VERSION,
        }

        # Acquire lock for writing
        with self._lock():
            cache_data = self._load_cache()
            cache_data[key] = entry
            self._save_cache(cache_data)

        logger.debug(f"Cached: {result['framework']} ({key[:16]}...)")

    def clear(self):
        """
        Clear entire cache.

        Useful for testing or manual cache invalidation.
        """
        with self._lock():
            self._save_cache({})
            logger.info("Cache cleared")

    def stats(self) -> Dict:
        """
        Get cache statistics.

        Returns:
            Dict with hit count, miss count, hit rate, size
        """
        with self._lock():
            metadata = self._load_metadata()
            cache_data = self._load_cache()

            hits = metadata.get("hits", 0)
            misses = metadata.get("misses", 0)
            total = hits + misses
            hit_rate = (hits / total * 100) if total > 0 else 0

            return {
                "hits": hits,
                "misses": misses,
                "total_requests": total,
                "hit_rate": f"{hit_rate:.1f}%",
                "cache_entries": len(cache_data),
                "cache_file_size": self.cache_file.stat().st_size if self.cache_file.exists() else 0,
            }

    def _lock(self):
        """
        Context manager for file locking.

        Ensures thread-safe access to cache files.

        Usage:
            with self._lock():
                # Critical section
                cache_data = self._load_cache()
        """
        return FileLock(self.lock_file)

    def _load_cache(self) -> Dict:
        """
        Load cache data from disk.

        Returns:
            Cache data dict (empty if file doesn't exist)
        """
        if not self.cache_file.exists():
            return {}

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load cache: {e}")
            return {}

    def _save_cache(self, cache_data: Dict):
        """
        Save cache data to disk.

        Args:
            cache_data: Cache data dict to save
        """
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save cache: {e}")

    def _load_metadata(self) -> Dict:
        """
        Load cache metadata (hit/miss counts).

        Returns:
            Metadata dict
        """
        if not self.metadata_file.exists():
            return {"hits": 0, "misses": 0}

        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"hits": 0, "misses": 0}

    def _save_metadata(self, metadata: Dict):
        """
        Save cache metadata to disk.

        Args:
            metadata: Metadata dict to save
        """
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save metadata: {e}")

    def _increment_hit(self):
        """Increment cache hit counter."""
        metadata = self._load_metadata()
        metadata["hits"] = metadata.get("hits", 0) + 1
        self._save_metadata(metadata)

    def _increment_miss(self):
        """Increment cache miss counter."""
        metadata = self._load_metadata()
        metadata["misses"] = metadata.get("misses", 0) + 1
        self._save_metadata(metadata)


class FileLock:
    """
    Context manager for file locking using fcntl.

    Ensures thread-safe and process-safe file access.

    Usage:
        with FileLock(lock_file):
            # Critical section - exclusive access
            data = read_file()
            modify_data(data)
            write_file(data)
    """

    def __init__(self, lock_file: Path):
        """
        Initialize file lock.

        Args:
            lock_file: Path to lock file
        """
        self.lock_file = lock_file
        self.lock_fd = None

    def __enter__(self):
        """Acquire lock."""
        # Ensure lock file exists
        self.lock_file.touch(exist_ok=True)

        # Open lock file
        self.lock_fd = open(self.lock_file, 'r')

        # Acquire exclusive lock (blocks until available)
        fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_EX)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.lock_fd:
            # Release lock
            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_UN)
            self.lock_fd.close()
            self.lock_fd = None
