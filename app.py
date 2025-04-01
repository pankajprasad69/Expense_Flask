from flask import Flask, render_template, request, redirect, url_for # type: ignore
import csv
from datetime import datetime
from Expense import EXPENSES_FILE, add_expense, view_expenses, delete_expense, edit_expense, monthly_summary

app = Flask(__name__)

# Route for the home page
@app.route("/")
def home():
    expenses = []
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header row
            expenses = list(reader)  # Read all rows into a list
    except FileNotFoundError:
        print("File not found: expenses.csv")
    print("Expenses:", expenses)  # Debugging: Print the expenses list to the console
    return render_template("index.html", expenses=expenses)

# Route to add a new expense
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        category = request.form["category"]
        sub_category = request.form["sub_category"]
        description = request.form.get("description", "")  # Default to empty string if not provided
        amount = request.form["amount"]
        date = datetime.now().strftime("%Y-%m-%d")
        print(f"Form Data: Category={category}, Sub-Category={sub_category}, Description={description}, Amount={amount}")  # Debugging
        try:
            with open(EXPENSES_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                file_exists = file.tell() > 0
                if not file_exists:
                    writer.writerow(["Date", "Category", "Sub-Category", "Description", "Amount"])
                writer.writerow([date, category, sub_category, description, amount])
            print("Expense added successfully!")  # Debugging
            return redirect(url_for("home"))
        except Exception as e:
            print(f"Error: {e}")  # Debugging
            return f"An error occurred: {e}"
    print("Rendering add.html")  # Debugging
    return render_template("add.html")

# Route to delete an expense
@app.route("/delete/<int:index>")
def delete(index):
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            rows = list(csv.reader(file))
        print(f"Rows: {rows}")
        print(f"Index passed: {index}")
        if 0 <= index < len(rows):
            del rows[index]
            with open(EXPENSES_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        return redirect(url_for("home"))
    except Exception as e:
        return f"An error occurred: {e}"

# Route to edit an expense
@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header row
            rows = list(reader)  # Read all rows from the CSV file
        print(f"Rows: {rows}")
        print(f"Index passed: {index}")
        if request.method == "POST":
            # Retrieve form data
            category = request.form["category"]
            sub_category = request.form["sub_category"]
            description = request.form.get("description", "")  # Default to empty string if not provided
            amount = request.form["amount"]
            # Update the specific row with the new data
            rows[index] = [rows[index][0], category, sub_category, description, amount]
            with open(EXPENSES_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                if header:  # Write the header row back to the file
                    writer.writerow(header)
                writer.writerows(rows)  # Write all rows back to the CSV file
            return redirect(url_for("home"))
        # Get the specific row to edit
        expense = rows[index]
        # Ensure the row has all required fields (fill missing fields with empty strings)
        while len(expense) < 5:
            expense.append("")
        return render_template("edit.html", expense=expense, index=index)
    except Exception as e:
        return f"An error occurred: {e}"

# Route for monthly summary
@app.route("/summary")
def summary():
    monthly_totals = {}
    try:
        with open(EXPENSES_FILE, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header row
            for row in reader:
                if row:
                    date = row[0]
                    amount = float(row[4])  # Amount is in the 5th column (index 4)
                    month = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")  # Convert to "Month Year"
                    if month not in monthly_totals:
                        monthly_totals[month] = 0
                    monthly_totals[month] += amount
    except FileNotFoundError:
        print("File not found: expenses.csv")
    except Exception as e:
        print(f"Error processing summary: {e}")
    return render_template("summary.html", monthly_totals=monthly_totals)

if __name__ == "__main__":
    app.run(debug=True)