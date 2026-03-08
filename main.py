from db_connection import create_connection
from functions import (
    add_transaction,
    view_all_transactions,
    view_by_category,
    get_summary,
    delete_transaction,
    show_charts
)

connection = create_connection()

while True:
    print("\n========= PERSONAL FINANCE TRACKER =========")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. View by Category")
    print("4. Financial Summary")
    print("5. Show Charts")
    print("6. Delete Transaction")
    print("7. Exit")
    print("=============================================")
    
    choice = input("Choose an option (1-7): ")
    
    if choice == "1":
        add_transaction(connection)
    elif choice == "2":
        view_all_transactions(connection)
    elif choice == "3":
        view_by_category(connection)
    elif choice == "4":
        get_summary(connection)
    elif choice == "5":
        show_charts(connection)
    elif choice == "6":
        delete_transaction(connection)
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid option, please choose between 1-7")
