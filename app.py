from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flask_user:test%40123@13.203.75.156/expense_tracker"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"

db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Route for the home page
@app.route("/")
def home():
    expenses = Expense.query.all()
    print(f"Expenses fetched from DB: {expenses}")
    return render_template("index.html", expenses=expenses)

# Route to add a new expense
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        category = request.form["category"]
        sub_category = request.form["sub_category"]
        description = request.form.get("description", "")
        amount = request.form["amount"]
        date = datetime.now().strftime("%Y-%m-%d")
        new_expense = Expense(date=date, category=category, sub_category=sub_category, description=description, amount=amount)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add.html")

# Route to delete an expense
@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("home"))

# Route to edit an expense
#@app.route("/edit/<int:id>", methods=["GET", "POST"])
#def edit(id):
 #   expense = Expense.query.get_or_404(id)
  #  print(f"Editing Expense: ID={expense.id}, Sub-Category={expense.sub_category}")
   # if request.method == "POST":
    #    expense.category = request.form["category"]
     #   expense.sub_category = request.form["sub_category"]
      #  expense.description = request.form.get("description", "")
       # expense.amount = request.form["amount"]
        #db.session.commit()
        #flash("Expense updated successfully!", "success")
        #return redirect(url_for("home"))
    #return render_template("edit.html", expense=expense)
#@app.route("/edit/<int:id>", methods=["GET", "POST"])
#def edit(id):
 #   expense = Expense.query.get_or_404(id)
  #  print(f"Editing Expense: ID={expense.id}, Category={expense.category}, Sub-Category={expense.sub_category}")
   # if request.method == "POST":
    #    expense.category = request.form["category"]
     #   expense.sub_category = request.form["sub_category"]
      #  expense.description = request.form.get("description", "")
       # expense.amount = request.form["amount"]
       # db.session.commit()
      #  flash("Expense updated successfully!", "success")
      #  return redirect(url_for("home"))
    #return render_template("edit.html", expense=expense)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    expense = Expense.query.get_or_404(id)
    # Fetch all unique sub-categories from the database
    sub_categories = db.session.query(Expense.sub_category).distinct().all()
    sub_categories = [sub_category[0] for sub_category in sub_categories]  # Extract values from tuples
    print(f"Editing Expense: ID={expense.id}, Category={expense.category}, Sub-Category={expense.sub_category}")
    print(f"Available Sub-Categories: {sub_categories}")
    if request.method == "POST":
        expense.category = request.form["category"]
        expense.sub_category = request.form["sub_category"]
        expense.description = request.form.get("description", "")
        expense.amount = request.form["amount"]
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for("home"))
    return render_template("edit.html", expense=expense, sub_categories=sub_categories)

# Route for monthly summary
@app.route("/summary")
def summary():
    expenses = Expense.query.all()
    monthly_totals = {}
    for expense in expenses:
        month = datetime.strptime(expense.date, "%Y-%m-%d").strftime("%B %Y")
        if month not in monthly_totals:
            monthly_totals[month] = 0
        monthly_totals[month] += expense.amount
    return render_template("summary.html", monthly_totals=monthly_totals)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
