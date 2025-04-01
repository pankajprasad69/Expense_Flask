import csv
from datetime import datetime
from collections import defaultdict

EXPENSES_FILE = "expenses.csv"

def set_file_path():
    """Set a custom file path for the expenses file."""
    global EXPENSES_FILE
    new_path = input("Enter the new file path for expenses (must end with .csv): ")
    if not new_path.lower().endswith(".csv"):
        new_path += ".csv"  # Ensure the file has a .csv extension
    EXPENSES_FILE = new_path
    print(f"File path updated to: {EXPENSES_FILE}")

def add_expense():
    """Add a new expense entry."""
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter the category (e.g., Food, Transport, Bills): ")
    description = input("Enter a description for the expense: ")
    amount = input("Enter the amount spent: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    # Check if the file exists and is empty
    file_exists = False
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            file_exists = True
            if file.read().strip() == "":  # Check if the file is empty
                file_exists = False
    except FileNotFoundError:
        pass

    try:
        with open(EXPENSES_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Write the header row
                writer.writerow(["Date", "Category", "Description", "Amount"])
            writer.writerow([date, category, description, amount])
            print("Expense added successfully!")
    except PermissionError:
        print(f"Permission denied: Unable to write to '{EXPENSES_FILE}'. Ensure the file is not open or locked.")

def view_expenses():
    """View all recorded expenses."""
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Read the header row
            if header:
                print(f"{header[0]:<12} {header[1]:<15} {header[2]:<30} {header[3]:<10}")
                print("-" * 70)
            total = 0
            for row in reader:
                print(f"{row[0]:<12} {row[1]:<15} {row[2]:<30} {row[3]:<10}")
                total += float(row[3])
            print("-" * 70)
            print(f"{'Total':<12} {'':<15} {'':<30} {total:<10.2f}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def delete_expense():
    """Delete an expense entry."""
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            rows = list(csv.reader(file))
        
        print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Description':<30} {'Amount':<10}")
        print("-" * 80)
        for index, row in enumerate(rows):
            print(f"{index:<6} {row[0]:<12} {row[1]:<15} {row[2]:<30} {row[3]:<10}")
        
        index_to_delete = input("Enter the index of the expense to delete: ")
        try:
            index_to_delete = int(index_to_delete)
            if 0 <= index_to_delete < len(rows):
                del rows[index_to_delete]
                with open(EXPENSES_FILE, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                print("Expense deleted successfully!")
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a numeric index.")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def edit_expense():
    """Edit an existing expense entry."""
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            rows = list(csv.reader(file))

        if len(rows) <= 1:  # Check if there are no expenses (only header exists)
            print("No expenses recorded yet.")
            return

        print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Description':<30} {'Amount':<10}")
        print("-" * 80)
        for index, row in enumerate(rows[1:], start=1):  # Skip the header row
            print(f"{index:<6} {row[0]:<12} {row[1]:<15} {row[2]:<30} {row[3]:<10}")

        index_to_edit = input("Enter the index of the expense to edit: ")
        try:
            index_to_edit = int(index_to_edit)
            if 1 <= index_to_edit < len(rows):
                # Display the current values
                print("Current values:")
                print(f"Date: {rows[index_to_edit][0]}")
                print(f"Category: {rows[index_to_edit][1]}")
                print(f"Description: {rows[index_to_edit][2]}")
                print(f"Amount: {rows[index_to_edit][3]}")

                # Prompt for new values
                new_date = input("Enter new date (YYYY-MM-DD) or press Enter to keep current: ")
                new_category = input("Enter new category or press Enter to keep current: ")
                new_description = input("Enter new description or press Enter to keep current: ")
                new_amount = input("Enter new amount or press Enter to keep current: ")

                # Update only the fields that are provided
                if new_date.strip():
                    rows[index_to_edit][0] = new_date
                if new_category.strip():
                    rows[index_to_edit][1] = new_category
                if new_description.strip():
                    rows[index_to_edit][2] = new_description
                if new_amount.strip():
                    try:
                        rows[index_to_edit][3] = str(float(new_amount))
                    except ValueError:
                        print("Invalid amount. Keeping the current value.")

                # Write the updated rows back to the file
                with open(EXPENSES_FILE, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                print("Expense updated successfully!")
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a numeric index.")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def monthly_summary():
    """Show a summary of expenses grouped by month."""
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            monthly_totals = defaultdict(float)
            header = next(reader, None)  # Skip the header row
            for row in reader:
                if row:  # Ensure the row is not empty
                    date = row[0]
                    amount = float(row[3])
                    month = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")  # Convert to "Month Year"
                    monthly_totals[month] += amount
            
            print(f"{'Month':<15} {'Total Expense':<15}")
            print("-" * 30)
            for month, total in sorted(monthly_totals.items()):
                print(f"{month:<15} {total:<15.2f}")
    except FileNotFoundError:
        print("No expenses recorded yet.")
    except ValueError:
        print("Error processing the file. Ensure all rows have valid data.")

def main():
    """Main function to run the expense tracker."""
    print("Welcome to the Daily Expense Tracker!")
    while True:
        print("\nOptions:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Monthly Summary")
        print("6. Set File Path")
        print("7. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6/7): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            edit_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            set_file_path()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()