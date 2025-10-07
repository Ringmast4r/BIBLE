// Arc Diagram - True Circular Arcs
// Bible Cross-Reference Visualization
// Created by Ringmast4r

class ArcDiagramTableauStyle {
    constructor(svgId, tooltipId) {
        this.svgId = svgId;
        this.tooltipId = tooltipId;
        this.svg = null;
        this.tooltip = null;
        this.width = 0;
        this.height = 1000;
        this.margin = { top: 60, right: 100, bottom: 150, left: 100 };
        this.densificationPoints = 50; // Points per arc for smooth curves
    }

    render(filters = {}) {
        const container = document.getElementById(this.svgId);
        if (!container) {
            console.error(`SVG container not found: #${this.svgId}`);
            return;
        }
        container.innerHTML = '';

        if (!dataLoader || !dataLoader.isLoaded) {
            console.log('Data not loaded yet');
            return;
        }

        this.width = container.clientWidth;

        this.svg = d3.select(`#${this.svgId}`)
            .attr('width', this.width)
            .attr('height', this.height);

        this.tooltip = d3.select(`#${this.tooltipId}`);

        const chapters = dataLoader.getChapters();
        let connections = dataLoader.getConnections();

        // Apply filters
        if (filters.testament && filters.testament !== 'all') {
            connections = dataLoader.filterConnectionsByTestament(filters.testament);
        }
        if (filters.book) {
            connections = dataLoader.filterConnectionsByBook(filters.book);
        }
        if (filters.minConnections > 1) {
            connections = connections.filter(c => c.weight >= filters.minConnections);
        }

        // Limit connections for performance (optional)
        const maxConnections = 50000;
        if (connections.length > maxConnections) {
            console.log(`Limiting to ${maxConnections} connections for performance`);
            connections = connections.slice(0, maxConnections);
        }

        this.drawTableauStyleArcs(chapters, connections);
    }

    drawTableauStyleArcs(chapters, connections) {
        const innerWidth = this.width - this.margin.left - this.margin.right;
        const innerHeight = this.height - this.margin.top - this.margin.bottom;

        const g = this.svg.append('g')
            .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`);

        // Create chapter index map
        const chapterIndexMap = new Map();
        chapters.forEach((ch, idx) => {
            chapterIndexMap.set(ch.id, idx);
        });

        // X scale: chapter position with edge padding
        // Padding creates buffer space beyond first/last chapters for smooth edge curves
        const edgePadding = 50; // pixels beyond edge chapters
        const xScale = d3.scaleLinear()
            .domain([0, chapters.length - 1])
            .range([edgePadding, innerWidth - edgePadding]);

        // Rainbow color scale based on distance between chapters
        const maxDistance = chapters.length - 1;
        const rainbowColorScale = d3.scaleSequential(d3.interpolateRainbow)
            .domain([0, maxDistance]);

        // Process connections and create arc paths
        console.log(`Drawing ${connections.length} connections with Tableau-style arcs...`);

        const arcPaths = [];

        connections.forEach(conn => {
            const sourceIdx = chapterIndexMap.get(conn.source);
            const targetIdx = chapterIndexMap.get(conn.target);

            if (sourceIdx === undefined || targetIdx === undefined) return;

            // Calculate arc parameters (Tableau formulas)
            const start = Math.min(sourceIdx, targetIdx);
            const end = Math.max(sourceIdx, targetIdx);
            const distance = Math.abs(targetIdx - sourceIdx);
            const radius = distance / 2;

            // Skip if same chapter
            if (distance === 0) return;

            // Generate arc path using trigonometric formula
            const pathPoints = this.generateCircularArcPath(
                start, end, radius, xScale, innerHeight
            );

            arcPaths.push({
                points: pathPoints,
                distance: distance,
                source: conn.source,
                target: conn.target,
                sourceIdx: sourceIdx,
                targetIdx: targetIdx,
                weight: conn.weight
            });
        });

        console.log(`Generated ${arcPaths.length} arc paths`);

        // Draw arcs
        const arcs = g.append('g')
            .attr('class', 'arcs')
            .selectAll('path')
            .data(arcPaths)
            .enter()
            .append('path')
            .attr('d', d => this.createPathString(d.points))
            .attr('fill', 'none')
            .attr('stroke', d => rainbowColorScale(d.distance))
            .attr('stroke-width', 0.5)
            .attr('opacity', 0.6)
            .on('mouseover', (event, d) => this.showTooltip(event, d, chapters))
            .on('mouseout', () => this.hideTooltip());

        // Draw chapter indicators at bottom with hover labels
        const chapterBars = g.append('g')
            .attr('class', 'chapter-bars')
            .attr('transform', `translate(0, ${innerHeight})`);

        // Create hover label for book names
        const hoverLabel = this.svg.append('text')
            .attr('class', 'hover-book-label')
            .attr('x', this.width / 2)
            .attr('y', innerHeight + this.margin.top + 30)
            .attr('text-anchor', 'middle')
            .attr('fill', '#FFD700')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .style('opacity', 0);

        chapterBars.selectAll('line')
            .data(chapters)
            .enter()
            .append('line')
            .attr('x1', (d, i) => xScale(i))
            .attr('x2', (d, i) => xScale(i))
            .attr('y1', 0)
            .attr('y2', 10)
            .attr('stroke', d => d.testament === 'OT' ? '#2ecc71' : '#00CED1')
            .attr('stroke-width', 1)
            .attr('opacity', 0.5)
            .style('cursor', 'pointer')
            .on('mouseover', (event, d) => {
                // Highlight the chapter bar
                d3.select(event.target)
                    .attr('stroke-width', 3)
                    .attr('opacity', 1);

                // Show book name
                const color = d.testament === 'OT' ? '#2ecc71' : '#00CED1';
                hoverLabel
                    .text(`${d.book} ${d.chapter}`)
                    .attr('fill', color)
                    .style('opacity', 1);
            })
            .on('mouseout', (event) => {
                // Reset chapter bar
                d3.select(event.target)
                    .attr('stroke-width', 1)
                    .attr('opacity', 0.5);

                // Hide book name
                hoverLabel.style('opacity', 0);
            });

        // Add title
        this.svg.append('text')
            .attr('x', this.width / 2)
            .attr('y', 30)
            .attr('text-anchor', 'middle')
            .attr('fill', '#FFD700')
            .attr('font-size', '24px')
            .attr('font-weight', 'bold')
            .text('Bible Cross-References by Ringmast4r');

        // Add subtitle
        this.svg.append('text')
            .attr('x', this.width / 2)
            .attr('y', 50)
            .attr('text-anchor', 'middle')
            .attr('fill', '#888')
            .attr('font-size', '14px')
            .text('Rainbow colors show distance between chapters');

        // Add legend
        this.drawRainbowLegend(g, innerWidth, innerHeight, rainbowColorScale, chapters);
    }

    /**
     * Generate circular arc path using Pythagorean theorem for perfect circles
     * Formula: y = sqrt(r² - x²) where r = radius, x = centerOffset
     * This creates true semicircular arcs (parts of perfect circles)
     * More stable than tan/acos approach which can hit infinity at 90°
     */
    generateCircularArcPath(start, end, radius, xScale, innerHeight) {
        const points = [];
        const numPoints = this.densificationPoints;

        for (let i = 0; i <= numPoints; i++) {
            // Index along the arc (0 to distance)
            const index = (i / numPoints) * (end - start);

            // X position
            const xPos = start + index;

            // Calculate Y using circular arc formula
            // This is the EXACT formula from Tableau workbook
            const centerOffset = xPos - start - radius;
            const normalizedX = centerOffset / radius;

            // Check bounds for acos (must be -1 to 1)
            if (normalizedX < -1 || normalizedX > 1) {
                // Outside arc bounds
                points.push({
                    x: xScale(xPos),
                    y: innerHeight
                });
            } else {
                // Inside arc bounds - calculate circular Y using Pythagorean theorem
                // For a circle: x² + y² = r², so y = sqrt(r² - x²)
                const radiusSquared = radius * radius;
                const offsetSquared = centerOffset * centerOffset;
                const yOffset = Math.sqrt(Math.abs(radiusSquared - offsetSquared));

                // Arc height (inverted, so it goes upward)
                const arcY = innerHeight - yOffset;

                points.push({
                    x: xScale(xPos),
                    y: arcY
                });
            }
        }

        return points;
    }

    /**
     * Create SVG path string from points
     */
    createPathString(points) {
        if (points.length === 0) return '';

        let path = `M ${points[0].x} ${points[0].y}`;

        for (let i = 1; i < points.length; i++) {
            path += ` L ${points[i].x} ${points[i].y}`;
        }

        return path;
    }

    /**
     * Draw rainbow gradient legend
     */
    drawRainbowLegend(g, innerWidth, innerHeight, colorScale, chapters) {
        const legendWidth = 300;
        const legendHeight = 20;
        const legendX = innerWidth - legendWidth - 20;
        const legendY = innerHeight + 40;

        // Create gradient
        const gradient = this.svg.append('defs')
            .append('linearGradient')
            .attr('id', 'rainbow-gradient-legend')
            .attr('x1', '0%')
            .attr('x2', '100%');

        // Add color stops
        for (let i = 0; i <= 10; i++) {
            const offset = i * 10;
            const distance = (i / 10) * (chapters.length - 1);
            gradient.append('stop')
                .attr('offset', `${offset}%`)
                .attr('stop-color', colorScale(distance));
        }

        // Draw legend rectangle
        g.append('rect')
            .attr('x', legendX)
            .attr('y', legendY)
            .attr('width', legendWidth)
            .attr('height', legendHeight)
            .attr('fill', 'url(#rainbow-gradient-legend)')
            .attr('stroke', '#444')
            .attr('stroke-width', 1);

        // Add labels
        g.append('text')
            .attr('x', legendX)
            .attr('y', legendY - 5)
            .attr('fill', '#888')
            .attr('font-size', '12px')
            .text('Close');

        g.append('text')
            .attr('x', legendX + legendWidth)
            .attr('y', legendY - 5)
            .attr('text-anchor', 'end')
            .attr('fill', '#888')
            .attr('font-size', '12px')
            .text('Far Apart');

        g.append('text')
            .attr('x', legendX + legendWidth / 2)
            .attr('y', legendY + legendHeight + 15)
            .attr('text-anchor', 'middle')
            .attr('fill', '#888')
            .attr('font-size', '11px')
            .text('Distance Between Chapters');
    }

    /**
     * Show tooltip on hover
     */
    showTooltip(event, d, chapters) {
        const sourceChapter = chapters.find(ch => ch.id === d.source);
        const targetChapter = chapters.find(ch => ch.id === d.target);

        this.tooltip
            .style('display', 'block')
            .style('left', (event.clientX + 10) + 'px')
            .style('top', (event.clientY - 10) + 'px')
            .html(`
                <strong>Connection</strong><br/>
                Source: ${sourceChapter ? sourceChapter.book + ' ' + sourceChapter.chapter : d.source}<br/>
                Target: ${targetChapter ? targetChapter.book + ' ' + targetChapter.chapter : d.target}<br/>
                Distance: ${d.distance} chapters<br/>
                Weight: ${d.weight} references
            `);
    }

    /**
     * Hide tooltip
     */
    hideTooltip() {
        this.tooltip.style('display', 'none');
    }
}

// Export for use in main.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ArcDiagramTableauStyle;
}
