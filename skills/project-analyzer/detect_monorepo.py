"""Monorepo detection for workspace-based projects.

Supports:
- npm workspaces (package.json)
- pnpm workspaces (pnpm-workspace.yaml)
- Yarn workspaces (package.json)
- Lerna (lerna.json)
- Nx (nx.json)

Usage:
    from detect_monorepo import MonorepoDetector

    detector = MonorepoDetector("/path/to/project")
    result = detector.detect()

    if result.is_monorepo:
        print(f"Found {len(result.workspaces)} workspaces")
        for workspace in result.workspaces:
            print(f"  - {workspace.name}: {workspace.path}")
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceInfo:
    """Information about a single workspace in a monorepo.

    Attributes:
        name: Workspace name (from package.json)
        path: Absolute path to workspace directory
        package_manager: Workspace manager type ('npm', 'pnpm', 'yarn', 'lerna', 'nx')
        framework: Detected framework (populated by analyze_project)
        detection_result: Full detection result (populated by analyze_project)
    """
    name: str
    path: Path
    package_manager: str
    framework: Optional[str] = None
    detection_result: Optional[object] = None  # DetectionResult from detect_stack


@dataclass
class MonorepoResult:
    """Result of monorepo detection.

    Attributes:
        is_monorepo: Whether the project is a monorepo
        workspace_manager: Type of workspace manager ('npm', 'pnpm', 'yarn', 'lerna', 'nx')
        workspaces: List of detected workspaces
        root_path: Root path of the monorepo
    """
    is_monorepo: bool
    workspace_manager: Optional[str] = None
    workspaces: List[WorkspaceInfo] = field(default_factory=list)
    root_path: Optional[Path] = None


class MonorepoDetector:
    """Detects monorepo workspace configurations.

    Supports multiple workspace managers:
    - npm workspaces (package.json)
    - pnpm workspaces (pnpm-workspace.yaml)
    - Yarn workspaces (package.json)
    - Lerna (lerna.json)
    - Nx (nx.json)

    Usage:
        detector = MonorepoDetector("/path/to/project")
        result = detector.detect()
    """

    def __init__(self, project_path: str | Path):
        """Initialize detector.

        Args:
            project_path: Path to project root directory
        """
        self.project_path = Path(project_path).resolve()

    def detect(self) -> MonorepoResult:
        """Detect if project is a monorepo and identify workspaces.

        Detection order:
        1. pnpm workspaces (pnpm-workspace.yaml)
        2. npm/Yarn workspaces (package.json)
        3. Lerna (lerna.json)
        4. Nx (nx.json)

        Returns:
            MonorepoResult with detection results
        """
        logger.debug(f"Checking for monorepo at: {self.project_path}")

        # Check for pnpm workspaces (highest priority)
        pnpm_workspace = self.project_path / "pnpm-workspace.yaml"
        if pnpm_workspace.exists():
            logger.debug("Found pnpm-workspace.yaml")
            return self._detect_pnpm_workspaces()

        # Check for npm/Yarn workspaces in package.json
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # npm/Yarn workspaces (in package.json)
                if "workspaces" in data:
                    logger.debug("Found workspaces in package.json")
                    return self._detect_npm_workspaces(data["workspaces"])
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to parse package.json: {e}")

        # Check for Lerna
        lerna_json = self.project_path / "lerna.json"
        if lerna_json.exists():
            logger.debug("Found lerna.json")
            return self._detect_lerna_workspaces()

        # Check for Nx
        nx_json = self.project_path / "nx.json"
        if nx_json.exists():
            logger.debug("Found nx.json")
            return self._detect_nx_workspaces()

        logger.debug("No monorepo configuration found")
        return MonorepoResult(is_monorepo=False, root_path=self.project_path)

    def _detect_npm_workspaces(self, workspaces_config) -> MonorepoResult:
        """Detect npm/Yarn workspaces from package.json.

        Args:
            workspaces_config: Workspaces field from package.json (array or object)

        Returns:
            MonorepoResult with npm workspace information
        """
        workspaces = []

        # workspaces can be array or object with "packages" key
        # Array format: ["packages/*", "apps/*"]
        # Object format: {"packages": ["packages/*", "apps/*"]}
        if isinstance(workspaces_config, list):
            patterns = workspaces_config
        elif isinstance(workspaces_config, dict):
            patterns = workspaces_config.get("packages", [])
        else:
            logger.warning(f"Unexpected workspaces config type: {type(workspaces_config)}")
            patterns = []

        for pattern in patterns:
            logger.debug(f"Scanning workspace pattern: {pattern}")

            # Glob pattern matching (e.g., "packages/*", "apps/*/")
            for workspace_dir in self.project_path.glob(pattern):
                if not workspace_dir.is_dir():
                    continue

                pkg_json = workspace_dir / "package.json"
                if pkg_json.exists():
                    try:
                        with open(pkg_json, 'r', encoding='utf-8') as f:
                            pkg_data = json.load(f)

                        workspace_name = pkg_data.get("name", workspace_dir.name)
                        logger.debug(f"Found workspace: {workspace_name} at {workspace_dir}")

                        workspaces.append(WorkspaceInfo(
                            name=workspace_name,
                            path=workspace_dir,
                            package_manager="npm"
                        ))
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"Failed to parse {pkg_json}: {e}")

        logger.info(f"Detected npm workspaces: {len(workspaces)} workspaces found")
        return MonorepoResult(
            is_monorepo=True,
            workspace_manager="npm",
            workspaces=workspaces,
            root_path=self.project_path
        )

    def _detect_pnpm_workspaces(self) -> MonorepoResult:
        """Detect pnpm workspaces from pnpm-workspace.yaml.

        Returns:
            MonorepoResult with pnpm workspace information
        """
        if not YAML_AVAILABLE:
            logger.error("PyYAML not installed, cannot parse pnpm-workspace.yaml")
            return MonorepoResult(is_monorepo=False, root_path=self.project_path)

        workspace_file = self.project_path / "pnpm-workspace.yaml"

        try:
            with open(workspace_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except (yaml.YAMLError, IOError) as e:
            logger.error(f"Failed to parse pnpm-workspace.yaml: {e}")
            return MonorepoResult(is_monorepo=False, root_path=self.project_path)

        if not config or "packages" not in config:
            logger.warning("pnpm-workspace.yaml has no 'packages' field")
            return MonorepoResult(is_monorepo=False, root_path=self.project_path)

        workspaces = []
        for pattern in config.get("packages", []):
            logger.debug(f"Scanning pnpm workspace pattern: {pattern}")

            for workspace_dir in self.project_path.glob(pattern):
                if not workspace_dir.is_dir():
                    continue

                pkg_json = workspace_dir / "package.json"
                if pkg_json.exists():
                    try:
                        with open(pkg_json, 'r', encoding='utf-8') as f:
                            pkg_data = json.load(f)

                        workspace_name = pkg_data.get("name", workspace_dir.name)
                        logger.debug(f"Found pnpm workspace: {workspace_name} at {workspace_dir}")

                        workspaces.append(WorkspaceInfo(
                            name=workspace_name,
                            path=workspace_dir,
                            package_manager="pnpm"
                        ))
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"Failed to parse {pkg_json}: {e}")

        logger.info(f"Detected pnpm workspaces: {len(workspaces)} workspaces found")
        return MonorepoResult(
            is_monorepo=True,
            workspace_manager="pnpm",
            workspaces=workspaces,
            root_path=self.project_path
        )

    def _detect_lerna_workspaces(self) -> MonorepoResult:
        """Detect Lerna workspaces from lerna.json.

        Returns:
            MonorepoResult with Lerna workspace information
        """
        lerna_json = self.project_path / "lerna.json"

        try:
            with open(lerna_json, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to parse lerna.json: {e}")
            return MonorepoResult(is_monorepo=False, root_path=self.project_path)

        # Lerna uses "packages" array for workspace patterns
        patterns = config.get("packages", ["packages/*"])

        workspaces = []
        for pattern in patterns:
            logger.debug(f"Scanning Lerna workspace pattern: {pattern}")

            for workspace_dir in self.project_path.glob(pattern):
                if not workspace_dir.is_dir():
                    continue

                pkg_json = workspace_dir / "package.json"
                if pkg_json.exists():
                    try:
                        with open(pkg_json, 'r', encoding='utf-8') as f:
                            pkg_data = json.load(f)

                        workspace_name = pkg_data.get("name", workspace_dir.name)
                        logger.debug(f"Found Lerna workspace: {workspace_name} at {workspace_dir}")

                        workspaces.append(WorkspaceInfo(
                            name=workspace_name,
                            path=workspace_dir,
                            package_manager="lerna"
                        ))
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"Failed to parse {pkg_json}: {e}")

        logger.info(f"Detected Lerna workspaces: {len(workspaces)} workspaces found")
        return MonorepoResult(
            is_monorepo=True,
            workspace_manager="lerna",
            workspaces=workspaces,
            root_path=self.project_path
        )

    def _detect_nx_workspaces(self) -> MonorepoResult:
        """Detect Nx workspaces from nx.json and workspace.json.

        Returns:
            MonorepoResult with Nx workspace information
        """
        # Nx uses workspace.json or project.json files
        # Nx >= 13 uses project.json in each project directory

        workspaces = []

        # Check for workspace.json (Nx < 13)
        workspace_json = self.project_path / "workspace.json"
        if workspace_json.exists():
            try:
                with open(workspace_json, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                projects = config.get("projects", {})
                for project_name, project_config in projects.items():
                    if isinstance(project_config, str):
                        # Project path as string
                        project_path = self.project_path / project_config
                    elif isinstance(project_config, dict):
                        # Project config object with "root" key
                        project_path = self.project_path / project_config.get("root", project_name)
                    else:
                        continue

                    if project_path.is_dir():
                        logger.debug(f"Found Nx workspace: {project_name} at {project_path}")
                        workspaces.append(WorkspaceInfo(
                            name=project_name,
                            path=project_path,
                            package_manager="nx"
                        ))
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to parse workspace.json: {e}")

        # Scan for project.json files (Nx >= 13)
        for project_json in self.project_path.glob("**/project.json"):
            if ".nx" in project_json.parts:
                continue  # Skip .nx cache directory

            workspace_dir = project_json.parent
            try:
                with open(project_json, 'r', encoding='utf-8') as f:
                    project_config = json.load(f)

                project_name = project_config.get("name", workspace_dir.name)
                logger.debug(f"Found Nx workspace: {project_name} at {workspace_dir}")

                workspaces.append(WorkspaceInfo(
                    name=project_name,
                    path=workspace_dir,
                    package_manager="nx"
                ))
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to parse {project_json}: {e}")

        logger.info(f"Detected Nx workspaces: {len(workspaces)} workspaces found")
        return MonorepoResult(
            is_monorepo=True,
            workspace_manager="nx",
            workspaces=workspaces,
            root_path=self.project_path
        )


if __name__ == "__main__":
    import sys

    # Simple CLI for testing
    if len(sys.argv) < 2:
        print("Usage: python detect_monorepo.py <project_path>")
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

    detector = MonorepoDetector(sys.argv[1])
    result = detector.detect()

    if result.is_monorepo:
        print(f"\n✓ Monorepo detected ({result.workspace_manager})")
        print(f"  Root: {result.root_path}")
        print(f"  Workspaces: {len(result.workspaces)}")
        for workspace in result.workspaces:
            print(f"    - {workspace.name} ({workspace.path.relative_to(result.root_path)})")
    else:
        print(f"\n✗ Not a monorepo")
        print(f"  Path: {result.root_path}")
