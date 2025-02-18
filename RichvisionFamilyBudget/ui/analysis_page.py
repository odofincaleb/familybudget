from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AnalysisPage(QWidget):
    def __init__(self, budget_data):
        super().__init__()
        self.budget_data = budget_data
        self.init_ui()

        # Connect the data_changed signal to update the charts
        self.budget_data.data_changed.connect(self.update_charts)

    def init_ui(self):
        """Initialize the UI for the Analysis Page."""
        self.layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Analysis")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: white;")  # White color for the title
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add the Monthly Projected vs. Actual Cost Chart
        self.monthly_chart = self.create_monthly_chart()
        self.layout.addWidget(self.monthly_chart)

        # Add the Category Performance Chart
        self.category_chart = self.create_category_chart()
        self.layout.addWidget(self.category_chart)

        # Set the layout
        self.setLayout(self.layout)

    def update_charts(self):
        """Update the charts when the data changes."""
        # Clear the existing charts
        self.layout.removeWidget(self.monthly_chart)
        self.monthly_chart.deleteLater()
        self.layout.removeWidget(self.category_chart)
        self.category_chart.deleteLater()

        # Add updated charts
        self.monthly_chart = self.create_monthly_chart()
        self.layout.addWidget(self.monthly_chart)
        self.category_chart = self.create_category_chart()
        self.layout.addWidget(self.category_chart)

    def create_monthly_chart(self):
        """Create the Monthly Projected vs. Actual Cost Chart."""
        # Create a Matplotlib figure and canvas
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Get actual data from budget_data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]  # Replace with actual months
        projected = [self.budget_data.get_category_total(category)[0] for category in self.budget_data.get_data()]
        actual = [self.budget_data.get_category_total(category)[1] for category in self.budget_data.get_data()]

        # Plot the data
        ax.plot(months, projected, label="Projected Cost", marker="o", color="blue", linewidth=2)
        ax.plot(months, actual, label="Actual Cost", marker="o", color="green", linewidth=2)

        # Add labels and title
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Cost ($)", fontsize=12)
        ax.set_title("Monthly Projected vs. Actual Cost", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

        # Return the canvas
        return canvas

    def create_category_chart(self):
        """Create the Category Performance Chart."""
        # Create a Matplotlib figure and canvas
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        # Get actual data from budget_data
        categories = list(self.budget_data.get_data().keys())
        if not categories:
            # Display a message if no data is available
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14, fontweight="bold")
            return canvas

        projected = [self.budget_data.get_category_total(category)[0] for category in categories]
        actual = [self.budget_data.get_category_total(category)[1] for category in categories]

        # Plot the data
        x = range(len(categories))  # X-axis positions
        ax.bar(x, projected, width=0.4, label="Projected Cost", align="center", color="blue", alpha=0.7)
        ax.bar([i + 0.4 for i in x], actual, width=0.4, label="Actual Cost", align="center", color="green", alpha=0.7)

        # Add labels and title
        ax.set_xlabel("Category", fontsize=12)
        ax.set_ylabel("Cost ($)", fontsize=12)
        ax.set_title("Category Performance (Projected vs. Actual)", fontsize=14, fontweight="bold")
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels(categories, rotation=45, ha="right")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

        # Return the canvas
        return canvas