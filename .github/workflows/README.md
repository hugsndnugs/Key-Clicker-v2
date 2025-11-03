# CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing, building, and releasing.

## Workflows

### `ci-cd.yml` - Main CI/CD Pipeline

This workflow handles:

1. **Linting & Testing** (runs on all pushes and PRs)
   - Python syntax validation
   - Code linting with flake8
   - Import validation

2. **Cross-Platform Builds** (runs after linting passes)
   - **Windows**: Builds `AutoKeyClicker.exe`
   - **macOS**: Builds `AutoKeyClicker`
   - **Linux**: Builds `AutoKeyClicker`

3. **Release Creation** (runs on version tags)
   - Automatically creates release archives when a tag starting with `v` is pushed
   - Creates `.zip` files for Windows and macOS
   - Creates `.tar.gz` file for Linux
   - Uploads all artifacts to the GitHub release

## Usage

### Running CI Locally

While you can't run GitHub Actions locally, you can simulate the checks:

```bash
# Install dependencies
pip install -r requirements.txt flake8 pytest

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Validate syntax
python -m py_compile key_clicker.py build.py

# Test imports
python -c "import key_clicker; print('✓ All imports successful')"

# Build executable
python build.py
```

### Creating a Release

1. **Tag your release:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **The workflow will automatically:**
   - Run all tests and linting
   - Build executables for all platforms
   - Create release archives
   - Upload them to the GitHub release

3. **Alternatively, create a release manually:**
   - Go to GitHub Releases page
   - Click "Draft a new release"
   - Create a tag (e.g., `v1.0.0`)
   - The workflow will build and attach artifacts

### Manual Workflow Dispatch

You can also trigger the workflow manually:

1. Go to the "Actions" tab in GitHub
2. Select "CI/CD Pipeline"
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## Workflow Triggers

- **Push** to `main`, `master`, or `develop` branches
- **Pull Requests** to `main`, `master`, or `develop` branches
- **Tags** starting with `v` (e.g., `v1.0.0`)
- **Releases** created via GitHub UI
- **Manual** dispatch via GitHub Actions UI

## Artifacts

Build artifacts are stored for 30 days and can be downloaded from:
- The workflow run page
- The GitHub release page (for tagged releases)

## Notes

- Builds require all dependencies from `requirements.txt`
- Linux builds require `python3-tk` system package
- macOS and Linux executables may require `chmod +x` to be executable
- Windows builds create `.exe` files automatically

