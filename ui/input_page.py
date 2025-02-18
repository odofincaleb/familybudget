from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox, QInputDialog, QComboBox, QSpinBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class InputPage(QWidget):
    def __init__(self, budget_data):
        super().__init__()
        self.budget_data = budget_data
        self.current_month = "January"  # Default month
        self.current_year = 2025  # Default year
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for the Input Page."""
        self.layout = QVBoxLayout()

        # Month selection dropdown
        self.month_selector = QComboBox()
        self.month_selector.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        self.month_selector.currentTextChanged.connect(self.change_month)
        self.layout.addWidget(self.month_selector)

        # Year selection spin box
        self.year_selector = QSpinBox()
        self.year_selector.setRange(2000, 2100)
        self.year_selector.setValue(self.current_year)
        self.year_selector.valueChanged.connect(self.change_year)
        self.layout.addWidget(self.year_selector)

        # Scroll area to handle many categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)

        # Add default categories
        self.category_widgets = {}
        self.load_categories()

        # Add a button to add new categories
        self.add_category_button = QPushButton("Add New Category")
        self.add_category_button.setStyleSheet("background-color: #0078D7; color: white; padding: 10px;")
        self.add_category_button.clicked.connect(self.add_new_category)

        # Save button
        save_button = QPushButton("Save Data")
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        save_button.clicked.connect(self.save_data)

        # Add widgets to the layout
        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)
        self.layout.addWidget(self.add_category_button)
        self.layout.addWidget(save_button)
        self.setLayout(self.layout)

    def load_categories(self):
        """Load categories from the budget data."""
        for category in self.budget_data.get_data(self.current_month, self.current_year)["categories"]:
            self.add_category_section(category)

    def change_month(self, month):
        """Change the current month and refresh the UI."""
        self.current_month = month
        self.refresh_ui()

    def change_year(self, year):
        """Change the current year and refresh the UI."""
        self.current_year = year
        self.refresh_ui()

    def add_category_section(self, category):
        """Add a section for a category with its expense items."""
        category_layout = QVBoxLayout()

        # Category label
        category_label = QLabel(category)
        category_label.setFont(QFont("Arial", 14, QFont.Bold))
        category_label.setStyleSheet("color: #00008B;")  # Dark blue color
        category_layout.addWidget(category_label)

        # Add expense items
        for expense_item in self.budget_data.get_data(self.current_month, self.current_year)["categories"][category]["expenses"]:
            self.add_expense_row(category, expense_item, category_layout)

        # Add a button to add new expense items
        add_expense_button = QPushButton(f"Add Expense Item to {category}")
        add_expense_button.setStyleSheet("background-color: #555; color: white; padding: 5px;")
        add_expense_button.clicked.connect(lambda: self.add_new_expense(category))
        category_layout.addWidget(add_expense_button)

        # Add a separator line
        separator = QLabel("——————————————————————————")
        separator.setStyleSheet("color: #555;")  # Gray color
        category_layout.addWidget(separator)

        # Add the category section to the scroll layout
        self.scroll_layout.addLayout(category_layout)

    def add_expense_row(self, category, expense_item, layout):
        """Add a row for an expense item under a category."""
        row_layout = QHBoxLayout()

        # Expense item label
        expense_label = QLabel(expense_item)
        expense_label.setFont(QFont("Arial", 12))
        expense_label.setStyleSheet("color: #00008B;")  # Dark blue color
        expense_label.setFixedWidth(250)  # Wider column for the expense item label

        # Projected cost input
        projected_input = QLineEdit()
        projected_input.setPlaceholderText("Projected Cost")
        projected_input.setStyleSheet("background-color: white; color: black; padding: 5px;")
        projected_input.setFixedWidth(150)
        projected_input.textChanged.connect(lambda: self.update_cost_difference(category, expense_item))

        # Actual cost input
        actual_input = QLineEdit()
        actual_input.setPlaceholderText("Actual Cost")
        actual_input.setStyleSheet("background-color: white; color: black; padding: 5px;")
        actual_input.setFixedWidth(150)
        actual_input.textChanged.connect(lambda: self.update_cost_difference(category, expense_item))

        # Cost Difference label
        cost_difference_label = QLabel("0")
        cost_difference_label.setFont(QFont("Arial", 12))
        cost_difference_label.setStyleSheet("color: #00008B;")  # Dark blue color
        cost_difference_label.setFixedWidth(150)
        cost_difference_label.setAlignment(Qt.AlignCenter)

        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("background-color: #FF4444; color: white; padding: 5px;")
        remove_button.setFixedWidth(80)  # Smaller width for the Remove button
        remove_button.clicked.connect(lambda: self.remove_expense(category, expense_item))

        # Add widgets to the row layout
        row_layout.addWidget(expense_label)
        row_layout.addWidget(projected_input)
        row_layout.addWidget(actual_input)
        row_layout.addWidget(cost_difference_label)
        row_layout.addWidget(remove_button)

        # Add row to the category layout
        layout.addLayout(row_layout)

        # Store the input widgets for later access
        self.category_widgets[(category, expense_item)] = {
            "projected_input": projected_input,
            "actual_input": actual_input,
            "cost_difference_label": cost_difference_label,
        }

        # Set initial values for projected and actual costs
        projected_value = self.budget_data.get_data(self.current_month, self.current_year)["categories"][category]["expenses"][expense_item]["projected"]
        actual_value = self.budget_data.get_data(self.current_month, self.current_year)["categories"][category]["expenses"][expense_item]["actual"]
        projected_input.setText(str(projected_value))
        actual_input.setText(str(actual_value))
        self.update_cost_difference(category, expense_item)

    def update_cost_difference(self, category, expense_item):
        """Update the Cost Difference when Projected or Actual Cost changes."""
        widgets = self.category_widgets.get((category, expense_item))
        if widgets:
            projected = float(widgets["projected_input"].text() or 0)
            actual = float(widgets["actual_input"].text() or 0)
            difference = projected - actual
            widgets["cost_difference_label"].setText(f"{difference:.2f}")

    def add_new_category(self):
        """Add a new category."""
        new_category, ok = QInputDialog.getText(self, "Add New Category", "Enter category name:")
        if ok and new_category:
            super_category, ok = QInputDialog.getItem(
                self, "Select Super Category", "Choose Super Category:", ["NEEDS", "FUN", "FUTURE"], 0, False
            )
            if ok:
                self.budget_data.add_category(self.current_month, self.current_year, new_category, super_category)
                self.add_category_section(new_category)

    def add_new_expense(self, category):
        """Add a new expense item under a category."""
        new_expense, ok = QInputDialog.getText(self, "Add New Expense Item", "Enter expense item name:")
        if ok and new_expense:
            self.budget_data.add_expense(self.current_month, self.current_year, category, new_expense)
            self.add_expense_row(category, new_expense, self.scroll_layout.itemAt(self.scroll_layout.count() - 1).layout())

    def remove_expense(self, category, expense_item):
        """Remove an expense item from a category."""
        self.budget_data.remove_expense(self.current_month, self.current_year, category, expense_item)
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh the UI to reflect changes."""
        # Clear the scroll layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)  # Take the first item
            widget = item.widget()
            if widget:
                widget.deleteLater()  # Delete the widget if it exists

        # Rebuild the UI with updated data
        self.category_widgets = {}
        self.load_categories()

    def save_data(self):
        """Save the entered data to the budget data object."""
        for category in self.budget_data.get_data(self.current_month, self.current_year)["categories"]:
            for expense_item in self.budget_data.get_data(self.current_month, self.current_year)["categories"][category]["expenses"]:
                projected = float(self.get_input_value(category, expense_item, "projected"))
                actual = float(self.get_input_value(category, expense_item, "actual"))
                self.budget_data.update_expense(self.current_month, self.current_year, category, expense_item, projected, actual)
        QMessageBox.information(self, "Success", "Data saved successfully!")
        self.budget_data.data_changed.emit()  # Emit the signal after saving data

    def get_input_value(self, category, expense_item, field):
        """Get the value from the input field for a specific expense item."""
        widgets = self.category_widgets.get((category, expense_item))
        if widgets:
            if field == "projected":
                return widgets["projected_input"].text() or "0"
            elif field == "actual":
                return widgets["actual_input"].text() or "0"
        return "0"