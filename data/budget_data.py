import json
from PyQt5.QtCore import QObject, pyqtSignal
from collections import defaultdict
import os

class BudgetData(QObject):
    # Define a signal that will be emitted when data changes
    data_changed = pyqtSignal()

    def __init__(self, data_file="budget_data.json"):
        super().__init__()
        self.data_file = data_file
        self.data = defaultdict(lambda: {
            "categories": {
                "Housing": {
                    "super_category": "NEEDS",
                    "expenses": {
                        "Mortgage/Rent": {"projected": 0, "actual": 0},
                        "Utilities (Electricity, Gas, Water)": {"projected": 0, "actual": 0},
                        "Cable": {"projected": 0, "actual": 0},
                        "Waste Removal": {"projected": 0, "actual": 0},
                        "Maintenance": {"projected": 0, "actual": 0},
                        "Supplies": {"projected": 0, "actual": 0},
                    },
                },
                "Transportation": {
                    "super_category": "NEEDS",
                    "expenses": {
                        "Car Payment": {"projected": 0, "actual": 0},
                        "Gas": {"projected": 0, "actual": 0},
                        "Insurance": {"projected": 0, "actual": 0},
                        "Maintenance": {"projected": 0, "actual": 0},
                        "Public Transportation": {"projected": 0, "actual": 0},
                    },
                },
                "Food": {
                    "super_category": "NEEDS",
                    "expenses": {
                        "Groceries": {"projected": 0, "actual": 0},
                        "Dining Out": {"projected": 0, "actual": 0},
                    },
                },
                "Entertainment": {
                    "super_category": "FUN",
                    "expenses": {
                        "Movies": {"projected": 0, "actual": 0},
                        "Concerts": {"projected": 0, "actual": 0},
                        "Sports": {"projected": 0, "actual": 0},
                    },
                },
                "Savings": {
                    "super_category": "FUTURE",
                    "expenses": {
                        "Emergency Fund": {"projected": 0, "actual": 0},
                        "Retirement": {"projected": 0, "actual": 0},
                        "Investments": {"projected": 0, "actual": 0},
                    },
                },
                "Health": {
                    "super_category": "NEEDS",
                    "expenses": {
                        "Insurance": {"projected": 0, "actual": 0},
                        "Medication": {"projected": 0, "actual": 0},
                        "Doctor Visits": {"projected": 0, "actual": 0},
                    },
                },
                "Insurance": {
                    "super_category": "NEEDS",
                    "expenses": {
                        "Health Insurance": {"projected": 0, "actual": 0},
                        "Life Insurance": {"projected": 0, "actual": 0},
                        "Auto Insurance": {"projected": 0, "actual": 0},
                    },
                },
            }
        })
        self.load_data()  # Load data from JSON file

    def add_category(self, month, year, category, super_category):
        """Add a new category with a super category."""
        key = f"{month}_{year}"
        if category not in self.data[key]["categories"]:
            self.data[key]["categories"][category] = {"super_category": super_category, "expenses": {}}
            self.data_changed.emit()  # Emit signal when data changes
            self.save_data()  # Save data to JSON file

    def remove_category(self, month, year, category):
        """Remove a category and its expenses."""
        key = f"{month}_{year}"
        if category in self.data[key]["categories"]:
            del self.data[key]["categories"][category]
            self.data_changed.emit()  # Emit signal when data changes
            self.save_data()  # Save data to JSON file

    def add_expense(self, month, year, category, expense_item, projected=0, actual=0):
        """Add an expense item under a category."""
        key = f"{month}_{year}"
        if category in self.data[key]["categories"]:
            self.data[key]["categories"][category]["expenses"][expense_item] = {
                "projected": projected,
                "actual": actual,
            }
            self.data_changed.emit()  # Emit signal when data changes
            self.save_data()  # Save data to JSON file

    def remove_expense(self, month, year, category, expense_item):
        """Remove an expense item from a category."""
        key = f"{month}_{year}"
        if category in self.data[key]["categories"] and expense_item in self.data[key]["categories"][category]["expenses"]:
            del self.data[key]["categories"][category]["expenses"][expense_item]
            self.data_changed.emit()  # Emit signal when data changes
            self.save_data()  # Save data to JSON file

    def update_expense(self, month, year, category, expense_item, projected, actual):
        """Update the projected and actual costs for an expense item."""
        key = f"{month}_{year}"
        if category in self.data[key]["categories"] and expense_item in self.data[key]["categories"][category]["expenses"]:
            self.data[key]["categories"][category]["expenses"][expense_item]["projected"] = projected
            self.data[key]["categories"][category]["expenses"][expense_item]["actual"] = actual
            self.data_changed.emit()  # Emit signal when data changes
            self.save_data()  # Save data to JSON file

    def get_category_total(self, month, year, category):
        """Calculate the total projected and actual costs for a category."""
        key = f"{month}_{year}"
        if category in self.data[key]["categories"]:
            projected_total = sum(expense["projected"] for expense in self.data[key]["categories"][category]["expenses"].values())
            actual_total = sum(expense["actual"] for expense in self.data[key]["categories"][category]["expenses"].values())
            return projected_total, actual_total
        return 0, 0

    def get_super_category_total(self, month, year, super_category):
        """Calculate the total projected and actual costs for a super category."""
        key = f"{month}_{year}"
        projected_total = 0
        actual_total = 0
        for category, data in self.data[key]["categories"].items():
            if data["super_category"] == super_category:
                projected, actual = self.get_category_total(month, year, category)
                projected_total += projected
                actual_total += actual
        return projected_total, actual_total

    def get_data(self, month, year):
        """Return the current budget data for a specific month and year."""
        key = f"{month}_{year}"
        # Initialize the month and year if not present
        if key not in self.data:
            self.data[key] = {
                "categories": {
                    "Housing": {
                        "super_category": "NEEDS",
                        "expenses": {
                            "Mortgage/Rent": {"projected": 0, "actual": 0},
                            "Utilities (Electricity, Gas, Water)": {"projected": 0, "actual": 0},
                            "Cable": {"projected": 0, "actual": 0},
                            "Waste Removal": {"projected": 0, "actual": 0},
                            "Maintenance": {"projected": 0, "actual": 0},
                            "Supplies": {"projected": 0, "actual": 0},
                        },
                    },
                    "Transportation": {
                        "super_category": "NEEDS",
                        "expenses": {
                            "Car Payment": {"projected": 0, "actual": 0},
                            "Gas": {"projected": 0, "actual": 0},
                            "Insurance": {"projected": 0, "actual": 0},
                            "Maintenance": {"projected": 0, "actual": 0},
                            "Public Transportation": {"projected": 0, "actual": 0},
                        },
                    },
                    "Food": {
                        "super_category": "NEEDS",
                        "expenses": {
                            "Groceries": {"projected": 0, "actual": 0},
                            "Dining Out": {"projected": 0, "actual": 0},
                        },
                    },
                    "Entertainment": {
                        "super_category": "FUN",
                        "expenses": {
                            "Movies": {"projected": 0, "actual": 0},
                            "Concerts": {"projected": 0, "actual": 0},
                            "Sports": {"projected": 0, "actual": 0},
                        },
                    },
                    "Savings": {
                        "super_category": "FUTURE",
                        "expenses": {
                            "Emergency Fund": {"projected": 0, "actual": 0},
                            "Retirement": {"projected": 0, "actual": 0},
                            "Investments": {"projected": 0, "actual": 0},
                        },
                    },
                    "Health": {
                        "super_category": "NEEDS",
                        "expenses": {
                            "Insurance": {"projected": 0, "actual": 0},
                            "Medication": {"projected": 0, "actual": 0},
                            "Doctor Visits": {"projected": 0, "actual": 0},
                        },
                    },
                    "Insurance": {
                        "super_category": "NEEDS",
                        "expenses": {
                            "Health Insurance": {"projected": 0, "actual": 0},
                            "Life Insurance": {"projected": 0, "actual": 0},
                            "Auto Insurance": {"projected": 0, "actual": 0},
                        },
                    },
                }
            }
        return self.data[key]

    def save_data(self):
        """Save the budget data to a JSON file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def load_data(self):
        """Load the budget data from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)