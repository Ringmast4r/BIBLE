"""
Statistics Dashboard
Shows key metrics and insights about cross-references
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class StatsView(QWidget):
    """Statistics dashboard component"""

    def __init__(self):
        super().__init__()
        self.stats = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Scroll area for stats
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #1a1a2e; }")

        # Container widget
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)

        # Title
        title = QLabel('Cross-Reference Statistics')
        title.setStyleSheet('color: #FFD700; font-size: 18pt; font-weight: bold; padding: 10px;')
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Stats grid
        self.stats_grid = QGridLayout()
        container_layout.addLayout(self.stats_grid)

        # Charts area (responsive size)
        self.figure = Figure(facecolor='#1a1a2e')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            self.canvas.sizePolicy().horizontalPolicy(),
            self.canvas.sizePolicy().verticalPolicy()
        )
        container_layout.addWidget(self.canvas)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        plt.style.use('dark_background')

    def set_data(self, stats):
        """Set statistics data"""
        self.stats = stats
        self.render()

    def render(self):
        """Render statistics"""
        if not self.stats:
            return

        # Clear previous stats
        for i in reversed(range(self.stats_grid.count())):
            self.stats_grid.itemAt(i).widget().setParent(None)

        # Add stat cards
        total_connections = self.stats.get('total_connections', 0)
        chapter_connections = self.stats.get('total_chapter_connections', 0)
        avg_connections = round(total_connections / chapter_connections, 2) if chapter_connections > 0 else 0

        stat_items = [
            ('Total Connections', f'{total_connections:,}', '#FFD700'),
            ('Chapter Connections', f'{chapter_connections:,}', '#00CED1'),
            ('Total Books', '66', '#2ecc71'),
            ('Avg Connections', avg_connections, '#9370DB'),
        ]

        for i, (label, value, color) in enumerate(stat_items):
            card = self.create_stat_card(label, value, color)
            self.stats_grid.addWidget(card, 0, i)

        # Render charts
        self.render_charts()

    def create_stat_card(self, label, value, color):
        """Create a stat card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: #16213e;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout()
        card.setLayout(layout)

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f'color: {color}; font-size: 24pt; font-weight: bold;')
        value_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(label)
        text_label.setStyleSheet('color: #00CED1; font-size: 10pt;')
        text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(value_label)
        layout.addWidget(text_label)

        return card

    def render_charts(self):
        """Render statistical charts"""
        if not self.stats:
            return

        self.figure.clear()

        # Top books by connections (most referenced)
        ax1 = self.figure.add_subplot(2, 2, 1)
        ax1.set_facecolor('#1a1a2e')

        if 'most_referenced_books' in self.stats:
            top_books = self.stats['most_referenced_books'][:10]
            books = list(top_books.keys())
            counts = list(top_books.values())

            bars = ax1.barh(books, counts, color='#FFD700', edgecolor='#00CED1')
            ax1.set_xlabel('Total References', color='#00CED1')
            ax1.set_title('Top 10 Most Referenced Books', color='#FFD700', fontweight='bold')
            ax1.tick_params(colors='#00CED1')

        # Testament distribution
        ax2 = self.figure.add_subplot(2, 2, 2)
        ax2.set_facecolor('#1a1a2e')

        if 'testament_distribution' in self.stats:
            testament_dist = self.stats['testament_distribution']
            labels = list(testament_dist.keys())
            sizes = list(testament_dist.values())
            colors = ['#2ecc71', '#00CED1', '#9370DB'][:len(labels)]

            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   textprops={'color': '#FFD700'})
            ax2.set_title('Connection Distribution by Testament',
                         color='#FFD700', fontweight='bold')

        # Most referencing books
        ax3 = self.figure.add_subplot(2, 2, 3)
        ax3.set_facecolor('#1a1a2e')

        if 'most_referencing_books' in self.stats:
            ref_books = self.stats['most_referencing_books'][:10]
            books = list(ref_books.keys())
            counts = list(ref_books.values())

            ax3.barh(books, counts, color='#00CED1', edgecolor='#FFD700')
            ax3.set_xlabel('Outgoing References', color='#00CED1')
            ax3.set_ylabel('Book', color='#00CED1')
            ax3.set_title('Top 10 Most Referencing Books',
                         color='#FFD700', fontweight='bold')
            ax3.tick_params(colors='#00CED1')

        # Summary info
        ax4 = self.figure.add_subplot(2, 2, 4)
        ax4.set_facecolor('#1a1a2e')
        ax4.axis('off')

        summary_text = f"""
        📊 Dataset Summary

        Total Verse References: {self.stats.get('total_verse_references', 0):,}
        Total Chapter Connections: {self.stats.get('total_chapter_connections', 0):,}
        Total Connections: {self.stats.get('total_connections', 0):,}

        Data Source:
        Treasury of Scripture Knowledge
        via OpenBible.info
        """

        ax4.text(0.1, 0.5, summary_text, color='#00CED1', fontsize=10,
                verticalalignment='center', fontfamily='monospace')

        self.figure.tight_layout()
        self.canvas.draw()

    def apply_filters(self, filters):
        """Stats view doesn't use filters"""
        pass

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export Statistics',
            'bible_stats.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
