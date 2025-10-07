"""
Sunburst Diagram Visualization using Matplotlib
Hierarchical view: Testament → Book → Chapter
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import defaultdict


class SunburstView(QWidget):
    """Sunburst diagram visualization component"""

    def __init__(self):
        super().__init__()
        self.data = None
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
        """Set data"""
        self.data = data
        self.render()

    def render(self):
        """Render sunburst diagram"""
        if not self.data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1a1a2e')
        ax.set_aspect('equal')

        # Organize data hierarchically
        hierarchy = self._build_hierarchy()

        # Draw sunburst
        self._draw_sunburst(ax, hierarchy)

        # Styling
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        ax.set_title('Bible Structure: Testament → Book → Chapter',
                     color='#FFD700', fontsize=16, fontweight='bold', pad=20)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ecc71', label='Old Testament', alpha=0.7),
            Patch(facecolor='#00CED1', label='New Testament', alpha=0.7)
        ]
        ax.legend(handles=legend_elements, loc='upper right',
                 facecolor='#16213e', edgecolor='#FFD700')

        self.figure.tight_layout()
        self.canvas.draw()

    def _build_hierarchy(self):
        """Build hierarchical structure from data"""
        hierarchy = {
            'OT': defaultdict(list),
            'NT': defaultdict(list)
        }

        for chapter in self.data['chapters']:
            testament = chapter['testament']
            book = chapter['book']
            chapter_num = chapter['chapter']
            hierarchy[testament][book].append(chapter_num)

        return hierarchy

    def _draw_sunburst(self, ax, hierarchy):
        """Draw sunburst diagram"""
        # Center circle
        center = patches.Circle((0, 0), 0.2, facecolor='#16213e',
                               edgecolor='#FFD700', linewidth=2)
        ax.add_patch(center)
        ax.text(0, 0, 'BIBLE', ha='center', va='center',
               fontsize=14, color='#FFD700', fontweight='bold')

        # Calculate angles for testaments
        total_chapters = sum(len(chapters) for testament in hierarchy.values()
                           for chapters in testament.values())

        current_angle = 0

        for testament_name, books in hierarchy.items():
            testament_chapters = sum(len(chapters) for chapters in books.values())
            testament_angle = (testament_chapters / total_chapters) * 360

            testament_color = '#2ecc71' if testament_name == 'OT' else '#00CED1'

            # Draw testament ring
            wedge = patches.Wedge((0, 0), 0.5, current_angle,
                                 current_angle + testament_angle,
                                 width=0.3, facecolor=testament_color,
                                 edgecolor='#FFD700', linewidth=1, alpha=0.6)
            ax.add_patch(wedge)

            # Add testament label
            label_angle = current_angle + testament_angle / 2
            label_rad = np.radians(label_angle)
            label_x = 0.35 * np.cos(label_rad)
            label_y = 0.35 * np.sin(label_rad)
            ax.text(label_x, label_y, testament_name, ha='center', va='center',
                   fontsize=10, color='white', fontweight='bold')

            # Draw books
            book_start_angle = current_angle
            for book_name, chapters in books.items():
                book_chapters = len(chapters)
                book_angle = (book_chapters / total_chapters) * 360

                # Book ring
                book_wedge = patches.Wedge((0, 0), 0.8, book_start_angle,
                                          book_start_angle + book_angle,
                                          width=0.3, facecolor=testament_color,
                                          edgecolor='#FFD700', linewidth=0.5,
                                          alpha=0.4)
                ax.add_patch(book_wedge)

                # Book label (only if large enough)
                if book_angle > 3:
                    label_angle = book_start_angle + book_angle / 2
                    label_rad = np.radians(label_angle)
                    label_x = 0.65 * np.cos(label_rad)
                    label_y = 0.65 * np.sin(label_rad)

                    # Rotate text for readability
                    rotation = label_angle - 90 if label_angle < 180 else label_angle + 90

                    ax.text(label_x, label_y, book_name, ha='center', va='center',
                           fontsize=6, color='white', rotation=rotation)

                # Draw chapters (outermost ring)
                chapter_start_angle = book_start_angle
                for chapter_num in sorted(chapters):
                    chapter_angle = (1 / total_chapters) * 360

                    chapter_wedge = patches.Wedge((0, 0), 1.0, chapter_start_angle,
                                                 chapter_start_angle + chapter_angle,
                                                 width=0.2, facecolor=testament_color,
                                                 edgecolor='#FFD700', linewidth=0.2,
                                                 alpha=0.3)
                    ax.add_patch(chapter_wedge)

                    chapter_start_angle += chapter_angle

                book_start_angle += book_angle

            current_angle += testament_angle

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        # Sunburst shows full structure, so just re-render
        self.render()

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export Sunburst Diagram',
            'bible_sunburst_diagram.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
