<div align="center">

![MiB Flash](assets/proselytized.gif)

# **🔦 GET PROSELYTIZED! 🔦**

### *You just got evangelized by the most powerful Bible exploration tools*

---

</div>

# Bible Cross-Reference Analysis & Visualization Project

> Explore 340,000+ Bible cross-references + 3,000+ people + 1,600+ places through **four different interfaces**: Command Line, Desktop GUI, Web Visualizer, and Web Terminal

**Created by [@Ringmast4r](https://github.com/Ringmast4r)**

### 🆕 NEW: Now with Geographic & Historical Data!
- 🗺️ **1,600+ Biblical Places** with GPS coordinates
- 👥 **3,000+ Biblical People** with relationships
- ⏱️ **1,700+ Historical Events** with timeline data
- 📖 **Easton's Bible Dictionary** integrated

![Project Status](https://img.shields.io/badge/Status-100%25%20Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

---

## 🚨 FOR DEVELOPERS: READ FIRST

**⚠️ CRITICAL RULE #1:** If you're contributing to this project, **IMMEDIATELY** read [`DEVELOPER_RULES.md`](DEVELOPER_RULES.md) **BEFORE** making any commits.

**Key Rule:** NEVER include Claude or any AI as co-author. ALL commits must be by @Ringmast4r only.

**Why:** We already had to delete and recreate this entire repository once due to accidental AI co-authoring. Don't repeat this mistake!

---

## 🌐 Live Demos

### 🚀 **[START HERE: Interactive Landing Page](https://ringmast4r.github.io/BIBLE/)**
**Choose your preferred tool from our beautiful landing page!**

**Direct Links** - No installation required:
- **[📊 Web Visualizer](https://ringmast4r.github.io/BIBLE/bible-visualizer-web/)** - 9 Interactive visualizations + Geographic Map + Timeline + People Network ✅ **PRODUCTION**
- **[⌨️ Web Terminal](https://ringmast4r.github.io/BIBLE/bible-cmd-web/)** - Browser-based CMD interface ⚙️ **IN DEVELOPMENT** (still needs refinement)

---

## 🎯 Four Ways to Explore the Data

This project gives you **four completely different ways** to explore the same Bible cross-reference dataset:

```
                        ┌─────────────────────────────────┐
                        │   340,000+ Cross-References     │
                        │   (Same Data, Four Interfaces)  │
                        └────────────┬────────────────────┘
                                     │
                    ┌────────────────┼────────────────┬────────────────┐
                    │                │                │                │
                    ▼                ▼                ▼                ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │ CMD Reader   │  │ Web Visualizer│  │ Desktop GUI  │  │ Web Terminal │
            │              │  │              │  │              │  │              │
            │ 💻 Python    │  │ 🌐 D3.js     │  │ 🖥️ PyQt5    │  │ ⌨️ Browser  │
            │ Read & Search│  │ Visualize    │  │ 3D Graphs    │  │ CMD Demo     │
            └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

### 1. 💻 **CMD Reader** - Text-Based Interface
**Best for:** Reading verses, searching keywords, studying cross-references

**Core Features:**
- Read any verse or chapter from 4 Bible translations (KJV, ASV, WEB, YLT)
- Search keywords across all translations
- See cross-references for every verse
- Beautiful colored terminal interface with 6 theme options

**New Enhanced Features:**
- 📊 **Statistics Dashboard** - Comprehensive Bible metrics and top verses
- 📚 **Books List** - View all 66 books with chapter counts
- 🔄 **Compare Translations** - See any verse in all 4 translations side-by-side
- 📜 **History Tracking** - Automatically tracks last 50 viewed verses
- ⭐ **Bookmark System** - Save and view favorite verses
- 🔍 **Advanced Search** - Filter by testament (--ot/--nt), book (--book), exact phrase (--exact)
- ⏭️ **Chapter Navigation** - Next/prev commands with auto book wrapping
- 🎲 **Random Verse** - Discover any verse in the Bible
- 💾 **Export** - Save bookmarks and history to text files

**Launch:**
```bash
cd bible-analysis-tool
python bible_reader.py
```

---

### 2. 🖥️ **Desktop GUI** - Interactive Desktop Application
**Best for:** Professional analysis, 3D visualizations, offline work

**9 Interactive Visualizations:**
- **3D Network Graph** - Rotate and explore connections in 3D space
- **2D Arc Diagram** - Beautiful flowing arcs showing relationships
- **Chord Diagram** - Circular book-to-book relationships
- **Heatmap** - 66x66 book connection matrix
- **Sunburst** - Hierarchical Testament→Book→Chapter view with zoom
- **Geographic Map** - 1,247 biblical places with GPS coordinates
- **Timeline** - Chronological historical events visualization
- **People Network** - 3,069 biblical figures and their relationships
- **Statistics Dashboard** - Comprehensive charts and metrics

**Features:**
- Filter by testament, connection strength
- Export visualizations as PNG/SVG (300 DPI)
- Theographic data integration (people, places, events)
- Real-time filtering and updates

**Launch:**
```bash
cd bible-desktop-gui
python visualizer_app.py
```

Or on Windows: Double-click `BibleVisualizer.bat`

---

### 3. 🌐 **Web Visualizer** - Beautiful Interactive Visualizations
**Best for:** Stunning visuals, interactive exploration, presentations

**✨ NEW - October 7, 2025:**
- ✅ **Responsive Design** - Auto-resizes with window changes (250ms debouncing)
- ✅ **Ultra-Wide Support** - Perfect for 49-inch monitors (up to 5120px)
- ✅ **Enhanced Detail** - More visible arcs and colors on large displays
- ✅ **Full-Width Expansion** - No 1600px limit, uses 100% screen width

**9 Interactive Visualizations:**
- **Arc Diagram (Tableau Style)** - 190,522 connections as perfect circular arcs
  - Pythagorean theorem formula: `y = √(r² - x²)`
  - Rainbow gradient distance-based coloring
  - Auto-resize feature for responsive design
  - Inspired by Chris Harrison 2007 visualization
- **Network Graph** - Force-directed graph with drag and zoom
- **Chord Diagram** - Circular book relationships
- **Heatmap** - Interactive 66x66 matrix
- **Sunburst** - Hierarchical Testament→Book→Chapter with zoom
- **Geographic Map** - Biblical places visualization
- **Timeline** - Historical events chronologically
- **People Network** - Biblical figures and relationships
- **Statistics** - Comprehensive metrics and charts
- All visualizations respond to filters in real-time

**Launch:**
```bash
# Visit live demo:
https://ringmast4r.github.io/BIBLE/bible-visualizer-web/

# Or run locally:
cd bible-visualizer-web
python -m http.server 8000
# Then open: http://localhost:8000/index.html
```

Or on Windows: Double-click `launch-server.bat`

---

### 4. ⌨️ **Web Terminal** - Browser-Based CMD Demo
**Best for:** Trying CMD features online, no installation, instant access

- Terminal-style interface in your browser
- All CMD reader features (verse lookup, search, cross-references)
- 4 Bible translations with instant switching
- Command history with arrow keys
- Daily inspirational verse
- No Python installation required

**Launch:**
```bash
# Visit live demo:
https://ringmast4r.github.io/BIBLE/bible-cmd-web/

# Or run locally:
cd bible-cmd-web
python -m http.server 8001
# Then open: http://localhost:8001/index.html
```

---

## 🚀 Quick Start - Launch Everything

**Windows Users:**
```bash
# Double-click this file to launch all four:
LAUNCH-ALL.bat
```

This will open:
- Web visualizer with D3.js graphs
- Desktop GUI application with 3D graphs
- Command line Bible reader
- Web terminal demo in browser

**Mac/Linux Users:**
```bash
# Terminal 1 - Web Visualizer
cd bible-visualizer-web && python3 -m http.server 8000

# Terminal 2 - Web Terminal
cd bible-cmd-web && python3 -m http.server 8001

# Terminal 3 - Desktop GUI
cd bible-desktop-gui && python3 visualizer_app.py

# Terminal 4 - CMD Reader
cd bible-analysis-tool && python3 bible_reader.py
```

---

## 📊 What's Included

### Data
- **344,799** verse-level cross-references (Treasury of Scripture Knowledge)
- **190,522** chapter-level connections (processed for visualization)
- **4 Bible translations**: KJV, ASV, WEB, YLT
- **66 books**, **1,189 chapters**, **31,000+ verses**

### Visualizations
- **17 different visualizations** across web and desktop (9 in Desktop GUI, 8 in Web Visualizer)
- **Interactive filtering** by testament, book, connection strength
- **Export capabilities** - Save as PNG, SVG, or HTML
- **Theographic integration** - Biblical people, places, and historical events

### Applications
- **4 complete interfaces** to explore the same data
- **Cross-platform** - Works on Windows, Mac, Linux
- **Offline-capable** - CMD Reader and Desktop GUI work offline
- **Online demos** - Web Visualizer and Web Terminal for instant access

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install Dependencies

**For CMD Reader:**
```bash
cd bible-analysis-tool
pip install colorama
```

**For Desktop Visualizer:**
```bash
cd bible-desktop-gui
pip install -r requirements.txt
```
*Installs: PyQt5, Plotly, NetworkX, Matplotlib, Seaborn, NumPy, Pandas*

**For Web Visualizer:**
- No installation needed! Uses Python's built-in HTTP server
- Just needs a modern web browser

**For Web Terminal:**
- No installation needed! Visit live demo or run local HTTP server
- Just needs a modern web browser

---

## 🎨 Which Interface Should I Use?

| Use Case | Best Option |
|----------|-------------|
| Reading Bible verses and studying cross-references | **CMD Reader** or **Web Terminal** |
| Quick keyword searches across translations | **CMD Reader** or **Web Terminal** |
| Beautiful presentations and screenshots | **Web Visualizer** |
| Interactive exploration and filtering | **Web Visualizer** |
| 3D visualizations and professional analysis | **Desktop GUI** |
| Offline work with no internet | **Desktop GUI** or **CMD Reader** |
| Exporting high-resolution images | **Desktop GUI** |
| Sharing visualizations with others | **Web Visualizer** |
| Trying before installing | **Web Terminal** or **Web Visualizer** |
| Demo for others online | **Web Terminal** or **Web Visualizer** |

---

## 📖 Documentation

Each component has detailed documentation:

- **[CMD Reader Guide](bible-analysis-tool/README.md)** - How to use the command line tool
- **[Web Visualizer Guide](bible-visualizer-web/README.md)** - Web interface and visualizations
- **[Desktop GUI Guide](bible-desktop-gui/README.md)** - Desktop application features
- **[Web Terminal Guide](bible-cmd-web/README.md)** - Browser-based CMD demo
- **[Developer Memory](bible-analysis-tool/MEMORY.md)** - Technical notes and gotchas
- **[Project Status](PROJECT_STATUS.md)** - Current implementation status

---

## 🎯 Example Usage

### CMD Reader - Search and Read
```
Enter command: love
→ Shows all verses containing "love" across all translations

Enter command: John 3:16
→ Displays verse with cross-references in beautiful colors

Enter command: translations
→ Lists available Bible versions
```

### Desktop GUI - Visual Analysis
1. Launch application
2. Click "3D Network Graph" tab
3. Drag to rotate, scroll to zoom
4. Adjust "Min Connections" slider to simplify
5. Click "Export Current View" to save

### Web Browser - Interactive Exploration
1. Open http://localhost:8000/index.html
2. Click through 6 different visualization tabs
3. Use Testament filter to focus on OT or NT
4. Hover over elements for tooltips
5. Click on Sunburst sections to zoom in

---

## 🛠️ Technical Stack

### CMD Reader
- Python 3.8+
- Colorama (terminal colors)
- JSON data files

### Web Visualizer
- D3.js v7 (visualizations)
- Vanilla JavaScript
- HTML5/CSS3
- Python HTTP server

### Desktop Visualizer
- PyQt5 (GUI framework)
- Plotly (3D graphs)
- NetworkX (graph algorithms)
- Matplotlib (2D charts)
- Seaborn (heatmaps)

---

## 📂 Project Structure

```
bible-cmd-reader/
├── index.html                        # Landing page with all 4 tools
├── LAUNCH-ALL.bat                    # Launch all applications (Windows)
├── README.md                         # This file
├── PROJECT_STATUS.md                 # Detailed project status
│
├── bible-analysis-tool/              # 1. CMD Reader (Python)
│   ├── bible_reader.py               # Main application
│   ├── bible-*-converted.json        # 4 Bible translations
│   ├── cross_references.txt          # 340,000+ cross-references
│   └── README.md
│
├── bible-visualizer-web/             # 2. Web Visualizer (D3.js)
│   ├── index.html                    # Main dashboard
│   ├── launch-server.bat             # Windows launcher
│   ├── css/styles.css
│   ├── js/
│   │   ├── arc-diagram.js            # 5 visualizations
│   │   ├── network-graph.js
│   │   ├── chord-diagram.js
│   │   ├── heatmap.js
│   │   └── sunburst.js
│   └── README.md
│
├── bible-desktop-gui/         # 3. Desktop GUI (PyQt5)
│   ├── visualizer_app.py             # Main PyQt5 application
│   ├── BibleVisualizer.bat           # Windows launcher
│   ├── requirements.txt
│   ├── components/
│   │   ├── network_view.py           # 4 visualization components
│   │   ├── arc_view.py
│   │   ├── heatmap_view.py
│   │   └── stats_view.py
│   └── README.md
│
├── bible-cmd-web/                    # 4. Web Terminal (Browser)
│   ├── index.html                    # Terminal interface
│   ├── css/terminal.css              # Terminal styling
│   ├── js/
│   │   ├── terminal.js               # Main controller
│   │   ├── bible-data.js             # Data loader
│   │   └── commands.js               # Command parser
│   └── README.md
│
└── shared-data/                       # Processed data (shared by all)
    ├── cross_references.txt
    ├── data_processor.py              # Data conversion script
    └── processed/
        ├── graph_data.json            # 190,522 connections
        └── stats.json                 # Statistics
```

---

## 🎓 Learning & Exploration

### For Bible Students
- Discover how Old and New Testament books interconnect
- See which books reference each other most frequently
- Find related passages through visual connections
- Study cross-references in context

### For Data Enthusiasts
- Explore graph theory applied to ancient texts
- See network analysis of literary connections
- Learn about hierarchical data visualization
- Study force-directed layouts and algorithms

### For Developers
- Learn D3.js visualization techniques
- Study PyQt5 desktop application development
- See data processing pipelines in action
- Explore graph algorithms with NetworkX

---

## 🤝 Contributing

This project is complete and ready to use! However, future enhancements could include:

- Additional Bible translations (NIV, ESV, etc.)
- Verse text display in web visualizations
- Search functionality in desktop/web apps
- Mobile-optimized web interface
- Standalone executables for distribution

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed implementation status.

---

## 📜 License

MIT License - Free and open source

---

## 🙏 Credits

### Data Sources

**Cross-Reference Data:**
- **[Treasury of Scripture Knowledge](https://www.openbible.info/labs/cross-references/)** - 340,000+ verse-level cross-references (Public Domain)
- **[OpenBible.info](https://www.openbible.info)** - TSK cross-reference data digitization and enhancement (Creative Commons Attribution)

**Geographic & Historical Data:**
- **[Theographic Bible Metadata](https://github.com/robertrouse/theographic-bible-metadata)** - Knowledge graph of biblical people, places, and events (CC BY-SA 4.0)
  - 3,394 Biblical people with biographical data
  - 1,638 Geographic places with GPS coordinates
  - 1,700+ Historical events with timeline data
  - Easton's Bible Dictionary (6,000+ entries)

**Bible Text:**
- **KJV, ASV, WEB, YLT** - Public domain Bible translations from various GitHub repositories (see MEMORY.md)

### Libraries & Tools
- **D3.js** - Data visualization library
- **PyQt5** - Desktop GUI framework
- **Plotly** - Interactive 3D graphs
- **NetworkX** - Graph algorithms
- **Matplotlib & Seaborn** - Statistical visualizations

---

## 🚀 Getting Started Right Now

### Fastest Way to See Everything:

**Windows:**
1. Double-click `LAUNCH-ALL.bat`
2. Wait for all three windows to open
3. Start exploring!

**Mac/Linux:**
1. Open 3 terminal windows
2. Run one command in each:
   - `cd bible-visualizer-web && python3 -m http.server 8000`
   - `cd bible-desktop-gui && python3 visualizer_app.py`
   - `cd bible-analysis-tool && python3 bible_reader.py`
3. Open browser to http://localhost:8000

### First Things to Try:

**CMD Reader:**
- Type: `John 3:16` and press Enter
- Type: `love` and press Enter
- Type: `help` to see all commands

**Desktop GUI:**
- Click "3D Network Graph" tab
- Drag the graph to rotate it
- Scroll to zoom in/out

**Web Browser:**
- Click through all 6 tabs
- Try the "Sunburst" tab - click on sections!
- Change "Testament Filter" to "Old Testament"

---

## 💡 Tips & Tricks

### CMD Reader
- Use `translation ASV` to switch between Bible versions
- Type `daily` for a random verse, or `random` for any Bible verse
- Search keywords work across all 4 translations simultaneously
- Use `search faith --nt` to search only New Testament
- Use `search love --book John --exact` for exact phrase in specific book
- Type `stats` for comprehensive Bible statistics dashboard
- Type `compare John 3:16` to see verse in all 4 translations
- Use `next` or `prev` to navigate chapters sequentially
- Save favorites with `bookmark [reference]` and view with `bookmarks`
- Export your bookmarks or history to text files

### Desktop GUI
- Increase "Min Connections" slider for simpler, cleaner graphs
- Use Testament filter to focus on specific sections
- Export button saves current view as high-resolution image

### Web Browser
- Hover over any element for detailed tooltips
- Network Graph: Drag nodes around, they spring back!
- Sunburst: Click center "Bible" text to zoom back out
- All visualizations update instantly when you change filters

---

## 🎉 Project Status: 100% Complete!

✅ All planned features implemented
✅ All visualizations working
✅ All three interfaces functional
✅ Complete documentation
✅ Ready for use and distribution

**May this tool help you explore the beautiful interconnections in God's Word!** 🙏

---

## 🚀 Quick Reference Card

### I Want To... → Use This Interface

| Task | Best Interface | Command |
|------|----------------|---------|
| Read John 3:16 | **CMD Reader** | `cd bible-analysis-tool && python bible_reader.py` then type `John 3:16` |
| Search for "love" | **CMD Reader** | Launch CMD Reader, type `love` |
| Search "faith" in NT only | **CMD Reader** | Launch CMD Reader, type `search faith --nt` |
| Compare translations | **CMD Reader** | Type `compare John 3:16` to see all 4 translations |
| View Bible statistics | **CMD Reader** | Type `stats` for comprehensive dashboard |
| Save favorite verses | **CMD Reader** | Type `bookmark John 3:16`, view with `bookmarks` |
| Navigate chapters | **CMD Reader** | Type `next` or `prev` after reading a chapter |
| See beautiful visualizations | **Web Browser** | `cd bible-visualizer-web && python -m http.server 8000` |
| Rotate a 3D graph | **Desktop GUI** | `cd bible-desktop-gui && python visualizer_app.py` |
| View biblical places map | **Desktop GUI** | Launch GUI, click "Geographic Map" tab |
| See people relationships | **Desktop GUI** | Launch GUI, click "People Network" tab |
| Create a presentation | **Web Browser** | Launch web server, open in browser, use fullscreen |
| Export high-res images | **Desktop GUI** | Launch GUI, click "Export Current View" |
| Work offline (no server) | **CMD Reader** or **Desktop GUI** | Either works without HTTP server |
| See which books connect most | **Web Browser** | Open Chord Diagram or Heatmap tab |
| Zoom into a specific testament | **Web Browser** | Open Sunburst, click on OT or NT section |

### Launch Everything at Once

**Windows:** Double-click `LAUNCH-ALL.bat`

**Mac/Linux:** Run these in 3 separate terminals:
```bash
# Terminal 1
cd bible-visualizer-web && python3 -m http.server 8000

# Terminal 2
cd bible-desktop-gui && python3 visualizer_app.py

# Terminal 3
cd bible-analysis-tool && python3 bible_reader.py
```

---

## 📚 Documentation Links

- **[Project Status Details](PROJECT_STATUS.md)** - Complete implementation status
- **[CMD Reader Guide](bible-analysis-tool/README.md)** - How to use the command line tool
- **[Web Visualizer Guide](bible-visualizer-web/README.md)** - Web interface and visualizations
- **[Desktop GUI Guide](bible-desktop-gui/README.md)** - Desktop application features
- **[Developer Notes](bible-analysis-tool/MEMORY.md)** - Technical notes and gotchas

---

## 🎓 Data Overview

**What's Included:**
- 340,799 verse-level cross-references
- 190,522 chapter-level connections
- 66 Bible books analyzed
- 4 English translations (KJV, ASV, WEB, YLT)
- 11 different visualizations

**Data Source:** Treasury of Scripture Knowledge (public domain)

---

<div align="center">

![MiB Flash Outro](assets/proselytized-outro.gif)

# **You've been proselytized. Now go forth and explore Scripture!**

### *🙏 May this tool bless your study of God's Word! 🙏*

</div>
