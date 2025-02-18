import sys
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QFont
from PyQt5.QtCore import Qt

# Import the InputPage, SummaryPage, and AnalysisPage
from ui.input_page import InputPage
from ui.summary_page import SummaryPage
from ui.analysis_page import AnalysisPage

class RichvisionFamilyBudgetApp(QMainWindow):
    def __init__(self, budget_data):
        super().__init__()
        self.budget_data = budget_data
        self.setWindowTitle("Richvision Family Budget")
        self.setGeometry(100, 100, 800, 600)  # Set window size

        # Set window background gradient
        self.set_background_gradient()

        # Create the tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Style the tab widget
        self.style_tab_widget()

        # Add tabs
        self.tabs.addTab(self.create_input_page(), "Input")
        self.tabs.addTab(self.create_summary_page(), "Summary")
        self.tabs.addTab(self.create_analysis_page(), "Analysis")

    def set_background_gradient(self):
        """Set a gradient background for the main window."""
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 30, 30))  # Dark gray at the top
        gradient.setColorAt(1, QColor(50, 50, 50))  # Slightly lighter gray at the bottom

        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def style_tab_widget(self):
        """Style the tab widget with custom colors and fonts."""
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background: #333;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab {
                background: #555;
                color: #FFF;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #444;
                border-bottom-color: #333;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: #0078D7;
                color: #FFF;
                border-bottom-color: #0078D7;
            }
            QTabBar::tab:hover {
                background: #0066B3;
            }
        """)

    def create_input_page(self):
        """Create the Input tab."""
        return InputPage(self.budget_data)

    def create_summary_page(self):
        """Create the Summary tab."""
        return SummaryPage(self.budget_data)

    def create_analysis_page(self):
        """Create the Analysis tab."""
        return AnalysisPage(self.budget_data)