# Automated Testing Framework

**Version**: 0.5.0-dev
**Status**: In Development
**Purpose**: Automated regression testing for project detection and subagent generation

---

## Test Structure

```
tests/
├── README.md                 # This file
├── conftest.py              # pytest configuration
├── test_detection.py        # Framework detection tests
├── test_generation.py       # Subagent generation tests
├── test_integration.py      # End-to-end integration tests
├── test_performance.py      # Performance benchmarks
└── sample_projects/         # Minimal test projects
    ├── nextjs-demo/
    ├── fastapi-demo/
    ├── go-demo/
    ├── flutter-demo/
    ├── react-demo/
    ├── vue-demo/
    ├── django-demo/
    ├── flask-demo/
    ├── python-ml-demo/
    ├── ios-swift-demo/
    └── php-demo/
```

---

## Test Categories

### 1. Detection Tests (`test_detection.py`)

**Purpose**: Verify framework detection accuracy

**Test Cases**:
- ✅ Detect Next.js with 100% confidence
- ✅ Detect FastAPI with 80%+ confidence
- ✅ Detect Go with 85%+ confidence
- ✅ Detect Flutter with 80%+ confidence
- ✅ Detect all 11 supported frameworks
- ✅ Return None for unsupported frameworks
- ✅ Extract correct version numbers
- ✅ Detect framework-specific tools (testing, database, etc.)

**Example**:
```python
def test_nextjs_detection():
    result = detect_tech_stack("tests/sample_projects/nextjs-demo")
    assert result is not None
    assert result.framework == "nextjs"
    assert result.confidence >= 0.95
    assert result.version.startswith("14.")
```

---

### 2. Generation Tests (`test_generation.py`)

**Purpose**: Verify subagent generation logic

**Test Cases**:
- ✅ Generate SUBAGENT_GUIDE.md with correct framework name
- ✅ Generate framework-specific templates
- ✅ Replace template variables ({{FRAMEWORK}}, {{VERSION}}, {{LANGUAGE}})
- ✅ Create .claude/agents/ directory if missing
- ✅ Add AGGRESSIVE policy to CLAUDE.md (if exists)
- ✅ Skip duplicates (safe to re-run)
- ✅ Handle missing templates gracefully

**Example**:
```python
def test_subagent_guide_generation(tmp_path):
    # Setup test project
    setup_nextjs_project(tmp_path)

    # Run analysis
    analyzer = ProjectAnalyzer(tmp_path, auto_confirm=True)
    success = analyzer.analyze()

    # Verify SUBAGENT_GUIDE.md
    guide_path = tmp_path / ".claude" / "agents" / "SUBAGENT_GUIDE.md"
    assert guide_path.exists()

    content = guide_path.read_text()
    assert "NEXTJS Projects" in content
    assert "AGGRESSIVE Mode" in content
    assert "Component Development" in content
```

---

### 3. Integration Tests (`test_integration.py`)

**Purpose**: End-to-end workflow testing

**Test Cases**:
- ✅ Full workflow: detection → generation → verification
- ✅ Update workflow: re-run on existing project
- ✅ Multiple projects in sequence
- ✅ Error handling (no framework detected)
- ✅ Error handling (missing dependencies)

**Example**:
```python
def test_full_workflow(tmp_path):
    # 1. Create test project
    create_fastapi_project(tmp_path)

    # 2. Run analysis
    result = analyze_project(tmp_path, auto=True)
    assert result.success

    # 3. Verify all outputs
    assert (tmp_path / ".claude" / "agents" / "SUBAGENT_GUIDE.md").exists()
    assert (tmp_path / ".claude" / "agents" / "fastapi-tester.md").exists()
    assert "AGGRESSIVE ポリシー" in (tmp_path / "CLAUDE.md").read_text()
```

---

### 4. Performance Tests (`test_performance.py`)

**Purpose**: Benchmark detection and generation speed

**Metrics**:
- Detection time (target: < 500ms)
- Generation time (target: < 2s)
- Memory usage (target: < 100MB)
- Token estimation (for SUBAGENT_GUIDE.md)

**Example**:
```python
import pytest
import time

@pytest.mark.benchmark
def test_detection_performance(benchmark):
    def detect():
        return detect_tech_stack("tests/sample_projects/nextjs-demo")

    result = benchmark(detect)
    assert result.framework == "nextjs"

    # Benchmark automatically tracks:
    # - Min/Max/Mean/Median time
    # - Standard deviation
    # - Iterations per second
```

---

## Sample Projects

### Minimal Test Projects

Each sample project contains the **minimum files needed** for accurate detection:

#### Next.js Demo
```
nextjs-demo/
├── package.json          # "next": "14.2.0"
├── next.config.js
├── app/
│   └── layout.tsx
└── tsconfig.json
```

#### FastAPI Demo
```
fastapi-demo/
├── pyproject.toml        # dependencies = ["fastapi", ...]
├── main.py               # from fastapi import FastAPI
└── requirements.txt
```

#### Go Demo
```
go-demo/
├── go.mod                # require github.com/gin-gonic/gin
└── main.go               # import "github.com/gin-gonic/gin"
```

**Why Minimal?**
- Fast test execution (< 1s per project)
- Easy to maintain
- Clear detection logic validation
- No external dependencies needed

---

## Running Tests

### Basic Usage

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_detection.py

# Run specific test
pytest tests/test_detection.py::test_nextjs_detection

# Run with coverage
pytest tests/ --cov=skills --cov-report=html

# Run performance benchmarks
pytest tests/test_performance.py --benchmark-only
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ --cov=skills --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## Test Data Management

### Fixtures (`conftest.py`)

```python
import pytest
from pathlib import Path

@pytest.fixture
def nextjs_project(tmp_path):
    """Create minimal Next.js project for testing."""
    project = tmp_path / "nextjs-demo"
    project.mkdir()

    # package.json
    (project / "package.json").write_text('''
    {
      "name": "test-nextjs",
      "dependencies": {
        "next": "14.2.0",
        "react": "18.2.0"
      }
    }
    ''')

    # next.config.js
    (project / "next.config.js").write_text('''
    module.exports = {}
    ''')

    return project

@pytest.fixture
def fastapi_project(tmp_path):
    """Create minimal FastAPI project for testing."""
    project = tmp_path / "fastapi-demo"
    project.mkdir()

    # main.py
    (project / "main.py").write_text('''
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Hello World"}
    ''')

    # requirements.txt
    (project / "requirements.txt").write_text('''
    fastapi==0.109.0
    uvicorn==0.27.0
    ''')

    return project
```

---

## Expected Test Results

### Detection Accuracy Targets

| Framework | Target Confidence | Actual (v0.4.3) | Status |
|-----------|------------------|----------------|--------|
| Next.js | 95%+ | 100% | ✅ Pass |
| FastAPI | 75%+ | 80% | ✅ Pass |
| Go | 80%+ | 85% | ✅ Pass |
| Flutter | 75%+ | 80% | ✅ Pass |
| Python ML | 95%+ | 100% | ✅ Pass |
| React | 75%+ | 80% | ✅ Pass |
| Vue | 85%+ | 90% | ✅ Pass |
| Django | 75%+ | 80% | ✅ Pass |
| Flask | 65%+ | 70% | ✅ Pass |
| iOS Swift | 75%+ | 80% | ✅ Pass |
| PHP | 75%+ | 80% | ✅ Pass |

**Pass Criteria**: All frameworks meet or exceed target confidence

### Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Detection Time | < 500ms | Per project |
| Generation Time | < 2s | SUBAGENT_GUIDE.md + templates |
| Memory Usage | < 100MB | Peak during analysis |
| Test Suite Time | < 30s | All tests |

---

## Continuous Improvement

### Test-Driven Development

**Process**:
1. Add new framework support
2. Write failing test first
3. Implement detection logic
4. Verify test passes
5. Update documentation

**Example**:
```python
# 1. Write test (fails initially)
def test_rust_detection():
    result = detect_tech_stack("tests/sample_projects/rust-demo")
    assert result.framework == "rust"
    assert result.confidence >= 0.80

# 2. Implement detection
# 3. Test passes
# 4. Update README.md with Rust support
```

### Regression Prevention

**Coverage Goals**:
- Detection logic: 90%+
- Generation logic: 85%+
- Error handling: 80%+
- Overall: 85%+

**Mutation Testing** (future):
- Use `mutmut` to verify test quality
- Ensure tests catch real bugs, not just pass

---

## Contributing

### Adding a New Test

1. Create test in appropriate file (`test_detection.py`, etc.)
2. Use fixtures from `conftest.py`
3. Follow naming convention: `test_<feature>_<scenario>`
4. Add docstring explaining what's tested
5. Run locally: `pytest tests/test_your_file.py -v`
6. Ensure coverage: `pytest --cov=skills`

### Adding a Sample Project

1. Create minimal project in `tests/sample_projects/<framework>-demo/`
2. Include only files needed for detection
3. Add fixture in `conftest.py`
4. Document in this README
5. Update detection test to include new framework

---

## Future Enhancements

### v0.6.0
- [ ] Parallel test execution (pytest-xdist)
- [ ] Visual regression testing (screenshot comparison)
- [ ] Property-based testing (Hypothesis)
- [ ] Mutation testing (mutmut)

### v1.0.0
- [ ] Load testing (1000+ projects)
- [ ] Fuzz testing (invalid inputs)
- [ ] Integration with real projects (not just demos)
- [ ] Test report dashboard

---

## Troubleshooting

### Tests Fail Locally

**Issue**: Tests pass in CI but fail locally
**Cause**: Different Python versions or dependencies
**Solution**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/
```

### Slow Test Execution

**Issue**: Tests take > 30s to run
**Cause**: Sample projects too large or network requests
**Solution**:
- Use minimal sample projects (< 10 files each)
- Mock network requests
- Run benchmarks separately: `pytest tests/ -m "not benchmark"`

---

## References

- pytest documentation: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/
- pytest-benchmark: https://pytest-benchmark.readthedocs.io/
- Anthropic Skills Cookbook: https://github.com/anthropics/claude-cookbooks/tree/main/skills

---

**Last Updated**: 2025-10-23
**Status**: 🚧 Under Development (v0.5.0)
**Target Release**: 2025-11
