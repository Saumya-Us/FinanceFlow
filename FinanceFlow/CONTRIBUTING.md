# Contributing to Personal Finance Tracker

First off, thank you for considering contributing to Personal Finance Tracker! It's people like you that make this tool better for everyone.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List some examples of how it would be used**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Follow the coding style** of the project
6. **Submit your pull request**

## 💻 Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

## 📝 Coding Guidelines

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Comment complex logic

### Code Organization
- Keep related code together
- Separate concerns (UI, database, business logic)
- Use type hints where appropriate
- Handle errors gracefully

### Database Changes
- Always test database migrations locally
- Ensure backward compatibility when possible
- Document any schema changes

### UI/UX
- Maintain consistent design language
- Ensure responsive layouts
- Add helpful error messages
- Keep the user experience intuitive

## 🧪 Testing

Before submitting a pull request:

1. Test all new features manually
2. Test with the mock data: `python seed_data.py`
3. Verify no errors in the console
4. Test on different screen sizes if UI changes were made

## 📋 Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Reference issues when applicable

Good examples:
```
Add budget tracking feature
Fix date filter bug in analytics
Update README with new screenshots
```

## 🎯 Priority Areas

We're especially interested in contributions for:

- User authentication and multi-user support
- Budget tracking and alerts
- Recurring transactions
- Data import/export features
- Mobile responsiveness
- Advanced analytics and visualizations
- Performance improvements
- Documentation improvements

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to open an issue with your question or reach out to the maintainers.

---

Thank you for contributing! 🎉
