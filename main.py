import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import RichvisionFamilyBudgetApp
from data.budget_data import BudgetData

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize budget data
    budget_data = BudgetData()

    # Create and show the main window
    window = RichvisionFamilyBudgetApp(budget_data)
    window.show()

    sys.exit(app.exec_())