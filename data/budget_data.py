from PyQt5.QtCore import QObject, pyqtSignal

class BudgetData(QObject):
    # Define a signal that will be emitted when data changes
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Initialize default categories with their super categories and expense items
        self.categories = {
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
                    "Vehicle Payment": {"projected": 0, "actual": 0},
                    "Bus/Taxi Fare": {"projected": 0, "actual": 0},
                    "Insurance": {"projected": 0, "actual": 0},
                    "Licensing": {"projected": 0, "actual": 0},
                    "Fuel": {"projected": 0, "actual": 0},
                    "Maintenance": {"projected": 0, "actual": 0},
                },
            },
            "Insurance": {
                "super_category": "NEEDS",
                "expenses": {
                    "Home Insurance": {"projected": 0, "actual": 0},
                    "Health Insurance": {"projected": 0, "actual": 0},
                    "Life Insurance": {"projected": 0, "actual": 0},
                    "Other Insurance": {"projected": 0, "actual": 0},
                },
            },
            "Food": {
                "super_category": "NEEDS",
                "expenses": {
                    "Groceries": {"projected": 0, "actual": 0},
                    "Dining Out": {"projected": 0, "actual": 0},
                    "Other Food Expenses": {"projected": 0, "actual": 0},
                },
            },
            "Children": {
                "super_category": "NEEDS",
                "expenses": {
                    "Medical": {"projected": 0, "actual": 0},
                    "Clothing": {"projected": 0, "actual": 0},
                    "School Tuition": {"projected": 0, "actual": 0},
                    "School Supplies": {"projected": 0, "actual": 0},
                    "Organization Dues/Fees": {"projected": 0, "actual": 0},
                    "Lunch Money": {"projected": 0, "actual": 0},
                    "Child Care": {"projected": 0, "actual": 0},
                    "Toys/Games": {"projected": 0, "actual": 0},
                },
            },
            "Legal": {
                "super_category": "NEEDS",
                "expenses": {
                    "Attorney Fees": {"projected": 0, "actual": 0},
                    "Alimony": {"projected": 0, "actual": 0},
                    "Payments": {"projected": 0, "actual": 0},
                    "Other Legal Expenses": {"projected": 0, "actual": 0},
                },
            },
            "Savings/Investments": {
                "super_category": "FUTURE",
                "expenses": {
                    "Retirement Account": {"projected": 0, "actual": 0},
                    "Investment Account": {"projected": 0, "actual": 0},
                    "College Savings": {"projected": 0, "actual": 0},
                    "Other Savings": {"projected": 0, "actual": 0},
                },
            },
            "Entertainment": {
                "super_category": "FUN",
                "expenses": {
                    "Streaming Apps": {"projected": 0, "actual": 0},
                    "Online Games": {"projected": 0, "actual": 0},
                    "Movies": {"projected": 0, "actual": 0},
                    "Concerts": {"projected": 0, "actual": 0},
                    "Sporting Events": {"projected": 0, "actual": 0},
                    "Live Theater": {"projected": 0, "actual": 0},
                    "Other Entertainment": {"projected": 0, "actual": 0},
                },
            },
            "Taxes": {
                "super_category": "NEEDS",
                "expenses": {
                    "Federal Taxes": {"projected": 0, "actual": 0},
                    "State Taxes": {"projected": 0, "actual": 0},
                    "Local Taxes": {"projected": 0, "actual": 0},
                    "Other Taxes": {"projected": 0, "actual": 0},
                },
            },
            "Personal Care": {
                "super_category": "FUN",
                "expenses": {
                    "Medical": {"projected": 0, "actual": 0},
                    "Hair/Nails": {"projected": 0, "actual": 0},
                    "Clothing": {"projected": 0, "actual": 0},
                    "Dry Cleaning": {"projected": 0, "actual": 0},
                    "Health Club": {"projected": 0, "actual": 0},
                    "Organization Dues/Fees": {"projected": 0, "actual": 0},
                    "Other Personal Care": {"projected": 0, "actual": 0},
                },
            },
            "Pets": {
                "super_category": "NEEDS",
                "expenses": {
                    "Food": {"projected": 0, "actual": 0},
                    "Medical": {"projected": 0, "actual": 0},
                    "Grooming": {"projected": 0, "actual": 0},
                    "Toys": {"projected": 0, "actual": 0},
                    "Other Pet Expenses": {"projected": 0, "actual": 0},
                },
            },
            "Gifts and Donations": {
                "super_category": "FUTURE",
                "expenses": {
                    "Charity 1": {"projected": 0, "actual": 0},
                    "Charity 2": {"projected": 0, "actual": 0},
                    "Charity 3": {"projected": 0, "actual": 0},
                    "Other Gifts/Donations": {"projected": 0, "actual": 0},
                },
            },
        }

    def add_category(self, category, super_category):
        """Add a new category with a super category."""
        if category not in self.categories:
            self.categories[category] = {"super_category": super_category, "expenses": {}}
            self.data_changed.emit()  # Emit signal when data changes

    def remove_category(self, category):
        """Remove a category and its expenses."""
        if category in self.categories:
            del self.categories[category]
            self.data_changed.emit()  # Emit signal when data changes

    def add_expense(self, category, expense_item, projected=0, actual=0):
        """Add an expense item under a category."""
        if category in self.categories:
            self.categories[category]["expenses"][expense_item] = {
                "projected": projected,
                "actual": actual,
            }
            self.data_changed.emit()  # Emit signal when data changes

    def remove_expense(self, category, expense_item):
        """Remove an expense item from a category."""
        if category in self.categories and expense_item in self.categories[category]["expenses"]:
            del self.categories[category]["expenses"][expense_item]
            self.data_changed.emit()  # Emit signal when data changes

    def update_expense(self, category, expense_item, projected, actual):
        """Update the projected and actual costs for an expense item."""
        if category in self.categories and expense_item in self.categories[category]["expenses"]:
            self.categories[category]["expenses"][expense_item]["projected"] = projected
            self.categories[category]["expenses"][expense_item]["actual"] = actual
            self.data_changed.emit()  # Emit signal when data changes

    def get_category_total(self, category):
        """Calculate the total projected and actual costs for a category."""
        if category in self.categories:
            projected_total = sum(expense["projected"] for expense in self.categories[category]["expenses"].values())
            actual_total = sum(expense["actual"] for expense in self.categories[category]["expenses"].values())
            return projected_total, actual_total
        return 0, 0

    def get_super_category_total(self, super_category):
        """Calculate the total projected and actual costs for a super category."""
        projected_total = 0
        actual_total = 0
        for category, data in self.categories.items():
            if data["super_category"] == super_category:
                projected, actual = self.get_category_total(category)
                projected_total += projected
                actual_total += actual
        return projected_total, actual_total

    def get_data(self):
        """Return the current budget data."""
        return self.categories