"""
Geographic Map Visualization using Matplotlib
Shows 1,600+ biblical places with GPS coordinates
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class GeographicMapView(QWidget):
    """Geographic map visualization component"""

    def __init__(self):
        super().__init__()
        self.places_data = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Info label
        self.info_label = QLabel('Loading geographic data...')
        self.info_label.setStyleSheet('color: #00CED1; padding: 10px;')
        layout.addWidget(self.info_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(14, 10), facecolor='#1a1a2e')
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

            self.places_data = theographic_loader.get_places_with_coords()
            self.info_label.setText(f'✓ Loaded {len(self.places_data)} places with GPS coordinates')
            print(f"GeographicMapView: Loaded {len(self.places_data)} places")
            self.render()
        except Exception as e:
            error_msg = f'✗ Error loading geographic data: {e}'
            self.info_label.setText(error_msg)
            print(f"GeographicMapView error: {e}")
            import traceback
            traceback.print_exc()

    def render(self):
        """Render geographic map"""
        if not self.places_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1a1a2e')

        # Extract coordinates and metadata
        lats = []
        lons = []
        colors = []
        sizes = []
        labels = []

        # Feature type colors
        type_colors = {
            'City': '#FFD700',
            'Region': '#00CED1',
            'Water': '#4169E1',
            'Mountain': '#8B4513',
            'Unknown': '#808080'
        }

        for place in self.places_data:
            fields = place.get('fields', {})
            lat = fields.get('latitude')
            lon = fields.get('longitude')
            name = fields.get('name', 'Unknown')
            feature = fields.get('feature', 'Unknown')
            verses_count = fields.get('verses_count', 0)

            if lat is not None and lon is not None:
                lats.append(lat)
                lons.append(lon)
                labels.append(name)
                colors.append(type_colors.get(feature, type_colors['Unknown']))
                # Size based on verse mentions
                sizes.append(max(10, min(100, verses_count * 2)))

        # Draw world map outline (simple)
        self._draw_world_outline(ax)

        # Plot places
        scatter = ax.scatter(lons, lats, c=colors, s=sizes, alpha=0.6,
                            edgecolors='white', linewidths=0.5)

        # Add labels for major places (top 50 by verse count)
        place_sizes = list(zip(labels, lons, lats, sizes))
        place_sizes.sort(key=lambda x: x[3], reverse=True)

        for label, lon, lat, size in place_sizes[:50]:
            ax.text(lon, lat, label, fontsize=6, ha='left', va='bottom',
                   color='white', alpha=0.7)

        # Styling
        ax.set_xlabel('Longitude', color='#00CED1', fontsize=12)
        ax.set_ylabel('Latitude', color='#00CED1', fontsize=12)
        ax.set_title(f'Biblical Places Map ({len(self.places_data)} locations)',
                     color='#FFD700', fontsize=16, fontweight='bold', pad=20)

        # Add grid
        ax.grid(True, color='#16213e', linestyle='--', alpha=0.3)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=type_colors['City'], label='City'),
            Patch(facecolor=type_colors['Region'], label='Region'),
            Patch(facecolor=type_colors['Water'], label='Water'),
            Patch(facecolor=type_colors['Mountain'], label='Mountain')
        ]
        ax.legend(handles=legend_elements, loc='upper left',
                 facecolor='#16213e', edgecolor='#FFD700')

        # Focus on Middle East region (biblical lands)
        ax.set_xlim(20, 50)
        ax.set_ylim(25, 45)

        self.figure.tight_layout()
        self.canvas.draw()

    def _draw_world_outline(self, ax):
        """Draw simple world coastline outline"""
        # Simple coastlines for Middle East region
        # Mediterranean Sea
        med_coast_x = [20, 25, 30, 35, 38, 40, 38, 35, 30, 25, 20]
        med_coast_y = [32, 33, 34, 35, 36, 35, 33, 32, 31, 31, 32]
        ax.plot(med_coast_x, med_coast_y, color='#4169E1', alpha=0.3, linewidth=2)

        # Red Sea
        red_sea_x = [32, 35, 38, 40, 42]
        red_sea_y = [30, 28, 26, 24, 22]
        ax.plot(red_sea_x, red_sea_y, color='#4169E1', alpha=0.3, linewidth=2)

        # Persian Gulf
        gulf_x = [47, 49, 50, 49, 48]
        gulf_y = [30, 29, 28, 27, 26]
        ax.plot(gulf_x, gulf_y, color='#4169E1', alpha=0.3, linewidth=2)

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        # Geographic map doesn't use testament filters
        self.render()

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export Geographic Map',
            'bible_geographic_map.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
