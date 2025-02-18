from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AnalysisPage(QWidget):
    def __init__(self, budget_data):
        super().__init__()
        self.budget_data = budget_data
        self.current_month = "January"  # Default month
        self.current_year = 2025  # Default year
        self.init_ui()

    def init_ui(self):
        """Initialize the UI for the Analysis Page."""
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

        # Title label
        title_label = QLabel("Analysis")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add the Monthly Trends Chart
        self.monthly_trends_chart = self.create_monthly_trends_chart()
        self.layout.addWidget(self.monthly_trends_chart)

        # Add the Category Performance Chart
        self.category_chart = self.create_category_chart()
        self.layout.addWidget(self.category_chart)

        # Set the layout
        self.setLayout(self.layout)

    def change_month(self, month):
        """Change the current month and refresh the UI."""
        self.current_month = month
        self.refresh_ui()

    def change_year(self, year):
        """Change the current year and refresh the UI."""
        self.current_year = year
        self.refresh_ui()

    def create_monthly_trends_chart(self):
        """Create a chart showing projected vs. actual costs per month."""
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Get actual data from budget_data
        months = list(self.budget_data.data.keys())
        if not months:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14, fontweight="bold")
            return canvas

        projected = [sum(self.budget_data.get_category_total(month.split('_')[0], month.split('_')[1], category)[0] for category in self.budget_data.get_data(month.split('_')[0], month.split('_')[1])["categories"]) for month in months]
        actual = [sum(self.budget_data.get_category_total(month.split('_')[0], month.split('_')[1], category)[1] for category in self.budget_data.get_data(month.split('_')[0], month.split('_')[1])["categories"]) for month in months]

        # Plot the data
        x = range(len(months))
        ax.plot(x, projected, label="Projected Cost", marker="o", color="blue", linewidth=2)
        ax.plot(x, actual, label="Actual Cost", marker="o", color="green", linewidth=2)

        # Customize the chart
        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45, ha="right")
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Cost ($)", fontsize=12)
        ax.set_title("Monthly Trends (Projected vs. Actual)", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

        return canvas

    def create_category_chart(self):
        """Create the Category Performance Chart."""
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Get actual data from budget_data
        categories = list(set(cat for month_data in self.budget_data.data.values() for cat in month_data["categories"].keys()))
        if not categories:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14, fontweight="bold")
            return canvas

        projected = [sum(self.budget_data.get_category_total(month.split('_')[0], month.split('_')[1], category)[0] for month in self.budget_data.data.keys()) for category in categories]
        actual = [sum(self.budget_data.get_category_total(month.split('_')[0], month.split('_')[1], category)[1] for month in self.budget_data.data.keys()) for category in categories]

        # Plot the data
        x = range(len(categories))
        ax.bar(x, projected, width=0.4, label="Projected Cost", align="center", color="blue", alpha=0.7)
        ax.bar([i + 0.4 for i in x], actual, width=0.4, label="Actual Cost", align="center", color="green", alpha=0.7)

        # Customize the chart
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.set_xlabel("Category", fontsize=12)
        ax.set_ylabel("Cost ($)", fontsize=12)
        ax.set_title("Category Performance (Projected vs. Actual)", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

        return canvas

    def refresh_ui(self):
        """Refresh the UI to reflect changes."""
        self.layout.removeWidget(self.monthly_trends_chart)
        self.monthly_trends_chart.deleteLater()
        self.layout.removeWidget(self.category_chart)
        self.category_chart.deleteLater()

        self.monthly_trends_chart = self.create_monthly_trends_chart()
        self.layout.addWidget(self.monthly_trends_chart)
        self.category_chart = self.create_category_chart()
        self.layout.addWidget(self.category_chart)