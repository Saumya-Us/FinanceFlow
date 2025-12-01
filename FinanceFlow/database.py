import sqlite3
import pandas as pd
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceDatabase:
    """Database handler for Personal Finance Tracker with improved error handling and security"""
    
    def __init__(self, db_name: str = "finance.db"):
        """Initialize database connection and create tables if they don't exist
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections with error handling
        
        Yields:
            sqlite3.Connection: Database connection object
        """
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_name,
                isolation_level='IMMEDIATE',
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _execute_query(self, query: str, params: tuple = (), fetch: bool = True, commit: bool = False):
        """Execute a database query with error handling
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters
            fetch (bool): Whether to fetch results
            commit (bool): Whether to commit the transaction
            
        Returns:
            Union[list, int]: Query results or last row ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                if fetch:
                    return cursor.fetchall()
                return cursor.lastrowid
            except sqlite3.Error as e:
                conn.rollback()
                logger.error(f"Query failed: {query} - {e}")
                raise
    
    def _init_database(self):
        """Create tables if they don't exist with proper constraints and indexes"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Enable foreign key constraints
                cursor.execute("PRAGMA foreign_keys = ON")
                
                # Create users table with better schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT username_length CHECK (length(username) >= 3)
                    )
                ''')
                
                # Create categories table for better category management
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL, -- 'Income' or 'Expense'
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, name, type),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        CONSTRAINT valid_type CHECK (type IN ('Income', 'Expense'))
                    )
                ''')
                
                # Create transactions table with improved schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT,
                        date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        CONSTRAINT amount_positive CHECK (amount > 0),
                        CONSTRAINT valid_type CHECK (type IN ('Income', 'Expense'))
                    )
                ''')
                
                # Create indexes for better query performance
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
                    ON transactions(user_id, date DESC)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_transactions_category 
                    ON transactions(user_id, category)
                ''')
                
                # Create default user if not exists (in a more secure way)
                cursor.execute('''
                    INSERT OR IGNORE INTO users (id, username) 
                    VALUES (1, 'default_user')
                ''')
                
                # Create default categories if they don't exist
                default_income_categories = [
                    (1, 'Salary', 'Income'),
                    (1, 'Freelance', 'Income'),
                    (1, 'Investment', 'Income'),
                    (1, 'Gift', 'Income'),
                    (1, 'Other Income', 'Income')
                ]
                
                default_expense_categories = [
                    (1, 'Food', 'Expense'),
                    (1, 'Transport', 'Expense'),
                    (1, 'Shopping', 'Expense'),
                    (1, 'Bills', 'Expense'),
                    (1, 'Entertainment', 'Expense'),
                    (1, 'Healthcare', 'Expense'),
                    (1, 'Education', 'Expense'),
                    (1, 'Rent', 'Expense'),
                    (1, 'Other Expense', 'Expense')
                ]
                
                cursor.executemany('''
                    INSERT OR IGNORE INTO categories (user_id, name, type)
                    VALUES (?, ?, ?)
                ''', default_income_categories + default_expense_categories)
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def add_transaction(
        self, 
        user_id: int, 
        trans_type: str, 
        amount: float, 
        category: str, 
        transaction_date: Union[str, date],
        description: str = ""
    ) -> bool:
        """Add a new transaction with validation
        
        Args:
            user_id: ID of the user
            trans_type: Type of transaction ('Income' or 'Expense')
            amount: Transaction amount (must be positive)
            category: Transaction category
            transaction_date: Date of the transaction (YYYY-MM-DD or date object)
            description: Optional description
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            ValueError: If validation fails
            sqlite3.Error: If database operation fails
        """
        try:
            # Convert date to string if it's a date object
            if isinstance(transaction_date, date):
                transaction_date = transaction_date.isoformat()
                
            query = """
                INSERT INTO transactions (user_id, type, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (user_id, trans_type, amount, category, description, transaction_date)
            self._execute_query(query, params, fetch=False, commit=True)
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Failed to add transaction: {e}")
            raise
    
    def get_summary(self, user_id: int, start_date: str, end_date: str) -> dict:
        """Get financial summary for a user within a date range
        
        Args:
            user_id: ID of the user
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            dict: Dictionary containing summary statistics
        """
        try:
            # Get total income
            income_query = """
                SELECT COALESCE(SUM(amount), 0) as total
                FROM transactions
                WHERE user_id = ? AND type = 'Income' AND date BETWEEN ? AND ?
            """
            income_result = self._execute_query(income_query, (user_id, start_date, end_date))
            total_income = income_result[0]['total'] if income_result else 0
            
            # Get total expenses
            expense_query = """
                SELECT COALESCE(SUM(amount), 0) as total
                FROM transactions
                WHERE user_id = ? AND type = 'Expense' AND date BETWEEN ? AND ?
            """
            expense_result = self._execute_query(expense_query, (user_id, start_date, end_date))
            total_expense = expense_result[0]['total'] if expense_result else 0
            
            # Get transaction count
            count_query = """
                SELECT COUNT(*) as count
                FROM transactions
                WHERE user_id = ? AND date BETWEEN ? AND ?
            """
            count_result = self._execute_query(count_query, (user_id, start_date, end_date))
            transaction_count = count_result[0]['count'] if count_result else 0
            
            return {
                'total_income': float(total_income),
                'total_expense': float(total_expense),
                'balance': float(total_income - total_expense),
                'transaction_count': transaction_count
            }
            
        except sqlite3.Error as e:
            logger.error(f"Failed to get summary: {e}")
            return {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'transaction_count': 0
            }
    
    def get_transactions(
        self, 
        user_id: int, 
        start_date: str, 
        end_date: str, 
        category: str = None
    ) -> pd.DataFrame:
        """Get transactions for a user within a date range, optionally filtered by category
        
        Args:
            user_id: ID of the user
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            category: Optional category to filter by
            
        Returns:
            pd.DataFrame: DataFrame containing transactions
        """
        try:
            query = """
                SELECT id, type, amount, category, description, date, created_at
                FROM transactions
                WHERE user_id = ? AND date BETWEEN ? AND ?
            """
            params = [user_id, start_date, end_date]
            
            if category and category != 'All':
                query += " AND category = ?"
                params.append(category)
                
            query += " ORDER BY date DESC"
            
            result = self._execute_query(query, tuple(params))
            
            # Convert to DataFrame
            if result:
                df = pd.DataFrame(result, columns=result[0].keys())
                # Convert date strings to datetime objects
                df['date'] = pd.to_datetime(df['date']).dt.date
                df['created_at'] = pd.to_datetime(df['created_at'])
                return df
            return pd.DataFrame()
            
        except sqlite3.Error as e:
            logger.error(f"Failed to get transactions: {e}")
            return pd.DataFrame()
    
    def get_all_categories(self, user_id: int) -> list:
        """Get all unique categories for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            list: List of unique categories
        """
        try:
            query = """
                SELECT DISTINCT category
                FROM transactions
                WHERE user_id = ?
                ORDER BY category
            """
            result = self._execute_query(query, (user_id,))
            return [row['category'] for row in result]
        except sqlite3.Error as e:
            logger.error(f"Failed to get categories: {e}")
            return []
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        trans_type = trans_type.capitalize()
        if trans_type not in ('Income', 'Expense'):
            raise ValueError("Transaction type must be 'Income' or 'Expense'")
            
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except (ValueError, TypeError):
            raise ValueError("Invalid amount")
            
        if not category or not isinstance(category, str):
            raise ValueError("Category is required")
            
        try:
            if isinstance(transaction_date, str):
                transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()
            elif not isinstance(transaction_date, date):
                raise ValueError("Invalid date format")
                
            # Ensure the date is not in the future
            if transaction_date > date.today():
                raise ValueError("Transaction date cannot be in the future")
                
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
            
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if category exists for the user
                cursor.execute('''
                    SELECT 1 FROM categories 
                    WHERE user_id = ? AND name = ? AND type = ?
                ''', (user_id, category, trans_type))
                
                if not cursor.fetchone():
                    # Add the new category
                    cursor.execute('''
                        INSERT INTO categories (user_id, name, type)
                        VALUES (?, ?, ?)
                    ''', (user_id, category, trans_type))
                
                # Insert the transaction
                cursor.execute('''
                    INSERT INTO transactions 
                    (user_id, type, amount, category, date, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, 
                    trans_type, 
                    round(amount, 2),  # Round to 2 decimal places
                    category, 
                    transaction_date, 
                    description[:255]  # Limit description length
                ))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logger.error(f"Failed to add transaction: {e}")
            raise
    
    def get_transactions(
        self, 
        user_id: int, 
        start_date: Optional[Union[str, date]] = None, 
        end_date: Optional[Union[str, date]] = None, 
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> pd.DataFrame:
        """Get transactions with optional filters and pagination
        
        Args:
            user_id: ID of the user
            start_date: Optional start date (inclusive)
            end_date: Optional end date (inclusive)
            category: Optional category filter
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            pd.DataFrame: DataFrame containing the transactions
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        # Convert date strings to date objects
        try:
            if start_date and isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                
            if end_date and isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                
            if start_date and end_date and start_date > end_date:
                raise ValueError("Start date cannot be after end date")
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {e}")
            
        try:
            query = """
                SELECT 
                    id,
                    type,
                    amount,
                    category,
                    description,
                    date,
                    created_at
                FROM transactions 
                WHERE user_id = :user_id
            """
            
            params = {"user_id": user_id}
            
            # Add date filters
            if start_date:
                query += " AND date >= :start_date"
                params["start_date"] = start_date
                
            if end_date:
                query += " AND date <= :end_date"
                params["end_date"] = end_date
            
            # Add category filter
            if category and category != "All":
                query += " AND category = :category"
                params["category"] = category
            
            # Add sorting
            query += " ORDER BY date DESC, created_at DESC"
            
            # Add pagination
            if limit is not None:
                query += " LIMIT :limit OFFSET :offset"
                params["limit"] = limit
                params["offset"] = offset
            
            # Use parameterized query to prevent SQL injection
            with self._get_connection() as conn:
                df = pd.read_sql_query(
                    query, 
                    conn, 
                    params=params,
                    parse_dates=['date', 'created_at']
                )
                
            return df
            
        except sqlite3.Error as e:
            logger.error(f"Failed to get transactions: {e}")
            raise
    
    def get_summary(
        self, 
        user_id: int, 
        start_date: Optional[Union[str, date]] = None, 
        end_date: Optional[Union[str, date]] = None
    ) -> Dict[str, Any]:
        """Get financial summary with improved performance
        
        Args:
            user_id: ID of the user
            start_date: Optional start date (inclusive)
            end_date: Optional end date (inclusive)
            
        Returns:
            dict: Summary containing total_income, total_expense, balance, and transaction_count
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        try:
            query = """
                SELECT 
                    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as total_expense,
                    COUNT(*) as transaction_count
                FROM transactions 
                WHERE user_id = :user_id
            """
            
            params = {"user_id": user_id}
            
            # Add date filters
            if start_date:
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                query += " AND date >= :start_date"
                params["start_date"] = start_date
                
            if end_date:
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                query += " AND date <= :end_date"
                params["end_date"] = end_date
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                
                if not result or result[0] is None:  # No transactions found
                    return {
                        'total_income': 0.0,
                        'total_expense': 0.0,
                        'balance': 0.0,
                        'transaction_count': 0
                    }
                
                total_income = float(result[0] or 0)
                total_expense = float(result[1] or 0)
                transaction_count = result[2] or 0
                
                return {
                    'total_income': round(total_income, 2),
                    'total_expense': round(total_expense, 2),
                    'balance': round(total_income - total_expense, 2),
                    'transaction_count': transaction_count
                }
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {e}")
        except sqlite3.Error as e:
            logger.error(f"Failed to get summary: {e}")
            raise
    
    def get_expense_by_category(
        self, 
        user_id: int, 
        start_date: Optional[Union[str, date]] = None, 
        end_date: Optional[Union[str, date]] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """Get expenses grouped by category with improved performance
        
        Args:
            user_id: ID of the user
            start_date: Optional start date (inclusive)
            end_date: Optional end date (inclusive)
            limit: Optional limit on number of categories to return
            
        Returns:
            pd.DataFrame: DataFrame with columns 'category' and 'amount'
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        try:
            query = """
                SELECT 
                    category,
                    SUM(amount) as amount
                FROM transactions 
                WHERE user_id = :user_id 
                AND type = 'Expense'
            """
            
            params = {"user_id": user_id}
            
            # Add date filters
            if start_date:
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                query += " AND date >= :start_date"
                params["start_date"] = start_date
                
            if end_date:
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                query += " AND date <= :end_date"
                params["end_date"] = end_date
            
            # Group and sort
            query += " GROUP BY category"
            query += " ORDER BY amount DESC"
            
            # Add limit if specified
            if limit is not None:
                query += " LIMIT :limit"
                params["limit"] = limit
            
            with self._get_connection() as conn:
                df = pd.read_sql_query(query, conn, params=params)
                
                # Ensure consistent return format
                if df.empty:
                    return pd.DataFrame(columns=['category', 'amount'])
                    
                return df
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format: {e}")
        except sqlite3.Error as e:
            logger.error(f"Failed to get expenses by category: {e}")
            raise
    
    def get_monthly_trend(
        self, 
        user_id: int, 
        months: int = 12
    ) -> pd.DataFrame:
        """Get monthly income vs expense trend for the specified number of months
        
        Args:
            user_id: ID of the user
            months: Number of months of data to return (default: 12)
            
        Returns:
            pd.DataFrame: DataFrame with columns 'month', 'type', and 'total'
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        if not isinstance(months, int) or months <= 0:
            raise ValueError("Months must be a positive integer")
            
        try:
            # Calculate the start date (months ago from today)
            from datetime import date, timedelta
            end_date = date.today()
            start_date = (end_date - timedelta(days=months*30)).replace(day=1)
            
            query = """
                WITH RECURSIVE months(month) AS (
                    SELECT :start_date
                    UNION ALL
                    SELECT date(month, '+1 month')
                    FROM months
                    WHERE month < date(:end_date, 'start of month')
                )
                SELECT 
                    strftime('%Y-%m', m.month) as month,
                    t.type,
                    COALESCE(SUM(tr.amount), 0) as total
                FROM months m
                CROSS JOIN (SELECT 'Income' as type UNION SELECT 'Expense') t
                LEFT JOIN transactions tr ON 
                    strftime('%Y-%m', tr.date) = strftime('%Y-%m', m.month) AND
                    tr.user_id = :user_id AND
                    tr.type = t.type
                GROUP BY m.month, t.type
                ORDER BY m.month, t.type
            """
            
            params = {
                'user_id': user_id,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            
            with self._get_connection() as conn:
                df = pd.read_sql_query(query, conn, params=params)
                
                # Ensure we have all months in the range, even with no transactions
                if not df.empty:
                    # Pivot the data for easier analysis
                    pivot_df = df.pivot(index='month', columns='type', values='total').fillna(0)
                    
                    # Ensure both Income and Expense columns exist
                    for col in ['Income', 'Expense']:
                        if col not in pivot_df.columns:
                            pivot_df[col] = 0.0
                    
                    # Reset index to make month a column again
                    result_df = pivot_df.reset_index()
                    
                    # Calculate balance
                    result_df['Balance'] = result_df['Income'] - result_df['Expense']
                    
                    return result_df
                
                return pd.DataFrame(columns=['month', 'Income', 'Expense', 'Balance'])
                
        except sqlite3.Error as e:
            logger.error(f"Failed to get monthly trend: {e}")
            raise
    
    def get_all_categories(
        self, 
        user_id: int, 
        trans_type: Optional[str] = None
    ) -> List[str]:
        """Get all unique categories for a user, optionally filtered by type
        
        Args:
            user_id: ID of the user
            trans_type: Optional type filter ('Income' or 'Expense')
            
        Returns:
            List[str]: List of category names
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        if trans_type and trans_type.capitalize() not in ('Income', 'Expense'):
            raise ValueError("Type must be 'Income' or 'Expense'")
            
        try:
            query = """
                SELECT DISTINCT name 
                FROM categories 
                WHERE user_id = :user_id
            """
            
            params = {"user_id": user_id}
            
            if trans_type:
                query += " AND type = :type"
                params["type"] = trans_type.capitalize()
                
            query += " ORDER BY name"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [row[0] for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            logger.error(f"Failed to get categories: {e}")
            raise
    
    def delete_transaction(self, user_id: int, transaction_id: int) -> bool:
        """Delete a transaction with validation
        
        Args:
            user_id: ID of the user making the request
            transaction_id: ID of the transaction to delete
            
        Returns:
            bool: True if successful, False if transaction not found
            
        Raises:
            ValueError: If input validation fails
            sqlite3.Error: If database operation fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        if not isinstance(transaction_id, int) or transaction_id <= 0:
            raise ValueError("Invalid transaction ID")
            
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # First verify the transaction exists and belongs to the user
                cursor.execute('''
                    SELECT 1 FROM transactions 
                    WHERE id = ? AND user_id = ?
                ''', (transaction_id, user_id))
                
                if not cursor.fetchone():
                    return False  # Transaction not found or not owned by user
                
                # Delete the transaction
                cursor.execute('''
                    DELETE FROM transactions 
                    WHERE id = ? AND user_id = ?
                ''', (transaction_id, user_id))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logger.error(f"Failed to delete transaction {transaction_id}: {e}")
            raise
