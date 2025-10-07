"""
Timeline Visualization using Matplotlib
Chronological view of biblical events
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime


class TimelineView(QWidget):
    """Timeline visualization component"""

    def __init__(self):
        super().__init__()
        self.events_data = None
        self.periods_data = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Info label
        self.info_label = QLabel('Loading timeline data...')
        self.info_label.setStyleSheet('color: #00CED1; padding: 10px;')
        layout.addWidget(self.info_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(16, 10), facecolor='#1a1a2e')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set style
        plt.style.use('dark_background')

    def set_theographic_data(self, theographic_loader):
        """Set theographic data"""
        try:
            if not theographic_loader or not theographic_loader.is_loaded:
                self.info_label.setText('⚠ Theographic data not available')
                return

            self.events_data = theographic_loader.get_events()
            self.periods_data = theographic_loader.get_periods()
            self.info_label.setText(f'✓ Loaded {len(self.events_data)} events and {len(self.periods_data)} periods')
            print(f"TimelineView: Loaded {len(self.events_data)} events, {len(self.periods_data)} periods")
            self.render()
        except Exception as e:
            error_msg = f'✗ Error loading timeline data: {e}'
            self.info_label.setText(error_msg)
            print(f"TimelineView error: {e}")
            import traceback
            traceback.print_exc()

    def render(self):
        """Render timeline"""
        if not self.events_data or not self.periods_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1a1a2e')

        # Filter events with valid dates
        valid_events = []
        for event in self.events_data:
            fields = event.get('fields', {})
            start_date = fields.get('startDate')
            if start_date:
                valid_events.append(event)

        # Sort by date
        valid_events.sort(key=lambda e: e['fields'].get('startDate', ''))

        # Take subset for visibility (top 100)
        display_events = valid_events[:100]

        # Draw periods as background bands
        period_colors = ['#2ecc71', '#00CED1', '#9370DB', '#FFD700', '#FF6347']
        for i, period in enumerate(self.periods_data[:20]):  # Limit periods
            fields = period.get('fields', {})
            start_date = fields.get('startDate')
            end_date = fields.get('endDate')
            name = fields.get('name', 'Unknown Period')

            if start_date and end_date:
                try:
                    start_year = self._parse_year(start_date)
                    end_year = self._parse_year(end_date)

                    color = period_colors[i % len(period_colors)]
                    ax.axvspan(start_year, end_year, alpha=0.1, color=color)

                    # Add period label
                    mid_year = (start_year + end_year) / 2
                    ax.text(mid_year, 95, name, ha='center', va='top',
                           fontsize=8, color=color, alpha=0.6, rotation=0)
                except:
                    pass

        # Plot events
        for i, event in enumerate(display_events):
            fields = event.get('fields', {})
            start_date = fields.get('startDate')
            name = fields.get('name', 'Unknown Event')

            try:
                year = self._parse_year(start_date)

                # Determine color based on testament
                testament = fields.get('testament', 'OT')
                color = '#2ecc71' if testament == 'OT' else '#00CED1'

                # Plot event point
                y_pos = 50 + (i % 40) * 1  # Stagger vertically
                ax.plot(year, y_pos, 'o', color=color, markersize=8, alpha=0.7)

                # Add label for major events (every 5th)
                if i % 5 == 0:
                    ax.text(year, y_pos + 2, name, fontsize=6,
                           ha='left', va='bottom', color='white', alpha=0.7,
                           rotation=45)

            except Exception as e:
                continue

        # Styling
        ax.set_xlabel('Year (BCE/CE)', color='#00CED1', fontsize=12, fontweight='bold')
        ax.set_ylabel('Events', color='#00CED1', fontsize=12)
        ax.set_title(f'Biblical Events Timeline ({len(display_events)} events shown)',
                     color='#FFD700', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylim(40, 100)
        ax.grid(True, axis='x', color='#16213e', linestyle='--', alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ecc71', label='Old Testament', alpha=0.7),
            Patch(facecolor='#00CED1', label='New Testament', alpha=0.7)
        ]
        ax.legend(handles=legend_elements, loc='upper left',
                 facecolor='#16213e', edgecolor='#FFD700')

        self.figure.tight_layout()
        self.canvas.draw()

    def _parse_year(self, date_str):
        """Parse year from various date formats"""
        # Handle BCE dates (negative)
        if 'BCE' in str(date_str):
            year_str = str(date_str).replace('BCE', '').strip()
            return -int(year_str)

        # Handle CE dates
        if 'CE' in str(date_str):
            year_str = str(date_str).replace('CE', '').strip()
            return int(year_str)

        # Try to parse as integer
        try:
            return int(date_str)
        except:
            # Try to extract year from ISO date
            if '-' in str(date_str):
                parts = str(date_str).split('-')
                return int(parts[0])

            return 0

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        self.render()

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export Timeline',
            'bible_timeline.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
