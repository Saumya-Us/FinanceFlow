# Installation Guide

This guide will help you set up the Personal Finance Tracker on your local machine.

## Prerequisites

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads) (optional, for cloning)

## Installation Methods

### Method 1: Using Git (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

2. **Create a virtual environment** (recommended)
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

### Method 2: Download ZIP

1. **Download** the repository as a ZIP file from GitHub
2. **Extract** the ZIP file to your desired location
3. **Open terminal/command prompt** in the extracted folder
4. **Create virtual environment and install** (same as steps 2-4 above)

## First Run

When you first run the application:

1. The SQLite database (`finance.db`) will be created automatically
2. A default user will be created
3. The app will open in your browser at `http://localhost:8501`

## Adding Sample Data

To test the app with realistic data:

```bash
python seed_data.py
```

This generates 6 months of sample transactions including:
- Monthly salary payments
- Random freelance income
- Diverse expenses across categories

## Troubleshooting

### Port Already in Use

If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Error

Make sure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Permission Denied

On macOS/Linux, you might need to use `python3` instead of `python`:
```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

### Database Locked Error

If you get a "database is locked" error:
1. Close all instances of the app
2. Delete `finance.db`
3. Restart the app

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: ~100MB for installation
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

1. **Deactivate virtual environment**
```bash
deactivate
```

2. **Delete the project folder**
```bash
cd ..
rm -rf personal-finance-tracker  # On macOS/Linux
# or manually delete the folder on Windows
```

## Development Installation

For contributors:

```bash
# Clone your fork
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker

# Add upstream remote
git remote add upstream https://github.com/original-owner/personal-finance-tracker.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a new branch
git checkout -b feature/your-feature-name
```

## Next Steps

After installation:

1. 📚 Read the [README.md](README.md) for features overview
2. 🎯 Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
3. 🚀 Start tracking your finances!

## Support

If you encounter any issues:

1. Check the [troubleshooting section](#troubleshooting) above
2. Search [existing issues](https://github.com/yourusername/personal-finance-tracker/issues)
3. Create a [new issue](https://github.com/yourusername/personal-finance-tracker/issues/new) with details

---

Happy tracking! 💰
