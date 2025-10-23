"""
pytest configuration and shared fixtures for Adaptive Claude Agents tests.

This module provides:
- Temporary project fixtures for all supported frameworks
- Common test utilities
- pytest configuration
"""

import pytest
import json
from pathlib import Path
from typing import Dict, Any


# ============================================================================
# pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "benchmark: marks performance benchmark tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks end-to-end integration tests"
    )


# ============================================================================
# Utility Functions
# ============================================================================

def create_package_json(project: Path, name: str, dependencies: Dict[str, str]) -> Path:
    """Create package.json for Node.js projects."""
    package_json = {
        "name": name,
        "version": "1.0.0",
        "dependencies": dependencies
    }
    path = project / "package.json"
    path.write_text(json.dumps(package_json, indent=2))
    return path


def create_requirements_txt(project: Path, dependencies: list[str]) -> Path:
    """Create requirements.txt for Python projects."""
    path = project / "requirements.txt"
    path.write_text("\n".join(dependencies))
    return path


def create_go_mod(project: Path, module_name: str, dependencies: Dict[str, str]) -> Path:
    """Create go.mod for Go projects."""
    go_mod_content = f"module {module_name}\n\ngo 1.21\n\nrequire (\n"
    for pkg, version in dependencies.items():
        go_mod_content += f"\t{pkg} {version}\n"
    go_mod_content += ")\n"

    path = project / "go.mod"
    path.write_text(go_mod_content)
    return path


def create_pubspec_yaml(project: Path, name: str, dependencies: Dict[str, str]) -> Path:
    """Create pubspec.yaml for Flutter projects."""
    pubspec_content = f"""name: {name}
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
"""
    for pkg, version in dependencies.items():
        pubspec_content += f"  {pkg}: {version}\n"

    path = project / "pubspec.yaml"
    path.write_text(pubspec_content)
    return path


# ============================================================================
# Next.js Fixtures
# ============================================================================

@pytest.fixture
def nextjs_project(tmp_path):
    """Create minimal Next.js project for testing."""
    project = tmp_path / "nextjs-demo"
    project.mkdir()

    # package.json
    create_package_json(project, "test-nextjs", {
        "next": "14.2.0",
        "react": "18.2.0",
        "react-dom": "18.2.0"
    })

    # next.config.js
    (project / "next.config.js").write_text("module.exports = {}\n")

    # tsconfig.json
    (project / "tsconfig.json").write_text(json.dumps({
        "compilerOptions": {
            "target": "ES2020",
            "lib": ["dom", "dom.iterable", "esnext"],
            "jsx": "preserve"
        }
    }, indent=2))

    # app directory (App Router)
    app_dir = project / "app"
    app_dir.mkdir()
    (app_dir / "layout.tsx").write_text('''
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
''')

    return project


# ============================================================================
# FastAPI Fixtures
# ============================================================================

@pytest.fixture
def fastapi_project(tmp_path):
    """Create minimal FastAPI project for testing."""
    project = tmp_path / "fastapi-demo"
    project.mkdir()

    # main.py
    (project / "main.py").write_text('''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
''')

    # requirements.txt
    create_requirements_txt(project, [
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.5.0"
    ])

    # pyproject.toml (optional but common)
    (project / "pyproject.toml").write_text('''[project]
name = "test-fastapi"
version = "0.1.0"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0"
]
''')

    return project


# ============================================================================
# Go Fixtures
# ============================================================================

@pytest.fixture
def go_project(tmp_path):
    """Create minimal Go project for testing."""
    project = tmp_path / "go-demo"
    project.mkdir()

    # go.mod
    create_go_mod(project, "github.com/example/test-go", {
        "github.com/gin-gonic/gin": "v1.9.1"
    })

    # main.go
    (project / "main.go").write_text('''package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    r.Run()
}
''')

    return project


# ============================================================================
# Flutter Fixtures
# ============================================================================

@pytest.fixture
def flutter_project(tmp_path):
    """Create minimal Flutter project for testing."""
    project = tmp_path / "flutter-demo"
    project.mkdir()

    # pubspec.yaml
    create_pubspec_yaml(project, "test_flutter", {
        "flutter": {"sdk": "flutter"},
        "provider": "^6.1.0"
    })

    # lib directory
    lib_dir = project / "lib"
    lib_dir.mkdir()

    # main.dart
    (lib_dir / "main.dart").write_text('''import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: const MyHomePage(),
    );
  }
}
''')

    # Create android/ and ios/ directories (minimal)
    (project / "android").mkdir()
    (project / "ios").mkdir()

    return project


# ============================================================================
# React (Vite) Fixtures
# ============================================================================

@pytest.fixture
def react_project(tmp_path):
    """Create minimal React (Vite) project for testing."""
    project = tmp_path / "react-demo"
    project.mkdir()

    # package.json
    create_package_json(project, "test-react", {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    })

    # Add dev dependencies with vite
    package_json_path = project / "package.json"
    package_data = json.loads(package_json_path.read_text())
    package_data["devDependencies"] = {
        "vite": "^5.0.0",
        "@vitejs/plugin-react": "^4.2.0"
    }
    package_json_path.write_text(json.dumps(package_data, indent=2))

    # vite.config.js
    (project / "vite.config.js").write_text('''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
''')

    # src directory
    src_dir = project / "src"
    src_dir.mkdir()
    (src_dir / "main.jsx").write_text('''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''')

    return project


# ============================================================================
# Vue Fixtures
# ============================================================================

@pytest.fixture
def vue_project(tmp_path):
    """Create minimal Vue project for testing."""
    project = tmp_path / "vue-demo"
    project.mkdir()

    # package.json
    create_package_json(project, "test-vue", {
        "vue": "^3.4.0"
    })

    # vite.config.js
    (project / "vite.config.js").write_text('''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
''')

    # src directory
    src_dir = project / "src"
    src_dir.mkdir()
    (src_dir / "App.vue").write_text('''<template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      message: 'Hello Vue!'
    }
  }
}
</script>
''')

    return project


# ============================================================================
# Django Fixtures
# ============================================================================

@pytest.fixture
def django_project(tmp_path):
    """Create minimal Django project for testing."""
    project = tmp_path / "django-demo"
    project.mkdir()

    # requirements.txt
    create_requirements_txt(project, [
        "Django==5.0.0",
        "djangorestframework==3.14.0"
    ])

    # manage.py
    (project / "manage.py").write_text('''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
''')

    # project directory
    project_dir = project / "project"
    project_dir.mkdir()
    (project_dir / "__init__.py").touch()
    (project_dir / "settings.py").write_text('''
SECRET_KEY = 'test-secret-key'
DEBUG = True
INSTALLED_APPS = ['django.contrib.contenttypes']
''')

    return project


# ============================================================================
# Flask Fixtures
# ============================================================================

@pytest.fixture
def flask_project(tmp_path):
    """Create minimal Flask project for testing."""
    project = tmp_path / "flask-demo"
    project.mkdir()

    # requirements.txt
    create_requirements_txt(project, [
        "Flask==3.0.0",
        "python-dotenv==1.0.0"
    ])

    # app.py
    (project / "app.py").write_text('''from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello World'}

@app.route('/users/<int:user_id>')
def get_user(user_id):
    return {'user_id': user_id}

if __name__ == '__main__':
    app.run(debug=True)
''')

    return project


# ============================================================================
# Python ML/CV Fixtures
# ============================================================================

@pytest.fixture
def python_ml_project(tmp_path):
    """Create minimal Python ML/CV project for testing."""
    project = tmp_path / "python-ml-demo"
    project.mkdir()

    # requirements.txt
    create_requirements_txt(project, [
        "numpy==1.26.0",
        "pandas==2.1.0",
        "scikit-learn==1.3.0",
        "torch==2.1.0",
        "opencv-python==4.8.0"
    ])

    # train.py
    (project / "train.py").write_text('''import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)

if __name__ == '__main__':
    model = SimpleModel()
    print("Training model...")
''')

    # detect.py (CV)
    (project / "detect.py").write_text('''import cv2
import numpy as np

def detect_objects(image_path):
    img = cv2.imread(image_path)
    # Detection logic here
    return []
''')

    return project


# ============================================================================
# iOS Swift Fixtures
# ============================================================================

@pytest.fixture
def ios_swift_project(tmp_path):
    """Create minimal iOS Swift project for testing."""
    project = tmp_path / "ios-swift-demo"
    project.mkdir()

    # Package.swift (Swift Package Manager)
    (project / "Package.swift").write_text('''// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "TestiOSApp",
    platforms: [.iOS(.v15)],
    products: [
        .library(name: "TestiOSApp", targets: ["TestiOSApp"]),
    ],
    dependencies: [],
    targets: [
        .target(name: "TestiOSApp", dependencies: []),
    ]
)
''')

    # Sources directory
    sources_dir = project / "Sources" / "TestiOSApp"
    sources_dir.mkdir(parents=True)

    # ContentView.swift
    (sources_dir / "ContentView.swift").write_text('''import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
            .padding()
    }
}
''')

    return project


# ============================================================================
# Vanilla PHP Fixtures
# ============================================================================

@pytest.fixture
def php_project(tmp_path):
    """Create minimal Vanilla PHP project for testing."""
    project = tmp_path / "php-demo"
    project.mkdir()

    # composer.json
    (project / "composer.json").write_text(json.dumps({
        "name": "test/php-app",
        "type": "project",
        "require": {
            "php": ">=8.1"
        }
    }, indent=2))

    # index.php
    (project / "index.php").write_text('''<?php
header('Content-Type: application/json');

$data = [
    'message' => 'Hello World',
    'timestamp' => time()
];

echo json_encode($data);
?>
''')

    # .htaccess
    (project / ".htaccess").write_text('''RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [QSA,L]
''')

    return project


# ============================================================================
# Common Test Utilities
# ============================================================================

@pytest.fixture
def analyzer_factory():
    """Factory fixture for creating ProjectAnalyzer instances."""
    from skills.project_analyzer.analyze_project import ProjectAnalyzer

    def _create_analyzer(project_path: Path, auto_confirm: bool = True):
        return ProjectAnalyzer(project_path, auto_confirm=auto_confirm)

    return _create_analyzer


@pytest.fixture
def detector():
    """Fixture providing detect_tech_stack function."""
    import sys
    from pathlib import Path

    # Add skills directory to Python path
    skills_dir = Path(__file__).parent.parent / "skills" / "project-analyzer"
    if str(skills_dir) not in sys.path:
        sys.path.insert(0, str(skills_dir))

    from detect_stack import detect_tech_stack
    return detect_tech_stack
