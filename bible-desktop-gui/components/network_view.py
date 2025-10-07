"""
3D Network Graph Visualization using Matplotlib (Fallback)
Interactive force-directed graph of Bible cross-references
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np


class NetworkView(QWidget):
    """3D Network graph visualization component (Matplotlib version)"""

    def __init__(self):
        super().__init__()
        self.data = None
        self.graph = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Info label
        self.info_label = QLabel('Loading network data...')
        self.info_label.setStyleSheet('color: #00CED1; padding: 10px;')
        layout.addWidget(self.info_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(14, 12), facecolor='#1a1a2e')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set style
        plt.style.use('dark_background')

    def set_data(self, data):
        """Set data and build graph"""
        try:
            self.data = data
            self.build_graph()
            self.render()
        except Exception as e:
            error_msg = f'✗ Error loading network: {e}'
            self.info_label.setText(error_msg)
            print(f"NetworkView error: {e}")
            import traceback
            traceback.print_exc()

    def build_graph(self):
        """Build NetworkX graph from data"""
        self.graph = nx.Graph()

        # PERFORMANCE: Limit to top 300 connections to prevent freezing
        connections = sorted(
            self.data['connections'],
            key=lambda x: x['weight'],
            reverse=True
        )[:300]

        # Get unique chapter IDs
        chapter_ids = set()
        for conn in connections:
            chapter_ids.add(conn['source'])
            chapter_ids.add(conn['target'])

        # Add nodes
        for chapter in self.data['chapters']:
            if chapter['id'] in chapter_ids:
                self.graph.add_node(
                    chapter['id'],
                    book=chapter['book'],
                    chapter_num=chapter['chapter'],
                    testament=chapter['testament']
                )

        # Add edges
        for conn in connections:
            if conn['source'] in self.graph and conn['target'] in self.graph:
                self.graph.add_edge(
                    conn['source'],
                    conn['target'],
                    weight=conn['weight']
                )

        self.info_label.setText(f'✓ Loaded {len(self.graph.nodes())} chapters, {len(self.graph.edges())} connections')

    def render(self, filters=None):
        """Render 3D network graph"""
        if not self.graph:
            return

        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111, projection='3d')
            ax.set_facecolor('#1a1a2e')

            # Apply filters if provided
            graph = self.graph.copy()
            if filters:
                graph = self.filter_graph(graph, filters)

            if len(graph.nodes()) == 0:
                ax.text(0.5, 0.5, 0.5, 'No data matches filters',
                       ha='center', va='center', color='#FFD700', fontsize=14)
                self.canvas.draw()
                return

            # Calculate 3D spring layout
            pos = nx.spring_layout(graph, dim=3, k=0.3, iterations=30, seed=42)

            # Separate nodes by testament
            ot_nodes = [n for n in graph.nodes() if graph.nodes[n]['testament'] == 'OT']
            nt_nodes = [n for n in graph.nodes() if graph.nodes[n]['testament'] == 'NT']

            # Plot edges
            for edge in graph.edges():
                x = [pos[edge[0]][0], pos[edge[1]][0]]
                y = [pos[edge[0]][1], pos[edge[1]][1]]
                z = [pos[edge[0]][2], pos[edge[1]][2]]
                ax.plot(x, y, z, color='#16213e', alpha=0.3, linewidth=0.5)

            # Plot OT nodes
            if ot_nodes:
                x = [pos[n][0] for n in ot_nodes]
                y = [pos[n][1] for n in ot_nodes]
                z = [pos[n][2] for n in ot_nodes]
                ax.scatter(x, y, z, c='#2ecc71', s=50, alpha=0.8,
                          edgecolors='#FFD700', linewidths=0.5, label='Old Testament')

            # Plot NT nodes
            if nt_nodes:
                x = [pos[n][0] for n in nt_nodes]
                y = [pos[n][1] for n in nt_nodes]
                z = [pos[n][2] for n in nt_nodes]
                ax.scatter(x, y, z, c='#00CED1', s=50, alpha=0.8,
                          edgecolors='#FFD700', linewidths=0.5, label='New Testament')

            # Styling
            ax.set_xlabel('', color='#00CED1')
            ax.set_ylabel('', color='#00CED1')
            ax.set_zlabel('', color='#00CED1')
            ax.set_title(f'Bible Cross-Reference Network\n({len(graph.nodes())} chapters, {len(graph.edges())} connections)',
                        color='#FFD700', fontsize=14, fontweight='bold', pad=20)

            # Remove tick labels
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_zticklabels([])

            # Set background
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.xaxis.pane.set_edgecolor('none')
            ax.yaxis.pane.set_edgecolor('none')
            ax.zaxis.pane.set_edgecolor('none')
            ax.grid(False)

            # Legend
            ax.legend(loc='upper right', facecolor='#16213e', edgecolor='#FFD700')

            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            print(f"Error rendering network: {e}")
            import traceback
            traceback.print_exc()

    def filter_graph(self, graph, filters):
        """Apply filters to graph"""
        filtered = graph.copy()

        testament = filters.get('testament', 'All')
        min_connections = filters.get('min_connections', 1)

        # Filter by testament
        if testament != 'All':
            nodes_to_remove = []
            for node in filtered.nodes():
                node_testament = filtered.nodes[node]['testament']

                if testament == 'Old Testament' and node_testament != 'OT':
                    nodes_to_remove.append(node)
                elif testament == 'New Testament' and node_testament != 'NT':
                    nodes_to_remove.append(node)
                elif testament == 'Cross-Testament':
                    neighbors = list(filtered.neighbors(node))
                    has_cross = any(
                        filtered.nodes[n]['testament'] != node_testament
                        for n in neighbors
                    )
                    if not has_cross:
                        nodes_to_remove.append(node)

            filtered.remove_nodes_from(nodes_to_remove)

        # Filter by minimum connections
        nodes_to_remove = [
            node for node in filtered.nodes()
            if filtered.degree(node) < min_connections
        ]
        filtered.remove_nodes_from(nodes_to_remove)

        return filtered

    def apply_filters(self, filters):
        """Apply filters and re-render"""
        self.render(filters)

    def export(self):
        """Export current view"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Export 3D Network',
            'bible_3d_network.png',
            'PNG Files (*.png);;SVG Files (*.svg)'
        )

        if filename:
            self.figure.savefig(filename, facecolor='#1a1a2e', dpi=300)
