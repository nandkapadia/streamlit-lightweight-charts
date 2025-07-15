# PyPI Release Guide for streamlit-lightweight-charts v0.8.0

## Prerequisites

Before releasing to PyPI, ensure you have:

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **TestPyPI Account**: Create an account at https://test.pypi.org/account/register/
3. **API Tokens**: Generate API tokens for both PyPI and TestPyPI

## Step 1: Install Required Tools

```bash
pip install build twine
```

## Step 2: Clean Previous Builds

```bash
# Remove any existing build artifacts
rm -rf build/ dist/ *.egg-info/
```

## Step 3: Test Build Locally

```bash
# Test the build process
python -m build

# Check the built package
ls -la dist/
```

## Step 4: Test Upload to TestPyPI

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ streamlit-lightweight-charts==0.8.0
```

## Step 5: Verify Package Contents

```bash
# Check package contents
tar -tzf dist/streamlit_lightweight_charts-0.8.0.tar.gz | head -20

# Verify frontend files are included
tar -tzf dist/streamlit_lightweight_charts-0.8.0.tar.gz | grep frontend
```

## Step 6: Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

## Step 7: Verify Installation

```bash
# Test installation from PyPI
pip install streamlit-lightweight-charts==0.8.0

# Test import
python -c "from streamlit_lightweight_charts import __version__; print(__version__)"
```

## Important Notes

### Package Structure Verification
- ✅ Frontend build files are present in `streamlit_lightweight_charts/frontend/build/`
- ✅ MANIFEST.in includes frontend build files
- ✅ Version is consistently set to 0.8.0 across all files
- ✅ Package name is consistent: `streamlit-lightweight-charts`

### Dependencies
- Core dependency: `streamlit>=1.0`
- Optional dependencies: `pandas>=1.0`, `numpy>=1.19` (for examples)

### Files Included in Package
- Python source code
- Frontend React build files
- README.md
- LICENSE
- Type definitions
- Examples (in extras_require)

## Troubleshooting

### Common Issues

1. **Frontend Build Missing**
   ```bash
   # Rebuild frontend if needed
   cd streamlit_lightweight_charts/frontend
   npm install
   npm run build
   cd ../..
   ```

2. **Authentication Issues**
   ```bash
   # Use API tokens instead of username/password
   twine upload --username __token__ --password pypi-TOKEN dist/*
   ```

3. **Package Already Exists**
   - Check if version 0.8.0 already exists on PyPI
   - If so, increment version number

### Pre-Release Checklist

- [ ] All version numbers are set to 0.8.0
- [ ] Frontend build files are present and up-to-date
- [ ] Tests pass: `pytest`
- [ ] Package builds successfully: `python -m build`
- [ ] Package installs correctly from local build
- [ ] README.md is up-to-date
- [ ] LICENSE file is present
- [ ] No debug files in the package

## Post-Release

1. **Tag the Release**
   ```bash
   git tag v0.8.0
   git push origin v0.8.0
   ```

2. **Create GitHub Release**
   - Go to GitHub repository
   - Create new release with tag v0.8.0
   - Add release notes

3. **Update Documentation**
   - Update any version-specific documentation
   - Update example requirements if needed

## Version History

- v0.7.19 - FIX: React build was not been commited
- v0.7.20 - Example loading from CSV
- v0.8.0 - OOP API with composite charts, trade visualization, and annotation systems 