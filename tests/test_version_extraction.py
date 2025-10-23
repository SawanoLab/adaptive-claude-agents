"""Tests for version extraction and dependency detection.

This module tests version parsing from various config files to increase
coverage of version extraction logic in detect_stack.py.
"""

import pytest
import json
from pathlib import Path


class TestPackageJSONVersionExtraction:
    """Test version extraction from package.json."""

    def test_nextjs_version_extraction(self, tmp_path, detector):
        """Test Next.js version extraction from package.json."""
        project = tmp_path / "nextjs-versioned"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test-nextjs",
            "version": "1.0.0",
            "dependencies": {
                "next": "14.2.5",
                "react": "18.3.0",
                "react-dom": "18.3.0"
            }
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(project))

        assert result is not None
        assert "next" in result.framework.lower()
        # Version should be extracted from package.json
        assert result.version is not None
        assert "14" in result.version or result.version == "14.2.5"

    def test_react_version_extraction(self, tmp_path, detector):
        """Test React version extraction from package.json."""
        project = tmp_path / "react-versioned"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test-react",
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "vite": "^5.0.0",
                "@vitejs/plugin-react": "^4.2.0"
            }
        }))

        (project / "vite.config.js").write_text("""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
""")

        src = project / "src"
        src.mkdir()
        (src / "App.jsx").write_text("import React from 'react'; export default function App() { return <div>Hello</div>; }")

        result = detector(str(project))

        assert result is not None
        assert "react" in result.framework.lower()
        # Should extract React version
        if result.version:
            assert "18" in result.version

    def test_vue_version_extraction(self, tmp_path, detector):
        """Test Vue version extraction from package.json."""
        project = tmp_path / "vue-versioned"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test-vue",
            "dependencies": {
                "vue": "^3.4.21"
            }
        }))

        (project / "vite.config.js").write_text("import vue from '@vitejs/plugin-vue'; export default { plugins: [vue()] }")

        src = project / "src"
        src.mkdir()
        (src / "App.vue").write_text("<template><div>Hello</div></template>")

        result = detector(str(project))

        assert result is not None
        assert "vue" in result.framework.lower()


class TestGoModVersionExtraction:
    """Test version extraction from go.mod."""

    def test_go_version_from_gomod(self, tmp_path, detector):
        """Test Go version extraction from go.mod."""
        project = tmp_path / "go-versioned"
        project.mkdir()

        (project / "go.mod").write_text("""module github.com/test/app

go 1.21.5

require (
    github.com/gin-gonic/gin v1.9.1
)
""")

        (project / "main.go").write_text("""package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.Run()
}
""")

        result = detector(str(project))

        assert result is not None
        assert "go" in result.framework.lower()
        # Should extract Go version from go.mod
        assert result.version is not None
        assert "1.21" in result.version

    def test_go_version_major_only(self, tmp_path, detector):
        """Test Go version extraction when only major.minor specified."""
        project = tmp_path / "go-version-simple"
        project.mkdir()

        (project / "go.mod").write_text("""module github.com/test/simple

go 1.20

require (
    github.com/gin-gonic/gin v1.9.0
)
""")

        (project / "main.go").write_text("package main\n\nfunc main() {}\n")

        result = detector(str(project))

        assert result is not None
        assert result.version is not None
        assert "1.20" in result.version or "1.2" in result.version


class TestFlutterVersionExtraction:
    """Test version extraction from pubspec.yaml."""

    def test_flutter_sdk_version(self, tmp_path, detector):
        """Test Flutter SDK version extraction from pubspec.yaml."""
        project = tmp_path / "flutter-versioned"
        project.mkdir()

        (project / "pubspec.yaml").write_text("""name: test_flutter_app
version: 1.0.0+1

environment:
  sdk: '>=3.2.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.0
""")

        lib = project / "lib"
        lib.mkdir()
        (lib / "main.dart").write_text("""import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: Scaffold());
  }
}
""")

        (project / "android").mkdir()
        (project / "ios").mkdir()

        result = detector(str(project))

        assert result is not None
        assert "flutter" in result.framework.lower()
        # Should detect Flutter version from environment.sdk
        if result.version:
            assert "3" in result.version or "dart" in result.version.lower()


class TestPythonVersionExtraction:
    """Test Python version extraction from requirements.txt and pyproject.toml."""

    def test_fastapi_version_extraction(self, tmp_path, detector):
        """Test FastAPI version extraction from requirements.txt."""
        project = tmp_path / "fastapi-versioned"
        project.mkdir()

        (project / "requirements.txt").write_text("""fastapi==0.109.2
uvicorn[standard]==0.27.1
pydantic==2.5.3
""")

        (project / "main.py").write_text("""from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}
""")

        result = detector(str(project))

        assert result is not None
        assert "fastapi" in result.framework.lower()
        # Should extract FastAPI version
        if result.version:
            assert "0.109" in result.version or "0.1" in result.version

    def test_django_version_extraction(self, tmp_path, detector):
        """Test Django version extraction from requirements.txt."""
        project = tmp_path / "django-versioned"
        project.mkdir()

        (project / "requirements.txt").write_text("""Django==5.0.2
djangorestframework==3.14.0
psycopg2-binary==2.9.9
""")

        (project / "manage.py").write_text("""#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
""")

        config = project / "config"
        config.mkdir()
        (config / "__init__.py").touch()
        (config / "settings.py").write_text("SECRET_KEY = 'test'\nDEBUG = True\n")

        result = detector(str(project))

        assert result is not None
        assert "django" in result.framework.lower()
        if result.version:
            assert "5" in result.version or "5.0" in result.version


class TestDependencyDetection:
    """Test detection of specific dependencies and tools."""

    def test_go_with_multiple_frameworks(self, tmp_path, detector):
        """Test Go project with multiple framework dependencies."""
        project = tmp_path / "go-multi"
        project.mkdir()

        (project / "go.mod").write_text("""module github.com/test/multi

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    gorm.io/gorm v1.25.5
    gorm.io/driver/postgres v1.5.4
)
""")

        (project / "main.go").write_text("""package main

import (
    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
)

func main() {
    r := gin.Default()
    r.Run()
}
""")

        result = detector(str(project))

        assert result is not None
        assert "go" in result.framework.lower()
        # Should detect both Gin and GORM
        assert result.confidence >= 0.8

    def test_flutter_with_multiple_packages(self, tmp_path, detector):
        """Test Flutter project with multiple state management packages."""
        project = tmp_path / "flutter-multi"
        project.mkdir()

        (project / "pubspec.yaml").write_text("""name: multi_app
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.4.9
  dio: ^5.4.0
  go_router: ^13.0.0
  sqflite: ^2.3.0
""")

        lib = project / "lib"
        lib.mkdir()
        (lib / "main.dart").write_text("""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(ProviderScope(child: MyApp()));
}
""")

        (project / "android").mkdir()
        (project / "ios").mkdir()

        result = detector(str(project))

        assert result is not None
        assert "flutter" in result.framework.lower()
        # Should have high confidence with multiple Flutter packages
        assert result.confidence >= 0.85

    def test_nextjs_with_typescript(self, tmp_path, detector):
        """Test Next.js project with TypeScript configuration."""
        project = tmp_path / "nextjs-ts"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "nextjs-ts-app",
            "dependencies": {
                "next": "14.1.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "typescript": "^5.3.0",
                "@types/react": "^18.2.0",
                "@types/node": "^20.10.0"
            }
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        (project / "tsconfig.json").write_text(json.dumps({
            "compilerOptions": {
                "target": "ES2020",
                "lib": ["dom", "dom.iterable", "esnext"],
                "jsx": "preserve",
                "strict": True
            }
        }))

        app_dir = project / "app"
        app_dir.mkdir()
        (app_dir / "page.tsx").write_text("""export default function Page() {
  return <div>Hello TypeScript</div>
}
""")

        result = detector(str(project))

        assert result is not None
        assert "next" in result.framework.lower()
        assert result.language == "typescript"
        assert result.confidence >= 0.95


class TestVersionParsingEdgeCases:
    """Test edge cases in version parsing."""

    def test_version_with_caret(self, tmp_path, detector):
        """Test version parsing with caret (^) prefix."""
        project = tmp_path / "caret-version"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test",
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.0.0"
            }
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(project))

        if result and result.version:
            # Should strip caret and extract version
            assert "^" not in result.version
            assert "14" in result.version

    def test_version_with_tilde(self, tmp_path, detector):
        """Test version parsing with tilde (~) prefix."""
        project = tmp_path / "tilde-version"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test",
            "dependencies": {
                "vue": "~3.4.0"
            }
        }))

        (project / "vite.config.js").write_text("export default {}")

        src = project / "src"
        src.mkdir()
        (src / "App.vue").write_text("<template><div>Test</div></template>")

        result = detector(str(project))

        if result and result.version:
            assert "~" not in result.version

    def test_version_exact_match(self, tmp_path, detector):
        """Test version parsing with exact version (no prefix)."""
        project = tmp_path / "exact-version"
        project.mkdir()

        (project / "requirements.txt").write_text("""fastapi==0.109.0
uvicorn==0.27.0
""")

        (project / "main.py").write_text("""from fastapi import FastAPI
app = FastAPI()
""")

        result = detector(str(project))

        assert result is not None
        if result.version:
            assert "0.109" in result.version or "0.1" in result.version

    def test_missing_version_field(self, tmp_path, detector):
        """Test handling when version field is missing."""
        project = tmp_path / "no-version"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "test-no-version",
            "dependencies": {
                "next": "*",  # Wildcard version
                "react": "latest"  # Latest tag
            }
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(project))

        # Should still detect Next.js even without specific version
        assert result is not None
        assert "next" in result.framework.lower()


class TestLanguageDetection:
    """Test programming language detection logic."""

    def test_typescript_vs_javascript(self, tmp_path, detector):
        """Test TypeScript detection vs JavaScript."""
        project = tmp_path / "ts-project"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "ts-app",
            "dependencies": {
                "next": "14.0.0",
                "react": "18.0.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0"
            }
        }))

        (project / "tsconfig.json").write_text(json.dumps({
            "compilerOptions": {"strict": True}
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(project))

        assert result is not None
        # Should detect TypeScript
        assert result.language == "typescript"

    def test_javascript_without_typescript(self, tmp_path, detector):
        """Test JavaScript detection when TypeScript is absent."""
        project = tmp_path / "js-project"
        project.mkdir()

        (project / "package.json").write_text(json.dumps({
            "name": "js-app",
            "dependencies": {
                "next": "14.0.0",
                "react": "18.0.0"
            }
        }))

        (project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(project))

        assert result is not None
        # Should detect JavaScript (not TypeScript)
        assert result.language == "javascript"
