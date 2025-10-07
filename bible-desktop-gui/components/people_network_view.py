"""
People Network Visualization using NetworkX and Matplotlib
Shows relationships between 3,000+ biblical people
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class PeopleNetworkView(QWidget):
    """People network visualization component"""

    def __init__(self):
        super().__init__()
        self.people_data = None
        self.groups_data = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Info label
        self.info_label = QLabel('Loading people network data...')
        self.info_label.setStyleSheet('color: #00CED1; padding: 10px;')
        layout.addWidget(self.info_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(14, 14), facecolor='#1a1a2e')
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

            self.people_data = theographic_loader.get_people()
            self.groups_data = theographic_loader.get_people_groups()
            self.info_label.setText(f'✓ Loaded {len(self.people_data)} people and {len(self.groups_data)} groups')
            print(f"PeopleNetworkView: Loaded {len(self.people_data)} people, {len(self.groups_data)} groups")
            self.render()
        except Exception as e:
            error_msg = f'✗ Error loading people network data: {e}'
            self.info_label.setText(error_msg)
            print(f"PeopleNetworkView error: {e}")
            import traceback
            traceback.print_exc()

    def render(self):
        """Render people network"""
        if not self.people_data or not self.groups_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1a1a2e')

        # Build network from groups (people connected through shared groups)
        group_members = defaultdict(list)

        # Map people to their groups
        for person in self.people_data:
            fields = person.get('fields', {})
            person_id = person.get('pk')
            name = fields.get('name', 'Unknown')
            groups = fields.get('peopleGroups', [])

            if person_id and groups:
                for group_id in groups:
                    group_members[group_id].append({
                        'id': person_id,
                        'name': name,
                        'gender': fields.get('gender', 'Unknown'),
                        'verses': fields.get('verses', [])
                    })

        # Find people with most connections (top 100)
        person_connections = defaultdict(set)
        for group_id, members in group_members.items():
            if len(members) > 1:  # Only groups with multiple members
                for member in members:
                    # Connect to other members in same group
                    for other in members:
                        if member['id'] != other['id']:
                            person_connections[member['id']].add(other['id'])

        # Sort by connection count
        top_people = sorted(person_connections.items(),
                          key=lambda x: len(x[1]), reverse=True)[:100]

        # Build positions using force-directed layout approximation
        positions = self._calculate_positions(top_people, person_connections)

        # Get person details
        person_lookup = {p.get('pk'): p.get('fields', {})
                        for p in self.people_data}

        # Draw edges (connections)
        for person_id, connections in top_people:
            if person_id not in positions:
                continue

            x1, y1 = positions[person_id]

            for connected_id in connections:
                if connected_id in positions:
                    x2, y2 = positions[connected_id]
                    ax.plot([x1, x2], [y1, y2], color='#16213e',
                           alpha=0.2, linewidth=0.5, zorder=1)

        # Draw nodes (people)
        for person_id, connections in top_people:
            if person_id not in positions:
                continue

            x, y = positions[person_id]
            person_fields = person_lookup.get(person_id, {})
            gender = person_fields.get('gender', 'Unknown')
            name = person_fields.get('name', 'Unknown')
            verse_count = len(person_fields.get('verses', []))

            # Color by gender
            if gender == 'Male':
                color = '#00CED1'
            elif gender == 'Female':
                color = '#FF69B4'
            else:
                color = '#808080'

            # Size by verse mentions
            size = max(50, min(500, verse_count * 10))

            ax.scatter(x, y, s=size, c=color, alpha=0.7,
                      edgecolors='white', linewidths=1, zorder=2)

            # Add label for major figures (top 30)
            if verse_count > 20:
                ax.text(x, y + 0.03, name, fontsize=7, ha='center', va='bottom',
                       color='white', alpha=0.8, fontweight='bold')

        # Styling
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Biblical People Network (Top {len(top_people)} connected individuals)',
                     color='#FFD700', fontsize=16, fontweight='bold', pad=20)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#00CED1', label='Male', alpha=0.7),
            Patch(facecolor='#FF69B4', label='Female', alpha=0.7),
            Patch(facecolor='#808080', label='Unknown Gender', alpha=0.7)
        ]
        ax.legend(handles=legend_elements, loc='upper right',
                 facecolor='#16213e', edgecolor='#FFD700')

        self.figure.tight_layout()
        self.canvas.draw()

    def _calculate_positions(self, top_people, person_connections):
        """Calculate node positions using simple force-directed layout"""
        # Initialize random positions
        positions = {}
        person_ids = [p[0] for p in top_people]

        # Random circular layout as starting point
        n = len(person_ids)
        for i, person_id in enumerate(person_ids):
            angle = 2 * np.pi * i / n
            positions[person_id] = [np.cos(angle), np.sin(angle)]

        # Simple force-directed iterations
        for iteration in range(50):
            forces = defaultdict(lambda: [0.0, 0.0])

            # Repulsive forces between all nodes
            for i, id1 in enumerate(person_ids):
                for id2 in person_ids[i+1:]:
                    x1, y1 = positions[id1]
                    x2, y2 = positions[id2]

                    dx = x2 - x1
                    dy = y2 - y1
                    dist = np.sqrt(dx*dx + dy*dy) + 0.01

                    # Repulsion
                    force = 0.01 / (dist * dist)
                    forces[id1][0] -= force * dx / dist
                    forces[id1][1] -= force * dy / dist
                    forces[id2][0] += force * dx / dist
                    forces[id2][1] += force * dy / dist

            # Attractive forces for connected nodes
            for person_id, connections in top_people:
                if person_id not in positions:
                    continue

                x1, y1 = positions[person_id]

                for connected_id in connections:
                    if connected_id in positions:
                        x2, y2 = positions[connected_id]

                        dx = x2 - x1
                        dy = y2 - y1
                        dist = np.sqrt(dx*dx + dy*dy) + 0.01

                        # Attraction
                        force = dist * 0.01
                        forces[person_id][0] += force * dx / dist
                        forces[person_id][1] += force * dy / dist

            # Apply forces
            for person_id in person_ids:
                positions[person_id][0] += forces[person_id][0]
                positions[person_id][1] += forces[person_id][1]

                # Keep within bounds
                dist = np.sqrt(positions[person_id][0]**2 + positions[person_id][1]**2)
                if dist > 1.0:
                    positions[person_id][0] /= dist
                    positions[person_id][1] /= dist

        return positions

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        self.render()

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export People Network',
            'bible_people_network.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
