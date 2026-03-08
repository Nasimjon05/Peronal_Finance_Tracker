#Functions
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

def add_transaction(connection):
    t_type = str(input('Type of transaction (income/expense): '))
    category = str(input('Category (food, rent, salary, transport, etc): '))
    amount = float(input('Amount: '))
    description = str(input('Description: '))
    
    cursor = connection.cursor()
    
    query = """
    INSERT INTO transactions (type, category, amount, description, date)
    VALUES (%s, %s, %s, %s, CURRENT_DATE)
    """
    
    cursor.execute(query, (t_type, category, amount, description))
    connection.commit()
    
    print("Transaction added successfully!")
    cursor.close()

def view_all_transactions(connection):
    cursor = connection.cursor()

    query = """
                SELECT id, type, category, amount, description
                FROM transactions
                ORDER BY date DESC
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    headers = ["ID", "Date", "Type", "Category", "Amount", "Description"]
    print(tabulate(rows, headers=headers, tablefmt="pretty"))
    
    cursor.close()
            
def view_by_category(connection):
    category = str(input('Write a category name to filter: '))

    cursor = connection.cursor()

    query = """
                SELECT id, type, category, amount, description
                FROM transactions
                WHERE category = %s
                ORDER BY date DESC
            """
    cursor.execute(query,(category,))
    rows = cursor.fetchall()

    headers = [ 'ID', "Category","Type","Amount","Description"]
    print(tabulate(rows, headers=headers, tablefmt='pretty'))

def get_summary(connection):
    cursor = connection.cursor()
    
    query = """
    SELECT 
        SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
        SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expenses,
        SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) AS net_balance
    FROM transactions
    """
    
    cursor.execute(query)
    row = cursor.fetchone()
    
    print("\n========= FINANCIAL SUMMARY =========")
    print(f"Total Income:    {row[0] or 0:,.2f}")
    print(f"Total Expenses:  {row[1] or 0:,.2f}")
    print(f"Net Balance:     {row[2] or 0:,.2f}")
    print("=====================================\n")
    
    cursor.close()

def delete_transaction(connection):
    view_all_transactions(connection)
    
    t_id = int(input("Enter the ID of transaction to delete: "))
    
    cursor = connection.cursor()
    
    query = "DELETE FROM transactions WHERE id = %s"
    
    cursor.execute(query, (t_id,))
    connection.commit()
    
    if cursor.rowcount > 0:
        print(f"Transaction {t_id} deleted successfully!")
    else:
        print(f"No transaction found with ID {t_id}")
    
    cursor.close()

def show_charts(connection):
    cursor = connection.cursor()
    
    query = """
    SELECT category, SUM(amount) as total
    FROM transactions
    WHERE type = 'expense'
    GROUP BY category
    ORDER BY total DESC
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    if not rows:
        print("No expense data to display yet!")
        return
    
    df = pd.DataFrame(rows, columns=["Category", "Amount"])
    
    # Bar chart - spending by category
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(df["Category"], df["Amount"], color="tomato")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    
    # Pie chart - proportion of spending
    plt.subplot(1, 2, 2)
    plt.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%", startangle=140)
    plt.title("Spending Distribution")
    
    plt.tight_layout()
    plt.show()