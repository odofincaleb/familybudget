from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SummaryPage(QWidget):
    def __init__(self, budget_data):
        super().__init__()
        self.budget_data = budget_data
        self.init_ui()

        # Connect the data_changed signal to update the UI
        self.budget_data.data_changed.connect(self.update_summary_table)
        self.budget_data.data_changed.connect(self.update_summary_section)

    def init_ui(self):
        """Initialize the UI for the Summary Page."""
        self.layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Summary")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: white;")  # White color for the title
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Create a table to display the summary
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(5)  # Category, Projected, Actual, Difference, Super Category
        self.summary_table.setHorizontalHeaderLabels(["Category", "Projected Cost", "Actual Cost", "Difference", "Super Category"])
        self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.summary_table.setStyleSheet("background-color: white; color: black;")

        # Populate the table with data
        self.update_summary_table()

        # Add the table to the layout
        self.layout.addWidget(self.summary_table)

        # Summary section for totals and percentage allocation
        self.summary_section = QLabel()
        self.summary_section.setFont(QFont("Arial", 12))
        self.summary_section.setStyleSheet("color: white;")  # White color for the text
        self.summary_section.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.summary_section)

        # Update the summary section
        self.update_summary_section()

        # Set the layout
        self.setLayout(self.layout)

    def update_summary_table(self):
        """Update the summary table with the latest data."""
        categories = self.budget_data.get_data()
        self.summary_table.setRowCount(len(categories))

        # Populate the table with data
        for i, (category, data) in enumerate(categories.items()):
            projected, actual = self.budget_data.get_category_total(category)
            difference = projected - actual
            super_category = data["super_category"]

            # Add data to the table
            self.summary_table.setItem(i, 0, QTableWidgetItem(category))
            self.summary_table.setItem(i, 1, QTableWidgetItem(f"{projected:.2f}"))
            self.summary_table.setItem(i, 2, QTableWidgetItem(f"{actual:.2f}"))
            self.summary_table.setItem(i, 3, QTableWidgetItem(f"{difference:.2f}"))
            self.summary_table.setItem(i, 4, QTableWidgetItem(super_category))

    def update_summary_section(self):
        """Update the summary section with totals and percentage allocation."""
        # Calculate totals for all categories
        total_projected = sum(
            self.budget_data.get_category_total(category)[0]
            for category in self.budget_data.get_data()
        )
        total_actual = sum(
            self.budget_data.get_category_total(category)[1]
            for category in self.budget_data.get_data()
        )
        total_difference = total_projected - total_actual

        # Calculate percentage allocation for each super category
        needs_projected, _ = self.budget_data.get_super_category_total("NEEDS")
        fun_projected, _ = self.budget_data.get_super_category_total("FUN")
        future_projected, _ = self.budget_data.get_super_category_total("FUTURE")

        needs_percentage = (needs_projected / total_projected) * 100 if total_projected != 0 else 0
        fun_percentage = (fun_projected / total_projected) * 100 if total_projected != 0 else 0
        future_percentage = (future_projected / total_projected) * 100 if total_projected != 0 else 0

        # Update the summary section
        self.summary_section.setText(
            f"TOTAL\n"
            f"Projected Cost: {total_projected:.2f}\n"
            f"Actual Cost: {total_actual:.2f}\n"
            f"Difference: {total_difference:.2f}\n\n"
            f"PERCENTAGE ALLOCATION:\n"
            f"NEEDS: {needs_percentage:.1f}%\n"
            f"FUN: {fun_percentage:.1f}%\n"
            f"FUTURE: {future_percentage:.1f}%"
        )