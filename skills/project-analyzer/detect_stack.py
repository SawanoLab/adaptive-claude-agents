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
            self._detect_vanilla_php_web() or
            self._detect_python_ml() or
            self._detect_ios_swift() or
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
        """
        Detect FastAPI projects.
        
        Detection criteria:
        - requirements.txt or pyproject.toml with 'fastapi'
        - Python files with FastAPI imports
        - FastAPI-specific patterns (APIRouter, dependencies, etc.)
        - Common tools: pytest, SQLAlchemy, pydantic, uvicorn
        
        Returns:
            DetectionResult if FastAPI detected, None otherwise
        """
        # Check for Python project files
        if not any([
            (self.project_path / "requirements.txt").exists(),
            (self.project_path / "pyproject.toml").exists(),
            (self.project_path / "setup.py").exists()
        ]):
            return None

        confidence = 0.0
        indicators = []
        version = None
        tools = {}

        # Check requirements.txt
        requirements_file = self.project_path / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    requirements = f.read()
                    requirements_lower = requirements.lower()
                    
                    # Check for FastAPI
                    if 'fastapi' in requirements_lower:
                        confidence += 0.5
                        indicators.append("'fastapi' in requirements.txt: +0.5")
                        
                        # Try to extract version
                        for line in requirements.splitlines():
                            if 'fastapi' in line.lower() and '==' in line:
                                version = line.split('==')[1].strip()
                                break
                    
                    # Check for common FastAPI tools
                    if 'uvicorn' in requirements_lower:
                        tools.setdefault('server', []).append('uvicorn')
                        confidence += 0.05
                        indicators.append("'uvicorn' server: +0.05")
                    
                    if 'pytest' in requirements_lower or 'pytest-asyncio' in requirements_lower:
                        tools.setdefault('testing', []).append('pytest')
                        if 'pytest-asyncio' in requirements_lower:
                            tools['testing'].append('pytest-asyncio')
                    
                    if 'sqlalchemy' in requirements_lower:
                        tools.setdefault('orm', []).append('sqlalchemy')
                    elif 'tortoise-orm' in requirements_lower:
                        tools.setdefault('orm', []).append('tortoise-orm')
                    
                    if 'pydantic' in requirements_lower:
                        tools.setdefault('validation', []).append('pydantic')
                    
                    if 'alembic' in requirements_lower:
                        tools.setdefault('migration', []).append('alembic')
                    
                    # Database drivers
                    if 'psycopg2' in requirements_lower or 'asyncpg' in requirements_lower:
                        tools.setdefault('database', []).append('postgresql')
                    if 'pymysql' in requirements_lower or 'aiomysql' in requirements_lower:
                        tools.setdefault('database', []).append('mysql')
                    if 'motor' in requirements_lower:
                        tools.setdefault('database', []).append('mongodb')
                        
            except UnicodeDecodeError:
                pass

        # Check pyproject.toml
        pyproject_file = self.project_path / "pyproject.toml"
        if pyproject_file.exists():
            try:
                with open(pyproject_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if 'fastapi' in content:
                        confidence += 0.5
                        indicators.append("'fastapi' in pyproject.toml: +0.5")
            except UnicodeDecodeError:
                pass

        # Check for Python files with fastapi imports
        python_files = list(self.project_path.glob("*.py"))
        python_files.extend(list(self.project_path.glob("app/**/*.py")))
        python_files.extend(list(self.project_path.glob("src/**/*.py")))

        fastapi_patterns = [
            'from fastapi import',
            'import fastapi',
            'FastAPI(',
            'APIRouter(',
            '@app.get',
            '@app.post',
            '@router.get',
            '@router.post'
        ]

        for py_file in python_files[:20]:  # Check first 20 files
            if 'venv' in str(py_file) or '.venv' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for pattern in fastapi_patterns:
                        if pattern in content:
                            confidence += 0.15
                            indicators.append(f"FastAPI pattern '{pattern}' in {py_file.name}: +0.15")
                            break
                            
            except (UnicodeDecodeError, PermissionError):
                continue

        # Check for main.py or app.py (common entry points)
        entry_points = [
            self.project_path / "main.py",
            self.project_path / "app.py",
            self.project_path / "app" / "main.py"
        ]
        
        for entry_point in entry_points:
            if entry_point.exists():
                try:
                    with open(entry_point, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'FastAPI(' in content or 'from fastapi import FastAPI' in content:
                            confidence += 0.1
                            indicators.append(f"{entry_point.name} with FastAPI app: +0.1")
                            break
                except (UnicodeDecodeError, PermissionError):
                    pass

        # Minimum confidence threshold
        if confidence < 0.5:
            return None

        # Determine recommended subagents
        recommended_subagents = ['api-developer', 'api-tester']
        
        if 'pytest' in tools.get('testing', []):
            recommended_subagents.append('pytest-specialist')
        
        if tools.get('orm'):
            if 'sqlalchemy' in tools['orm']:
                recommended_subagents.append('sqlalchemy-specialist')
            elif 'tortoise-orm' in tools['orm']:
                recommended_subagents.append('orm-specialist')
        
        if 'pydantic' in tools.get('validation', []):
            recommended_subagents.append('pydantic-specialist')
        
        if tools.get('database'):
            if 'postgresql' in tools['database']:
                recommended_subagents.append('postgresql-specialist')
            elif 'mysql' in tools['database']:
                recommended_subagents.append('mysql-specialist')
            elif 'mongodb' in tools['database']:
                recommended_subagents.append('mongodb-specialist')

        # Project structure
        project_structure = {
            'has_requirements_txt': requirements_file.exists(),
            'has_pyproject_toml': pyproject_file.exists(),
            'has_app_directory': (self.project_path / 'app').exists(),
            'has_tests': (self.project_path / 'tests').exists() or (self.project_path / 'test').exists()
        }

        return DetectionResult(
            framework="fastapi",
            version=version,
            language="python",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
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
        """
        Detect Go projects.

        Detection criteria:
        - go.mod file (Go modules)
        - Go framework detection (Gin, Echo, Fiber, Chi, Gorilla)
        - Go files with common patterns
        - Testing framework detection
        - Database drivers and ORM detection

        Returns:
            DetectionResult if Go project detected, None otherwise
        """
        go_mod = self.project_path / "go.mod"
        if not go_mod.exists():
            return None

        confidence = 0.7
        indicators = ["go.mod exists: +0.7"]
        tools = {}
        version = None

        # Try to detect framework and dependencies
        framework = "go"
        framework_detected = False

        try:
            with open(go_mod, 'r', encoding='utf-8') as f:
                content = f.read()

                # Framework detection
                if 'gin-gonic/gin' in content:
                    framework = "go-gin"
                    indicators.append("Gin framework: +0.15")
                    confidence += 0.15
                    framework_detected = True
                    tools['web-framework'] = ['gin']
                elif 'labstack/echo' in content:
                    framework = "go-echo"
                    indicators.append("Echo framework: +0.15")
                    confidence += 0.15
                    framework_detected = True
                    tools['web-framework'] = ['echo']
                elif 'gofiber/fiber' in content:
                    framework = "go-fiber"
                    indicators.append("Fiber framework: +0.15")
                    confidence += 0.15
                    framework_detected = True
                    tools['web-framework'] = ['fiber']
                elif 'go-chi/chi' in content:
                    framework = "go-chi"
                    indicators.append("Chi router: +0.15")
                    confidence += 0.15
                    framework_detected = True
                    tools['web-framework'] = ['chi']
                elif 'gorilla/mux' in content:
                    framework = "go-gorilla"
                    indicators.append("Gorilla Mux router: +0.15")
                    confidence += 0.15
                    framework_detected = True
                    tools['web-framework'] = ['gorilla-mux']

                # Go version detection
                import re
                go_version_match = re.search(r'go (\d+\.\d+)', content)
                if go_version_match:
                    version = go_version_match.group(1)

                # ORM/Database libraries
                if 'gorm.io/gorm' in content:
                    tools.setdefault('orm', []).append('gorm')
                    indicators.append("GORM ORM: +0.05")
                    confidence += 0.05
                elif 'ent' in content or 'entgo.io' in content:
                    tools.setdefault('orm', []).append('ent')
                    indicators.append("Ent ORM: +0.05")
                    confidence += 0.05

                # Database drivers
                if 'lib/pq' in content or 'gorm.io/driver/postgres' in content:
                    tools.setdefault('database', []).append('postgresql')
                elif 'go-sql-driver/mysql' in content or 'gorm.io/driver/mysql' in content:
                    tools.setdefault('database', []).append('mysql')
                elif 'mattn/go-sqlite3' in content or 'gorm.io/driver/sqlite' in content:
                    tools.setdefault('database', []).append('sqlite')
                elif 'go.mongodb.org/mongo-driver' in content:
                    tools.setdefault('database', []).append('mongodb')

                # Testing frameworks
                if 'testify' in content or 'stretchr/testify' in content:
                    tools.setdefault('testing', []).append('testify')
                if 'ginkgo' in content:
                    tools.setdefault('testing', []).append('ginkgo')
                if 'goconvey' in content:
                    tools.setdefault('testing', []).append('goconvey')

                # API/HTTP clients
                if 'go-resty/resty' in content:
                    tools.setdefault('http-client', []).append('resty')

                # Logging
                if 'sirupsen/logrus' in content:
                    tools.setdefault('logging', []).append('logrus')
                elif 'uber-go/zap' in content:
                    tools.setdefault('logging', []).append('zap')

                # Config management
                if 'spf13/viper' in content:
                    tools.setdefault('config', []).append('viper')

        except UnicodeDecodeError:
            pass

        # Check for Go source files with common patterns
        go_files = list(self.project_path.glob("*.go"))
        go_files.extend(list(self.project_path.glob("cmd/**/*.go")))
        go_files.extend(list(self.project_path.glob("internal/**/*.go")))
        go_files.extend(list(self.project_path.glob("pkg/**/*.go")))

        go_patterns = [
            'func main(',
            'http.ListenAndServe',
            'router.Run(',
            'e.Start(',
            'app.Listen('
        ]

        for go_file in go_files[:15]:
            if 'vendor' in str(go_file):
                continue

            try:
                with open(go_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for pattern in go_patterns:
                        if pattern in content:
                            confidence += 0.05
                            indicators.append(f"Go pattern '{pattern}' in {go_file.name}: +0.05")
                            break

            except (UnicodeDecodeError, PermissionError):
                continue

        # Check for Dockerfile (common in Go projects)
        if (self.project_path / "Dockerfile").exists():
            tools.setdefault('containerization', []).append('docker')
            confidence += 0.05
            indicators.append("Dockerfile: +0.05")

        # Recommended subagents
        recommended_subagents = ['go-developer', 'go-reviewer', 'concurrency-checker']

        if framework_detected and tools.get('web-framework'):
            recommended_subagents.append('api-developer')

        if 'testify' in tools.get('testing', []):
            recommended_subagents.append('go-tester')

        if tools.get('orm'):
            if 'gorm' in tools['orm']:
                recommended_subagents.append('gorm-specialist')
            elif 'ent' in tools['orm']:
                recommended_subagents.append('ent-specialist')

        if tools.get('database'):
            if 'postgresql' in tools['database']:
                recommended_subagents.append('postgresql-specialist')
            elif 'mysql' in tools['database']:
                recommended_subagents.append('mysql-specialist')
            elif 'mongodb' in tools['database']:
                recommended_subagents.append('mongodb-specialist')

        # Project structure
        project_structure = {
            'has_go_mod': True,
            'has_cmd_dir': (self.project_path / 'cmd').exists(),
            'has_internal_dir': (self.project_path / 'internal').exists(),
            'has_pkg_dir': (self.project_path / 'pkg').exists(),
            'has_dockerfile': (self.project_path / 'Dockerfile').exists(),
            'framework': framework
        }

        return DetectionResult(
            framework=framework,
            version=version,
            language="go",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
        )

    def _detect_flutter(self) -> Optional[DetectionResult]:
        """
        Detect Flutter projects.

        Detection criteria:
        - pubspec.yaml with flutter SDK
        - Dart files with Flutter imports
        - Flutter project structure (lib/, android/, ios/)
        - State management libraries detection
        - Testing frameworks detection

        Returns:
            DetectionResult if Flutter project detected, None otherwise
        """
        pubspec = self.project_path / "pubspec.yaml"
        if not pubspec.exists():
            return None

        confidence = 0.0
        indicators = []
        tools = {}
        version = None

        # Parse pubspec.yaml
        try:
            import yaml
            with open(pubspec, 'r', encoding='utf-8') as f:
                pubspec_data = yaml.safe_load(f)

            if not pubspec_data:
                return None

            # Check for flutter SDK (in dependencies or as top-level config)
            deps = pubspec_data.get('dependencies', {})
            has_flutter_dep = 'flutter' in deps
            has_flutter_config = 'flutter' in pubspec_data

            if not has_flutter_dep and not has_flutter_config:
                # Has pubspec.yaml but no flutter - likely a Dart CLI project
                return None

            confidence += 0.6
            indicators.append("pubspec.yaml with flutter SDK: +0.6")

            # deps already defined above, continue using it
            dev_deps = pubspec_data.get('dev_dependencies', {})
            all_deps = {**deps, **dev_deps}

            # Flutter SDK version
            flutter_config = pubspec_data.get('flutter', {})
            if isinstance(flutter_config, dict) and 'sdk' in flutter_config:
                version = "flutter"

            # State management
            if 'provider' in deps:
                tools.setdefault('state-management', []).append('provider')
            if 'riverpod' in deps or 'flutter_riverpod' in deps:
                tools.setdefault('state-management', []).append('riverpod')
            if 'bloc' in deps or 'flutter_bloc' in deps:
                tools.setdefault('state-management', []).append('bloc')
            if 'get' in deps or 'get_it' in deps:
                tools.setdefault('state-management', []).append('getx' if 'get' in deps else 'get_it')
            if 'mobx' in deps or 'flutter_mobx' in deps:
                tools.setdefault('state-management', []).append('mobx')

            # HTTP clients
            if 'dio' in deps:
                tools.setdefault('http-client', []).append('dio')
            if 'http' in deps:
                tools.setdefault('http-client', []).append('http')

            # Database/Storage
            if 'sqflite' in deps:
                tools.setdefault('database', []).append('sqflite')
            if 'hive' in deps or 'hive_flutter' in deps:
                tools.setdefault('database', []).append('hive')
            if 'shared_preferences' in deps:
                tools.setdefault('storage', []).append('shared_preferences')

            # Navigation
            if 'go_router' in deps:
                tools.setdefault('navigation', []).append('go_router')
            if 'auto_route' in deps:
                tools.setdefault('navigation', []).append('auto_route')

            # Testing
            if 'flutter_test' in dev_deps:
                tools.setdefault('testing', []).append('flutter_test')
            if 'mockito' in dev_deps:
                tools.setdefault('testing', []).append('mockito')
            if 'integration_test' in dev_deps:
                tools.setdefault('testing', []).append('integration_test')

            # UI libraries
            if 'google_fonts' in deps:
                tools.setdefault('ui', []).append('google_fonts')

        except (yaml.YAMLError, ImportError) as e:
            # If YAML parsing fails or yaml module not available, use basic detection
            try:
                with open(pubspec, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'flutter:' in content or 'sdk: flutter' in content:
                        confidence += 0.6
                        indicators.append("pubspec.yaml with flutter reference: +0.6")
                    else:
                        return None
            except UnicodeDecodeError:
                return None

        # Check for Flutter project structure
        has_lib = (self.project_path / 'lib').is_dir()
        has_android = (self.project_path / 'android').is_dir()
        has_ios = (self.project_path / 'ios').is_dir()
        has_test = (self.project_path / 'test').is_dir()

        if has_lib:
            confidence += 0.15
            indicators.append("lib/ directory: +0.15")
        if has_android and has_ios:
            confidence += 0.1
            indicators.append("android/ and ios/ directories: +0.1")
        elif has_android or has_ios:
            confidence += 0.05
            indicators.append("platform directory exists: +0.05")

        # Check for main.dart
        main_dart = self.project_path / 'lib' / 'main.dart'
        if main_dart.exists():
            confidence += 0.1
            indicators.append("lib/main.dart exists: +0.1")

            # Check for Flutter widgets in main.dart
            try:
                with open(main_dart, 'r', encoding='utf-8') as f:
                    content = f.read()
                    flutter_patterns = ['import \'package:flutter', 'MaterialApp', 'StatelessWidget', 'StatefulWidget', 'runApp']

                    for pattern in flutter_patterns:
                        if pattern in content:
                            confidence += 0.02
                            indicators.append(f"Flutter pattern '{pattern}' in main.dart: +0.02")
                            break

            except (UnicodeDecodeError, PermissionError):
                pass

        # Check for Dart files with Flutter imports
        dart_files = list(self.project_path.glob("lib/**/*.dart"))

        flutter_widget_count = 0
        for dart_file in dart_files[:10]:
            try:
                with open(dart_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'import \'package:flutter' in content or 'import "package:flutter' in content:
                        flutter_widget_count += 1

            except (UnicodeDecodeError, PermissionError):
                continue

        if flutter_widget_count > 0:
            confidence += 0.05
            indicators.append(f"{flutter_widget_count} files with Flutter imports: +0.05")

        # Minimum confidence threshold
        if confidence < 0.6:
            return None

        # Recommended subagents
        recommended_subagents = ['flutter-developer', 'widget-reviewer']

        if tools.get('state-management'):
            if 'provider' in tools['state-management']:
                recommended_subagents.append('provider-specialist')
            elif 'riverpod' in tools['state-management']:
                recommended_subagents.append('riverpod-specialist')
            elif 'bloc' in tools['state-management']:
                recommended_subagents.append('bloc-specialist')

        if 'flutter_test' in tools.get('testing', []):
            recommended_subagents.append('flutter-tester')

        if tools.get('database'):
            if 'sqflite' in tools['database']:
                recommended_subagents.append('sqflite-specialist')
            elif 'hive' in tools['database']:
                recommended_subagents.append('hive-specialist')

        # Project structure
        project_structure = {
            'has_lib': has_lib,
            'has_android': has_android,
            'has_ios': has_ios,
            'has_test': has_test,
            'has_main_dart': main_dart.exists(),
            'dart_files_count': len(dart_files)
        }

        return DetectionResult(
            framework="flutter",
            version=version,
            language="dart",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
        )

    def _detect_vanilla_php_web(self) -> Optional[DetectionResult]:
        """
        Detect vanilla PHP/JavaScript web applications.
        
        Identifies custom PHP applications without major frameworks
        (Laravel, Symfony, CodeIgniter, CakePHP).
        
        Detection criteria:
        - composer.json WITHOUT major framework dependencies
        - Multiple root-level *.php files
        - Custom routing (index.php with FastRoute or manual routing)
        - Custom MVC structure (src/app/ or app/)
        - .htaccess with custom rewrite rules
        - Testing tools: Playwright, Codeception, PHPUnit
        
        Returns:
            DetectionResult if PHP web app detected, None otherwise
        """
        indicators = []
        confidence = 0.0
        tools = {}
        version = None
        language = "php"
        
        # Check for composer.json
        composer_file = self.project_path / "composer.json"
        if not composer_file.exists():
            # No composer - check for raw PHP files
            root_php_files = list(self.project_path.glob("*.php"))
            if len(root_php_files) >= 3:
                # Likely a very simple PHP project
                confidence += 0.3
                indicators.append(f"{len(root_php_files)} root-level PHP files (no Composer)")
            else:
                return None
        else:
            indicators.append("composer.json exists: +0.1")
            confidence += 0.1
            
            try:
                composer_data = json.load(open(composer_file))
                requires = composer_data.get('require', {})
                
                # NEGATIVE CHECK: Major frameworks (immediately disqualify)
                framework_packages = {
                    'laravel/framework': 'Laravel',
                    'symfony/framework-bundle': 'Symfony',
                    'codeigniter4/framework': 'CodeIgniter',
                    'cakephp/cakephp': 'CakePHP',
                    'yiisoft/yii2': 'Yii2'
                }
                
                for pkg, fw_name in framework_packages.items():
                    if pkg in requires or pkg in composer_data.get('require-dev', {}):
                        logger.info(f"Found {fw_name} package - not vanilla PHP")
                        return None
                
                # POSITIVE: PHP version requirement
                if 'php' in requires:
                    php_version = requires['php'].lstrip('^~>=<')
                    version = php_version
                    indicators.append(f"PHP {php_version} required: +0.1")
                    confidence += 0.1
                
                # BONUS: Minimal dependencies (indicates custom app)
                total_deps = len(requires) + len(composer_data.get('require-dev', {}))
                if total_deps < 10:
                    indicators.append(f"minimal dependencies ({total_deps}): +0.1")
                    confidence += 0.1
                elif total_deps < 20:
                    indicators.append(f"moderate dependencies ({total_deps}): +0.05")
                    confidence += 0.05
                    
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not parse composer.json: {e}")
                return None
        
        # Check for root-level PHP files
        root_php_files = list(self.project_path.glob("*.php"))
        num_root_php = len(root_php_files)

        if num_root_php >= 10:
            indicators.append(f"{num_root_php} root-level PHP files: +0.2")
            confidence += 0.2
        elif num_root_php >= 5:
            indicators.append(f"{num_root_php} root-level PHP files: +0.15")
            confidence += 0.15
        elif num_root_php >= 2:
            # Lowered threshold: even 2 PHP files can indicate a simple PHP project
            indicators.append(f"{num_root_php} root-level PHP files: +0.1")
            confidence += 0.1
        elif num_root_php >= 1 and composer_file.exists():
            # If has composer.json + at least 1 PHP file, likely a PHP project
            indicators.append(f"{num_root_php} PHP file with composer.json: +0.05")
            confidence += 0.05
        else:
            # Too few PHP files
            return None
        
        # Check for index.php with routing logic
        index_php = self.project_path / "index.php"
        if index_php.exists():
            try:
                content = index_php.read_text(encoding='utf-8', errors='ignore')
                routing_indicators = ['FastRoute', 'Dispatcher', 'REQUEST_URI', '$_SERVER', 'routes']
                
                found_routing = [r for r in routing_indicators if r in content]
                if found_routing:
                    indicators.append(f"index.php with custom routing ({', '.join(found_routing)}): +0.15")
                    confidence += 0.15
                else:
                    indicators.append("index.php exists: +0.05")
                    confidence += 0.05
            except IOError:
                pass
        
        # Check for custom MVC structure
        mvc_structures = [
            self.project_path / "src" / "app",
            self.project_path / "app",
            self.project_path / "application"
        ]
        
        for mvc_dir in mvc_structures:
            if mvc_dir.exists():
                has_controllers = (mvc_dir / "Controllers").exists() or (mvc_dir / "controllers").exists()
                has_views = (mvc_dir / "Views").exists() or (mvc_dir / "views").exists()
                has_models = (
                    (mvc_dir / "Models").exists() or 
                    (mvc_dir / "models").exists() or
                    (mvc_dir / "Repositories").exists()
                )
                
                if has_controllers and has_views:
                    indicators.append("custom MVC structure: +0.15")
                    confidence += 0.15
                    break
                elif has_controllers or has_views:
                    indicators.append("partial MVC structure: +0.05")
                    confidence += 0.05
                    break
        
        # Check for .htaccess with custom rules
        htaccess = self.project_path / ".htaccess"
        if htaccess.exists():
            try:
                content = htaccess.read_text(encoding='utf-8', errors='ignore')
                if 'RewriteEngine' in content and 'index.php' in content:
                    indicators.append(".htaccess with custom rewrite rules: +0.05")
                    confidence += 0.05
            except IOError:
                pass
        
        # Check for custom bootstrap.php
        for bootstrap_file in self.project_path.rglob("bootstrap.php"):
            if 'vendor' not in str(bootstrap_file):
                try:
                    content = bootstrap_file.read_text(encoding='utf-8', errors='ignore')
                    if 'require' in content and ('config' in content or 'autoload' in content):
                        indicators.append("custom bootstrap.php: +0.05")
                        confidence += 0.05
                        break
                except IOError:
                    pass
        
        # Detect language (PHP vs PHP + TypeScript)
        if (self.project_path / "tsconfig.json").exists():
            language = "php-typescript"
        elif list(self.project_path.glob("**/*.ts")):
            language = "php-typescript"
        
        # Testing frameworks detection
        testing_frameworks = []
        
        # Playwright
        if (self.project_path / "playwright.config.js").exists() or \
           (self.project_path / "playwright.config.ts").exists():
            testing_frameworks.append("playwright")
            indicators.append("Playwright E2E testing: +0.05")
            confidence += 0.05
        
        # Codeception
        if (self.project_path / "codeception.yml").exists():
            testing_frameworks.append("codeception")
            indicators.append("Codeception testing: +0.05")
            confidence += 0.05
        
        # PHPUnit
        phpunit_configs = [
            self.project_path / "phpunit.xml",
            self.project_path / "phpunit.xml.dist"
        ]
        for phpunit_config in phpunit_configs:
            if phpunit_config.exists():
                testing_frameworks.append("phpunit")
                indicators.append("PHPUnit testing: +0.05")
                confidence += 0.05
                break
        
        if testing_frameworks:
            tools['testing'] = testing_frameworks
        
        # Database detection
        env_file = self.project_path / ".env"
        if env_file.exists():
            try:
                env_content = env_file.read_text(encoding='utf-8', errors='ignore')
                if 'DB_HOST' in env_content or 'DATABASE_URL' in env_content:
                    if 'mysql' in env_content.lower():
                        tools['database'] = ['mysql']
                    elif 'postgres' in env_content.lower():
                        tools['database'] = ['postgresql']
                    elif 'sqlite' in env_content.lower():
                        tools['database'] = ['sqlite']
            except IOError:
                pass
        
        # Frontend detection
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                pkg_data = json.load(open(package_json))
                deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                
                # Check for modern JS frameworks (disqualifies as "vanilla")
                modern_frameworks = ['react', 'vue', '@vue/cli', 'angular', '@angular/core', 'next', 'nuxt', 'svelte']
                if any(fw in deps for fw in modern_frameworks):
                    # Has modern framework - reduce confidence slightly
                    confidence -= 0.1
                    indicators.append("modern JS framework detected: -0.1")
                else:
                    tools['frontend'] = ['vanilla-js']
            except (json.JSONDecodeError, IOError):
                pass
        else:
            tools['frontend'] = ['vanilla-js']
        
        # Docker detection
        if (self.project_path / "docker-compose.yml").exists() or \
           (self.project_path / "Dockerfile").exists():
            tools['containerization'] = ['docker']
        
        # Minimum confidence threshold
        if confidence < 0.3:
            return None
        
        # Recommended subagents based on detected components
        recommended_subagents = ['php-developer']
        
        if 'playwright' in testing_frameworks:
            recommended_subagents.append('playwright-tester')
        if 'codeception' in testing_frameworks:
            recommended_subagents.append('codeception-tester')
        if 'phpunit' in testing_frameworks:
            recommended_subagents.append('phpunit-tester')
        
        if tools.get('frontend') == ['vanilla-js']:
            recommended_subagents.append('vanilla-js-developer')
        
        if 'mysql' in tools.get('database', []):
            recommended_subagents.append('mysql-specialist')
        elif 'postgresql' in tools.get('database', []):
            recommended_subagents.append('postgresql-specialist')
        
        if 'docker' in tools.get('containerization', []):
            recommended_subagents.append('docker-specialist')
        
        # Project structure information
        project_structure = {
            'has_composer': composer_file.exists(),
            'has_mvc_structure': any((mvc_dir.exists() for mvc_dir in mvc_structures)),
            'has_htaccess': htaccess.exists(),
            'has_docker': 'docker' in tools.get('containerization', []),
            'root_php_files': num_root_php
        }
        
        return DetectionResult(
            framework="vanilla-php-web",
            version=version,
            language=language,
            confidence=min(1.0, confidence),  # Cap at 1.0
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
        )

    def _detect_python_ml(self) -> Optional[DetectionResult]:
        """
        Detect Python ML/Data Science/Image Processing projects.
        
        Detection criteria:
        - requirements.txt or environment.yml with ML libraries
        - Python files with ML/CV imports (numpy, pandas, sklearn, torch, tensorflow, opencv)
        - Jupyter notebooks (.ipynb files)
        - Common ML project structure (data/, models/, notebooks/)
        
        Returns:
            DetectionResult if Python ML project detected, None otherwise
        """
        # Check for Python project files
        has_requirements = (self.project_path / "requirements.txt").exists()
        has_pyproject = (self.project_path / "pyproject.toml").exists()
        has_conda_env = (self.project_path / "environment.yml").exists()
        
        if not (has_requirements or has_pyproject or has_conda_env):
            return None

        confidence = 0.0
        indicators = []
        tools = {}
        ml_type = None  # 'general-ml', 'deep-learning', 'computer-vision', 'nlp'
        
        # ML/DS library keywords with categories
        ml_libraries = {
            'general': ['numpy', 'pandas', 'scikit-learn', 'sklearn', 'scipy', 'matplotlib', 'seaborn'],
            'deep-learning': ['tensorflow', 'keras', 'torch', 'pytorch', 'jax', 'mxnet'],
            'computer-vision': ['opencv', 'cv2', 'pillow', 'pil', 'scikit-image', 'skimage', 'albumentations'],
            'nlp': ['nltk', 'spacy', 'transformers', 'huggingface', 'gensim', 'wordcloud'],
            'tools': ['jupyter', 'notebook', 'jupyterlab', 'mlflow', 'wandb', 'tensorboard']
        }
        
        detected_categories = {cat: [] for cat in ml_libraries.keys()}
        
        # Check requirements.txt
        requirements_file = self.project_path / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    requirements = f.read().lower()
                    
                    for category, libs in ml_libraries.items():
                        for lib in libs:
                            if lib in requirements:
                                detected_categories[category].append(lib)
                                
            except UnicodeDecodeError:
                pass
        
        # Check environment.yml
        env_file = self.project_path / "environment.yml"
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    env_content = f.read().lower()
                    
                    for category, libs in ml_libraries.items():
                        for lib in libs:
                            if lib in env_content:
                                detected_categories[category].append(lib)
                                
            except UnicodeDecodeError:
                pass
        
        # Calculate confidence based on detected libraries
        if detected_categories['general']:
            confidence += 0.3
            indicators.append(f"General ML libraries: {', '.join(set(detected_categories['general']))}: +0.3")
            tools['ml-general'] = list(set(detected_categories['general']))
        
        if detected_categories['deep-learning']:
            confidence += 0.25
            indicators.append(f"Deep learning libraries: {', '.join(set(detected_categories['deep-learning']))}: +0.25")
            tools['deep-learning'] = list(set(detected_categories['deep-learning']))
            ml_type = 'deep-learning'
        
        if detected_categories['computer-vision']:
            confidence += 0.2
            indicators.append(f"Computer vision libraries: {', '.join(set(detected_categories['computer-vision']))}: +0.2")
            tools['computer-vision'] = list(set(detected_categories['computer-vision']))
            if not ml_type:
                ml_type = 'computer-vision'
        
        if detected_categories['nlp']:
            confidence += 0.2
            indicators.append(f"NLP libraries: {', '.join(set(detected_categories['nlp']))}: +0.2")
            tools['nlp'] = list(set(detected_categories['nlp']))
            if not ml_type:
                ml_type = 'nlp'
        
        if detected_categories['tools']:
            tools['ml-tools'] = list(set(detected_categories['tools']))
        
        # If no ML type determined yet, set as general
        if not ml_type and detected_categories['general']:
            ml_type = 'general-ml'
        
        # Check for Jupyter notebooks
        notebooks = list(self.project_path.glob("*.ipynb"))
        notebooks.extend(list(self.project_path.glob("notebooks/**/*.ipynb")))
        notebooks.extend(list(self.project_path.glob("**/*.ipynb")))
        
        num_notebooks = len([nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)])
        
        if num_notebooks > 0:
            confidence += 0.15
            indicators.append(f"{num_notebooks} Jupyter notebooks: +0.15")
            tools.setdefault('ml-tools', []).append('jupyter')
        
        # Check for Python files with ML imports
        python_files = list(self.project_path.glob("*.py"))
        python_files.extend(list(self.project_path.glob("src/**/*.py")))
        python_files.extend(list(self.project_path.glob("scripts/**/*.py")))
        
        ml_import_patterns = [
            'import numpy',
            'import pandas',
            'import torch',
            'import tensorflow',
            'from sklearn',
            'import cv2',
            'from PIL import'
        ]
        
        for py_file in python_files[:15]:
            if 'venv' in str(py_file) or '.venv' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for pattern in ml_import_patterns:
                        if pattern in content:
                            confidence += 0.05
                            indicators.append(f"ML import '{pattern}' in {py_file.name}: +0.05")
                            break
                            
            except (UnicodeDecodeError, PermissionError):
                continue
        
        # Check for common ML project directories
        ml_directories = {
            'data': self.project_path / 'data',
            'datasets': self.project_path / 'datasets',
            'models': self.project_path / 'models',
            'notebooks': self.project_path / 'notebooks',
            'experiments': self.project_path / 'experiments',
            'checkpoints': self.project_path / 'checkpoints'
        }
        
        found_dirs = [name for name, path in ml_directories.items() if path.exists()]
        if found_dirs:
            confidence += 0.1
            indicators.append(f"ML project directories: {', '.join(found_dirs)}: +0.1")
        
        # Minimum confidence threshold
        if confidence < 0.3:
            return None
        
        # Determine recommended subagents
        recommended_subagents = ['python-ml-developer']
        
        if 'jupyter' in tools.get('ml-tools', []):
            recommended_subagents.append('notebook-specialist')
        
        if tools.get('deep-learning'):
            if 'torch' in tools['deep-learning'] or 'pytorch' in tools['deep-learning']:
                recommended_subagents.append('pytorch-specialist')
            if 'tensorflow' in tools['deep-learning']:
                recommended_subagents.append('tensorflow-specialist')
        
        if tools.get('computer-vision'):
            recommended_subagents.append('cv-specialist')
        
        if tools.get('nlp'):
            recommended_subagents.append('nlp-specialist')
        
        if 'pandas' in tools.get('ml-general', []):
            recommended_subagents.append('data-analyst')
        
        # Project structure
        project_structure = {
            'has_notebooks': num_notebooks > 0,
            'has_data_dir': (self.project_path / 'data').exists(),
            'has_models_dir': (self.project_path / 'models').exists(),
            'has_conda_env': has_conda_env,
            'ml_type': ml_type
        }
        
        return DetectionResult(
            framework="python-ml",
            version=None,
            language="python",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
        )

    def _detect_ios_swift(self) -> Optional[DetectionResult]:
        """
        Detect iOS Swift projects.
        
        Detection criteria:
        - Xcode project files (.xcodeproj, .xcworkspace)
        - Swift source files (.swift)
        - Info.plist, Podfile, Package.swift
        - Common iOS frameworks (UIKit, SwiftUI)
        
        Returns:
            DetectionResult if iOS Swift project detected, None otherwise
        """
        confidence = 0.0
        indicators = []
        tools = {}
        ui_framework = None
        
        # Check for Xcode project files
        xcodeproj = list(self.project_path.glob("*.xcodeproj"))
        xcworkspace = list(self.project_path.glob("*.xcworkspace"))
        
        if xcodeproj:
            confidence += 0.4
            indicators.append(f".xcodeproj found: +0.4")
        
        if xcworkspace:
            confidence += 0.2
            indicators.append(f".xcworkspace found: +0.2")
        
        if not xcodeproj and not xcworkspace:
            return None
        
        # Check for Swift files
        swift_files = list(self.project_path.glob("**/*.swift"))
        swift_files = [f for f in swift_files if 'Pods' not in str(f) and '.build' not in str(f)]
        
        num_swift_files = len(swift_files)
        if num_swift_files > 0:
            confidence += 0.3
            indicators.append(f"{num_swift_files} Swift files: +0.3")
        else:
            # Might be Objective-C project
            return None
        
        # Check for SwiftUI vs UIKit
        swiftui_patterns = ['import SwiftUI', 'struct.*: View', '@State', '@Binding', '@ObservedObject']
        uikit_patterns = ['import UIKit', 'class.*: UIViewController', 'UIView', 'UITableView']
        
        swiftui_count = 0
        uikit_count = 0
        
        for swift_file in swift_files[:20]:  # Check first 20 files
            try:
                content = swift_file.read_text(encoding='utf-8', errors='ignore')
                
                if any(pattern in content for pattern in swiftui_patterns):
                    swiftui_count += 1
                if any(pattern in content for pattern in uikit_patterns):
                    uikit_count += 1
                    
            except (IOError, PermissionError):
                continue
        
        if swiftui_count > uikit_count:
            ui_framework = 'swiftui'
            tools['ui-framework'] = ['swiftui']
            indicators.append(f"SwiftUI detected in {swiftui_count} files")
        elif uikit_count > 0:
            ui_framework = 'uikit'
            tools['ui-framework'] = ['uikit']
            indicators.append(f"UIKit detected in {uikit_count} files")
        
        # Check for CocoaPods
        if (self.project_path / "Podfile").exists():
            tools['dependency-manager'] = ['cocoapods']
            confidence += 0.05
            indicators.append("CocoaPods (Podfile): +0.05")
        
        # Check for Swift Package Manager
        if (self.project_path / "Package.swift").exists():
            tools.setdefault('dependency-manager', []).append('spm')
            confidence += 0.05
            indicators.append("Swift Package Manager: +0.05")
        
        # Check for Info.plist
        info_plist = list(self.project_path.glob("**/Info.plist"))
        if info_plist:
            confidence += 0.05
            indicators.append("Info.plist found: +0.05")
        
        # Check for testing frameworks
        if any('Test' in str(f) or 'Spec' in str(f) for f in swift_files):
            tools['testing'] = ['xctest']
        
        # Detect app type
        app_type = 'ios-app'
        
        # Minimum confidence threshold
        if confidence < 0.5:
            return None
        
        # Recommended subagents
        recommended_subagents = ['swift-developer']
        
        if ui_framework == 'swiftui':
            recommended_subagents.append('swiftui-specialist')
        elif ui_framework == 'uikit':
            recommended_subagents.append('uikit-specialist')
        
        if 'xctest' in tools.get('testing', []):
            recommended_subagents.append('xctest-specialist')
        
        # Project structure
        project_structure = {
            'has_xcodeproj': len(xcodeproj) > 0,
            'has_xcworkspace': len(xcworkspace) > 0,
            'swift_files_count': num_swift_files,
            'ui_framework': ui_framework,
            'app_type': app_type
        }
        
        return DetectionResult(
            framework="ios-swift",
            version=None,
            language="swift",
            confidence=min(confidence, 1.0),
            indicators=indicators,
            tools=tools,
            recommended_subagents=recommended_subagents,
            project_structure=project_structure
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
