#!/usr/bin/env python3
"""
Development phase detection logic for Adaptive Claude Agents.

This module analyzes project signals to detect the current development phase
(Prototype, MVP, Production) and adjusts code review rigor accordingly.

Usage:
    from detect_phase import detect_phase
    result = detect_phase("/path/to/project")

Dependencies:
    - Python 3.9+
    - No external dependencies (uses stdlib only)
"""

import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PhaseResult:
    """
    Development phase detection result.

    Attributes:
        phase: Detected phase (prototype, mvp, production)
        confidence: Detection confidence score (0.0 to 1.0)
        rigor: Review rigor level (3, 6, or 10)
        signals: Dict of detected signals with scores
        description: Human-readable phase description
    """
    phase: str  # "prototype", "mvp", "production"
    confidence: float  # 0.0 to 1.0
    rigor: int  # 3 (light), 6 (moderate), 10 (strict)
    signals: Dict[str, float]  # Signal name → score
    description: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class PhaseDetector:
    """
    Development phase detector.

    Analyzes project files and structure to determine if project is in
    Prototype (3/10 rigor), MVP (6/10 rigor), or Production (10/10 rigor) phase.
    """

    # Signal weights for phase detection
    PROTOTYPE_SIGNALS = {
        'todo_comments': 0.15,          # TODO, FIXME, HACK comments
        'placeholder_data': 0.10,       # Mock data, hardcoded values
        'console_logging': 0.10,        # console.log, print() debugging
        'no_tests': 0.20,               # Missing test files
        'no_ci': 0.15,                  # No CI/CD config
        'no_env_config': 0.10,          # No .env or config files
        'small_commit_count': 0.10,     # < 20 commits
        'single_contributor': 0.10,     # Only 1 contributor
    }

    MVP_SIGNALS = {
        'basic_tests': 0.15,            # Some tests present
        'env_config': 0.15,             # .env files exist
        'ci_config': 0.15,              # CI/CD configured
        'readme': 0.10,                 # README exists
        'gitignore': 0.05,              # .gitignore exists
        'moderate_commits': 0.10,       # 20-100 commits
        'multiple_contributors': 0.10,  # 2-5 contributors
        'basic_error_handling': 0.10,   # Try-catch, error handlers
        'some_documentation': 0.10,     # Some docs beyond README
    }

    PRODUCTION_SIGNALS = {
        'comprehensive_tests': 0.15,    # High test coverage
        'monitoring': 0.15,             # Error monitoring (Sentry, etc.)
        'logging': 0.10,                # Structured logging
        'security': 0.15,               # Security headers, HTTPS, auth
        'documentation': 0.10,          # Comprehensive docs
        'ci_cd': 0.10,                  # Full CI/CD pipeline
        'many_commits': 0.10,           # 100+ commits
        'team_contributors': 0.05,      # 5+ contributors
        'code_quality_tools': 0.05,     # Linters, formatters
        'production_deps': 0.05,        # Production-ready dependencies
    }

    def __init__(self, project_path: Path):
        """
        Initialize phase detector.

        Args:
            project_path: Path to project root directory
        """
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")

        logger.info(f"Initialized phase detector for: {self.project_path}")

    def detect(self) -> PhaseResult:
        """
        Detect development phase.

        Returns:
            PhaseResult with detected phase, confidence, and rigor level
        """
        logger.info("Starting development phase detection")

        # Calculate scores for each phase
        prototype_score = self._calculate_prototype_score()
        mvp_score = self._calculate_mvp_score()
        production_score = self._calculate_production_score()

        logger.info(f"Phase scores - Prototype: {prototype_score:.2f}, "
                   f"MVP: {mvp_score:.2f}, Production: {production_score:.2f}")

        # Determine phase based on highest score
        scores = {
            'prototype': prototype_score,
            'mvp': mvp_score,
            'production': production_score
        }

        detected_phase = max(scores, key=scores.get)
        confidence = scores[detected_phase]

        # Get all detected signals for reporting
        all_signals = {
            **self._get_prototype_signals(),
            **self._get_mvp_signals(),
            **self._get_production_signals()
        }

        # Map phase to rigor level and description
        phase_info = {
            'prototype': {
                'rigor': 3,
                'description': 'Prototype phase - Focus on "Does it work?" with light review'
            },
            'mvp': {
                'rigor': 6,
                'description': 'MVP phase - Focus on "Is it secure?" with moderate review'
            },
            'production': {
                'rigor': 10,
                'description': 'Production phase - Focus on "Is it perfect?" with strict review'
            }
        }

        info = phase_info[detected_phase]

        result = PhaseResult(
            phase=detected_phase,
            confidence=confidence,
            rigor=info['rigor'],
            signals=all_signals,
            description=info['description']
        )

        logger.info(f"Detected phase: {detected_phase} (confidence: {confidence:.0%}, "
                   f"rigor: {info['rigor']}/10)")

        return result

    def _calculate_prototype_score(self) -> float:
        """Calculate prototype phase score (0.0 to 1.0)."""
        signals = self._get_prototype_signals()
        weighted_score = sum(
            signals[name] * weight
            for name, weight in self.PROTOTYPE_SIGNALS.items()
            if name in signals
        )
        return min(weighted_score, 1.0)

    def _calculate_mvp_score(self) -> float:
        """Calculate MVP phase score (0.0 to 1.0)."""
        signals = self._get_mvp_signals()
        weighted_score = sum(
            signals[name] * weight
            for name, weight in self.MVP_SIGNALS.items()
            if name in signals
        )
        return min(weighted_score, 1.0)

    def _calculate_production_score(self) -> float:
        """Calculate production phase score (0.0 to 1.0)."""
        signals = self._get_production_signals()
        weighted_score = sum(
            signals[name] * weight
            for name, weight in self.PRODUCTION_SIGNALS.items()
            if name in signals
        )
        return min(weighted_score, 1.0)

    def _get_prototype_signals(self) -> Dict[str, float]:
        """Detect prototype-specific signals."""
        signals = {}

        # TODO comments (high in prototype)
        todo_count = self._count_pattern(['TODO', 'FIXME', 'HACK', 'XXX'])
        signals['todo_comments'] = min(todo_count / 20.0, 1.0)  # Normalize to 0-1

        # Placeholder data (hardcoded strings, mock data)
        placeholder_count = self._count_pattern(['PLACEHOLDER', 'MOCK', 'DUMMY', 'TEST_'])
        signals['placeholder_data'] = min(placeholder_count / 10.0, 1.0)

        # Console logging (debugging statements)
        console_count = self._count_pattern(['console.log', 'print(', 'var_dump', 'dd('])
        signals['console_logging'] = min(console_count / 30.0, 1.0)

        # No tests
        test_files = list(self.project_path.rglob('*test*.py')) + \
                     list(self.project_path.rglob('*test*.js')) + \
                     list(self.project_path.rglob('*test*.ts')) + \
                     list(self.project_path.rglob('*spec*.js')) + \
                     list(self.project_path.rglob('*spec*.ts'))
        signals['no_tests'] = 0.0 if test_files else 1.0

        # No CI/CD
        ci_files = [
            self.project_path / '.github' / 'workflows',
            self.project_path / '.gitlab-ci.yml',
            self.project_path / '.circleci',
            self.project_path / 'Jenkinsfile'
        ]
        signals['no_ci'] = 0.0 if any(f.exists() for f in ci_files) else 1.0

        # No environment config
        env_files = [
            self.project_path / '.env',
            self.project_path / '.env.example',
            self.project_path / 'config.py',
            self.project_path / 'config.js'
        ]
        signals['no_env_config'] = 0.0 if any(f.exists() for f in env_files) else 1.0

        # Small commit count (git history)
        commit_count = self._get_commit_count()
        signals['small_commit_count'] = 1.0 if commit_count < 20 else 0.0

        # Single contributor
        contributor_count = self._get_contributor_count()
        signals['single_contributor'] = 1.0 if contributor_count == 1 else 0.0

        return signals

    def _get_mvp_signals(self) -> Dict[str, float]:
        """Detect MVP-specific signals."""
        signals = {}

        # Basic tests exist
        test_files = list(self.project_path.rglob('*test*.py')) + \
                     list(self.project_path.rglob('*test*.js')) + \
                     list(self.project_path.rglob('*test*.ts'))
        signals['basic_tests'] = 1.0 if test_files else 0.0

        # Environment config
        env_files = [
            self.project_path / '.env.example',
            self.project_path / 'config' / 'environments'
        ]
        signals['env_config'] = 1.0 if any(f.exists() for f in env_files) else 0.0

        # CI config
        ci_files = [
            self.project_path / '.github' / 'workflows',
            self.project_path / '.gitlab-ci.yml'
        ]
        signals['ci_config'] = 1.0 if any(f.exists() for f in ci_files) else 0.0

        # README exists
        readme_files = list(self.project_path.glob('README.*'))
        signals['readme'] = 1.0 if readme_files else 0.0

        # .gitignore exists
        signals['gitignore'] = 1.0 if (self.project_path / '.gitignore').exists() else 0.0

        # Moderate commits (20-100)
        commit_count = self._get_commit_count()
        signals['moderate_commits'] = 1.0 if 20 <= commit_count <= 100 else 0.0

        # Multiple contributors (2-5)
        contributor_count = self._get_contributor_count()
        signals['multiple_contributors'] = 1.0 if 2 <= contributor_count <= 5 else 0.0

        # Basic error handling (try-catch blocks)
        error_handling_count = self._count_pattern(['try:', 'catch', 'except', 'rescue'])
        signals['basic_error_handling'] = min(error_handling_count / 10.0, 1.0)

        # Some documentation (docs/ folder)
        docs_dir = self.project_path / 'docs'
        signals['some_documentation'] = 1.0 if docs_dir.exists() else 0.0

        return signals

    def _get_production_signals(self) -> Dict[str, float]:
        """Detect production-specific signals."""
        signals = {}

        # Comprehensive tests (high coverage)
        test_files = list(self.project_path.rglob('*test*.py')) + \
                     list(self.project_path.rglob('*test*.js')) + \
                     list(self.project_path.rglob('*test*.ts'))
        signals['comprehensive_tests'] = 1.0 if len(test_files) > 20 else 0.0

        # Monitoring (Sentry, error tracking)
        monitoring_patterns = ['sentry', 'bugsnag', 'rollbar', 'newrelic', 'datadog']
        monitoring_count = self._count_pattern(monitoring_patterns)
        signals['monitoring'] = 1.0 if monitoring_count > 0 else 0.0

        # Structured logging
        logging_patterns = ['winston', 'bunyan', 'structlog', 'loguru', 'logging.']
        logging_count = self._count_pattern(logging_patterns)
        signals['logging'] = min(logging_count / 5.0, 1.0)

        # Security (HTTPS, auth, headers)
        security_patterns = ['helmet', 'cors', 'csrf', 'jwt', 'bcrypt', 'https']
        security_count = self._count_pattern(security_patterns)
        signals['security'] = min(security_count / 3.0, 1.0)

        # Documentation (comprehensive docs/)
        docs_dir = self.project_path / 'docs'
        if docs_dir.exists():
            doc_files = list(docs_dir.rglob('*.md'))
            signals['documentation'] = 1.0 if len(doc_files) > 5 else 0.5
        else:
            signals['documentation'] = 0.0

        # Full CI/CD pipeline
        ci_files = [
            self.project_path / '.github' / 'workflows',
            self.project_path / 'deploy.yml',
            self.project_path / 'Dockerfile'
        ]
        signals['ci_cd'] = 1.0 if sum(f.exists() for f in ci_files) >= 2 else 0.0

        # Many commits (100+)
        commit_count = self._get_commit_count()
        signals['many_commits'] = 1.0 if commit_count >= 100 else 0.0

        # Team contributors (5+)
        contributor_count = self._get_contributor_count()
        signals['team_contributors'] = 1.0 if contributor_count >= 5 else 0.0

        # Code quality tools (linters, formatters)
        quality_files = [
            self.project_path / '.eslintrc',
            self.project_path / '.prettierrc',
            self.project_path / 'pyproject.toml',
            self.project_path / '.pylintrc'
        ]
        signals['code_quality_tools'] = 1.0 if any(f.exists() for f in quality_files) else 0.0

        # Production dependencies (check package.json, requirements.txt)
        prod_patterns = ['gunicorn', 'uvicorn', 'pm2', 'nginx', 'redis']
        prod_count = self._count_pattern(prod_patterns)
        signals['production_deps'] = 1.0 if prod_count > 0 else 0.0

        return signals

    def _count_pattern(self, patterns: List[str]) -> int:
        """
        Count occurrences of patterns in project files.

        Args:
            patterns: List of patterns to search for

        Returns:
            Total count of all patterns found
        """
        count = 0
        extensions = ['.py', '.js', '.ts', '.tsx', '.jsx', '.php', '.go', '.dart']

        for ext in extensions:
            for file_path in self.project_path.rglob(f'*{ext}'):
                # Skip node_modules, venv, etc.
                if any(part in file_path.parts for part in ['node_modules', 'venv', '.venv', 'vendor', 'build', 'dist']):
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for pattern in patterns:
                        count += content.lower().count(pattern.lower())
                except Exception as e:
                    logger.debug(f"Error reading {file_path}: {e}")
                    continue

        return count

    def _get_commit_count(self) -> int:
        """
        Get number of git commits.

        Returns:
            Number of commits (0 if not a git repo)
        """
        git_dir = self.project_path / '.git'
        if not git_dir.exists():
            return 0

        try:
            import subprocess
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
        except Exception as e:
            logger.debug(f"Error getting commit count: {e}")

        return 0

    def _get_contributor_count(self) -> int:
        """
        Get number of unique contributors.

        Returns:
            Number of contributors (1 if not a git repo)
        """
        git_dir = self.project_path / '.git'
        if not git_dir.exists():
            return 1

        try:
            import subprocess
            result = subprocess.run(
                ['git', 'shortlog', '-sn', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return len(lines) if lines[0] else 1
        except Exception as e:
            logger.debug(f"Error getting contributor count: {e}")

        return 1


def detect_phase(project_path: str) -> PhaseResult:
    """
    Convenience function for phase detection.

    Args:
        project_path: Path to project root

    Returns:
        PhaseResult with detected phase information
    """
    detector = PhaseDetector(Path(project_path))
    return detector.detect()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_phase.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    try:
        result = detect_phase(project_path)

        print("\n" + "="*60)
        print("DEVELOPMENT PHASE DETECTION")
        print("="*60)
        print(f"\nProject: {project_path}")
        print(f"\nDetected Phase: {result.phase.upper()}")
        print(f"Confidence: {result.confidence:.0%}")
        print(f"Review Rigor: {result.rigor}/10")
        print(f"Description: {result.description}")

        print("\n" + "-"*60)
        print("DETECTED SIGNALS")
        print("-"*60)

        for signal_name, score in sorted(result.signals.items(), key=lambda x: -x[1]):
            if score > 0:
                bar = '█' * int(score * 20)
                print(f"{signal_name:30s} {bar} {score:.0%}")

        print("\n" + "="*60)

    except Exception as e:
        logger.error(f"Error detecting phase: {e}")
        sys.exit(1)
