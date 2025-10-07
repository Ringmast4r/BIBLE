#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bible Analysis Tool
A beautiful command-line Bible analysis tool with search and cross-reference features
"""

import json
import re
import os
import sys
import time
import random
from collections import defaultdict
from colorama import init, Fore, Back, Style

# Enable Windows VT100 terminal for better Unicode support
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Enable ANSI escape code processing (Windows 10+)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        # Set UTF-8 output encoding
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback for older Windows versions
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

# Initialize colorama for Windows color support
init(autoreset=True)

# RGB color helper functions (DEATH-STAR style)
def rgb(r, g, b):
    """Create RGB color escape code for vibrant terminal colors"""
    return f'\033[38;2;{r};{g};{b}m'

def rgb_bg(r, g, b):
    """Create RGB background color escape code"""
    return f'\033[48;2;{r};{g};{b}m'

RESET = '\033[0m'

# Theme definitions (DEATH-STAR inspired multi-theme system)
THEMES = {
    "professional": {
        "name": "Professional",
        "primary": rgb(70, 130, 180),      # Steel blue
        "secondary": rgb(176, 196, 222),   # Light steel blue
        "accent": rgb(255, 215, 0),        # Gold
        "success": rgb(60, 179, 113),      # Medium sea green
        "error": rgb(220, 20, 60),         # Crimson
        "text": rgb(240, 240, 240),        # Off-white
        "dim": rgb(169, 169, 169),         # Dark gray
        "highlight_bg": rgb(255, 215, 0),  # Gold
        "highlight_fg": rgb(0, 0, 0),      # Black
    },
    "vibrant": {
        "name": "Vibrant",
        "primary": rgb(0, 255, 255),       # Electric cyan
        "secondary": rgb(255, 0, 255),     # Hot magenta
        "accent": rgb(255, 215, 0),        # Bright gold
        "success": rgb(0, 255, 65),        # Neon green
        "error": rgb(255, 0, 0),           # Bright red
        "text": rgb(255, 255, 255),        # Pure white
        "dim": rgb(128, 128, 128),         # Medium gray
        "highlight_bg": rgb(255, 255, 0),  # Yellow
        "highlight_fg": rgb(0, 0, 0),      # Black
    },
    "matrix": {
        "name": "Matrix",
        "primary": rgb(0, 255, 65),        # Matrix green
        "secondary": rgb(0, 150, 40),      # Dark green
        "accent": rgb(0, 255, 127),        # Spring green
        "success": rgb(50, 205, 50),       # Lime green
        "error": rgb(255, 0, 0),           # Red
        "text": rgb(200, 255, 200),        # Light green
        "dim": rgb(100, 100, 100),         # Gray
        "highlight_bg": rgb(0, 255, 65),   # Matrix green
        "highlight_fg": rgb(0, 0, 0),      # Black
    },
    "sunset": {
        "name": "Sunset",
        "primary": rgb(255, 127, 80),      # Coral
        "secondary": rgb(255, 165, 0),     # Orange
        "accent": rgb(255, 215, 0),        # Gold
        "success": rgb(255, 140, 0),       # Dark orange
        "error": rgb(178, 34, 34),         # Firebrick
        "text": rgb(255, 250, 240),        # Floral white
        "dim": rgb(160, 160, 160),         # Gray
        "highlight_bg": rgb(255, 140, 0),  # Dark orange
        "highlight_fg": rgb(255, 255, 255),# White
    },
    "royal": {
        "name": "Royal",
        "primary": rgb(138, 43, 226),      # Blue-violet
        "secondary": rgb(147, 112, 219),   # Medium purple
        "accent": rgb(255, 215, 0),        # Gold
        "success": rgb(72, 61, 139),       # Dark slate blue
        "error": rgb(220, 20, 60),         # Crimson
        "text": rgb(248, 248, 255),        # Ghost white
        "dim": rgb(169, 169, 169),         # Dark gray
        "highlight_bg": rgb(255, 215, 0),  # Gold
        "highlight_fg": rgb(75, 0, 130),   # Indigo
    },
    "ocean": {
        "name": "Ocean",
        "primary": rgb(0, 191, 255),       # Deep sky blue
        "secondary": rgb(64, 224, 208),    # Turquoise
        "accent": rgb(0, 255, 255),        # Cyan
        "success": rgb(32, 178, 170),      # Light sea green
        "error": rgb(220, 20, 60),         # Crimson
        "text": rgb(240, 255, 255),        # Azure
        "dim": rgb(119, 136, 153),         # Light slate gray
        "highlight_bg": rgb(0, 255, 255),  # Cyan
        "highlight_fg": rgb(0, 0, 0),      # Black
    }
}

# Default static color class for loading screen (always professional)
class LoadingColors:
    """Professional colors for loading screen"""
    GOLD = rgb(70, 130, 180)           # Steel blue
    CYAN = rgb(176, 196, 222)          # Light steel blue
    GREEN = rgb(60, 179, 113)          # Medium sea green
    WHITE = rgb(240, 240, 240)         # Off-white
    GRAY = rgb(169, 169, 169)          # Dark gray
    SUCCESS = rgb(60, 179, 113)        # Medium sea green
    ERROR = rgb(220, 20, 60)           # Crimson
    RESET = RESET

# Dynamic color class (changes with theme)
class Colors:
    """Dynamic colors that change based on current theme"""

    @staticmethod
    def set_theme(theme_name):
        """Update colors based on theme"""
        theme = THEMES.get(theme_name, THEMES["professional"])

        Colors.BRIGHT_GOLD = theme["accent"]
        Colors.BRIGHT_CYAN = theme["primary"]
        Colors.BRIGHT_GREEN = theme["success"]
        Colors.BRIGHT_MAGENTA = theme["secondary"]
        Colors.BRIGHT_BLUE = theme["primary"]
        Colors.BRIGHT_WHITE = theme["text"]
        Colors.BRIGHT_RED = theme["error"]
        Colors.ORANGE = theme["accent"]
        Colors.LIME = theme["success"]
        Colors.PINK = theme["secondary"]
        Colors.PURPLE = theme["secondary"]
        Colors.YELLOW = theme["accent"]

        Colors.GRAY = theme["dim"]
        Colors.DIM_CYAN = theme["secondary"]
        Colors.DIM_GOLD = theme["accent"]

        # Legacy names
        Colors.GOLD = Colors.BRIGHT_GOLD
        Colors.CYAN = Colors.BRIGHT_CYAN
        Colors.GREEN = Colors.BRIGHT_GREEN
        Colors.RED = Colors.BRIGHT_RED
        Colors.BLUE = Colors.BRIGHT_BLUE
        Colors.MAGENTA = Colors.BRIGHT_MAGENTA
        Colors.WHITE = Colors.BRIGHT_WHITE

        # Special combinations
        Colors.TITLE = Colors.BRIGHT_CYAN
        Colors.VERSE_REF = Colors.BRIGHT_GOLD
        Colors.VERSE_TEXT = Colors.BRIGHT_WHITE
        Colors.CROSS_REF = Colors.BRIGHT_MAGENTA
        Colors.HIGHLIGHT = rgb_bg(*_rgb_tuple(theme["highlight_bg"])) + rgb(*_rgb_tuple(theme["highlight_fg"]))
        Colors.SUCCESS = Colors.BRIGHT_GREEN
        Colors.ERROR = Colors.BRIGHT_RED
        Colors.PROMPT = Colors.BRIGHT_CYAN

        Colors.RESET = RESET

def _rgb_tuple(color_code):
    """Extract RGB values from color code string"""
    # Parse '\033[38;2;R;G;Bm' format
    import re
    match = re.search(r'38;2;(\d+);(\d+);(\d+)', color_code)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return (255, 255, 255)

# Initialize with professional theme
Colors.set_theme("professional")

# Border helper functions
def make_border_top(width=78):
    """Create top border"""
    return f"╔{'═' * width}╗"

def make_border_bottom(width=78):
    """Create bottom border"""
    return f"╚{'═' * width}╝"

def make_border_line(text, width=78, align='left'):
    """Create a bordered line with proper padding"""
    # Remove ANSI codes for width calculation
    visible_text = re.sub(r'\033\[[0-9;]+m', '', text)
    visible_len = len(visible_text)

    padding_total = width - visible_len - 2  # -2 for spaces around text

    if align == 'center':
        left_pad = padding_total // 2
        right_pad = padding_total - left_pad
        return f"║ {' ' * left_pad}{text}{' ' * right_pad} ║"
    elif align == 'right':
        return f"║ {' ' * padding_total}{text} ║"
    else:  # left
        return f"║ {text}{' ' * padding_total} ║"

# Beautiful ASCII Art
ASCII_CROSS = f"""{Colors.GOLD}
            ╔═══╗
            ║   ║
        ════╬═══╬════
            ║   ║
            ║   ║
            ║   ║
            ╚═══╝
{Colors.RESET}"""

ASCII_BIBLE = f"""{Colors.CYAN}
        ┌─────────────────────┐
        │  _______________    │
        │ │               │   │
        │ │  HOLY BIBLE   │   │
        │ │_______________│   │
        │                     │
        └─────────────────────┘
{Colors.RESET}"""

class BibleReader:
    def __init__(self):
        self.translations = {}
        self.current_translation = 'KJV'
        self.cross_refs = defaultdict(list)
        self.daily_verses = [
            "John 3:16", "Psalms 23:1", "Philippians 4:13", "Jeremiah 29:11",
            "Romans 8:28", "Proverbs 3:5", "Isaiah 40:31", "Matthew 5:16",
            "1 Corinthians 13:4", "Psalms 46:1", "Joshua 1:9", "Romans 12:2"
        ]

        # Translation metadata
        self.translation_info = {
            'KJV': {'name': 'King James Version', 'year': '1611'},
            'ASV': {'name': 'American Standard Version', 'year': '1901'},
            'WEB': {'name': 'World English Bible', 'year': '2000'},
            'YLT': {'name': "Young's Literal Translation", 'year': '1898'}
        }

        # Theme system
        self.theme_list = ["professional", "vibrant", "matrix", "sunset", "royal", "ocean"]
        self.current_theme = "professional"
        Colors.set_theme(self.current_theme)

        # History and bookmarks
        self.history = []  # Recently viewed verses
        self.bookmarks = []  # Favorite verses
        self.current_chapter_ref = None  # For next/prev navigation

        # Book metadata
        self.book_order = [
            # Old Testament
            'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
            'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
            '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
            'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
            'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations',
            'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah',
            'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai',
            'Zechariah', 'Malachi',
            # New Testament
            'Matthew', 'Mark', 'Luke', 'John', 'Acts',
            'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
            'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
            '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
            'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
            'Jude', 'Revelation'
        ]

        print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║                    Loading Bible Data...                     ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

        self.load_all_translations()
        self.load_cross_references()

    def load_all_translations(self):
        """Load all available Bible translations"""
        translation_files = {
            'KJV': 'bible-kjv-converted.json',
            'ASV': 'bible-asv-converted.json',
            'WEB': 'bible-web-converted.json',
            'YLT': 'bible-ylt-converted.json'
        }

        for abbrev, filename in translation_files.items():
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.translations[abbrev] = json.load(f)
                info = self.translation_info.get(abbrev, {})
                print(f"{Colors.SUCCESS}  ✓ {abbrev} loaded - {info.get('name', abbrev)} ({len(self.translations[abbrev]):,} verses){Colors.RESET}")
            except FileNotFoundError:
                if abbrev == 'KJV':
                    # Fallback to original KJV file
                    try:
                        with open('bible-kjv.json', 'r', encoding='utf-8') as f:
                            self.translations[abbrev] = json.load(f)
                        print(f"{Colors.SUCCESS}  ✓ {abbrev} loaded - King James Version ({len(self.translations[abbrev]):,} verses){Colors.RESET}")
                    except:
                        print(f"{Colors.ERROR}  ✗ Error loading {abbrev}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.ERROR}  ✗ Error loading {abbrev}: {e}{Colors.RESET}")

        if not self.translations:
            print(f"{Colors.ERROR}  ✗ No translations loaded! Please check your files.{Colors.RESET}")
        else:
            print(f"\n{Colors.GOLD}  → Current translation: {self.current_translation} ({self.translation_info[self.current_translation]['name']}){Colors.RESET}\n")

    @property
    def bible_data(self):
        """Get current translation data"""
        return self.translations.get(self.current_translation, {})

    def expand_book_name(self, abbrev):
        """Expand book abbreviation to full name"""
        book_map = {
            'Gen': 'Genesis', 'Exod': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers', 'Deut': 'Deuteronomy',
            'Josh': 'Joshua', 'Judg': 'Judges', 'Ruth': 'Ruth', '1Sam': '1 Samuel', '2Sam': '2 Samuel',
            '1Kgs': '1 Kings', '2Kgs': '2 Kings', '1Chr': '1 Chronicles', '2Chr': '2 Chronicles',
            'Ezra': 'Ezra', 'Neh': 'Nehemiah', 'Esth': 'Esther', 'Job': 'Job', 'Ps': 'Psalms',
            'Prov': 'Proverbs', 'Eccl': 'Ecclesiastes', 'Song': 'Song of Solomon', 'Isa': 'Isaiah',
            'Jer': 'Jeremiah', 'Lam': 'Lamentations', 'Ezek': 'Ezekiel', 'Dan': 'Daniel',
            'Hos': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos', 'Obad': 'Obadiah', 'Jonah': 'Jonah',
            'Mic': 'Micah', 'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai',
            'Zech': 'Zechariah', 'Mal': 'Malachi', 'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke',
            'John': 'John', 'Acts': 'Acts', 'Rom': 'Romans', '1Cor': '1 Corinthians', '2Cor': '2 Corinthians',
            'Gal': 'Galatians', 'Eph': 'Ephesians', 'Phil': 'Philippians', 'Col': 'Colossians',
            '1Thess': '1 Thessalonians', '2Thess': '2 Thessalonians', '1Tim': '1 Timothy', '2Tim': '2 Timothy',
            'Titus': 'Titus', 'Phlm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James', '1Pet': '1 Peter',
            '2Pet': '2 Peter', '1John': '1 John', '2John': '2 John', '3John': '3 John', 'Jude': 'Jude',
            'Rev': 'Revelation'
        }
        return book_map.get(abbrev, abbrev)

    def convert_ref_format(self, ref):
        """Convert Gen.1.1 or Ps.23.1-Ps.23.2 format to Genesis 1:1 format"""
        if '-' in ref:
            parts = ref.split('-')
            start = self.convert_ref_format(parts[0])
            return start

        parts = ref.split('.')
        if len(parts) >= 3:
            book = self.expand_book_name(parts[0])
            chapter = parts[1]
            verse = parts[2]
            return f"{book} {chapter}:{verse}"
        return ref

    def load_cross_references(self):
        """Load cross-reference data"""
        try:
            with open('cross_references.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        from_verse = self.convert_ref_format(parts[0])
                        to_verse = self.convert_ref_format(parts[1])
                        try:
                            votes = int(parts[2])
                            self.cross_refs[from_verse].append({
                                'verse': to_verse,
                                'votes': votes
                            })
                        except ValueError:
                            pass

            for verse in self.cross_refs:
                self.cross_refs[verse].sort(key=lambda x: x['votes'], reverse=True)

            print(f"{Colors.SUCCESS}  ✓ Cross-references loaded - {len(self.cross_refs):,} verses with connections{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}  ✗ Error loading cross-references: {e}{Colors.RESET}")

    def format_verse_text(self, text):
        """Format verse text with colors"""
        text = text.replace('# ', '')
        # Color italic words (words in brackets) in gray
        text = re.sub(r'\[([^\]]+)\]', f'{Colors.GRAY}[\\1]{Colors.RESET}', text)
        return text

    def get_verse(self, reference):
        """Get a specific verse by reference"""
        if reference in self.bible_data:
            return self.bible_data[reference]
        for key in self.bible_data.keys():
            if key.lower() == reference.lower():
                return self.bible_data[key]
        return None

    def display_verse(self, reference, show_refs=True):
        """Display a verse with beautiful formatting, metadata panel, and cross-references"""
        text = self.get_verse(reference)

        if text:
            # Add to history
            self.add_to_history(reference)
            # Parse reference for metadata
            parts = reference.split()
            book = ' '.join(parts[:-1]) if len(parts) > 1 else reference
            chapter_verse = parts[-1] if len(parts) > 1 else ''

            # Get translation info
            trans_info = self.translation_info.get(self.current_translation, {})
            trans_name = trans_info.get('name', self.current_translation)
            trans_year = trans_info.get('year', 'N/A')

            # Count characters and words
            plain_text = re.sub(r'\[([^\]]+)\]', r'\1', text)
            char_count = len(plain_text)
            word_count = len(plain_text.split())

            # Metadata panel
            header = f"{Colors.BRIGHT_GOLD}VERSE DETAILS{Colors.RESET}"
            ref_line = f"{Colors.DIM_CYAN}Reference:{Colors.RESET}  {Colors.BRIGHT_WHITE}{reference}{Colors.RESET}"
            book_line = f"{Colors.DIM_CYAN}Book:{Colors.RESET}       {Colors.BRIGHT_WHITE}{book}{Colors.RESET}"
            trans_line = f"{Colors.DIM_CYAN}Translation:{Colors.RESET} {Colors.ORANGE}{trans_name} ({trans_year}){Colors.RESET}"
            stats_line = f"{Colors.DIM_CYAN}Stats:{Colors.RESET}      {Colors.LIME}{word_count} words{Colors.RESET}, {Colors.PINK}{char_count} characters{Colors.RESET}"

            print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
            print(make_border_line(header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(ref_line))
            print(make_border_line(book_line))
            print(make_border_line(trans_line))
            print(make_border_line(stats_line))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            # Verse text panel
            text_header = f"{Colors.BRIGHT_WHITE}TEXT{Colors.RESET}"
            print(f"{Colors.BRIGHT_GOLD}{make_border_top()}")
            print(make_border_line(text_header, align='center'))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            # Word wrap for long verses
            formatted = self.format_verse_text(text)
            words = formatted.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                # Account for ANSI codes in length check
                visible_length = len(re.sub(r'\033\[[0-9;]+m', '', test_line))
                if visible_length <= 74:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for line in lines:
                print(f"  {Colors.VERSE_TEXT}{line}{Colors.RESET}")
            print()

            if show_refs:
                self.display_cross_references(reference)
        else:
            error_header = f"{Colors.BRIGHT_WHITE}ERROR{Colors.RESET}"
            error_msg = f"{Colors.WHITE}Verse not found: {reference}{Colors.RESET}"
            print(f"\n{Colors.BRIGHT_RED}{make_border_top()}")
            print(make_border_line(error_header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(error_msg))
            print(f"╚════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

    def display_cross_references(self, reference, limit=5):
        """Display cross-references with statistics panel"""
        refs = self.cross_refs.get(reference, [])

        if refs:
            total_refs = len(refs)
            showing = min(limit, total_refs)

            # Stats panel
            header = f"{Colors.BRIGHT_GOLD}CROSS-REFERENCES{Colors.RESET}"
            total_line = f"{Colors.DIM_CYAN}Total Found:{Colors.RESET}  {Colors.LIME}{total_refs} related verses{Colors.RESET}"
            showing_line = f"{Colors.DIM_CYAN}Showing:{Colors.RESET}      {Colors.ORANGE}Top {showing} most voted{Colors.RESET}"

            print(f"{Colors.BRIGHT_MAGENTA}{make_border_top()}")
            print(make_border_line(header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(total_line))
            print(make_border_line(showing_line))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            for i, ref in enumerate(refs[:limit], 1):
                verse_text = self.get_verse(ref['verse'])
                if verse_text:
                    preview = verse_text[:65] + "..." if len(verse_text) > 65 else verse_text
                    preview = preview.replace('# ', '')
                    preview = re.sub(r'\[([^\]]+)\]', r'\1', preview)
                    votes = ref.get('votes', 0)

                    print(f"  {Colors.BRIGHT_MAGENTA}[{i}]{Colors.RESET} {Colors.BRIGHT_GOLD}{ref['verse']}{Colors.RESET} {Colors.GRAY}({votes} votes){Colors.RESET}")
                    print(f"      {Colors.DIM_CYAN}↳{Colors.RESET} {Colors.WHITE}{preview}{Colors.RESET}\n")

            if len(refs) > limit:
                print(f"{Colors.GRAY}{'─' * 80}")
                print(f"  💡 {len(refs) - limit} more references available")
                print(f"{'─' * 80}{Colors.RESET}\n")

    def search_keyword(self, keyword, limit=15, testament=None, book=None, exact_phrase=False):
        """Search for verses containing a keyword with optional filters

        Args:
            keyword: Search term or phrase
            limit: Maximum results to show
            testament: Filter by 'OT' or 'NT' (optional)
            book: Filter by specific book name (optional)
            exact_phrase: If True, search for exact phrase; if False, search for word presence
        """
        keyword_lower = keyword.lower()
        results = []

        # Define Old Testament books for filtering
        ot_books = set(self.book_order[:39])
        nt_books = set(self.book_order[39:])

        for ref, text in self.bible_data.items():
            # Extract book name from reference
            ref_parts = ref.split()
            if len(ref_parts) > 1 and not ref_parts[1][0].isdigit():
                ref_book = ref_parts[0] + ' ' + ref_parts[1]
            else:
                ref_book = ref_parts[0]

            # Apply testament filter
            if testament:
                if testament.upper() == 'OT' and ref_book not in ot_books:
                    continue
                elif testament.upper() == 'NT' and ref_book not in nt_books:
                    continue

            # Apply book filter
            if book and ref_book.lower() != book.lower():
                continue

            # Apply keyword search
            if exact_phrase:
                # Exact phrase matching
                if keyword_lower in text.lower():
                    results.append((ref, text))
            else:
                # Word presence matching (all words must be present)
                words = keyword_lower.split()
                if all(word in text.lower() for word in words):
                    results.append((ref, text))

        if results:
            total_found = len(results)
            showing = min(limit, total_found)

            # Search statistics panel
            header = f"{Colors.BRIGHT_GOLD}SEARCH RESULTS{Colors.RESET}"
            trans_info = self.translation_info[self.current_translation]

            # Build filter description
            filter_parts = []
            if testament:
                filter_parts.append(f"Testament: {testament.upper()}")
            if book:
                filter_parts.append(f"Book: {book}")
            if exact_phrase:
                filter_parts.append("Exact phrase")
            else:
                filter_parts.append("Contains words")
            filter_desc = ", ".join(filter_parts) if filter_parts else "No filters"

            search_line = f"{Colors.DIM_CYAN}Search Term:{Colors.RESET}   {Colors.ORANGE}'{keyword}'{Colors.RESET}"
            trans_line = f"{Colors.DIM_CYAN}Translation:{Colors.RESET}  {Colors.PURPLE}{self.current_translation} - {trans_info['name']}{Colors.RESET}"
            filter_line = f"{Colors.DIM_CYAN}Filters:{Colors.RESET}       {Colors.YELLOW}{filter_desc}{Colors.RESET}"
            total_line = f"{Colors.DIM_CYAN}Total Found:{Colors.RESET}   {Colors.LIME}{total_found} verses{Colors.RESET}"
            showing_line = f"{Colors.DIM_CYAN}Showing:{Colors.RESET}       {Colors.PINK}{showing} of {total_found} results{Colors.RESET}"

            print(f"\n{Colors.BRIGHT_GREEN}{make_border_top()}")
            print(make_border_line(header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(search_line))
            print(make_border_line(trans_line))
            print(make_border_line(filter_line))
            print(make_border_line(total_line))
            print(make_border_line(showing_line))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            for i, (ref, text) in enumerate(results[:limit], 1):
                text_display = text.replace('# ', '')
                # Highlight keyword
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)

                # Find the keyword and create highlighted version
                matches = list(pattern.finditer(text_display))
                if matches:
                    highlighted_text = ""
                    last_end = 0
                    for match in matches:
                        highlighted_text += text_display[last_end:match.start()]
                        highlighted_text += f"{Colors.HIGHLIGHT}{match.group()}{Colors.RESET}{Colors.VERSE_TEXT}"
                        last_end = match.end()
                    highlighted_text += text_display[last_end:]
                    text_display = highlighted_text

                # Result entry with preview
                preview = text_display[:75] + "..." if len(text_display) > 75 else text_display
                print(f"  {Colors.BRIGHT_GREEN}[{i}]{Colors.RESET} {Colors.BRIGHT_GOLD}{ref}{Colors.RESET}")
                print(f"      {Colors.DIM_CYAN}↳{Colors.RESET} {Colors.VERSE_TEXT}{preview}{Colors.RESET}\n")

            if len(results) > limit:
                print(f"{Colors.GRAY}{'─' * 80}")
                print(f"  💡 {len(results) - limit} more verses match your search")
                print(f"  📌 Tip: Type a specific verse reference to see the full text")
                print(f"{'─' * 80}{Colors.RESET}\n")
        else:
            header = f"{Colors.BRIGHT_WHITE}NO RESULTS{Colors.RESET}"
            msg1 = f"{Colors.WHITE}No verses found containing '{keyword}'{Colors.RESET}"
            msg2 = f"{Colors.GRAY}Try a different search term or check spelling{Colors.RESET}"

            print(f"\n{Colors.BRIGHT_RED}{make_border_top()}")
            print(make_border_line(header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(msg1))
            print(make_border_line(msg2))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

    def display_chapter(self, book, chapter):
        """Display an entire chapter with beautiful formatting"""
        chapter_verses = []
        pattern = f"{book} {chapter}:"

        for ref, text in self.bible_data.items():
            if ref.startswith(pattern):
                chapter_verses.append((ref, text))

        if chapter_verses:
            # Track current chapter for next/prev navigation
            self.current_chapter_ref = f"{book} {chapter}"
            # Calculate stats
            verse_count = len(chapter_verses)
            total_words = sum(len(text.split()) for _, text in chapter_verses)
            avg_words = total_words // verse_count if verse_count > 0 else 0

            # Get translation info
            trans_info = self.translation_info.get(self.current_translation, {})
            trans_name = trans_info.get('name', self.current_translation)

            # Chapter info panel
            header = f"{Colors.BRIGHT_GOLD}CHAPTER READING{Colors.RESET}"
            book_line = f"{Colors.DIM_CYAN}Book & Chapter:{Colors.RESET} {Colors.BRIGHT_WHITE}{book} {chapter}{Colors.RESET}"
            trans_line = f"{Colors.DIM_CYAN}Translation:{Colors.RESET}    {Colors.PURPLE}{trans_name}{Colors.RESET}"
            verses_line = f"{Colors.DIM_CYAN}Total Verses:{Colors.RESET}   {Colors.LIME}{verse_count} verses{Colors.RESET}"
            words_line = f"{Colors.DIM_CYAN}Total Words:{Colors.RESET}    {Colors.PINK}{total_words} words{Colors.RESET}"
            avg_line = f"{Colors.DIM_CYAN}Avg Words/Verse:{Colors.RESET} {Colors.ORANGE}~{avg_words} words{Colors.RESET}"

            print(f"\n{Colors.BRIGHT_BLUE}{make_border_top()}")
            print(make_border_line(header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(book_line))
            print(make_border_line(trans_line))
            print(make_border_line(verses_line))
            print(make_border_line(words_line))
            print(make_border_line(avg_line))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            # Chapter text panel
            text_header = f"{Colors.BRIGHT_WHITE}TEXT{Colors.RESET}"
            print(f"{Colors.BRIGHT_GOLD}{make_border_top()}")
            print(make_border_line(text_header, align='center'))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            for ref, text in chapter_verses:
                verse_num = ref.split(':')[-1]
                formatted_text = self.format_verse_text(text)

                if text.startswith('# '):
                    print()

                print(f"{Colors.BRIGHT_GOLD}{verse_num:>4}.{Colors.RESET} {Colors.VERSE_TEXT}{formatted_text}{Colors.RESET}")

            print(f"\n{Colors.BRIGHT_BLUE}{'═' * 80}")
            print(f"{Colors.GRAY}  📖 End of {book} {chapter} ({verse_count} verses)")
            print(f"{'═' * 80}{Colors.RESET}\n")
        else:
            error_header = f"{Colors.BRIGHT_WHITE}ERROR{Colors.RESET}"
            error_msg = f"{Colors.WHITE}Chapter not found: {book} {chapter}{Colors.RESET}"

            print(f"\n{Colors.BRIGHT_RED}{make_border_top()}")
            print(make_border_line(error_header, align='center'))
            print(f"╠{'═' * 78}╣")
            print(make_border_line(error_msg))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

    def show_daily_verse(self):
        """Show a random inspirational verse with vibrant colors"""
        verse_ref = random.choice(self.daily_verses)
        daily_header = f"{Colors.BRIGHT_GOLD}VERSE OF THE DAY{Colors.RESET}"

        print(f"\n{Colors.BRIGHT_MAGENTA}{make_border_top()}")
        print(make_border_line(daily_header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")
        self.display_verse(verse_ref, show_refs=False)

    def switch_translation(self, abbrev):
        """Switch to a different Bible translation"""
        abbrev = abbrev.upper()
        if abbrev in self.translations:
            self.current_translation = abbrev
            info = self.translation_info.get(abbrev, {})
            print(f"\n{Colors.SUCCESS}✓ Switched to {abbrev} - {info.get('name', abbrev)} ({info.get('year', '')}){Colors.RESET}")
            print(f"{Colors.GRAY}  {len(self.translations[abbrev]):,} verses loaded{Colors.RESET}\n")
        else:
            print(f"\n{Colors.ERROR}✗ Translation '{abbrev}' not available{Colors.RESET}")
            self.list_translations()

    def list_translations(self):
        """List all available translations"""
        header = f"{Colors.GOLD}Available Translations{Colors.RESET}"

        print(f"\n{Colors.CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        for abbrev in sorted(self.translations.keys()):
            info = self.translation_info.get(abbrev, {})
            current = " ← Current" if abbrev == self.current_translation else ""
            print(f"  {Colors.VERSE_REF}{abbrev:6}{Colors.RESET} {Colors.WHITE}{info.get('name', abbrev):40}{Colors.RESET} {Colors.GRAY}({info.get('year', 'N/A')}){Colors.RESET}{Colors.GOLD}{current}{Colors.RESET}")

        print(f"\n{Colors.GRAY}  Type 'translation [CODE]' to switch (e.g., 'translation ASV'){Colors.RESET}\n")

    def show_statistics(self):
        """Display comprehensive Bible statistics dashboard"""
        # Calculate stats
        total_verses = len(self.bible_data)
        total_books = len(set(ref.split()[0] + (' ' + ref.split()[1] if ref.split()[1].isdigit() == False and len(ref.split()) > 2 else '') for ref in self.bible_data.keys()))
        total_chapters = len(set(' '.join(ref.split()[:2]) if ':' in ref.split()[1] else ref.split()[0] + ' ' + ref.split()[1] for ref in self.bible_data.keys()))
        total_cross_refs = sum(len(refs) for refs in self.cross_refs.values())
        verses_with_refs = len([v for v in self.cross_refs if len(self.cross_refs[v]) > 0])

        # Calculate word stats
        total_words = sum(len(text.split()) for text in self.bible_data.values())
        avg_words_per_verse = total_words // total_verses if total_verses > 0 else 0

        # Most referenced verses
        most_ref_verses = sorted(self.cross_refs.items(), key=lambda x: len(x[1]), reverse=True)[:10]

        # Translation info
        trans_info = self.translation_info.get(self.current_translation, {})
        trans_name = trans_info.get('name', self.current_translation)

        # Header
        header = f"{Colors.BRIGHT_GOLD}BIBLE STATISTICS DASHBOARD{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        # General Stats
        gen_header = f"{Colors.BRIGHT_WHITE}📊 GENERAL STATISTICS{Colors.RESET}"
        print(f"{Colors.BRIGHT_MAGENTA}{make_border_top()}")
        print(make_border_line(gen_header))
        print(f"╠{'═' * 78}╣")
        print(make_border_line(f"{Colors.DIM_CYAN}Current Translation:{Colors.RESET} {Colors.ORANGE}{trans_name}{Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Total Books:{Colors.RESET}         {Colors.LIME}66 books{Colors.RESET} {Colors.GRAY}(39 OT + 27 NT){Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Total Chapters:{Colors.RESET}      {Colors.PINK}1,189 chapters{Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Total Verses:{Colors.RESET}        {Colors.BRIGHT_GOLD}{total_verses:,} verses{Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Total Words:{Colors.RESET}         {Colors.BRIGHT_WHITE}{total_words:,} words{Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Avg Words/Verse:{Colors.RESET}    {Colors.ORANGE}~{avg_words_per_verse} words{Colors.RESET}"))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        # Cross-Reference Stats
        ref_header = f"{Colors.BRIGHT_WHITE}🔗 CROSS-REFERENCE STATISTICS{Colors.RESET}"
        print(f"{Colors.BRIGHT_GREEN}{make_border_top()}")
        print(make_border_line(ref_header))
        print(f"╠{'═' * 78}╣")
        print(make_border_line(f"{Colors.DIM_CYAN}Total Cross-Refs:{Colors.RESET}   {Colors.LIME}{total_cross_refs:,} connections{Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Verses with Refs:{Colors.RESET}   {Colors.PINK}{verses_with_refs:,} verses{Colors.RESET} {Colors.GRAY}({verses_with_refs*100//total_verses}% of Bible){Colors.RESET}"))
        print(make_border_line(f"{Colors.DIM_CYAN}Avg Refs/Verse:{Colors.RESET}     {Colors.ORANGE}~{total_cross_refs//verses_with_refs if verses_with_refs > 0 else 0} references{Colors.RESET}"))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        # Top Referenced Verses
        top_header = f"{Colors.BRIGHT_WHITE}⭐ TOP 10 MOST REFERENCED VERSES{Colors.RESET}"
        print(f"{Colors.BRIGHT_BLUE}{make_border_top()}")
        print(make_border_line(top_header))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        for i, (ref, refs_list) in enumerate(most_ref_verses, 1):
            ref_count = len(refs_list)
            verse_text = self.get_verse(ref)
            if verse_text:
                preview = verse_text[:50] + "..." if len(verse_text) > 50 else verse_text
                preview = preview.replace('# ', '')
                preview = re.sub(r'\[([^\]]+)\]', r'\1', preview)
                print(f"  {Colors.BRIGHT_BLUE}{i:2}.{Colors.RESET} {Colors.BRIGHT_GOLD}{ref:20}{Colors.RESET} {Colors.GRAY}({ref_count} refs){Colors.RESET}")
                print(f"      {Colors.DIM_CYAN}↳{Colors.RESET} {Colors.WHITE}{preview}{Colors.RESET}\n")

        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}")
        print(f"{Colors.GRAY}  💡 Type 'books' to see all books, 'history' to see recent verses{Colors.RESET}")
        print(f"{'═' * 80}{Colors.RESET}\n")

    def show_books_list(self):
        """Display list of all Bible books with chapter counts"""
        header = f"{Colors.BRIGHT_GOLD}BIBLE BOOKS INDEX{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        # Count chapters per book
        book_chapters = defaultdict(set)
        for ref in self.bible_data.keys():
            parts = ref.split()
            # Handle books like "1 Samuel" vs "Genesis"
            if len(parts) > 1 and not parts[1][0].isdigit():
                book = parts[0] + ' ' + parts[1]
                chapter = parts[2].split(':')[0] if ':' in parts[2] else parts[2]
            else:
                book = parts[0]
                chapter = parts[1].split(':')[0] if ':' in parts[1] else parts[1]
            book_chapters[book].add(chapter)

        # Old Testament
        ot_header = f"{Colors.BRIGHT_WHITE}OLD TESTAMENT (39 Books){Colors.RESET}"
        print(f"{Colors.BRIGHT_GREEN}{make_border_top()}")
        print(make_border_line(ot_header))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        ot_books = self.book_order[:39]
        for i, book in enumerate(ot_books, 1):
            chapters = len(book_chapters.get(book, []))
            print(f"  {Colors.LIME}{i:2}.{Colors.RESET} {Colors.BRIGHT_WHITE}{book:20}{Colors.RESET} {Colors.GRAY}({chapters} chapters){Colors.RESET}")
            if i % 2 == 0:
                print()

        # New Testament
        print(f"\n{Colors.BRIGHT_BLUE}{make_border_top()}")
        nt_header = f"{Colors.BRIGHT_WHITE}NEW TESTAMENT (27 Books){Colors.RESET}"
        print(make_border_line(nt_header))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        nt_books = self.book_order[39:]
        for i, book in enumerate(nt_books, 1):
            chapters = len(book_chapters.get(book, []))
            print(f"  {Colors.BRIGHT_CYAN}{i:2}.{Colors.RESET} {Colors.BRIGHT_WHITE}{book:20}{Colors.RESET} {Colors.GRAY}({chapters} chapters){Colors.RESET}")
            if i % 2 == 0:
                print()

        print(f"\n{Colors.GRAY}{'─' * 80}")
        print(f"  💡 Type a book name and chapter number to read (e.g., 'Genesis 1'){Colors.RESET}")
        print(f"{'─' * 80}{Colors.RESET}\n")

    def compare_translations(self, reference):
        """Show verse in all 4 translations side-by-side"""
        header = f"{Colors.BRIGHT_GOLD}TRANSLATION COMPARISON{Colors.RESET}"
        ref_line = f"{Colors.DIM_CYAN}Reference:{Colors.RESET} {Colors.BRIGHT_WHITE}{reference}{Colors.RESET}"

        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"╠{'═' * 78}╣")
        print(make_border_line(ref_line))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        for abbrev in ['KJV', 'ASV', 'WEB', 'YLT']:
            verse = self.translations.get(abbrev, {}).get(reference)
            info = self.translation_info.get(abbrev, {})
            name = info.get('name', abbrev)

            trans_header = f"{Colors.BRIGHT_MAGENTA}{abbrev}{Colors.RESET} {Colors.GRAY}- {name}{Colors.RESET}"
            print(f"{Colors.BRIGHT_BLUE}{make_border_top()}")
            print(make_border_line(trans_header))
            print(f"{make_border_bottom()}{Colors.RESET}")

            if verse:
                formatted = verse.replace('# ', '').replace('[', '').replace(']', '')
                # Word wrap
                words = formatted.split()
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) <= 74:
                        current_line = current_line + " " + word if current_line else word
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)

                for line in lines:
                    print(f"  {Colors.WHITE}{line}{Colors.RESET}")
            else:
                print(f"  {Colors.GRAY}(Not available in this translation){Colors.RESET}")
            print()

        print(f"{Colors.GRAY}{'─' * 80}{Colors.RESET}\n")

    def show_history(self):
        """Show recently viewed verses"""
        if not self.history:
            print(f"\n{Colors.GRAY}No history yet. View some verses to see them here!{Colors.RESET}\n")
            return

        header = f"{Colors.BRIGHT_GOLD}RECENTLY VIEWED VERSES{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        for i, ref in enumerate(reversed(self.history[-10:]), 1):
            verse_text = self.get_verse(ref)
            if verse_text:
                preview = verse_text[:60] + "..." if len(verse_text) > 60 else verse_text
                preview = preview.replace('# ', '')
                preview = re.sub(r'\[([^\]]+)\]', r'\1', preview)
                print(f"  {Colors.BRIGHT_CYAN}{i:2}.{Colors.RESET} {Colors.BRIGHT_GOLD}{ref:20}{Colors.RESET}")
                print(f"      {Colors.DIM_CYAN}↳{Colors.RESET} {Colors.WHITE}{preview}{Colors.RESET}\n")

        print(f"{Colors.GRAY}{'─' * 80}")
        print(f"  💡 Type a verse reference to view it again{Colors.RESET}")
        print(f"{'─' * 80}{Colors.RESET}\n")

    def add_bookmark(self, reference):
        """Add verse to bookmarks"""
        if reference not in self.bookmarks:
            self.bookmarks.append(reference)
            print(f"\n{Colors.SUCCESS}✓ Bookmarked: {reference}{Colors.RESET}\n")
        else:
            print(f"\n{Colors.GRAY}Already bookmarked: {reference}{Colors.RESET}\n")

    def show_bookmarks(self):
        """Show all bookmarked verses"""
        if not self.bookmarks:
            print(f"\n{Colors.GRAY}No bookmarks yet. Type 'bookmark [reference]' to save favorites!{Colors.RESET}\n")
            return

        header = f"{Colors.BRIGHT_GOLD}BOOKMARKED VERSES{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(header, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        for i, ref in enumerate(self.bookmarks, 1):
            verse_text = self.get_verse(ref)
            if verse_text:
                preview = verse_text[:60] + "..." if len(verse_text) > 60 else verse_text
                preview = preview.replace('# ', '')
                preview = re.sub(r'\[([^\]]+)\]', r'\1', preview)
                print(f"  {Colors.BRIGHT_MAGENTA}{i:2}.{Colors.RESET} {Colors.BRIGHT_GOLD}{ref:20}{Colors.RESET}")
                print(f"      {Colors.DIM_CYAN}↳{Colors.RESET} {Colors.WHITE}{preview}{Colors.RESET}\n")

        print(f"{Colors.GRAY}{'─' * 80}")
        print(f"  💡 Type a verse reference to view it{Colors.RESET}")
        print(f"{'─' * 80}{Colors.RESET}\n")

    def show_random_verse(self):
        """Show a random verse from the Bible"""
        random_ref = random.choice(list(self.bible_data.keys()))
        print(f"\n{Colors.BRIGHT_MAGENTA}🎲 Random Verse{Colors.RESET}\n")
        self.display_verse(random_ref)

    def add_to_history(self, reference):
        """Add verse to history (max 50 entries)"""
        if reference in self.history:
            self.history.remove(reference)
        self.history.append(reference)
        if len(self.history) > 50:
            self.history.pop(0)

    def get_chapter_count(self, book):
        """Get the number of chapters in a book"""
        chapter_counts = {}
        for ref in self.bible_data.keys():
            ref_parts = ref.split()
            if len(ref_parts) > 1 and not ref_parts[1][0].isdigit():
                ref_book = ref_parts[0] + ' ' + ref_parts[1]
                chapter_num = ref_parts[2].split(':')[0] if ':' in ref_parts[2] else ref_parts[2]
            else:
                ref_book = ref_parts[0]
                chapter_num = ref_parts[1].split(':')[0] if ':' in ref_parts[1] else ref_parts[1]

            if ref_book not in chapter_counts:
                chapter_counts[ref_book] = set()
            chapter_counts[ref_book].add(int(chapter_num))

        return max(chapter_counts.get(book, [0]))

    def next_chapter(self):
        """Navigate to the next chapter"""
        if not self.current_chapter_ref:
            print(f"\n{Colors.GRAY}No chapter currently open. Read a chapter first (e.g., 'Genesis 1'){Colors.RESET}\n")
            return

        # Parse current chapter reference
        parts = self.current_chapter_ref.rsplit(' ', 1)
        if len(parts) != 2:
            print(f"\n{Colors.ERROR}✗ Invalid chapter reference{Colors.RESET}\n")
            return

        book, chapter = parts
        chapter_num = int(chapter)

        # Get total chapters in current book
        total_chapters = self.get_chapter_count(book)

        # Check if we're at the last chapter of this book
        if chapter_num < total_chapters:
            # Move to next chapter in same book
            next_chapter_num = chapter_num + 1
            self.display_chapter(book, str(next_chapter_num))
        else:
            # Move to first chapter of next book
            try:
                current_book_index = self.book_order.index(book)
                if current_book_index < len(self.book_order) - 1:
                    next_book = self.book_order[current_book_index + 1]
                    print(f"\n{Colors.BRIGHT_CYAN}📖 Moving to next book: {next_book}{Colors.RESET}\n")
                    self.display_chapter(next_book, "1")
                else:
                    print(f"\n{Colors.BRIGHT_GOLD}📜 You've reached the end of the Bible! (Revelation 22){Colors.RESET}\n")
            except ValueError:
                print(f"\n{Colors.ERROR}✗ Book not found in order{Colors.RESET}\n")

    def prev_chapter(self):
        """Navigate to the previous chapter"""
        if not self.current_chapter_ref:
            print(f"\n{Colors.GRAY}No chapter currently open. Read a chapter first (e.g., 'Genesis 1'){Colors.RESET}\n")
            return

        # Parse current chapter reference
        parts = self.current_chapter_ref.rsplit(' ', 1)
        if len(parts) != 2:
            print(f"\n{Colors.ERROR}✗ Invalid chapter reference{Colors.RESET}\n")
            return

        book, chapter = parts
        chapter_num = int(chapter)

        # Check if we're at the first chapter of this book
        if chapter_num > 1:
            # Move to previous chapter in same book
            prev_chapter_num = chapter_num - 1
            self.display_chapter(book, str(prev_chapter_num))
        else:
            # Move to last chapter of previous book
            try:
                current_book_index = self.book_order.index(book)
                if current_book_index > 0:
                    prev_book = self.book_order[current_book_index - 1]
                    prev_book_last_chapter = self.get_chapter_count(prev_book)
                    print(f"\n{Colors.BRIGHT_CYAN}📖 Moving to previous book: {prev_book}{Colors.RESET}\n")
                    self.display_chapter(prev_book, str(prev_book_last_chapter))
                else:
                    print(f"\n{Colors.BRIGHT_GOLD}📜 You're at the beginning of the Bible! (Genesis 1){Colors.RESET}\n")
            except ValueError:
                print(f"\n{Colors.ERROR}✗ Book not found in order{Colors.RESET}\n")

    def export_bookmarks(self, filename=None):
        """Export bookmarks to a text file"""
        if not self.bookmarks:
            print(f"\n{Colors.GRAY}No bookmarks to export. Add some bookmarks first!{Colors.RESET}\n")
            return

        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bible_bookmarks_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("BIBLE BOOKMARKS\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Translation: {self.current_translation} - {self.translation_info[self.current_translation]['name']}\n")
                f.write("=" * 80 + "\n\n")

                for i, ref in enumerate(self.bookmarks, 1):
                    verse_text = self.get_verse(ref)
                    if verse_text:
                        clean_text = verse_text.replace('# ', '').replace('[', '').replace(']', '')
                        f.write(f"{i}. {ref}\n")
                        f.write(f"   {clean_text}\n\n")

                f.write("=" * 80 + "\n")
                f.write(f"Total: {len(self.bookmarks)} bookmarked verses\n")

            print(f"\n{Colors.SUCCESS}✓ Bookmarks exported to: {filename}{Colors.RESET}\n")
        except Exception as e:
            print(f"\n{Colors.ERROR}✗ Error exporting bookmarks: {e}{Colors.RESET}\n")

    def export_history(self, filename=None):
        """Export history to a text file"""
        if not self.history:
            print(f"\n{Colors.GRAY}No history to export. View some verses first!{Colors.RESET}\n")
            return

        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bible_history_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("BIBLE READING HISTORY\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Translation: {self.current_translation} - {self.translation_info[self.current_translation]['name']}\n")
                f.write("=" * 80 + "\n\n")

                for i, ref in enumerate(reversed(self.history[-50:]), 1):
                    verse_text = self.get_verse(ref)
                    if verse_text:
                        clean_text = verse_text.replace('# ', '').replace('[', '').replace(']', '')
                        f.write(f"{i}. {ref}\n")
                        f.write(f"   {clean_text}\n\n")

                f.write("=" * 80 + "\n")
                f.write(f"Total: {len(self.history)} verses in history\n")

            print(f"\n{Colors.SUCCESS}✓ History exported to: {filename}{Colors.RESET}\n")
        except Exception as e:
            print(f"\n{Colors.ERROR}✗ Error exporting history: {e}{Colors.RESET}\n")

    def cycle_theme(self):
        """Cycle to next theme and redraw screen"""
        current_index = self.theme_list.index(self.current_theme)
        next_index = (current_index + 1) % len(self.theme_list)
        self.current_theme = self.theme_list[next_index]
        Colors.set_theme(self.current_theme)

        # Clear screen and redraw dashboard with new theme
        print("\033[2J\033[H", end='', flush=True)

        # Redraw dashboard header
        title = f"{Colors.BRIGHT_GOLD}✟  BIBLE ANALYSIS TOOL  ✟{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(title, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        info = self.translation_info.get(self.current_translation, {})
        trans_line = f"Translation: {self.current_translation} - {info.get('name', '')} ({info.get('year', '')})"
        theme_name = THEMES[self.current_theme]["name"]
        print(f"{Colors.GRAY}  {trans_line}")
        print(f"  Theme: {Colors.BRIGHT_GOLD}{theme_name}{Colors.RESET} {Colors.GRAY}(Press 't' to change)")
        print(f"  Created by {Colors.CYAN}@Ringmast4r{Colors.RESET}\n")

    def animated_splash(self):
        """Display animated pixelate-in splash screen (skippable with Enter)"""
        # Clear screen
        print("\033[2J\033[H", end='', flush=True)

        # ASCII art splash - Custom Bible Design
        splash_art = f"""{Colors.CYAN}
                          ..::..::::::::::::.::.
                         ..:+=.:*######*#**#::.
                         ..:=:=%-:-+#+::*+:*::.
                          .:=#*.:%=#::-#+:+*::..
                        ...:-#:*--+-**#-=+**.-....
                     ...:::.:#=+:+=+++=-*:+*.=.:-....
                 ....::::=#::#-:#**.:#**.:#*.***=:.-:..
               ...:::-+#+++=.%:+:.+*#-.+*=:*.**+=+*+:::...
              ..:::=*+=====+.#=+:*==+:#==+-+.**++=+=++-:::..
            ..:::=#+====+=.-.*+:***:-#**::*+.+:.++=====+=:::..
           ..::-*+=====.:+#*.=-=*::=*+::*%:+:-.=+::++====+-::..
         ..:.:=*+====.-#+..-::--=***++**+=-=::....=-.=+=+==+:::..
         .-::++===*::#+.. .:::=:--======--::-:..  ..=::+====+::-..
        .:::++====.-#..  ..-:=+-:-=++++=-:.==--:.  ...-:=+===+:::.
        .::=*===+.-*.....-:=-:++=-:-=*+---=+-:+--..   .=:-=====:::
.::::::.-==*++++==%:...::-=:+*==*+**+-=*+=+=:#=:=-:.....--+=====--.::::::.
.:-=---:::::::...:::::::-=-=:=*##-:+*+#:=+#*====:+-:::-----=====+++++++=::
.:=.:=+-:-+-:::=+=:::==:-:=:#:+=-+#-+*:+*#--+#*-=-=:*:.:=+:-::==::.==::=.:
.:+=:+-+=*-+#-+==*==*#:-:+--#+:-***.:+--====-=*:=:--.=+*+-=*===-*+=+-*:+.:
::+*+-+++=-+*=+:=**--*:=:+*-:-##+*+**+*****+++::*=:+:*-=**=:***+:+=*-:*+.:
::*-.#::***-:***--*#-#:+:++:=++=-:.:-+--**=:-+-+==:=:+=%=:+##=:+**+:=+:*.:
::+*.-+#=.=*#=:-**+:=*:--=+:#*-:=**=:#:=++++-:#=-::-.#-:***::*#+-:**+.*+.:
::=+-++--*=*-:***-:#::=:::*:=::#=-+-:**-*+::#+*:-:=:#:=#:=-#+:==**:=+#-=:-
::=..:=#=:.+#-..*#-:-:+-:-:*-:.#*=::*+++::*#+::+:-:-:--:#*-.:+#*:.-#*::-.-
-.:-::::::::::::::::::::.:+:+*:-#*#*-:=+***#==+.-:......::::::::::::::::.-
.:::--==++-=*****-:=----:+.=-.++.::::-+#+-=*-::-.#+:..::--*+=++-:-:::::::.
     ..  .:.==---=.:-.. ..:=:-+:::+#*+=+*::.*::+*... .:::*==-=-.=.
        ..::.+-:-:=-.+.......::.::*%#*#%*::.:.=..  ..-:-+=--==.-:.
         ...:.--:--=+.:+... .:=++%%*+==*%#*::-:. ..:::*+---=-.=-.
           ..:..=:::-=+.:=..:.*+.=*:..:+:.+#.+::.=::#+=-==+:.*-..
            ..:..:=---==+=.:-.*+.+.#=-*:=+.*#=.::-*=----==.-*..
             ...=..:+=--===+#.#*..#*#.:+*#::+=:=+-----=*.:*-..
                ..:-..==---=-:*++-=*:=@-=:*-.+.=-=--=-..*+.
                   ..=:..=+=-:*-#*::+*+::*#*:*.====..=#-.
                      ..=+.:::++:*=#=.#=%-.*=#.-..*#-..
                          ..::+*:-*+++:+*+=.+*.=...
                          ..::+==--*.-#-=::+:=--:
                          ..-:#.+*-.****.:*#--=:-
                           .-:#.=:-%:-*:=%::==*.-
                          ..-:#+:++**:.***+:.**.-.
                          ..-:*:+:=+:==:++--:=*.-.
                          ..:---**-.**++=:=#+-+.-.
                          .::=::*::#:+=--#::+-+:-.
                          .-.*+:-=#**::**+*-.=+:-.
                          .-.#+=:=*+-+=--+=--.*--..
                          .=.#:=#+-:*+**-::**::--..
                          .-:%:++-++:+=-:#-.=-:--:
                          .::#--***#:.:+**++::*=:-.
                          .:-**-:+=+-+::==+---:+.=.
                          ..-*:*+=:.=#*+--::*=:*.+.
                          .:=*.#*:-*:==+-:+-*=-*.+.
                          .:=*:--=*++.:=+#*=.-=*:=.
                         ..:=*+:=+===-+--=+++::+-::
                         .::==:+=-+:.+**+-=.:#:=+.:
                         .::+..#*::*=*==+-.+-*::+.:
                         .-:#..-:+**-.:+:.##-.-*=.-.
                         .-.#*.:*====*-.-*++*=.++:-.
                         .-.#:*::-+=:.+#=-+=:-*.*:=.
                         .::+.***+:.-#**+:.:**+:-.+.
                         .::+...::=#:...-##**+.:=.=.
                         ..:####**++++*++*+++***#.-:.
                         .+*#######################..
{Colors.RESET}

{Colors.WHITE}
 ██████╗ ██╗██████╗ ██╗     ███████╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗██╗███████╗
 ██╔══██╗██║██╔══██╗██║     ██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██║██╔════╝
 ██████╔╝██║██████╔╝██║     █████╗      ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗██║███████╗
 ██╔══██╗██║██╔══██╗██║     ██╔══╝      ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██║╚════██║
 ██████╔╝██║██████╔╝███████╗███████╗    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║██║███████║
 ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝╚══════╝
                                   ████████╗ ██████╗  ██████╗ ██╗
                                   ╚══██╔══╝██╔═══██╗██╔═══██╗██║
                                      ██║   ██║   ██║██║   ██║██║
                                      ██║   ╚██████╔╝╚██████╔╝███████╗
                                      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{Colors.RESET}
{Colors.GRAY}                      Explore 340,000+ Scripture Cross-References
                            4 Bible Translations Available
{Colors.RESET}"""

        lines = splash_art.split('\n')
        skip_animation = False

        def check_skip():
            """Check if Enter was pressed to skip animation"""
            if sys.platform == 'win32':
                try:
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key in (b'\r', b'\n', b' '):
                            return True
                except:
                    pass
            return False

        # Stage 1: 20% visible
        print("\033[2J\033[H", end='', flush=True)
        for line in lines:
            pixelated = ''.join(c if random.random() < 0.20 else ' ' for c in line)
            print(pixelated)
        sys.stdout.flush()
        if check_skip():
            skip_animation = True

        if not skip_animation:
            time.sleep(0.3)

            # Stage 2: 40% visible
            print("\033[2J\033[H", end='', flush=True)
            for line in lines:
                pixelated = ''.join(c if random.random() < 0.40 else ' ' for c in line)
                print(pixelated)
            sys.stdout.flush()
            if check_skip():
                skip_animation = True

        if not skip_animation:
            time.sleep(0.3)

            # Stage 3: 60% visible
            print("\033[2J\033[H", end='', flush=True)
            for line in lines:
                pixelated = ''.join(c if random.random() < 0.60 else ' ' for c in line)
                print(pixelated)
            sys.stdout.flush()
            if check_skip():
                skip_animation = True

        if not skip_animation:
            time.sleep(0.3)

            # Stage 4: 80% visible
            print("\033[2J\033[H", end='', flush=True)
            for line in lines:
                pixelated = ''.join(c if random.random() < 0.80 else ' ' for c in line)
                print(pixelated)
            sys.stdout.flush()
            if check_skip():
                skip_animation = True

        if not skip_animation:
            time.sleep(0.3)

        # Final: 100% visible
        print("\033[2J\033[H", end='', flush=True)
        print(splash_art)
        sys.stdout.flush()

        if not skip_animation:
            time.sleep(3.0)  # Pause so users can see the art
            # Prompt to continue (prevents scrolling away)
            print(f"\n{Colors.GRAY}                    Press Enter to continue...{Colors.RESET}")
            try:
                input()
            except:
                pass  # Handle timeout or EOF gracefully

    def main_menu(self):
        """Display beautiful main menu and handle user input"""
        # Show animated splash screen
        self.animated_splash()

        # Clear screen before showing main menu (user feedback: clean dashboard)
        print("\033[2J\033[H", end='', flush=True)

        # Show main dashboard header
        title = f"{Colors.BRIGHT_GOLD}✟  BIBLE ANALYSIS TOOL  ✟{Colors.RESET}"
        print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
        print(make_border_line(title, align='center'))
        print(f"{make_border_bottom()}{Colors.RESET}\n")

        info = self.translation_info.get(self.current_translation, {})
        trans_line = f"Translation: {self.current_translation} - {info.get('name', '')} ({info.get('year', '')})"
        theme_name = THEMES[self.current_theme]["name"]
        print(f"{Colors.GRAY}  {trans_line}")
        print(f"  Theme: {Colors.BRIGHT_GOLD}{theme_name}{Colors.RESET} {Colors.GRAY}(Press 't' to change)")
        print(f"  Created by {Colors.CYAN}@Ringmast4r{Colors.RESET}\n")

        # Show daily verse
        self.show_daily_verse()

        while True:
            # Bright, colorful command menu (DEATH-STAR inspired)
            menu_title = f"{Colors.BRIGHT_GOLD}BIBLE ANALYSIS COMMANDS{Colors.RESET}"
            print(f"\n{Colors.BRIGHT_CYAN}{make_border_top()}")
            print(make_border_line(menu_title, align='center'))
            print(f"{make_border_bottom()}{Colors.RESET}\n")

            # Color-coded command categories
            print(f"  {Colors.BRIGHT_GOLD}📖 VERSE LOOKUP{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type verse reference{Colors.RESET}    {Colors.GRAY}(e.g., {Colors.ORANGE}'John 3:16'{Colors.GRAY} or {Colors.ORANGE}'Romans 8:28'{Colors.GRAY}){Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_CYAN}📚 CHAPTER READING{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type book and chapter{Colors.RESET}   {Colors.GRAY}(e.g., {Colors.LIME}'Genesis 1'{Colors.GRAY} or {Colors.LIME}'Psalms 23'{Colors.GRAY}){Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Navigation:{Colors.RESET}             {Colors.GRAY}{Colors.ORANGE}'next'{Colors.GRAY} or {Colors.ORANGE}'n'{Colors.GRAY} for next chapter, {Colors.ORANGE}'prev'{Colors.GRAY} or {Colors.ORANGE}'p'{Colors.GRAY} for previous{Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_GREEN}🔍 KEYWORD SEARCH{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Basic search:{Colors.RESET}        {Colors.GRAY}Type keyword (e.g., {Colors.PINK}'love'{Colors.GRAY}, {Colors.PINK}'faith'{Colors.GRAY}){Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Advanced search:{Colors.RESET}     {Colors.GRAY}{Colors.ORANGE}'search [term] --ot/--nt --book [name] --exact'{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Examples:{Colors.RESET}            {Colors.GRAY}{Colors.ORANGE}'search faith --nt'{Colors.GRAY}, {Colors.ORANGE}'search love --book John'{Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_MAGENTA}🌟 DAILY INSPIRATION{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'daily'{Colors.DIM_CYAN} for random verse or {Colors.ORANGE}'random'{Colors.DIM_CYAN} for any verse{Colors.RESET}\n")

            print(f"  {Colors.PURPLE}🔄 BIBLE TRANSLATIONS{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'translations'{Colors.DIM_CYAN} to list all versions{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'translation XXX'{Colors.DIM_CYAN} to switch (e.g., {Colors.ORANGE}'translation ASV'{Colors.DIM_CYAN}){Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'compare [ref]'{Colors.DIM_CYAN} to see verse in all translations{Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_BLUE}📊 STATISTICS & INFO{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'stats'{Colors.DIM_CYAN} for Bible statistics dashboard{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'books'{Colors.DIM_CYAN} to see list of all 66 books{Colors.RESET}\n")

            print(f"  {Colors.LIME}📌 HISTORY & BOOKMARKS{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'history'{Colors.DIM_CYAN} to see recently viewed verses{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'bookmark [ref]'{Colors.DIM_CYAN} to save a favorite verse{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'bookmarks'{Colors.DIM_CYAN} to view all saved bookmarks{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'export bookmarks'{Colors.DIM_CYAN} or {Colors.ORANGE}'export history'{Colors.DIM_CYAN} to save to file{Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_GOLD}🎨 THEME TOGGLE{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'t'{Colors.DIM_CYAN} to cycle through color themes{Colors.RESET}\n")

            print(f"  {Colors.BRIGHT_RED}❌ EXIT PROGRAM{Colors.RESET}")
            print(f"     {Colors.DIM_CYAN}Type {Colors.ORANGE}'quit'{Colors.DIM_CYAN} or {Colors.ORANGE}'exit'{Colors.DIM_CYAN} to close{Colors.RESET}\n")

            print(f"{Colors.BRIGHT_GOLD}{'═' * 80}{Colors.RESET}")
            choice = input(f"\n{Colors.BRIGHT_CYAN}⊳ Enter your choice:{Colors.RESET} ").strip()

            if not choice:
                continue

            # Check for quit
            if choice.lower() in ['quit', 'exit', 'q']:
                goodbye_msg = f"{Colors.BRIGHT_CYAN}May God bless you on your journey!{Colors.RESET}"
                print(f"\n{Colors.BRIGHT_GOLD}{make_border_top()}")
                print(make_border_line(goodbye_msg, align='center'))
                print(f"{make_border_bottom()}{Colors.RESET}\n")
                break

            # Theme toggle
            if choice.lower() == 't':
                self.cycle_theme()

            # Daily verse
            elif choice.lower() == 'daily':
                self.show_daily_verse()

            # List translations
            elif choice.lower() == 'translations':
                self.list_translations()

            # Switch translation
            elif choice.lower().startswith('translation '):
                abbrev = choice[12:].strip()
                if abbrev:
                    self.switch_translation(abbrev)
                else:
                    self.list_translations()

            # Statistics dashboard
            elif choice.lower() == 'stats':
                self.show_statistics()

            # Books list
            elif choice.lower() == 'books':
                self.show_books_list()

            # Compare translations
            elif choice.lower().startswith('compare '):
                reference = choice[8:].strip()
                if reference:
                    self.compare_translations(reference)
                else:
                    print(f"\n{Colors.ERROR}✗ Please provide a verse reference (e.g., 'compare John 3:16'){Colors.RESET}\n")

            # History
            elif choice.lower() == 'history':
                self.show_history()

            # Bookmark verse
            elif choice.lower().startswith('bookmark '):
                reference = choice[9:].strip()
                if reference:
                    self.add_bookmark(reference)
                else:
                    print(f"\n{Colors.ERROR}✗ Please provide a verse reference (e.g., 'bookmark John 3:16'){Colors.RESET}\n")

            # Show bookmarks
            elif choice.lower() == 'bookmarks':
                self.show_bookmarks()

            # Random verse
            elif choice.lower() == 'random':
                self.show_random_verse()

            # Next chapter navigation
            elif choice.lower() in ['next', 'n']:
                self.next_chapter()

            # Previous chapter navigation
            elif choice.lower() in ['prev', 'previous', 'p']:
                self.prev_chapter()

            # Export commands
            elif choice.lower().startswith('export '):
                export_type = choice[7:].strip().lower()
                if export_type == 'bookmarks':
                    self.export_bookmarks()
                elif export_type == 'history':
                    self.export_history()
                else:
                    print(f"\n{Colors.ERROR}✗ Unknown export type. Use 'export bookmarks' or 'export history'{Colors.RESET}\n")

            # Advanced search with filters
            elif choice.lower().startswith('search '):
                # Parse search command with filters
                search_input = choice[7:].strip()
                testament = None
                book = None
                exact_phrase = False

                # Check for filters
                if '--ot' in search_input.lower():
                    testament = 'OT'
                    search_input = re.sub(r'--ot', '', search_input, flags=re.IGNORECASE).strip()
                elif '--nt' in search_input.lower():
                    testament = 'NT'
                    search_input = re.sub(r'--nt', '', search_input, flags=re.IGNORECASE).strip()

                if '--exact' in search_input.lower():
                    exact_phrase = True
                    search_input = re.sub(r'--exact', '', search_input, flags=re.IGNORECASE).strip()

                # Check for --book filter
                book_match = re.search(r'--book\s+([A-Za-z0-9 ]+?)(?:\s+--|$)', search_input, re.IGNORECASE)
                if book_match:
                    book = book_match.group(1).strip()
                    search_input = re.sub(r'--book\s+[A-Za-z0-9 ]+', '', search_input, flags=re.IGNORECASE).strip()

                if search_input:
                    self.search_keyword(search_input, testament=testament, book=book, exact_phrase=exact_phrase)
                else:
                    print(f"\n{Colors.ERROR}✗ Please provide a search term{Colors.RESET}\n")

            # Check if it's a verse reference (contains a colon)
            elif ':' in choice:
                self.display_verse(choice)

            # Check if it's a chapter reference
            elif re.match(r'^[A-Za-z]+ \d+$', choice) or re.match(r'^\d? ?[A-Za-z]+ \d+$', choice):
                parts = choice.rsplit(' ', 1)
                if len(parts) == 2:
                    book, chapter = parts
                    self.display_chapter(book, chapter)

            # Otherwise treat as basic search keyword
            else:
                self.search_keyword(choice)

if __name__ == "__main__":
    try:
        reader = BibleReader()
        reader.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GOLD}May God bless you! Goodbye.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.ERROR}An error occurred: {e}{Colors.RESET}\n")
