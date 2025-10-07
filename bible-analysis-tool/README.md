# ✟ Bible Analysis Tool - CMD Reader

> A beautiful command-line Bible analysis tool with multiple translations, keyword search, and 340,000+ cross-references

**Created by [@Ringmast4r](https://github.com/Ringmast4r)**

### 🌐 **[View All Tools: Interactive Landing Page](https://ringmast4r.github.io/BIBLE/)**

> **📌 Note:** This is **one of four ways** to explore Bible cross-references in this project!
> - **💻 This Tool (CMD Reader)** - Text-based reading and search
> - **🌐 [Web Visualizer](../bible-visualizer-web/)** - Interactive browser visualizations
> - **🖥️ [Desktop GUI](../bible-desktop-gui/)** - 3D graphs and professional analysis
> - **⌨️ [Web Terminal](../bible-cmd-web/)** - Browser-based CMD demo

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why Use the CMD Reader?

**Best for:**
- 📖 Reading Bible verses and chapters
- 🔍 Searching keywords across 4 translations
- 📚 Studying cross-references in text format
- ⚡ Quick lookups without launching a GUI
- 💻 Working in terminal/command line environments

**Not for visualizations?** Check out the [Web Visualizer](../bible-visualizer-web/) or [Desktop GUI](../bible-desktop-gui/) instead!

---

## 🌟 Features

### 📖 **Multiple Bible Translations**
- **KJV** - King James Version (1611)
- **ASV** - American Standard Version (1901)
- **WEB** - World English Bible (2000)
- **YLT** - Young's Literal Translation (1898)
- Switch between translations instantly
- Compare all 4 translations side-by-side for any verse

### 🔍 **Advanced Search**
- Search by keyword across all 31,000+ verses
- **Testament Filters** - Search only OT (`--ot`) or NT (`--nt`)
- **Book Filters** - Search within specific books (`--book John`)
- **Exact Phrase** - Match exact phrases (`--exact`)
- Combine filters for precise results
- Highlighted search results
- Case-insensitive matching

### 🔗 **Cross-References**
- 340,000+ cross-references from Treasury of Scripture Knowledge
- See related verses automatically when reading
- Discover connections throughout Scripture

### 📊 **Statistics & Analysis**
- Comprehensive Bible statistics dashboard
- Total verses, words, chapters breakdown
- Cross-reference statistics and metrics
- Top 10 most referenced verses
- View all 66 books with chapter counts

### 📌 **History & Bookmarks**
- Automatic history tracking (last 50 verses viewed)
- Bookmark system to save favorite verses
- Export bookmarks and history to text files
- Quick access to recently viewed passages

### ⏭️ **Navigation**
- Next/prev chapter commands
- Automatic book wrapping (Genesis → Revelation)
- Random verse discovery
- Daily inspirational verses

### 🎨 **Beautiful Interface**
- 6 color themes (Professional, Vibrant, Matrix, Sunset, Royal, Ocean)
- Color-coded display with gold, cyan, and vibrant highlights
- Unicode box-drawing characters for elegant formatting
- Clean, modern terminal UI with real-time theme switching

### 📚 **Reading Modes**
- Read individual verses with cross-references
- Read entire chapters at once
- Word-wrapped text for readability
- Verse numbering and paragraph markers
- Metadata panels with verse statistics

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bible-analysis-tool.git
   cd bible-analysis-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install colorama
   ```

3. **Run the application:**
   ```bash
   python bible_reader.py
   ```

   **Or on Windows, double-click:**
   ```
   bible.bat
   ```

---

## 📋 Usage

### Basic Commands

Once the program is running, you can:

| Command | Example | Description |
|---------|---------|-------------|
| **Read a verse** | `John 3:16` | Display verse with cross-references |
| **Read a chapter** | `Psalms 23` | Display entire chapter |
| **Search keyword** | `love` | Find all verses containing the word |
| **Advanced search** | `search faith --nt` | Search with filters (--ot, --nt, --book, --exact) |
| **Compare translations** | `compare John 3:16` | See verse in all 4 translations |
| **Statistics** | `stats` | Display Bible statistics dashboard |
| **Books list** | `books` | Show all 66 books with chapter counts |
| **History** | `history` | View recently read verses |
| **Bookmark** | `bookmark John 3:16` | Save a favorite verse |
| **View bookmarks** | `bookmarks` | Display all bookmarked verses |
| **Random verse** | `random` | Show any random Bible verse |
| **Daily verse** | `daily` | Show inspirational verse |
| **Next chapter** | `next` or `n` | Navigate to next chapter |
| **Previous chapter** | `prev` or `p` | Navigate to previous chapter |
| **Export bookmarks** | `export bookmarks` | Save bookmarks to text file |
| **Export history** | `export history` | Save reading history to text file |
| **List translations** | `translations` | Show all available Bible versions |
| **Switch translation** | `translation ASV` | Change to a different version |
| **Change theme** | `t` | Cycle through 6 color themes |
| **Quit** | `quit` or `exit` | Exit the program |

### Example Session

```
⊳ Enter your choice: John 3:16

╔══════════════════════════════════════════════════════════════════╗
║                           John 3:16                            ║
╚══════════════════════════════════════════════════════════════════╝

  For God so loved the world, that he gave his only begotten
  Son, that whosoever believeth in him should not perish, but
  have everlasting life.

┌──────────────────────────────────────────────────────────────────┐
│  ★ Related Verses (Cross-References)                          │
└──────────────────────────────────────────────────────────────────┘

  [1] Romans 5:8
      But God commendeth his love toward us...

  [2] 1 John 4:9
      In this was manifested the love of God...

      ... and 18 more related verses
```

---

## 🗂️ Project Structure

```
bible-analysis-tool/
├── bible_reader.py              # Main application
├── convert_translations.py      # Translation format converter
├── preview.py                   # Feature preview script
├── bible.bat                    # Windows launcher
│
├── bible-kjv-converted.json     # King James Version
├── bible-asv-converted.json     # American Standard Version
├── bible-web-converted.json     # World English Bible
├── bible-ylt-converted.json     # Young's Literal Translation
├── cross_references.txt         # 340,000+ cross-references
│
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CHANGELOG.md                 # Version history
├── MEMORY.md                    # Development notes
├── QUICKSTART.txt               # Quick start guide
└── VISUAL_GUIDE.txt             # Visual features guide
```

---

## 🎯 Purpose & Vision

This tool was created to help people engage with Scripture through technology, making Bible study more accessible, interconnected, and beautiful. By combining multiple translations with comprehensive cross-references, users can:

- **Discover connections** between different parts of the Bible
- **Compare translations** to gain deeper understanding
- **Search efficiently** for themes and keywords
- **Study systematically** with cross-references guiding the way

Perfect for personal devotions, sermon preparation, Bible study groups, or anyone seeking to explore God's Word.

---

## 📊 Data Sources

### Bible Texts
All translations are in the public domain:

- **KJV**: GitHub - farskipper/kjv
- **ASV**: GitHub - bibleapi/bibleapi-bibles-json
- **WEB**: GetBible API (api.getbible.net)
- **YLT**: GetBible API (api.getbible.net)

### Cross-References
- **Source**: [OpenBible.info](https://www.openbible.info/labs/cross-references/)
- **Based on**: Treasury of Scripture Knowledge (TSK)
- **License**: Creative Commons Attribution
- **Count**: 340,000+ verse connections

---

## 🛠️ Technical Details

### Requirements
- Python 3.6 or higher
- colorama library (for Windows color support)

### Key Technologies
- **colorama**: Cross-platform terminal colors
- **JSON**: Data storage format
- **UTF-8 encoding**: Proper Unicode support
- **ANSI escape codes**: Terminal formatting

### Performance
- Loads 31,000+ verses instantly
- Fast keyword search across entire Bible
- Efficient cross-reference lookup
- Memory-optimized data structures

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more public domain translations
- Implement verse comparison view
- Add bookmarking/favorites system
- Create study notes feature
- Develop mobile-friendly version
- Add audio Bible integration

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Bible Text Licenses
All included Bible translations (KJV, ASV, WEB, YLT) are in the **public domain**.

### Cross-Reference License
Cross-reference data from OpenBible.info is licensed under **Creative Commons Attribution**.

---

## 🙏 Acknowledgments

**Data Sources:**
- **[Treasury of Scripture Knowledge](https://www.openbible.info/labs/cross-references/)** - 340,000+ cross-references (Public Domain)
- **[OpenBible.info](https://www.openbible.info)** - TSK data digitization and enhancement (CC Attribution)
- **[Theographic Bible Metadata](https://github.com/robertrouse/theographic-bible-metadata)** - Biblical people, places, and events knowledge graph (CC BY-SA 4.0)
- **Bible API Contributors** - Public domain Bible translations

**Libraries:**
- **[Colorama](https://pypi.org/project/colorama/)** - Cross-platform terminal color support

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [MEMORY.md](MEMORY.md) file for development notes and troubleshooting

---

**May God bless your study of His Word!** ✟

