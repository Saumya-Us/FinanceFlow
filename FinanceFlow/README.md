# 💰 Personal Finance Tracker

A beautiful and intuitive personal finance management application built with **Streamlit** and **SQLite**. Track your income, expenses, and visualize your spending patterns with interactive charts and analytics.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📊 Dashboard
- **Real-time Overview**: View your financial summary at a glance
- **Key Metrics**: Total income, expenses, balance, and transaction count
- **Recent Transactions**: Quick access to your latest financial activities
- **Date Filtering**: Analyze your finances for any time period

### ➕ Transaction Management
- **Add Income**: Record salary, freelance work, investments, and more
- **Add Expenses**: Track spending across multiple categories
- **Custom Categories**: Organized categories for both income and expenses
- **Detailed Descriptions**: Add notes to remember transaction details

### 📝 Transaction History
- **Complete History**: View all your transactions in one place
- **Advanced Filtering**: Filter by date range and category
- **CSV Export**: Download your transaction data for external analysis
- **Search & Sort**: Easily find specific transactions

### 📈 Analytics & Visualizations
- **Pie Chart**: Visual breakdown of expenses by category
- **Trend Analysis**: Line chart showing income vs expenses over time
- **Monthly Summaries**: Track your financial progress month by month
- **Category Insights**: Identify your biggest spending categories

## 🖼️ Screenshots

*Dashboard View*
> Add your dashboard screenshot here

*Add Transaction*
> Add your add transaction screenshot here

*Analytics*
> Add your analytics screenshot here

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**
The app will automatically open at `http://localhost:8501`

### 🌱 Seed Mock Data (Optional)

To test the app with sample data:
```bash
python seed_data.py
```

This will generate 6 months of realistic transaction data including:
- Monthly salary payments
- Random income from freelance and other sources
- Diverse expenses across all categories

## 📁 Project Structure

```
personal-finance-tracker/
│
├── app.py                 # Main Streamlit application
├── database.py            # Database operations and queries
├── seed_data.py          # Mock data generator
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore           # Git ignore rules
├── finance.db           # SQLite database (generated on first run)
└── .streamlit/
    └── config.toml      # Streamlit configuration
```

## 💻 Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[SQLite](https://www.sqlite.org/)** - Lightweight database
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[Matplotlib](https://matplotlib.org/)** - Data visualization
- **Python 3.11+** - Programming language

## 🎯 Usage Guide

### Adding a Transaction
1. Navigate to **➕ Add Transaction** from the sidebar
2. Select transaction type (Income or Expense)
3. Choose a category
4. Enter the amount and date
5. Add an optional description
6. Click **Add Transaction**

### Viewing Analytics
1. Go to **📈 Analytics** from the sidebar
2. Select your desired date range
3. View pie charts for expense distribution
4. Analyze income vs expense trends

### Exporting Data
1. Navigate to **📝 View Transactions**
2. Apply your desired filters
3. Click **📥 Download CSV Report**

## 🛠️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions
- Add user authentication and multi-user support
- Implement budget tracking and alerts
- Add recurring transaction support
- Create mobile-responsive design
- Add data backup/restore functionality
- Implement advanced analytics and predictions

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Personal Finance Tracker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🐛 Known Issues

None at the moment! If you find any bugs, please [open an issue](https://github.com/yourusername/personal-finance-tracker/issues).

## 🔮 Future Enhancements

- [ ] User authentication system
- [ ] Budget planning and alerts
- [ ] Recurring transactions
- [ ] Multi-currency support
- [ ] Mobile app version
- [ ] Data import from bank statements
- [ ] AI-powered spending insights
- [ ] Bill reminders

## 📧 Contact

For questions or suggestions, please open an issue or reach out to the maintainer.

---

**Made with ❤️ using Python and Streamlit**

⭐ Star this repository if you find it helpful!
