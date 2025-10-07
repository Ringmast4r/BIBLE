# Bible Cross-Reference Visualizer - Desktop GUI

> Interactive desktop application for exploring Bible cross-references with 3D and 2D visualizations using PyQt5 and Plotly

**Created by [@Ringmast4r](https://github.com/Ringmast4r)**

### 🌐 **[View All Tools: Interactive Landing Page](https://ringmast4r.github.io/BIBLE/)**

> **📌 Note:** This is **one of four ways** to explore Bible cross-references in this project!
> - **🖥️ This Tool (Desktop GUI)** - Professional 3D graphs and offline analysis
> - **💻 [CMD Reader](../bible-analysis-tool/)** - Text-based reading and search
> - **🌐 [Web Visualizer](../bible-visualizer-web/)** - Interactive browser visualizations
> - **⌨️ [Web Terminal](../bible-cmd-web/)** - Browser-based CMD demo

---

## Why Use the Desktop GUI?

**Best for:**
- 🎮 3D interactive network graphs (rotate, zoom, pan)
- 💼 Professional analysis and presentations
- 📴 Offline work (no web server needed)
- 📸 High-resolution exports (300 DPI PNG/SVG)
- 🖥️ Native desktop experience
- 📊 Complex filtering and data manipulation

**Need text reading?** Use the [CMD Reader](../bible-analysis-tool/) instead!
**Want browser-based?** Try the [Web Visualizer](../bible-visualizer-web/) instead!

---

## Features

### 9 Interactive Visualizations

**Cross-Reference Visualizations:**
- **3D Network Graph** - Interactive force-directed graph using Plotly
  - Rotate, zoom, and pan through 3D space
  - Color-coded by testament (Green=OT, Cyan=NT)
  - Hover tooltips with chapter details
  - Physics-based layout

- **Arc Diagram** - Beautiful 2D arc visualization ✨ **UPDATED Oct 7, 2025**
  - **Perfect circular arcs** using Pythagorean theorem formula
  - Mathematical formula: `y = √(r² - x²)` where r = distance/2
  - **Advantages over previous implementation:**
    - No singularities at 90° angles (unlike tan/acos)
    - Faster computation (square root vs trigonometric combo)
    - True circular geometry at all arc lengths
    - Stable and smooth at all connection distances
  - Color-coded connections
  - Testament filtering
  - **Formula details:**
    ```python
    # Perfect circular arcs using Pythagorean theorem
    radius = distance / 2
    center = (x1 + x2) / 2
    center_offset = x_pos - center
    y_offset = np.sqrt(radius**2 - center_offset**2)
    y = y_offset * height / radius  # Scale for visibility
    ```
  - **File:** `components/arc_view.py` (lines 106-127)

- **Chord Diagram** - Circular book-to-book relationships
  - 66 books arranged in a circle
  - Connection chords between books
  - Testament color-coding

- **Heatmap** - 66x66 book connection matrix
  - Intensity-based visualization
  - Testament dividers
  - Book-to-book relationships

- **Sunburst** - Hierarchical Testament→Book→Chapter view
  - Interactive zoom into sections
  - Color-coded by testament
  - Click to explore hierarchy

**Theographic Visualizations:**
- **Geographic Map** - 1,247 biblical places with GPS coordinates
  - World map with biblical location markers
  - Testament color-coding
  - Place names and references

- **Timeline** - Chronological historical events
  - Biblical events on timeline
  - BCE/CE date ranges
  - Event descriptions

- **People Network** - 3,069 biblical figures and relationships
  - Force-directed network of people
  - Relationship connections
  - Interactive exploration

**Analytics:**
- **Statistics Dashboard** - Comprehensive metrics
  - Top books by connections
  - Testament distribution
  - Connection weight analysis
  - Cross-reference statistics

## Installation

### Requirements

- Python 3.8+
- Windows/Mac/Linux

### Setup

1. **Install dependencies:**
   ```bash
   cd bible-visualizer-desktop
   pip install -r requirements.txt
   ```

2. **Verify data files exist:**
   - Ensure `../shared-data/processed/graph_data.json` exists
   - If not, run: `cd ../shared-data && python data_processor.py`

## Usage

### Launch Application

```bash
python visualizer_app.py
```

Or on Windows, double-click `launch.bat`

### Controls

**Filters Panel:**
- **Testament Filter** - Show only OT, NT, or cross-testament connections
- **Min Connections Slider** - Filter weak connections
- **Reset Filters** - Clear all filters
- **Export Current View** - Save visualization as image

**3D Network Graph:**
- **Left Click + Drag** - Rotate view
- **Scroll** - Zoom in/out
- **Right Click + Drag** - Pan view
- **Hover** - Show chapter details

**Tab Navigation:**
- Switch between different visualization types
- Each view updates based on filter settings

## Data

- **Source**: Treasury of Scripture Knowledge via OpenBible.info
- **Connections**: 190,522 chapter-level cross-references
- **Chapters**: 1,189 total chapters
- **Books**: 66 Bible books

## Color Scheme

Matches the CMD tool and web visualizer:
- **Gold (#FFD700)** - Headers, highlights
- **Cyan (#00CED1)** - New Testament
- **Green (#2ecc71)** - Old Testament
- **Purple (#9370DB)** - Cross-testament connections
- **Dark Background** - For optimal contrast

## Technical Stack

- **PyQt5** - GUI framework
- **Plotly** - 3D interactive graphs
- **Matplotlib** - 2D static visualizations
- **NetworkX** - Graph algorithms and layouts
- **Seaborn** - Statistical visualizations
- **Pandas/NumPy** - Data processing

## Project Structure

```
bible-desktop-gui/
├── visualizer_app.py            # Main application
├── theographic_data.py          # Theographic data loader
├── requirements.txt             # Python dependencies
├── launch.bat                   # Windows launcher (optional)
├── components/
│   ├── network_view.py          # 3D network graph (Plotly)
│   ├── network_view_matplotlib.py # 3D network (Matplotlib fallback)
│   ├── arc_view.py              # 2D arc diagram
│   ├── chord_view.py            # Circular chord diagram
│   ├── heatmap_view.py          # 66x66 book heatmap
│   ├── sunburst_view.py         # Hierarchical sunburst
│   ├── geographic_map_view.py   # Biblical places map
│   ├── timeline_view.py         # Historical timeline
│   ├── people_network_view.py   # People relationships
│   └── stats_view.py            # Statistics dashboard
├── test_data_loading.py         # Data loading tests
└── README.md                    # This file
```

## Exporting Visualizations

All views support export:
1. Select the visualization tab
2. Click "Export Current View"
3. Choose PNG or SVG format
4. High-resolution output (300 DPI)

## Troubleshooting

### Application won't start
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### "Data files not found" error
- Run data processor: `cd ../shared-data && python data_processor.py`
- Verify `graph_data.json` exists in `../shared-data/processed/`

### 3D graph not displaying
- Ensure PyQtWebEngine is installed: `pip install PyQtWebEngine`
- Try updating Plotly: `pip install --upgrade plotly`

### Slow performance
- Increase minimum connections filter to reduce graph complexity
- Filter by testament to show fewer nodes
- Close other applications to free memory

## Performance Notes

- **3D Network**: May be slow with all 1,189 chapters
  - Recommended: Use filters to show subset
  - Minimum connections slider helps performance

- **Heatmap**: Fast, shows all 66 books simultaneously

- **Arc Diagram**: Performance depends on connection count
  - Filter to improve rendering speed

## Future Enhancements

- [ ] Community detection coloring (Louvain algorithm)
- [ ] Search by verse reference
- [ ] Click nodes to show verse text
- [ ] Animation of cross-reference patterns
- [ ] Save/load filter presets
- [ ] Export to interactive HTML
- [ ] Standalone executable (.exe)

## Related Projects

- **bible-analysis-tool** - Original CMD reader
- **bible-visualizer-web** - Web-based visualizations
- **shared-data** - Data processing scripts

## Credits

**Data Sources:**
- **[Treasury of Scripture Knowledge](https://www.openbible.info/labs/cross-references/)** - 340,000+ cross-references (Public Domain)
- **[OpenBible.info](https://www.openbible.info)** - Cross-reference data digitization (CC Attribution)
- **[Theographic Bible Metadata](https://github.com/robertrouse/theographic-bible-metadata)** - People, places, events knowledge graph (CC BY-SA 4.0)

**Libraries:**
- **PyQt5** - GUI framework
- **Plotly** - Interactive 3D visualizations
- **NetworkX** - Graph algorithms
- **Matplotlib & Seaborn** - Statistical visualizations

---

**May this tool help you explore the beautiful interconnections in God's Word!**
