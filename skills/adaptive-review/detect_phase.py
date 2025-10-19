#!/usr/bin/env python3
"""
Development phase detection for Adaptive Claude Agents.

Analyzes project maturity using multiple signals to determine
development phase: prototype, mvp, or production.

Usage:
    from detect_phase import detect_development_phase
    result = detect_development_phase("/path/to/project")
    print(f"Phase: {result.phase} (confidence: {result.confidence})")
"""

import json
import logging
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SignalResult:
    """Result from a single detection signal."""
    signal_name: str
    detected_phase: str  # 'prototype', 'mvp', 'production'
    confidence: float  # 0.0 to 1.0
    weight: float  # Signal weight in final decision
    indicators: List[str] = field(default_factory=list)

    def weighted_score(self) -> Dict[str, float]:
        """Calculate weighted contribution to each phase."""
        score = {
            'prototype': 0.0,
            'mvp': 0.0,
            'production': 0.0
        }
        score[self.detected_phase] = self.confidence * self.weight
        return score


@dataclass
class PhaseResult:
    """Final phase detection result."""
    phase: str  # 'prototype', 'mvp', 'production'
    confidence: float  # 0.0 to 1.0
    signals: List[SignalResult]
    indicators: List[str]
    override_source: Optional[str] = None  # 'user', 'cache', None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'phase': self.phase,
            'confidence': self.confidence,
            'override_source': self.override_source,
            'indicators': self.indicators,
            'signals': [
                {
                    'name': s.signal_name,
                    'detected_phase': s.detected_phase,
                    'confidence': s.confidence,
                    'weight': s.weight
                }
                for s in self.signals
            ]
        }


class DevelopmentPhaseDetector:
    """Detects development phase using multiple signals."""

    # Signal weights (must sum to ~1.0 excluding user override)
    WEIGHTS = {
        'user_config': 1.00,  # 100% - complete override
        'version_number': 0.30,
        'git_history': 0.20,
        'test_coverage': 0.15,
        'ci_cd': 0.15,
        'documentation': 0.10,
        'code_structure': 0.10
    }

    def __init__(self, project_path: Path):
        """Initialize detector."""
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")

        logger.info(f"Initialized phase detector for: {self.project_path}")

    def detect(self) -> PhaseResult:
        """
        Detect development phase using all available signals.

        Returns:
            PhaseResult with detected phase and confidence
        """
        logger.info("Starting phase detection")

        # Check for user override first
        user_signal = self._detect_user_config()
        if user_signal and user_signal.confidence > 0.9:
            logger.info(f"User override detected: {user_signal.detected_phase}")
            return PhaseResult(
                phase=user_signal.detected_phase,
                confidence=user_signal.confidence,
                signals=[user_signal],
                indicators=user_signal.indicators,
                override_source='user'
            )

        # Gather all signals
        signals = []

        if user_signal:
            signals.append(user_signal)

        signals.extend([
            self._detect_version_number(),
            self._detect_git_history(),
            self._detect_test_coverage(),
            self._detect_ci_cd(),
            self._detect_documentation(),
            self._detect_code_structure()
        ])

        # Filter out None signals
        signals = [s for s in signals if s is not None]

        if not signals:
            logger.warning("No signals detected, defaulting to prototype")
            return PhaseResult(
                phase='prototype',
                confidence=0.3,
                signals=[],
                indicators=['No indicators found - assuming early prototype']
            )

        # Calculate weighted scores
        phase_scores = {'prototype': 0.0, 'mvp': 0.0, 'production': 0.0}
        total_weight = 0.0

        for signal in signals:
            if signal.signal_name == 'user_config':
                continue  # Already handled above

            weighted = signal.weighted_score()
            for phase, score in weighted.items():
                phase_scores[phase] += score
            total_weight += signal.weight

        # Normalize scores
        if total_weight > 0:
            for phase in phase_scores:
                phase_scores[phase] /= total_weight

        # Determine winner
        detected_phase = max(phase_scores, key=phase_scores.get)
        confidence = phase_scores[detected_phase]

        # Collect all indicators
        all_indicators = []
        for signal in signals:
            all_indicators.extend(signal.indicators)

        logger.info(f"Detected phase: {detected_phase} (confidence: {confidence:.2f})")

        return PhaseResult(
            phase=detected_phase,
            confidence=confidence,
            signals=signals,
            indicators=all_indicators
        )

    def _detect_user_config(self) -> Optional[SignalResult]:
        """Check for user-specified phase in .claude/phase.yml."""
        phase_file = self.project_path / '.claude' / 'phase.yml'

        if not phase_file.exists():
            return None

        try:
            with open(phase_file, 'r') as f:
                config = yaml.safe_load(f)

            phase = config.get('phase', '').lower()
            if phase not in ['prototype', 'mvp', 'production']:
                logger.warning(f"Invalid phase in config: {phase}")
                return None

            return SignalResult(
                signal_name='user_config',
                detected_phase=phase,
                confidence=1.0,
                weight=self.WEIGHTS['user_config'],
                indicators=[f"User-specified phase: {phase}"]
            )

        except (yaml.YAMLError, IOError) as e:
            logger.error(f"Error reading phase config: {e}")
            return None

    def _detect_version_number(self) -> Optional[SignalResult]:
        """Detect phase from package.json or pyproject.toml version."""
        # Check package.json (JavaScript/TypeScript)
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                version = data.get('version', '0.0.0')
                return self._analyze_version(version, 'package.json')
            except (json.JSONDecodeError, IOError):
                pass

        # Check pyproject.toml (Python)
        pyproject = self.project_path / 'pyproject.toml'
        if pyproject.exists():
            try:
                with open(pyproject, 'r') as f:
                    content = f.read()
                    match = re.search(r'version\s*=\s*"([^"]+)"', content)
                    if match:
                        version = match.group(1)
                        return self._analyze_version(version, 'pyproject.toml')
            except IOError:
                pass

        return None

    def _analyze_version(self, version: str, source: str) -> SignalResult:
        """Analyze version string to determine phase."""
        # Parse version
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
        if not match:
            return SignalResult(
                signal_name='version_number',
                detected_phase='prototype',
                confidence=0.5,
                weight=self.WEIGHTS['version_number'],
                indicators=[f"Invalid version format in {source}: {version}"]
            )

        major, minor, patch = map(int, match.groups())

        # Phase determination
        if major == 0 and minor == 0:
            # 0.0.x = very early prototype
            phase = 'prototype'
            confidence = 0.9
            indicators = [f"Version {version} (0.0.x) → early prototype"]
        elif major == 0:
            # 0.x.x = prototype/MVP
            phase = 'mvp' if minor >= 1 else 'prototype'
            confidence = 0.8
            indicators = [f"Version {version} (0.x.x) → {phase}"]
        elif major == 1 and minor == 0 and patch == 0:
            # 1.0.0 = first production release
            phase = 'production'
            confidence = 0.9
            indicators = [f"Version {version} (1.0.0) → production"]
        elif major >= 1:
            # 1.x.x+ = production
            phase = 'production'
            confidence = 0.95
            indicators = [f"Version {version} (>=1.0.0) → production"]
        else:
            phase = 'prototype'
            confidence = 0.5
            indicators = [f"Version {version} → default to prototype"]

        return SignalResult(
            signal_name='version_number',
            detected_phase=phase,
            confidence=confidence,
            weight=self.WEIGHTS['version_number'],
            indicators=indicators
        )

    def _detect_git_history(self) -> Optional[SignalResult]:
        """Analyze git history for maturity indicators."""
        git_dir = self.project_path / '.git'
        if not git_dir.exists():
            return SignalResult(
                signal_name='git_history',
                detected_phase='prototype',
                confidence=0.3,
                weight=self.WEIGHTS['git_history'],
                indicators=["No git repository - likely early prototype"]
            )

        try:
            # Get commit count
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            commit_count = int(result.stdout.strip()) if result.returncode == 0 else 0

            # Get recent commit activity (last 30 days)
            thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            result = subprocess.run(
                ['git', 'rev-list', '--count', f'--since={thirty_days_ago}', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            recent_commits = int(result.stdout.strip()) if result.returncode == 0 else 0

            # Check for tags (releases)
            result = subprocess.run(
                ['git', 'tag', '--list'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            tags = result.stdout.strip().split('\n') if result.returncode == 0 else []
            tag_count = len([t for t in tags if t])

            # Analyze
            indicators = []
            confidence = 0.7

            if commit_count < 50:
                phase = 'prototype'
                indicators.append(f"{commit_count} commits → early development")
            elif commit_count < 200:
                phase = 'mvp'
                indicators.append(f"{commit_count} commits → MVP stage")
            else:
                phase = 'production'
                indicators.append(f"{commit_count} commits → mature project")

            if tag_count > 0:
                indicators.append(f"{tag_count} release tags")
                if tag_count >= 5:
                    phase = 'production'
                    confidence = 0.85

            if recent_commits > 20:
                indicators.append(f"{recent_commits} commits in last 30 days → active development")

            return SignalResult(
                signal_name='git_history',
                detected_phase=phase,
                confidence=confidence,
                weight=self.WEIGHTS['git_history'],
                indicators=indicators
            )

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError) as e:
            logger.warning(f"Git analysis failed: {e}")
            return None

    def _detect_test_coverage(self) -> Optional[SignalResult]:
        """Check for test files and coverage configuration."""
        indicators = []

        # Check for test files
        test_patterns = [
            '**/*test*.py', '**/*spec*.py',  # Python
            '**/*test*.js', '**/*spec*.js', '**/*test*.ts', '**/*spec*.ts',  # JS/TS
            '**/*Test*.swift', '**/*Spec*.swift',  # Swift
            '**/*_test.go'  # Go
        ]

        test_file_count = 0
        for pattern in test_patterns:
            test_file_count += len(list(self.project_path.glob(pattern)))

        # Check for test config files
        test_configs = [
            'pytest.ini', 'vitest.config.js', 'vitest.config.ts',
            'jest.config.js', 'jest.config.ts', '.coveragerc',
            'coverage.xml', 'htmlcov/', '.coverage'
        ]

        has_test_config = any((self.project_path / cfg).exists() for cfg in test_configs)

        # Determine phase
        if test_file_count == 0:
            phase = 'prototype'
            confidence = 0.7
            indicators.append("No test files found")
        elif test_file_count < 10:
            phase = 'mvp'
            confidence = 0.6
            indicators.append(f"{test_file_count} test files → basic testing")
        else:
            phase = 'production'
            confidence = 0.75
            indicators.append(f"{test_file_count} test files → comprehensive testing")

        if has_test_config:
            indicators.append("Test configuration present")
            if phase == 'prototype':
                phase = 'mvp'
            confidence += 0.1

        return SignalResult(
            signal_name='test_coverage',
            detected_phase=phase,
            confidence=min(confidence, 1.0),
            weight=self.WEIGHTS['test_coverage'],
            indicators=indicators
        )

    def _detect_ci_cd(self) -> Optional[SignalResult]:
        """Check for CI/CD configuration."""
        ci_files = [
            '.github/workflows',
            '.gitlab-ci.yml',
            'circle.yml', '.circleci/config.yml',
            'Jenkinsfile',
            '.travis.yml',
            'azure-pipelines.yml'
        ]

        indicators = []
        has_ci = False

        for ci_file in ci_files:
            ci_path = self.project_path / ci_file
            if ci_path.exists():
                has_ci = True
                indicators.append(f"CI/CD config: {ci_file}")

        if has_ci:
            phase = 'production'
            confidence = 0.8
        else:
            phase = 'prototype'
            confidence = 0.6
            indicators.append("No CI/CD configuration")

        return SignalResult(
            signal_name='ci_cd',
            detected_phase=phase,
            confidence=confidence,
            weight=self.WEIGHTS['ci_cd'],
            indicators=indicators
        )

    def _detect_documentation(self) -> Optional[SignalResult]:
        """Check documentation completeness."""
        indicators = []

        # Check for README
        readme_files = ['README.md', 'README.rst', 'README.txt']
        has_readme = any((self.project_path / r).exists() for r in readme_files)

        # Check for additional docs
        doc_indicators = [
            'CONTRIBUTING.md', 'CHANGELOG.md', 'LICENSE',
            'docs/', 'documentation/', 'API.md'
        ]

        doc_count = sum(1 for doc in doc_indicators if (self.project_path / doc).exists())

        # Determine phase
        if not has_readme:
            phase = 'prototype'
            confidence = 0.7
            indicators.append("No README found")
        elif doc_count == 0:
            phase = 'mvp'
            confidence = 0.6
            indicators.append("README present, minimal docs")
        elif doc_count < 3:
            phase = 'mvp'
            confidence = 0.7
            indicators.append(f"README + {doc_count} doc files")
        else:
            phase = 'production'
            confidence = 0.8
            indicators.append(f"Comprehensive documentation ({doc_count} files)")

        return SignalResult(
            signal_name='documentation',
            detected_phase=phase,
            confidence=confidence,
            weight=self.WEIGHTS['documentation'],
            indicators=indicators
        )

    def _detect_code_structure(self) -> Optional[SignalResult]:
        """Analyze code organization and structure."""
        indicators = []

        # Check for proper project structure
        structure_indicators = [
            ('src/', 'Source directory'),
            ('lib/', 'Library directory'),
            ('app/', 'Application directory'),
            ('tests/', 'Test directory'),
            ('docs/', 'Documentation directory'),
            ('.gitignore', 'Git ignore file'),
            ('requirements.txt', 'Python requirements'),
            ('package.json', 'Node package config'),
            ('Dockerfile', 'Docker configuration'),
            ('docker-compose.yml', 'Docker Compose')
        ]

        structure_count = 0
        for path, desc in structure_indicators:
            if (self.project_path / path).exists():
                structure_count += 1
                indicators.append(desc)

        # Determine phase
        if structure_count < 2:
            phase = 'prototype'
            confidence = 0.6
        elif structure_count < 5:
            phase = 'mvp'
            confidence = 0.7
        else:
            phase = 'production'
            confidence = 0.75

        indicators.insert(0, f"{structure_count}/10 structure indicators")

        return SignalResult(
            signal_name='code_structure',
            detected_phase=phase,
            confidence=confidence,
            weight=self.WEIGHTS['code_structure'],
            indicators=indicators
        )


def detect_development_phase(project_path: str) -> PhaseResult:
    """
    Main entry point for phase detection.

    Args:
        project_path: Path to project root

    Returns:
        PhaseResult with detected phase and confidence
    """
    detector = DevelopmentPhaseDetector(Path(project_path))
    return detector.detect()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_phase.py <project_path>")
        sys.exit(1)

    result = detect_development_phase(sys.argv[1])

    print("\n" + "="*60)
    print("Development Phase Detection Result")
    print("="*60)
    print(f"Phase: {result.phase.upper()}")
    print(f"Confidence: {result.confidence:.1%}")
    if result.override_source:
        print(f"Source: {result.override_source}")
    print("\nIndicators:")
    for indicator in result.indicators:
        print(f"  • {indicator}")
    print("\nSignals:")
    for signal in result.signals:
        print(f"  • {signal.signal_name}: {signal.detected_phase} "
              f"(confidence: {signal.confidence:.1%}, weight: {signal.weight:.0%})")
    print("="*60)
