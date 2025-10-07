// Data Loader for Bible Visualizer

class BibleDataLoader {
    constructor() {
        this.graphData = null;
        this.stats = null;
        this.isLoaded = false;
        this.isPreviewMode = false;
        this.loadingProgress = 0;
        this.progressCallbacks = [];
    }

    /**
     * Register a callback for loading progress updates
     * @param {Function} callback - Called with (percentage, message)
     */
    onProgress(callback) {
        this.progressCallbacks.push(callback);
    }

    updateProgress(percentage, message) {
        this.loadingProgress = percentage;
        this.progressCallbacks.forEach(cb => cb(percentage, message));
    }

    /**
     * Load preview data instantly (97KB, top 200 connections)
     */
    loadPreview() {
        if (typeof PREVIEW_DATA === 'undefined') {
            console.warn('Preview data not available');
            return false;
        }

        console.log('⚡ Loading preview data instantly...');
        this.graphData = PREVIEW_DATA;
        this.isPreviewMode = true;
        this.isLoaded = true;
        this.updateProgress(100, 'Preview loaded');

        console.log('✓ Preview mode active:', {
            connections: PREVIEW_DATA.connections.length,
            chapters: PREVIEW_DATA.chapters.length,
            isPreview: PREVIEW_DATA.metadata.is_preview
        });

        return true;
    }

    async load() {
        if (this.isLoaded && !this.isPreviewMode) return;

        try {
            // Determine if we're on localhost or GitHub Pages
            const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

            let urls = [];

            if (isLocal) {
                // Local development - use relative path
                urls = ['../shared-data/processed/graph_data.json'];
            } else {
                // GitHub Pages - try jsDelivr CDN first (faster global delivery), then fallback to GitHub Pages
                urls = [
                    'https://cdn.jsdelivr.net/gh/Ringmast4r/BIBLE@main/shared-data/processed/graph_data.json',
                    '../shared-data/processed/graph_data.json'
                ];
            }

            console.log('Loading data from URLs:', urls);

            // Load graph data with timeout and CDN fallback
            console.log('Fetching graph_data.json (14.5MB)...');
            let graphResponse = null;
            let lastError = null;

            for (const url of urls) {
                try {
                    console.log(`Attempting to load from: ${url}`);
                    this.updateProgress(5, 'Connecting to CDN...');

                    const controller = new AbortController();
                    const timeout = setTimeout(() => controller.abort(), 30000); // 30 second timeout per attempt

                    graphResponse = await fetch(url, {
                        signal: controller.signal,
                        cache: 'default'
                    });
                    clearTimeout(timeout);

                    if (graphResponse.ok) {
                        console.log(`✅ Successfully connected to: ${url}`);
                        this.updateProgress(20, 'Downloading 14.5MB dataset...');
                        break;
                    }
                } catch (error) {
                    console.warn(`Failed to load from ${url}:`, error.message);
                    lastError = error;
                    graphResponse = null;
                }
            }

            if (!graphResponse || !graphResponse.ok) {
                throw lastError || new Error('Failed to load from all sources');
            }

            console.log('Graph response received, parsing JSON...');
            this.updateProgress(60, 'Parsing 14.5MB JSON data...');
            this.graphData = await graphResponse.json();
            this.updateProgress(80, 'Processing graph data...');
            console.log('Graph data loaded successfully:', Object.keys(this.graphData));

            // Load statistics
            const statsUrl = isLocal
                ? '../shared-data/processed/stats.json'
                : 'https://cdn.jsdelivr.net/gh/Ringmast4r/BIBLE@main/shared-data/processed/stats.json';

            const statsResponse = await fetch(statsUrl);
            if (!statsResponse.ok) {
                throw new Error(`HTTP error! status: ${statsResponse.status}`);
            }
            this.stats = await statsResponse.json();

            this.isLoaded = true;
            this.isPreviewMode = false; // Full data loaded
            this.updateProgress(100, 'Full dataset loaded!');

            console.log('✓ Full data loaded successfully:', {
                books: this.graphData.metadata.total_books,
                chapters: this.graphData.metadata.total_chapters,
                connections: this.graphData.metadata.total_connections
            });

            return this.graphData;
        } catch (error) {
            console.error('Error loading data:', error);

            if (error.name === 'AbortError') {
                throw new Error('Request timed out after 60 seconds. The 15MB file may be loading slowly. Please try again or check your internet connection.');
            }

            console.error('Full error details:', {
                name: error.name,
                message: error.message,
                stack: error.stack
            });

            throw error;
        }
    }

    getBooks() {
        return this.graphData ? this.graphData.books : [];
    }

    getChapters() {
        return this.graphData ? this.graphData.chapters : [];
    }

    getConnections() {
        return this.graphData ? this.graphData.connections : [];
    }

    getBookMatrix() {
        if (!this.graphData || !this.graphData.book_matrix) {
            return null;
        }

        // Return object with both books array and matrix
        return {
            books: this.graphData.books.map(book => book.name),
            matrix: this.graphData.book_matrix
        };
    }

    /**
     * Compute comprehensive statistics from the data
     */
    computeComprehensiveStats() {
        if (!this.graphData) return {};

        const chapters = this.graphData.chapters;
        const connections = this.graphData.connections;
        const books = this.graphData.books;
        const stats = this.stats || {};

        console.log('Computing comprehensive statistics...');

        // Helper: Get chapter by ID
        const getChapter = (id) => chapters[id];

        // ====================
        // CROSS-REFERENCE ANALYTICS
        // ====================

        // 1. Longest connection (most distant chapters)
        let longestConnection = { distance: 0, source: null, target: null };
        connections.forEach(conn => {
            if (conn.distance > longestConnection.distance) {
                longestConnection = {
                    distance: conn.distance,
                    source: getChapter(conn.source),
                    target: getChapter(conn.target),
                    weight: conn.weight
                };
            }
        });

        // 2. Shortest connection (minimum distance > 0)
        let shortestConnection = { distance: Infinity, source: null, target: null };
        connections.forEach(conn => {
            if (conn.distance > 0 && conn.distance < shortestConnection.distance) {
                shortestConnection = {
                    distance: conn.distance,
                    source: getChapter(conn.source),
                    target: getChapter(conn.target),
                    weight: conn.weight
                };
            }
        });

        // 3. Average connection distance
        const avgDistance = connections.reduce((sum, conn) => sum + conn.distance, 0) / connections.length;

        // 4. Strongest single connection (highest weight)
        let strongestConnection = { weight: 0, source: null, target: null };
        connections.forEach(conn => {
            if (conn.weight > strongestConnection.weight) {
                strongestConnection = {
                    weight: conn.weight,
                    source: getChapter(conn.source),
                    target: getChapter(conn.target),
                    distance: conn.distance
                };
            }
        });

        // 5. Most connected chapter (total degree centrality)
        const chapterDegree = {};
        connections.forEach(conn => {
            chapterDegree[conn.source] = (chapterDegree[conn.source] || 0) + 1;
            chapterDegree[conn.target] = (chapterDegree[conn.target] || 0) + 1;
        });
        let mostConnected = { id: null, degree: 0, chapter: null };
        Object.entries(chapterDegree).forEach(([id, degree]) => {
            if (degree > mostConnected.degree) {
                mostConnected = { id: parseInt(id), degree, chapter: getChapter(parseInt(id)) };
            }
        });

        // 6. Self-referencing books
        const bookSelfRefs = {};
        connections.forEach(conn => {
            const sourceCh = getChapter(conn.source);
            const targetCh = getChapter(conn.target);
            if (sourceCh && targetCh && sourceCh.book === targetCh.book) {
                bookSelfRefs[sourceCh.book] = (bookSelfRefs[sourceCh.book] || 0) + 1;
            }
        });
        const mostSelfReferencing = Object.entries(bookSelfRefs)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        // 7. Cross-testament bridge books
        const crossTestamentBooks = {};
        connections.forEach(conn => {
            const sourceCh = getChapter(conn.source);
            const targetCh = getChapter(conn.target);
            if (sourceCh && targetCh && sourceCh.testament !== targetCh.testament) {
                crossTestamentBooks[sourceCh.book] = (crossTestamentBooks[sourceCh.book] || 0) + 1;
                crossTestamentBooks[targetCh.book] = (crossTestamentBooks[targetCh.book] || 0) + 1;
            }
        });
        const topBridgeBooks = Object.entries(crossTestamentBooks)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        // ====================
        // BOOK & CHAPTER STATS
        // ====================

        // Testament totals
        const otBooks = books.filter(b => b.testament === 'OT').length;
        const ntBooks = books.filter(b => b.testament === 'NT').length;
        const otChapters = books.filter(b => b.testament === 'OT').reduce((sum, b) => sum + b.chapters, 0);
        const ntChapters = books.filter(b => b.testament === 'NT').reduce((sum, b) => sum + b.chapters, 0);

        // Longest & shortest books by chapters
        const longestBook = books.reduce((max, b) => b.chapters > max.chapters ? b : max, books[0]);
        const shortestBook = books.reduce((min, b) => b.chapters < min.chapters ? b : min, books[0]);

        // Average connections per chapter
        const avgConnectionsPerChapter = connections.length / chapters.length;

        // Connection density by testament
        const otConnections = stats.testament_distribution?.OT_to_OT || 0;
        const ntConnections = stats.testament_distribution?.NT_to_NT || 0;
        const otDensity = otConnections / (otChapters * otChapters);
        const ntDensity = ntConnections / (ntChapters * ntChapters);

        // ====================
        // FUN/INTERESTING STATS
        // ====================

        // Bidirectional connections (reciprocity)
        const connectionPairs = new Set();
        let reciprocalCount = 0;
        connections.forEach(conn => {
            const pair1 = `${conn.source}-${conn.target}`;
            const pair2 = `${conn.target}-${conn.source}`;
            if (connectionPairs.has(pair2)) {
                reciprocalCount++;
            }
            connectionPairs.add(pair1);
        });
        const reciprocityRate = (reciprocalCount / connections.length) * 100;

        // Gospel similarities (Matthew, Mark, Luke, John)
        const gospels = ['Matthew', 'Mark', 'Luke', 'John'];
        const gospelConnections = {};
        connections.forEach(conn => {
            const sourceCh = getChapter(conn.source);
            const targetCh = getChapter(conn.target);
            if (sourceCh && targetCh && gospels.includes(sourceCh.book) && gospels.includes(targetCh.book)) {
                const key = [sourceCh.book, targetCh.book].sort().join('-');
                gospelConnections[key] = (gospelConnections[key] || 0) + 1;
            }
        });

        // Pauline epistles
        const paulineBooks = ['Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
                              'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
                              '1 Timothy', '2 Timothy', 'Titus', 'Philemon'];
        let paulineConnections = 0;
        connections.forEach(conn => {
            const sourceCh = getChapter(conn.source);
            const targetCh = getChapter(conn.target);
            if (sourceCh && targetCh && paulineBooks.includes(sourceCh.book) && paulineBooks.includes(targetCh.book)) {
                paulineConnections++;
            }
        });

        // Torah/Pentateuch (Genesis-Deuteronomy)
        const torahBooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'];
        let torahConnections = 0;
        connections.forEach(conn => {
            const sourceCh = getChapter(conn.source);
            const targetCh = getChapter(conn.target);
            if (sourceCh && targetCh && torahBooks.includes(sourceCh.book) && torahBooks.includes(targetCh.book)) {
                torahConnections++;
            }
        });

        console.log('✓ Comprehensive statistics computed');

        return {
            // Original stats
            ...stats,

            // Cross-Reference Analytics
            longestConnection,
            shortestConnection,
            avgDistance: avgDistance.toFixed(1),
            strongestConnection,
            mostConnectedChapter: mostConnected,
            mostSelfReferencingBooks: mostSelfReferencing,
            topBridgeBooks,

            // Book & Chapter Stats
            otBooks,
            ntBooks,
            otChapters,
            ntChapters,
            totalChapters: chapters.length,
            longestBook,
            shortestBook,
            avgConnectionsPerChapter: avgConnectionsPerChapter.toFixed(1),
            otDensity: (otDensity * 100).toFixed(4),
            ntDensity: (ntDensity * 100).toFixed(4),

            // Fun/Interesting
            reciprocalConnections: reciprocalCount,
            reciprocityRate: reciprocityRate.toFixed(2),
            gospelConnections,
            paulineConnections,
            torahConnections
        };
    }

    getStats() {
        return this.stats || {};
    }

    getComprehensiveStats() {
        return this.computeComprehensiveStats();
    }

    filterConnectionsByTestament(testament) {
        if (!this.graphData) return [];

        const connections = this.graphData.connections;
        const chapters = this.graphData.chapters;

        if (testament === 'all') {
            return connections;
        }

        return connections.filter(conn => {
            const sourceChapter = chapters[conn.source];
            const targetChapter = chapters[conn.target];

            if (testament === 'OT') {
                return sourceChapter.testament === 'OT' && targetChapter.testament === 'OT';
            } else if (testament === 'NT') {
                return sourceChapter.testament === 'NT' && targetChapter.testament === 'NT';
            } else if (testament === 'cross') {
                return sourceChapter.testament !== targetChapter.testament;
            }

            return true;
        });
    }

    filterConnectionsByBook(bookName) {
        if (!this.graphData || !bookName) return this.getConnections();

        const connections = this.graphData.connections;
        const chapters = this.graphData.chapters;

        return connections.filter(conn => {
            const sourceChapter = chapters[conn.source];
            const targetChapter = chapters[conn.target];

            return sourceChapter.book === bookName || targetChapter.book === bookName;
        });
    }

    filterConnectionsByWeight(minWeight) {
        if (!this.graphData) return [];

        return this.graphData.connections.filter(conn => conn.weight >= minWeight);
    }

    getConnectionType(sourceTestament, targetTestament) {
        if (sourceTestament === 'OT' && targetTestament === 'OT') return 'ot-ot';
        if (sourceTestament === 'NT' && targetTestament === 'NT') return 'nt-nt';
        return 'cross-testament';
    }
}

// Global data loader instance
const dataLoader = new BibleDataLoader();
