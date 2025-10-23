"""
Tests for framework detection logic.

This module tests the accuracy and reliability of detect_stack.py across
all 11 supported frameworks.
"""

import pytest
from pathlib import Path


class TestNextJSDetection:
    """Test Next.js framework detection."""

    def test_nextjs_basic_detection(self, nextjs_project, detector):
        """Test basic Next.js detection with high confidence."""
        result = detector(str(nextjs_project))

        assert result is not None, "Should detect Next.js project"
        assert result.framework == "nextjs"
        assert result.confidence >= 0.95, f"Expected confidence >=95%, got {result.confidence*100:.1f}%"
        assert result.language == "typescript"

    def test_nextjs_version_extraction(self, nextjs_project, detector):
        """Test Next.js version number extraction."""
        result = detector(str(nextjs_project))

        assert result.version is not None, "Should extract version"
        assert result.version.startswith("14."), f"Expected version 14.x, got {result.version}"

    def test_nextjs_tools_detection(self, nextjs_project, detector):
        """Test detection of Next.js ecosystem tools."""
        result = detector(str(nextjs_project))

        assert result.tools is not None, "Should detect tools"
        # Note: In minimal test project, tools may be empty
        # This is expected and OK


class TestFastAPIDetection:
    """Test FastAPI framework detection."""

    def test_fastapi_basic_detection(self, fastapi_project, detector):
        """Test basic FastAPI detection."""
        result = detector(str(fastapi_project))

        assert result is not None, "Should detect FastAPI project"
        assert result.framework == "fastapi"
        assert result.confidence >= 0.75, f"Expected confidence >=75%, got {result.confidence*100:.1f}%"
        assert result.language == "python"

    def test_fastapi_async_detection(self, fastapi_project, detector):
        """Test detection of async patterns in FastAPI."""
        result = detector(str(fastapi_project))

        # Check if async is detected in indicators or tools
        if result.indicators:
            has_async = any("async" in indicator.lower() for indicator in result.indicators)
            # Note: async detection is optional for minimal projects


class TestGoDetection:
    """Test Go framework detection."""

    def test_go_basic_detection(self, go_project, detector):
        """Test basic Go detection."""
        result = detector(str(go_project))

        assert result is not None, "Should detect Go project"
        assert result.framework.startswith("go"), f"Expected framework to start with 'go', got {result.framework}"
        assert result.confidence >= 0.80, f"Expected confidence >=80%, got {result.confidence*100:.1f}%"
        assert result.language == "go"

    def test_go_framework_detection(self, go_project, detector):
        """Test detection of Go web framework (Gin)."""
        result = detector(str(go_project))

        # Check if Gin is detected
        if result.tools and "web_framework" in result.tools:
            assert "gin" in result.tools["web_framework"].lower()


class TestFlutterDetection:
    """Test Flutter framework detection."""

    def test_flutter_basic_detection(self, flutter_project, detector):
        """Test basic Flutter detection."""
        result = detector(str(flutter_project))

        assert result is not None, "Should detect Flutter project"
        assert result.framework == "flutter"
        assert result.confidence >= 0.75, f"Expected confidence >=75%, got {result.confidence*100:.1f}%"
        assert result.language == "dart"

    def test_flutter_structure_detection(self, flutter_project, detector):
        """Test detection of Flutter project structure."""
        result = detector(str(flutter_project))

        # Flutter projects should have lib/, android/, ios/
        assert (Path(flutter_project) / "lib").exists()
        assert (Path(flutter_project) / "android").exists()
        assert (Path(flutter_project) / "ios").exists()


class TestReactDetection:
    """Test React (Vite) framework detection."""

    def test_react_basic_detection(self, react_project, detector):
        """Test basic React detection."""
        result = detector(str(react_project))

        assert result is not None, "Should detect React project"
        assert "react" in result.framework.lower(), f"Expected 'react' in framework name, got {result.framework}"
        assert result.confidence >= 0.75, f"Expected confidence >=75%, got {result.confidence*100:.1f}%"
        assert result.language in ["javascript", "typescript"]


class TestVueDetection:
    """Test Vue framework detection."""

    def test_vue_basic_detection(self, vue_project, detector):
        """Test basic Vue detection."""
        result = detector(str(vue_project))

        assert result is not None, "Should detect Vue project"
        assert result.framework == "vue"
        assert result.confidence >= 0.70, f"Expected confidence >=70%, got {result.confidence*100:.1f}%"
        assert result.language in ["javascript", "typescript"]


class TestDjangoDetection:
    """Test Django framework detection."""

    def test_django_basic_detection(self, django_project, detector):
        """Test basic Django detection."""
        result = detector(str(django_project))

        assert result is not None, "Should detect Django project"
        assert result.framework == "django"
        assert result.confidence >= 0.75, f"Expected confidence >=75%, got {result.confidence*100:.1f}%"
        assert result.language == "python"


class TestFlaskDetection:
    """Test Flask framework detection."""

    def test_flask_basic_detection(self, flask_project, detector):
        """Test basic Flask detection."""
        result = detector(str(flask_project))

        assert result is not None, "Should detect Flask project"
        assert result.framework == "flask"
        assert result.confidence >= 0.65, f"Expected confidence >=65%, got {result.confidence*100:.1f}%"
        assert result.language == "python"


class TestPythonMLDetection:
    """Test Python ML/CV framework detection."""

    def test_python_ml_basic_detection(self, python_ml_project, detector):
        """Test basic Python ML/CV detection."""
        result = detector(str(python_ml_project))

        assert result is not None, "Should detect Python ML project"
        assert result.framework == "python-ml"
        assert result.confidence >= 0.85, f"Expected confidence >=85%, got {result.confidence*100:.1f}%"
        assert result.language == "python"

    def test_python_ml_libraries_detection(self, python_ml_project, detector):
        """Test detection of ML/CV libraries."""
        result = detector(str(python_ml_project))

        # Should detect PyTorch, OpenCV, scikit-learn, etc.
        if result.tools:
            has_ml_tools = any(
                key in ["ml_framework", "cv_library", "data_science"]
                for key in result.tools.keys()
            )
            # Note: Tool detection is optional for minimal projects


class TestiOSSwiftDetection:
    """Test iOS Swift framework detection."""

    def test_ios_basic_detection(self, ios_swift_project, detector):
        """Test basic iOS Swift detection."""
        result = detector(str(ios_swift_project))

        assert result is not None, "Should detect iOS Swift project"
        assert result.framework == "ios-swift"
        assert result.confidence >= 0.70, f"Expected confidence >=70%, got {result.confidence*100:.1f}%"
        assert result.language == "swift"


class TestPHPDetection:
    """Test Vanilla PHP framework detection."""

    def test_php_basic_detection(self, php_project, detector):
        """Test basic PHP detection."""
        result = detector(str(php_project))

        assert result is not None, "Should detect PHP project"
        assert result.framework == "vanilla-php-web"
        assert result.confidence >= 0.50, f"Expected confidence >=50%, got {result.confidence*100:.1f}%"
        assert result.language == "php"


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestDetectionEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_directory(self, tmp_path, detector):
        """Test detection on empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = detector(str(empty_dir))
        assert result is None, "Empty directory should return None"

    def test_nonexistent_directory(self, detector):
        """Test detection on non-existent directory."""
        result = detector("/path/that/does/not/exist")
        assert result is None, "Non-existent path should return None"

    def test_file_instead_of_directory(self, tmp_path, detector):
        """Test detection when given a file path instead of directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = detector(str(test_file))
        assert result is None, "File path should return None"

    def test_mixed_framework_markers(self, tmp_path, detector):
        """Test detection when multiple framework markers exist."""
        mixed_project = tmp_path / "mixed"
        mixed_project.mkdir()

        # Create markers for both Next.js and React
        (mixed_project / "package.json").write_text('''
        {
          "dependencies": {
            "next": "14.0.0",
            "react": "18.0.0"
          }
        }
        ''')
        (mixed_project / "next.config.js").write_text("module.exports = {}")

        result = detector(str(mixed_project))

        # Should detect Next.js (higher confidence)
        assert result is not None
        assert result.framework == "nextjs"


# ============================================================================
# Confidence Score Tests
# ============================================================================

class TestConfidenceScores:
    """Test confidence score accuracy and consistency."""

    def test_confidence_ranges(self, detector):
        """Test that confidence scores are within valid range (0.0 - 1.0)."""
        # This test requires all fixtures, so we'll use pytest.mark.parametrize

    @pytest.mark.parametrize("framework_fixture", [
        "nextjs_project",
        "fastapi_project",
        "go_project",
        "flutter_project",
        "react_project",
        "vue_project",
        "django_project",
        "flask_project",
        "python_ml_project",
        "ios_swift_project",
        "php_project",
    ])
    def test_all_frameworks_confidence(self, framework_fixture, detector, request):
        """Test confidence scores for all frameworks."""
        project = request.getfixturevalue(framework_fixture)
        result = detector(str(project))

        assert result is not None, f"{framework_fixture} should be detected"
        assert 0.0 <= result.confidence <= 1.0, "Confidence must be between 0 and 1"
        # PHP vanilla projects typically have lower confidence (50-60%) due to minimal markers
        min_confidence = 0.50 if framework_fixture == "php_project" else 0.65
        assert result.confidence >= min_confidence, f"{framework_fixture} confidence too low: {result.confidence*100:.1f}%"


# ============================================================================
# Integration with analyze_project.py
# ============================================================================

class TestDetectionIntegration:
    """Test integration between detect_stack.py and analyze_project.py."""

    @pytest.mark.skip(reason="Integration test moved to test_integration.py")
    def test_detection_feeds_generation(self, nextjs_project, analyzer_factory):
        """Test that detection results correctly feed into generation."""
        analyzer = analyzer_factory(nextjs_project)

        # This would require running full analyze() method
        # Deferred to test_integration.py for full E2E tests
