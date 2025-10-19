#!/usr/bin/env python3
"""
Tech stack detection logic for Adaptive Claude Agents.

This module analyzes project files to detect frameworks, languages,
and tooling configurations.

Usage:
    from detect_stack import detect_tech_stack
    result = detect_tech_stack("/path/to/project")

Dependencies:
    - Python 3.9+
    - No external dependencies (uses stdlib only)
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    """
    Structured result from tech stack detection.

    Attributes:
        framework: Primary framework (e.g., "nextjs", "fastapi", "go")
        version: Framework version if detectable
        language: Primary language (e.g., "typescript", "python", "go")
        confidence: Detection confidence score (0.0 to 1.0)
        indicators: List of detection indicators with weights
        tools: Dict of detected tools (testing, styling, state, etc.)
        recommended_subagents: List of recommended subagent names
        project_structure: Dict describing project layout
    """
    framework: str
    version: Optional[str] = None
    language: str = "unknown"
    confidence: float = 0.0
    indicators: List[str] = field(default_factory=list)
    tools: Dict[str, List[str]] = field(default_factory=dict)
    recommended_subagents: List[str] = field(default_factory=list)
    project_structure: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class TechStackDetector:
    """
    Main tech stack detector class.

    Uses file-based detection and content analysis to identify
    project frameworks and tools.
    """

    def __init__(self, project_path: Path):
        """
        Initialize detector.

        Args:
            project_path: Path to project root directory
        """
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")

        logger.info(f"Initialized detector for: {self.project_path}")

    def detect(self) -> Optional[DetectionResult]:
        """
        Detect tech stack.

        Returns:
            DetectionResult if successful, None if detection failed
        """
        logger.info("Starting tech stack detection")

        # Try detection in order of specificity
        result = (
            self._detect_nextjs() or
            self._detect_react() or
            self._detect_vue() or
            self._detect_fastapi() or
            self._detect_django() or
            self._detect_flask() or
            self._detect_go() or
            self._detect_flutter()
        )

        if result and result.confidence > 0.5:
            logger.info(f"Detected: {result.framework} (confidence: {result.confidence:.2f})")
            return result

        logger.warning("Could not confidently detect tech stack")
        return None

    def _detect_nextjs(self) -> Optional[DetectionResult]:
        """Detect Next.js projects."""
        indicators = []
        confidence = 0.0

        # Check for package.json
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return None

        indicators.append("package.json exists: +0.1")
        confidence += 0.1

        # Read package.json
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Failed to read package.json: {e}")
            return None

        # Check for next dependency
        deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
        if 'next' in deps:
            indicators.append(f"'next' dependency found: +0.4")
            confidence += 0.4
            version = deps['next'].lstrip('^~')
        else:
            return None

        # Check for next.config.js/ts
        if (self.project_path / "next.config.js").exists() or \
           (self.project_path / "next.config.ts").exists() or \
           (self.project_path / "next.config.mjs").exists():
            indicators.append("next.config.* exists: +0.3")
            confidence += 0.3

        # Check for app/ or pages/ directory
        has_app_dir = (self.project_path / "app").is_dir()
        has_pages_dir = (self.project_path / "pages").is_dir()

        if has_app_dir:
            indicators.append("app/ directory (App Router): +0.2")
            confidence += 0.2
        elif has_pages_dir:
            indicators.append("pages/ directory (Pages Router): +0.2")
            confidence += 0.2

        # Detect TypeScript
        language = "javascript"
        if (self.project_path / "tsconfig.json").exists():
            language = "typescript"
            indicators.append("TypeScript detected")

        # Detect additional tools
        tools = {}

        # Testing
        testing_tools = []
        if 'vitest' in deps:
            testing_tools.append('vitest')
        if 'jest' in deps:
            testing_tools.append('jest')
        if '@testing-library/react' in deps:
            testing_tools.append('testing-library')
        if testing_tools:
            tools['testing'] = testing_tools

        # Styling
        styling_tools = []
        if 'tailwindcss' in deps:
            styling_tools.append('tailwindcss')
        if 'styled-components' in deps:
            styling_tools.append('styled-components')
        if '@emotion/react' in deps:
            styling_tools.append('emotion')
        if styling_tools:
            tools['styling'] = styling_tools

        # State management
        state_tools = []
        if 'zustand' in deps:
            state_tools.append('zustand')
        if 'redux' in deps or '@reduxjs/toolkit' in deps:
            state_tools.append('redux')
        if state_tools:
            tools['state'] = state_tools

        # API clients
        api_tools = []
        if 'axios' in deps:
            api_tools.append('axios')
        if 'swr' in deps:
            api_tools.append('swr')
        if '@tanstack/react-query' in deps:
            api_tools.append('react-query')
        if api_tools:
            tools['api'] = api_tools

        # Recommended subagents
        subagents = ['nextjs-tester', 'component-reviewer']
        if language == 'typescript':
            subagents.append('type-checker')
        if has_app_dir:
            subagents.append('app-router-specialist')

        return DetectionResult(
            framework="nextjs",
            version=version,
            language=language,
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=subagents,
            project_structure={
                "app_router": has_app_dir,
                "pages_router": has_pages_dir,
                "typescript": language == "typescript"
            }
        )

    def _detect_react(self) -> Optional[DetectionResult]:
        """Detect standalone React projects (non-Next.js)."""
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return None

        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

        deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}

        # Must have react but NOT next
        if 'react' not in deps or 'next' in deps:
            return None

        confidence = 0.6  # Base confidence for React detection
        indicators = ["'react' dependency: +0.6"]

        # Detect build tool
        framework = "react"
        if 'vite' in deps:
            framework = "vite-react"
            confidence += 0.2
            indicators.append("Vite build tool: +0.2")
        elif 'react-scripts' in deps:
            framework = "create-react-app"
            confidence += 0.2
            indicators.append("Create React App: +0.2")

        language = "typescript" if (self.project_path / "tsconfig.json").exists() else "javascript"

        return DetectionResult(
            framework=framework,
            language=language,
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools={},
            recommended_subagents=['react-tester', 'component-reviewer'],
            project_structure={"typescript": language == "typescript"}
        )

    def _detect_vue(self) -> Optional[DetectionResult]:
        """Detect Vue.js projects."""
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return None

        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

        deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}

        if 'vue' not in deps:
            return None

        confidence = 0.7
        indicators = ["'vue' dependency: +0.7"]

        if 'vite' in deps:
            confidence += 0.2
            indicators.append("Vite build tool: +0.2")

        return DetectionResult(
            framework="vue",
            language="javascript",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools={},
            recommended_subagents=['vue-tester', 'component-reviewer'],
            project_structure={}
        )

    def _detect_fastapi(self) -> Optional[DetectionResult]:
        """Detect FastAPI projects."""
        # Check for Python project files
        if not any([
            (self.project_path / "requirements.txt").exists(),
            (self.project_path / "pyproject.toml").exists(),
            (self.project_path / "setup.py").exists()
        ]):
            return None

        confidence = 0.0
        indicators = []

        # Check requirements.txt
        requirements_file = self.project_path / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    requirements = f.read().lower()
                    if 'fastapi' in requirements:
                        confidence += 0.6
                        indicators.append("'fastapi' in requirements.txt: +0.6")
            except UnicodeDecodeError:
                pass

        # Check for Python files with fastapi imports
        python_files = list(self.project_path.glob("*.py"))
        python_files.extend(self.project_path.glob("**/*.py"))

        for py_file in python_files[:10]:  # Check first 10 files
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'from fastapi import' in content or 'import fastapi' in content:
                        confidence += 0.3
                        indicators.append(f"FastAPI import in {py_file.name}: +0.3")
                        break
            except (UnicodeDecodeError, PermissionError):
                continue

        if confidence < 0.5:
            return None

        return DetectionResult(
            framework="fastapi",
            language="python",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools={},
            recommended_subagents=['fastapi-tester', 'api-reviewer', 'async-checker'],
            project_structure={}
        )

    def _detect_django(self) -> Optional[DetectionResult]:
        """Detect Django projects."""
        # Check for manage.py (Django's signature file)
        if not (self.project_path / "manage.py").exists():
            return None

        confidence = 0.8
        indicators = ["manage.py exists: +0.8"]

        return DetectionResult(
            framework="django",
            language="python",
            confidence=confidence,
            indicators=indicators,
            tools={},
            recommended_subagents=['django-tester', 'model-reviewer'],
            project_structure={}
        )

    def _detect_flask(self) -> Optional[DetectionResult]:
        """Detect Flask projects."""
        requirements_file = self.project_path / "requirements.txt"
        if not requirements_file.exists():
            return None

        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.read().lower()
                if 'flask' in requirements:
                    return DetectionResult(
                        framework="flask",
                        language="python",
                        confidence=0.7,
                        indicators=["'flask' in requirements.txt: +0.7"],
                        tools={},
                        recommended_subagents=['flask-tester', 'api-reviewer'],
                        project_structure={}
                    )
        except UnicodeDecodeError:
            pass

        return None

    def _detect_go(self) -> Optional[DetectionResult]:
        """Detect Go projects."""
        go_mod = self.project_path / "go.mod"
        if not go_mod.exists():
            return None

        confidence = 0.8
        indicators = ["go.mod exists: +0.8"]

        # Try to detect framework
        framework = "go"
        try:
            with open(go_mod, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'gin-gonic/gin' in content:
                    framework = "go-gin"
                    indicators.append("Gin framework: +0.1")
                    confidence += 0.1
                elif 'labstack/echo' in content:
                    framework = "go-echo"
                    indicators.append("Echo framework: +0.1")
                    confidence += 0.1
                elif 'gofiber/fiber' in content:
                    framework = "go-fiber"
                    indicators.append("Fiber framework: +0.1")
                    confidence += 0.1
        except UnicodeDecodeError:
            pass

        return DetectionResult(
            framework=framework,
            language="go",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools={},
            recommended_subagents=['go-tester', 'go-reviewer', 'concurrency-checker'],
            project_structure={}
        )

    def _detect_flutter(self) -> Optional[DetectionResult]:
        """Detect Flutter projects."""
        pubspec = self.project_path / "pubspec.yaml"
        if not pubspec.exists():
            return None

        confidence = 0.8
        indicators = ["pubspec.yaml exists: +0.8"]

        return DetectionResult(
            framework="flutter",
            language="dart",
            confidence=confidence,
            indicators=indicators,
            tools={},
            recommended_subagents=['flutter-tester', 'widget-reviewer'],
            project_structure={}
        )


def detect_tech_stack(project_path: str) -> Optional[DetectionResult]:
    """
    Main entry point for tech stack detection.

    Args:
        project_path: Path to project root directory

    Returns:
        DetectionResult if successful, None otherwise

    Example:
        >>> result = detect_tech_stack("/path/to/nextjs-project")
        >>> print(result.framework)
        'nextjs'
        >>> print(result.confidence)
        0.95
    """
    try:
        detector = TechStackDetector(Path(project_path))
        return detector.detect()
    except Exception as e:
        logger.error(f"Detection failed: {e}")
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_stack.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    result = detect_tech_stack(project_path)

    if result:
        print("\n" + "=" * 60)
        print("Tech Stack Detection Result")
        print("=" * 60)
        print(result.to_json())
        print("=" * 60)
    else:
        print("❌ Could not detect tech stack")
        sys.exit(1)
