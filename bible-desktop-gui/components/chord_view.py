"""
Chord Diagram Visualization using Matplotlib
Circular diagram showing relationships between Bible books
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class ChordView(QWidget):
    """Chord diagram visualization component"""

    def __init__(self):
        super().__init__()
        self.data = None
        self.filtered_data = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 12), facecolor='#1a1a2e')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set style
        plt.style.use('dark_background')

    def set_data(self, data):
        """Set data and aggregate by books"""
        self.data = data
        self.filtered_data = self._aggregate_by_books(data)
        self.render()

    def _aggregate_by_books(self, data):
        """Aggregate chapter connections into book connections"""
        book_connections = defaultdict(lambda: defaultdict(int))

        for conn in data['connections']:
            # Find source and target chapters
            source_ch = next((ch for ch in data['chapters'] if ch['id'] == conn['source']), None)
            target_ch = next((ch for ch in data['chapters'] if ch['id'] == conn['target']), None)

            if source_ch and target_ch:
                source_book = source_ch['book']
                target_book = target_ch['book']

                # Don't count self-connections
                if source_book != target_book:
                    book_connections[source_book][target_book] += conn['weight']

        return book_connections

    def render(self):
        """Render chord diagram"""
        if not self.filtered_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='polar')
        ax.set_facecolor('#1a1a2e')

        # Get all books in Bible order
        ot_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
                    'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
                    '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
                    'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
                    'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
                    'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
                    'Haggai', 'Zechariah', 'Malachi']

        nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
                    '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
                    '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus',
                    'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
                    '3 John', 'Jude', 'Revelation']

        all_books = ot_books + nt_books
        num_books = len(all_books)

        # Create angular positions for each book
        angles = np.linspace(0, 2 * np.pi, num_books, endpoint=False)
        book_angles = {book: angle for book, angle in zip(all_books, angles)}

        # Draw book arcs
        arc_width = (2 * np.pi) / num_books * 0.8
        radius = 1.0

        for book, angle in book_angles.items():
            color = '#2ecc71' if book in ot_books else '#00CED1'
            ax.bar(angle, radius, width=arc_width, bottom=0,
                   color=color, alpha=0.7, edgecolor='#FFD700', linewidth=1)

            # Add book labels
            label_angle = angle
            ha = 'left' if label_angle < np.pi else 'right'
            rotation = np.degrees(label_angle)
            if rotation > 90 and rotation < 270:
                rotation = rotation - 180

            ax.text(label_angle, radius + 0.1, book,
                   rotation=rotation, ha=ha, va='center',
                   fontsize=6, color=color, fontweight='bold')

        # Draw connection chords (top connections only for visibility)
        connections_list = []
        for source_book, targets in self.filtered_data.items():
            for target_book, weight in targets.items():
                if source_book in book_angles and target_book in book_angles:
                    connections_list.append((source_book, target_book, weight))

        # Sort by weight and take top 100
        connections_list.sort(key=lambda x: x[2], reverse=True)
        top_connections = connections_list[:100]

        max_weight = max(conn[2] for conn in top_connections) if top_connections else 1

        for source_book, target_book, weight in top_connections:
            angle1 = book_angles[source_book]
            angle2 = book_angles[target_book]

            # Determine color
            if source_book in ot_books and target_book in ot_books:
                color = '#2ecc71'
            elif source_book in nt_books and target_book in nt_books:
                color = '#00CED1'
            else:
                color = '#9370DB'

            # Draw bezier curve between books
            alpha = min(0.6, weight / max_weight)
            linewidth = np.sqrt(weight) / 5

            # Create curved path
            t = np.linspace(0, 1, 100)
            theta = (1 - t) * angle1 + t * angle2

            # Make it curve inward
            r = radius * 0.8 * np.sin(np.pi * t)

            ax.plot(theta, r, color=color, alpha=alpha, linewidth=linewidth)

        # Styling
        ax.set_ylim(0, radius + 0.3)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(False)
        ax.spines['polar'].set_visible(False)

        ax.set_title(f'Bible Books Chord Diagram (Top {len(top_connections)} connections)',
                     color='#FFD700', fontsize=14, fontweight='bold', pad=20)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ecc71', label='Old Testament'),
            Patch(facecolor='#00CED1', label='New Testament'),
            Patch(facecolor='#9370DB', label='Cross-Testament')
        ]
        ax.legend(handles=legend_elements, loc='upper right',
                 facecolor='#16213e', edgecolor='#FFD700')

        self.figure.tight_layout()
        self.canvas.draw()

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        if not self.data:
            return

        testament = filters.get('testament', 'All')
        min_connections = filters.get('min_connections', 1)

        # Re-aggregate with filters
        book_connections = defaultdict(lambda: defaultdict(int))

        for conn in self.data['connections']:
            if conn['weight'] < min_connections:
                continue

            source_ch = next((ch for ch in self.data['chapters'] if ch['id'] == conn['source']), None)
            target_ch = next((ch for ch in self.data['chapters'] if ch['id'] == conn['target']), None)

            if not source_ch or not target_ch:
                continue

            source_testament = source_ch['testament']
            target_testament = target_ch['testament']

            # Apply testament filter
            if testament == 'Old Testament' and (source_testament != 'OT' or target_testament != 'OT'):
                continue
            elif testament == 'New Testament' and (source_testament != 'NT' or target_testament != 'NT'):
                continue
            elif testament == 'Cross-Testament' and source_testament == target_testament:
                continue

            source_book = source_ch['book']
            target_book = target_ch['book']

            if source_book != target_book:
                book_connections[source_book][target_book] += conn['weight']

        self.filtered_data = book_connections
        self.render()

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export Chord Diagram',
            'bible_chord_diagram.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
