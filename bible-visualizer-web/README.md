# 🎨 Bible Cross-Reference Visualizer - Web Browser

> Interactive web-based visualizations of 340,000+ Bible cross-references + 3,000+ people + 1,600+ places using D3.js

**Created by [@Ringmast4r](https://github.com/Ringmast4r)**

### 🆕 NEW: Geographic & Historical Visualizations!
- 🗺️ **Geographic Map** - 1,600+ biblical places with GPS coordinates
- ⏱️ **Timeline** - Chronological view of biblical events
- 👥 **People Network** - Relationships between 3,000+ biblical figures

### 🌐 **[View All Tools: Interactive Landing Page](https://ringmast4r.github.io/BIBLE/)**

> **📌 Note:** This is **one of four ways** to explore Bible cross-references in this project!
> - **🌐 This Tool (Web Visualizer)** - Beautiful interactive browser visualizations
> - **💻 [CMD Reader](../bible-analysis-tool/)** - Text-based reading and search
> - **🖥️ [Desktop GUI](../bible-desktop-gui/)** - 3D graphs and offline analysis
> - **⌨️ [Web Terminal](../bible-cmd-web/)** - Browser-based CMD demo

---

## Why Use the Web Visualizer?

**Best for:**
- 🎨 Beautiful, stunning visualizations
- 🖱️ Interactive exploration with mouse/touch
- 📊 Seeing patterns and connections visually
- 🎯 Presentations and demonstrations
- 🌐 Easy sharing (just send a link to localhost)
- 📱 Works in any modern browser

**Need text reading?** Use the [CMD Reader](../bible-analysis-tool/) instead!
**Want 3D graphs?** Try the [Desktop GUI](../bible-desktop-gui/) instead!

---

## 🚀 Quick Start

### Option 1: Local Server (Recommended)

**Windows:**
```bash
# Double-click this file:
launch-server.bat

# Or run manually:
cd bible-visualizer-web
python -m http.server 8000
# Then open: http://localhost:8000/index.html
```

**Mac/Linux:**
```bash
cd bible-visualizer-web
python3 -m http.server 8000
# Then open: http://localhost:8000/index.html
```

### Option 2: Direct File Opening (Limited)

**Note:** Opening `index.html` directly may not load data due to browser CORS restrictions. Use Option 1 instead.

### What You'll See

1. **Dark themed dashboard** with 6 visualization tabs
2. **Interactive filters** at the top
3. **Beautiful visualizations** that respond to your mouse
4. **Export buttons** to save as SVG

## ✨ Features

### Current Visualizations

#### ✅ Arc Diagram
- **190,522 chapter-level connections** displayed as true circular arcs
- **Pythagorean theorem formula** for perfect circular arcs: `y = √(r² - x²)`
- **Rainbow gradient coloring** - Distance-based (warm = close chapters, cool = far apart)
- Each arc is part of a perfect circle (not bezier approximation)
- Edge padding prevents clipping at visualization boundaries
- 100px margins on left/right with 50px edge padding for smooth curves
- **Interactive hover tooltips** - Shows connection source, target, distance, and weight
- **Interactive book labels** - Hover over chapter bars to see book name and chapter number
- Filter by testament, book, or minimum connections
- **Created by Ringmast4r**

#### ✅ Network Graph
- **Force-directed interactive graph** with physics simulation
- Drag nodes to reposition them
- Zoom and pan with mouse/trackpad
- Top 200 most connected chapters for performance
- Hover highlighting of connections
- Reset zoom button

#### ✅ Chord Diagram
- **Circular visualization** of 66 Bible books
- Interactive ribbons showing book-to-book connections
- Hover over arcs or ribbons for details
- Testament filtering (OT, NT, or both)
- Book labels around the perimeter

#### ✅ Heatmap
- **66x66 book connection matrix**
- Color intensity shows connection strength (Yellow→Orange→Red)
- Testament dividers (gold lines)
- Hover to highlight row/column
- Interactive cell tooltips

#### ✅ Sunburst
- **Hierarchical view**: Testament → Book → Chapter
- Click to zoom into sections
- Breadcrumb navigation at bottom
- Multi-level color coding (darker = deeper level)
- Click center to zoom back out

#### ✅ Geographic Map
- **1,600+ biblical places** plotted on world map
- GPS coordinates for accurate location
- Color-coded by feature type (City, Region, Water, Mountain)
- Zoom and pan to explore regions
- Hover to see place details and verse counts
- Clustered markers for nearby locations

#### ✅ Timeline
- **Chronological view** of biblical events across history
- Events connected to historical periods
- Interactive timeline navigation
- Hover for event details and context
- Color-coded periods and events
- Visual connections between periods and events

#### ✅ People Network
- **3,000+ biblical people** in relationship graph
- Connections show shared groups (tribes, families)
- Color-coded by gender (Male/Female/Unknown)
- Node size based on verse mentions
- Drag nodes to explore relationships
- Zoom and pan for detailed exploration

#### ✅ Statistics Dashboard
- **40+ comprehensive metrics** across 6 categorized sections
- 📊 Core Statistics (cross-refs, connections, books, chapters)
- 🔗 Cross-Reference Analytics (density, reciprocity, strongest connections)
- 👥 People & Places (3,069 people, 1,274 places with GPS)
- 📖 Book Collections (Gospels, Pauline Epistles, Torah)
- 🏆 Top Books (most referenced, self-referencing, cross-testament bridges)
- 🎯 Testament Distribution (OT/NT connection patterns)
- Responsive grid layout with mobile support
- **Created by Ringmast4r**

---

## 📱 Responsive Design (NEW - October 7, 2025)

### Auto-Resize Feature
**Visualizations automatically adapt to window size changes!**

- ✅ **Automatic window resize detection** with 250ms debouncing
- ✅ **Instant re-rendering** when you resize your browser
- ✅ **No manual updates needed** - everything adjusts automatically
- ✅ **Performance optimized** - debouncing prevents excessive re-renders during resize

**How it works:**
```javascript
// Window resize event listener with debouncing
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        renderCurrentVisualization();  // Auto-updates after 250ms
    }, 250);
});
```

### Full-Width Support for Ultra-Wide Monitors
**Perfect for 49-inch displays and beyond!**

- ✅ **Container expands to 100% width** (no 1600px limit)
- ✅ **Works on monitors up to 5120px wide** (49-inch super-ultra-wide)
- ✅ **Arc diagrams show more detail** on larger screens
- ✅ **Rainbow colors more distinct** with wider visualizations
- ✅ **Better use of screen real estate**

**Before vs After:**
| Screen Size | Before (1600px limit) | After (100% width) |
|-------------|----------------------|--------------------|
| Laptop (1920px) | Full width ✅ | Full width ✅ |
| Ultra-wide (3440px) | Stopped at 1600px ❌ | Full width ✅ |
| 49" Monitor (5120px) | Stopped at 1600px ❌ | Full width ✅ |

**Benefits on large displays:**
- More arc detail visible
- Colors more distinguishable
- Smoother curves with more pixels
- Professional appearance on high-end setups

**Technical Details:**
- Container CSS changed from `max-width: 1600px` to `max-width: 100%`
- Arc diagram recalculates width using `container.clientWidth`
- All SVG elements redraw at new dimensions
- Scales maintain proper proportions
- Edge padding and margins prevent clipping

**Files:**
- `css/styles.css` (line 92) - Container width
- `js/main.js` (lines 697-706) - Resize event listener
- `tableau-arc-demo.html` (lines 303-314) - Demo page resize handler

---

## 📊 Data

**Cross-Reference Data:**
- **344,799** verse-level cross-references
- **190,522** chapter-level connections
- **66** Bible books
- **1,189** chapters total
- Source: [Treasury of Scripture Knowledge](https://www.openbible.info/labs/cross-references/) via [OpenBible.info](https://www.openbible.info)

**Theographic Data:**
- **3,394** Biblical people with biographical details
- **1,638** Geographic places with GPS coordinates
- **1,700+** Historical events with timeline data
- **90** Time periods for chronological context
- **6,000+** Easton's Bible Dictionary entries
- Source: [Theographic Bible Metadata](https://github.com/robertrouse/theographic-bible-metadata) (CC BY-SA 4.0)

## 🎨 Color Scheme

- **Gold (#FFD700)** - Headers, highlights
- **Cyan (#00CED1)** - New Testament, accents
- **Green (#2ecc71)** - Old Testament
- **Purple (#9370DB)** - Cross-testament connections
- **Dark Background** - For optimal contrast

## 🖱️ Controls

| Control | Function |
|---------|----------|
| **Testament Filter** | Show only OT, NT, or cross-testament refs |
| **Book Focus** | Highlight connections for specific book |
| **Min Connections** | Filter out weak connections |
| **Reset View** | Clear all filters |
| **Export SVG** | Download current visualization |

## 💻 Technical Stack

- **D3.js v7** - Data visualization
- **Vanilla JavaScript** - No framework overhead
- **CSS Grid** - Responsive layout
- **SVG** - Scalable vector graphics

## 📂 File Structure

```
bible-visualizer-web/
├── index.html              # Main dashboard
├── css/
│   └── styles.css          # Beautiful styling
├── js/
│   ├── main.js             # App controller
│   ├── data-loader.js      # Data management
│   ├── arc-diagram.js      # Arc visualization ✓
│   ├── network-graph.js    # Network (placeholder)
│   ├── chord-diagram.js    # Chord (placeholder)
│   ├── heatmap.js          # Heatmap (placeholder)
│   └── sunburst.js         # Sunburst (placeholder)
└── README.md               # This file
```

## 🌐 Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern browsers with ES6+ support

## 🎯 Usage Tips

1. **Start with "All"** testament filter to see full picture
2. **Focus on a book** to explore its specific connections
3. **Increase min connections** to see only strong relationships
4. **Hover over arcs** to see verse details
5. **Hover over chapter bars** to highlight related arcs

## 🔮 Future Enhancements

- [x] Complete network graph with physics simulation ✅
- [x] Interactive chord diagram with animations ✅
- [x] Clickable heatmap cells with verse lists ✅
- [x] Sunburst with zoom functionality ✅
- [ ] Search by verse reference
- [ ] Save/share visualization states
- [ ] Custom color themes
- [ ] Mobile optimization
- [ ] Click nodes to show verse text
- [ ] Export to high-res PNG

## 🔧 Troubleshooting

### No Visualizations Showing?

**✅ FIXED IN SESSION 7** - If you're seeing blank screens:

1. **Hard Refresh Browser** - Use `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. **Check Browser Console** (F12) for errors
3. **Verify Files Exist**:
   - `js/preview-data.js` (97KB - instant load)
   - `../shared-data/processed/graph_data.json` (15MB - full dataset)
4. **Use HTTP Server** - Don't open as `file://` (CORS issues)

### Common Issues:

**"Data not loaded" Error:**
- Make sure you're running an HTTP server (not opening directly)
- Check that `graph_data.json` and `stats.json` exist in `../shared-data/processed/`
- Wait for preview mode banner to appear (should be instant)

**Blank Screens on Tabs:**
- This was the Session 7 bug - update to latest version
- All 5 visualizations must be initialized in `main.js`
- Check browser console for "Visualizations initialized successfully"

**Slow Loading:**
- Preview mode (200 connections) loads instantly
- Full dataset (190K connections) loads in background (10-30 seconds)
- Banner will update when full data loads

**GitHub Pages Not Updating:**
- Wait 1-2 minutes for GitHub Actions to rebuild
- Hard refresh browser to clear cache
- Check deployment status: https://github.com/Ringmast4r/PROJECT-BIBLE-A-Proselytize-Project/actions

### Developer Notes:

**Data Access Pattern:**
```javascript
// ✅ CORRECT
if (!dataLoader || !dataLoader.isLoaded) return;
const chapters = dataLoader.getChapters();
const connections = dataLoader.getConnections();

// ❌ WRONG
const data = window.bibleData;  // Doesn't exist!
```

**All Visualizations Must Be Initialized:**
```javascript
// In main.js initializeVisualizations()
this.visualizations.arc = new ArcDiagram(...);
this.visualizations.network = new NetworkGraph(...);
this.visualizations.chord = new ChordDiagram(...);
this.visualizations.heatmap = new Heatmap(...);
this.visualizations.sunburst = new Sunburst(...);
```

See `SESSION-7-SUMMARY.md` for full details on the critical bug fix.

---

## 📝 Notes

- **Data Processing**: Run `../shared-data/data_processor.py` if data files missing
- **Performance**: Large datasets may be slow on older browsers
- **Internet Required**: For D3.js CDN (or download D3.js locally)
- **Production Status**: ✅ ALL 6 TABS WORKING (as of Session 7)

## 🙏 Credits

**Data Sources:**
- **[Treasury of Scripture Knowledge](https://www.openbible.info/labs/cross-references/)** - 340,000+ cross-references (Public Domain)
- **[OpenBible.info](https://www.openbible.info)** - Cross-reference data digitization (CC Attribution)
- **[Theographic Bible Metadata](https://github.com/robertrouse/theographic-bible-metadata)** - People, places, events knowledge graph (CC BY-SA 4.0)

**Libraries:**
- **[D3.js](https://d3js.org/)** - Data visualization library
- **[Leaflet](https://leafletjs.com/)** - Geographic mapping (used in map visualization)

**Acknowledgments:**
- Arc diagram visualization inspired by Chris Harrison's 2007 cross-reference arc concept and Robert Rouse's Tableau implementation
- **[Viz.Bible](https://viz.bible)** - Visualization inspiration from Theographic project
- **You!** - For using this tool to explore God's Word

---

**Open `index.html` in your browser to begin exploring!** 🚀
