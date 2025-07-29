import math
from typing import Tuple

from models import PortfolioSummary


class AbstractSVGGenerator:
    def __init__(self, width: int = 500, height: int = 500):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.max_radius = min(width, height) // 2 - 50
        
        # Matrix/techno color palette - neon greens, blues, purples
        self.category_colors = {
            "politics": ["#FF0040", "#FF3366", "#FF6699"],     # Neon red/pink
            "crypto": ["#00FF41", "#33FF66", "#66FF88"],       # Matrix green
            "sports": ["#0080FF", "#3399FF", "#66B3FF"],       # Electric blue
            "entertainment": ["#FF00FF", "#FF33FF", "#FF66FF"], # Neon magenta
            "technology": ["#8000FF", "#9933FF", "#B366FF"],   # Electric purple
            "economics": ["#00FFFF", "#33FFFF", "#66FFFF"],    # Cyan
            "other": ["#FFFFFF", "#CCCCCC", "#999999"]         # White/gray
        }
        
        # Sacred geometry ratios
        self.golden_ratio = 1.618
        self.fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
    
    def generate_abstract_svg(self, portfolio: PortfolioSummary) -> str:
        """Generate animated techno abstract pattern based on portfolio data"""
        
        if not portfolio.category_percentages:
            return self._generate_empty_pattern(portfolio.trader_address)
        
        svg_elements = []
        
        # Start SVG with animations, filters and effects
        svg_elements.append(f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                {self._create_animated_filters()}
                {self._create_gradient_definitions(portfolio.category_percentages)}
                {self._create_animated_patterns()}
            </defs>''')
        
        # Animated matrix background
        svg_elements.append(self._create_animated_background())
        
        # Generate data-driven patterns
        categories = sorted(portfolio.category_percentages.items(), key=lambda x: x[1], reverse=True)
        
        # Dynamic grid with category representation
        svg_elements.extend(self._create_dynamic_grid(categories))
        
        # Main visualization - works well for single or multiple categories
        svg_elements.extend(self._create_fluid_visualization(categories, portfolio.total_volume))
        
        # Volume display in corner
        svg_elements.append(self._create_volume_display(portfolio))
        
        # Ambient particles and effects
        svg_elements.extend(self._create_ambient_effects(categories))
        
        # Data breakdown in corner (keeping this as requested)
        svg_elements.append(self._create_data_breakdown(categories))
        
        svg_elements.append('</svg>')
        
        return '\n'.join(svg_elements)
    
    def _create_animated_filters(self) -> str:
        """Create animated filters with techno effects"""
        return '''
            <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3" result="coloredBlur">
                    <animate attributeName="stdDeviation" values="2;4;2" dur="3s" repeatCount="indefinite"/>
                </feGaussianBlur>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <filter id="pulse-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2" result="coloredBlur">
                    <animate attributeName="stdDeviation" values="1;3;1" dur="2s" repeatCount="indefinite"/>
                </feGaussianBlur>
                <feFlood flood-opacity="0.8" result="flood">
                    <animate attributeName="flood-opacity" values="0.3;0.9;0.3" dur="2s" repeatCount="indefinite"/>
                </feFlood>
                <feComposite in="flood" in2="coloredBlur" operator="multiply"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <filter id="fluid-distort" x="-50%" y="-50%" width="200%" height="200%">
                <feTurbulence baseFrequency="0.02" numOctaves="3" result="noise">
                    <animate attributeName="baseFrequency" values="0.01;0.03;0.01" dur="8s" repeatCount="indefinite"/>
                </feTurbulence>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/>
            </filter>
            <filter id="cyber-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="1" result="blur"/>
                <feDropShadow dx="0" dy="0" stdDeviation="4" flood-opacity="0.8">
                    <animate attributeName="flood-opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
                </feDropShadow>
            </filter>
            <filter id="data-glitch" x="-50%" y="-50%" width="200%" height="200%">
                <feTurbulence baseFrequency="0.8" numOctaves="2" result="noise">
                    <animate attributeName="baseFrequency" values="0.5;1.2;0.5" dur="0.3s" repeatCount="indefinite"/>
                </feTurbulence>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="2">
                    <animate attributeName="scale" values="0;3;0" dur="0.15s" repeatCount="indefinite"/>
                </feDisplacementMap>
            </filter>
        '''

    def _create_gradient_definitions(self, categories: dict) -> str:
        """Create neon gradient definitions for each category"""
        gradients = []
        
        # Matrix background gradient
        gradients.append('''
            <radialGradient id="matrix-bg" cx="50%" cy="50%" r="70%">
                <stop offset="0%" style="stop-color:#000000;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#001100;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
            </radialGradient>
        ''')
        
        # Create neon gradients for each category
        for category in categories.keys():
            colors = self.category_colors.get(category, ["#FFFFFF", "#CCCCCC", "#999999"])
            gradients.append(f'''
                <linearGradient id="neon-{category}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{colors[0]};stop-opacity:1" />
                    <stop offset="50%" style="stop-color:{colors[1]};stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:{colors[2]};stop-opacity:0.6" />
                </linearGradient>
                <radialGradient id="glow-{category}" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" style="stop-color:{colors[0]};stop-opacity:0.9" />
                    <stop offset="100%" style="stop-color:{colors[0]};stop-opacity:0" />
                </radialGradient>
            ''')
        
        return '\n'.join(gradients)

    def _create_matrix_background(self) -> str:
        """Create a dark matrix-style background"""
        return f'<rect width="{self.width}" height="{self.height}" fill="url(#matrix-bg)"/>'

    def _create_animated_patterns(self) -> str:
        """Create animated techno patterns"""
        return '''
            <pattern id="flowing-circuit" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
                <rect width="60" height="60" fill="none"/>
                <g opacity="0.4">
                    <line x1="0" y1="30" x2="60" y2="30" stroke="rgba(0,255,155,0.6)" stroke-width="1">
                        <animate attributeName="stroke-opacity" values="0.2;0.8;0.2" dur="3s" repeatCount="indefinite"/>
                    </line>
                    <line x1="30" y1="0" x2="30" y2="60" stroke="rgba(0,255,155,0.6)" stroke-width="1">
                        <animate attributeName="stroke-opacity" values="0.8;0.2;0.8" dur="3s" repeatCount="indefinite"/>
                    </line>
                    <circle cx="30" cy="30" r="3" fill="rgba(0,255,155,0.4)">
                        <animate attributeName="r" values="2;5;2" dur="2s" repeatCount="indefinite"/>
                        <animate attributeName="fill-opacity" values="0.2;0.8;0.2" dur="2s" repeatCount="indefinite"/>
                    </circle>
                </g>
            </pattern>
            <pattern id="data-stream" x="0" y="0" width="100" height="30" patternUnits="userSpaceOnUse">
                <rect width="100" height="30" fill="none"/>
                <g>
                    <rect x="10" y="12" width="15" height="6" fill="rgba(0,255,255,0.5)" rx="2">
                        <animateTransform attributeName="transform" type="translate" values="0,0;80,0;0,0" dur="4s" repeatCount="indefinite"/>
                        <animate attributeName="fill-opacity" values="0.3;0.8;0.3" dur="4s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="35" y="12" width="8" height="6" fill="rgba(255,0,255,0.5)" rx="2">
                        <animateTransform attributeName="transform" type="translate" values="0,0;60,0;0,0" dur="3s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="50" y="12" width="12" height="6" fill="rgba(255,255,0,0.5)" rx="2">
                        <animateTransform attributeName="transform" type="translate" values="0,0;40,0;0,0" dur="5s" repeatCount="indefinite"/>
                    </rect>
                </g>
            </pattern>
        '''

    def _create_digital_grid(self) -> list:
        """Create digital grid pattern"""
        elements = []
        
        # Horizontal lines
        for y in range(0, self.height, 40):
            elements.append(f'<line x1="0" y1="{y}" x2="{self.width}" y2="{y}" stroke="rgba(0,255,65,0.1)" stroke-width="0.5"/>')
        
        # Vertical lines
        for x in range(0, self.width, 40):
            elements.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{self.height}" stroke="rgba(0,255,65,0.1)" stroke-width="0.5"/>')
        
        # Add circuit pattern overlay
        elements.append(f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="url(#circuit)" opacity="0.3"/>')
        
        return elements

    def _create_lotus_petal(self, start_angle: float, end_angle: float, radius: float, category: str) -> str:
        """Create a lotus petal shape"""
        mid_angle = (start_angle + end_angle) / 2
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        mid_rad = math.radians(mid_angle)
        
        # Control points for curved petal
        inner_radius = radius * 0.3
        outer_radius = radius
        
        # Petal tip
        tip_x = self.center_x + outer_radius * math.cos(mid_rad)
        tip_y = self.center_y + outer_radius * math.sin(mid_rad)
        
        # Base points
        base1_x = self.center_x + inner_radius * math.cos(start_rad)
        base1_y = self.center_y + inner_radius * math.sin(start_rad)
        base2_x = self.center_x + inner_radius * math.cos(end_rad)
        base2_y = self.center_y + inner_radius * math.sin(end_rad)
        
        # Control points for curves
        ctrl1_x = self.center_x + (outer_radius * 0.8) * math.cos(start_rad + (end_rad - start_rad) * 0.3)
        ctrl1_y = self.center_y + (outer_radius * 0.8) * math.sin(start_rad + (end_rad - start_rad) * 0.3)
        ctrl2_x = self.center_x + (outer_radius * 0.8) * math.cos(start_rad + (end_rad - start_rad) * 0.7)
        ctrl2_y = self.center_y + (outer_radius * 0.8) * math.sin(start_rad + (end_rad - start_rad) * 0.7)
        
        path = f"M {base1_x} {base1_y} Q {ctrl1_x} {ctrl1_y} {tip_x} {tip_y} Q {ctrl2_x} {ctrl2_y} {base2_x} {base2_y} Z"
        
        return f'<path d="{path}" fill="url(#neon-{category})" stroke="rgba(255,255,255,0.2)" stroke-width="1" filter="url(#glow)"/>'

    def _create_geometric_segment(self, start_angle: float, end_angle: float, radius: float, category: str) -> str:
        """Create geometric diamond/rhombus segments"""
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = math.radians(mid_angle)
        
        # Create diamond shape
        inner_r = radius * 0.4
        outer_r = radius * 0.9
        
        # Diamond points
        outer_x = self.center_x + outer_r * math.cos(mid_rad)
        outer_y = self.center_y + outer_r * math.sin(mid_rad)
        inner_x = self.center_x + inner_r * math.cos(mid_rad)
        inner_y = self.center_y + inner_r * math.sin(mid_rad)
        
        # Side points
        side_r = radius * 0.65
        side1_angle = mid_angle - 8
        side2_angle = mid_angle + 8
        side1_x = self.center_x + side_r * math.cos(math.radians(side1_angle))
        side1_y = self.center_y + side_r * math.sin(math.radians(side1_angle))
        side2_x = self.center_x + side_r * math.cos(math.radians(side2_angle))
        side2_y = self.center_y + side_r * math.sin(math.radians(side2_angle))
        
        path = f"M {inner_x} {inner_y} L {side1_x} {side1_y} L {outer_x} {outer_y} L {side2_x} {side2_y} Z"
        
        return f'<path d="{path}" fill="url(#neon-{category})" stroke="rgba(255,255,255,0.3)" stroke-width="0.5" filter="url(#shadow)"/>'

    def _create_intricate_pattern(self, start_angle: float, end_angle: float, radius: float, category: str) -> str:
        """Create intricate inner patterns"""
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = math.radians(mid_angle)
        
        # Create a small decorative element
        center_offset = radius * 0.6
        element_x = self.center_x + center_offset * math.cos(mid_rad)
        element_y = self.center_y + center_offset * math.sin(mid_rad)
        
        colors = self.category_colors.get(category, ["#D3D3D3"])
        
        return f'''
            <circle cx="{element_x}" cy="{element_y}" r="3" fill="{colors[0]}" opacity="0.8" filter="url(#glow)"/>
            <circle cx="{element_x}" cy="{element_y}" r="1.5" fill="white" opacity="0.6"/>
        '''

    def _create_inner_sacred_geometry(self, categories: list) -> list:
        """Create inner sacred geometry patterns"""
        elements = []
        
        # Create multiple concentric geometric shapes
        for i, radius_mult in enumerate([0.35, 0.25, 0.15]):
            radius = self.max_radius * radius_mult
            sides = 6 + i * 2  # Hexagon, octagon, decagon
            
            # Create polygon
            points = []
            for j in range(sides):
                angle = (j * 360 / sides - 90) * math.pi / 180
                x = self.center_x + radius * math.cos(angle)
                y = self.center_y + radius * math.sin(angle)
                points.append(f"{x},{y}")
            
            points_str = " ".join(points)
            elements.append(f'''
                <polygon points="{points_str}" fill="none" 
                        stroke="rgba(255,255,255,0.2)" stroke-width="1" 
                        filter="url(#glow)"/>
            ''')
        
        return elements

    def _create_center_crystal(self, portfolio: PortfolioSummary) -> str:
        """Create crystalline center with portfolio data"""
        crystal_radius = 35
        
        # Multi-layered crystal center
        crystal = f'''
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{crystal_radius}" 
                   fill="rgba(255,255,255,0.9)" stroke="rgba(200,200,255,0.8)" 
                   stroke-width="2" filter="url(#crystal)"/>
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{crystal_radius-8}" 
                   fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{crystal_radius-16}" 
                   fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
            
            <text x="{self.center_x}" y="{self.center_y - 10}" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="9" font-weight="600" fill="#1a1a2e">
                  VOLUME</text>
            <text x="{self.center_x}" y="{self.center_y + 2}" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="700" fill="#2d3748">
                  ${portfolio.total_volume:,.0f}</text>
            <text x="{self.center_x}" y="{self.center_y + 14}" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="8" fill="#718096">
                  {portfolio.trade_count} trades</text>
        '''
        
        return crystal

    def _create_floating_elements(self, categories: list) -> list:
        """Create floating decorative elements"""
        elements = []
        
        import random
        random.seed(42)
        
        # Add floating particles around the mandala
        for i in range(20):
            # Random position in outer area
            angle = random.uniform(0, 360)
            distance = random.uniform(self.max_radius + 20, self.max_radius + 60)
            
            x = self.center_x + distance * math.cos(math.radians(angle))
            y = self.center_y + distance * math.sin(math.radians(angle))
            
            # Keep within bounds
            if 10 < x < self.width - 10 and 10 < y < self.height - 10:
                size = random.uniform(1, 3)
                opacity = random.uniform(0.2, 0.6)
                elements.append(f'<circle cx="{x}" cy="{y}" r="{size}" fill="rgba(255,255,255,{opacity})" filter="url(#glow)"/>')
        
        return elements

    def _create_artistic_title(self, trader_address: str) -> str:
        """Create artistic title with modern styling"""
        return f'''
            <text x="{self.center_x}" y="30" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="300" 
                  fill="rgba(255,255,255,0.9)" filter="url(#glow)">
                  COSMIC PORTFOLIO MANDALA</text>
            <text x="{self.center_x}" y="48" text-anchor="middle" 
                  font-family="'Courier New', monospace" font-size="10" 
                  fill="rgba(255,255,255,0.6)">
                  {trader_address[:8]}...{trader_address[-6:]}</text>
        '''
    
    def _generate_empty_mandala(self, trader_address: str) -> str:
        """Generate artistic empty mandala for traders with no data"""
        return f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="empty-bg" cx="50%" cy="50%" r="70%">
                    <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#1a1a2e;stop-opacity:1" />
                </radialGradient>
                <filter id="empty-glow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <rect width="{self.width}" height="{self.height}" fill="url(#empty-bg)"/>
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{self.max_radius}" 
                   fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" 
                   stroke-dasharray="10,5" filter="url(#empty-glow)"/>
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{self.max_radius * 0.7}" 
                   fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{self.max_radius * 0.4}" 
                   fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
            
            <text x="{self.center_x}" y="{self.center_y - 15}" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="300" 
                  fill="rgba(255,255,255,0.8)" filter="url(#empty-glow)">
                  AWAITING COSMIC DATA</text>
            <text x="{self.center_x}" y="{self.center_y + 5}" text-anchor="middle" 
                  font-family="'Courier New', monospace" font-size="10" 
                  fill="rgba(255,255,255,0.5)">
                  {trader_address[:8]}...{trader_address[-6:]}</text>
            <text x="{self.center_x}" y="{self.center_y + 25}" text-anchor="middle" 
                  font-family="'Segoe UI', Arial, sans-serif" font-size="9" 
                  fill="rgba(255,255,255,0.3)">
                  No trading activity detected</text>
        </svg>'''

    def _create_data_visualization(self, categories: list) -> list:
        """Create abstract data visualization elements"""
        elements = []
        total_angle = 0
        
        for category, percentage in categories:
            angle_size = (percentage / 100) * 360
            
            # Create concentric rings for data representation
            for ring in range(3):
                radius = self.max_radius * (0.7 - ring * 0.15)
                ring_elements = self._create_data_ring(total_angle, total_angle + angle_size, radius, category, ring)
                elements.extend(ring_elements)
            
            total_angle += angle_size
        
        return elements

    def _create_data_ring(self, start_angle: float, end_angle: float, radius: float, category: str, ring_index: int) -> list:
        """Create individual data ring segments"""
        elements = []
        mid_angle = (start_angle + end_angle) / 2
        
        # Create arc segment
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Arc path
        inner_radius = radius - 15
        outer_radius = radius
        
        x1 = self.center_x + inner_radius * math.cos(start_rad)
        y1 = self.center_y + inner_radius * math.sin(start_rad)
        x2 = self.center_x + outer_radius * math.cos(start_rad)
        y2 = self.center_y + outer_radius * math.sin(start_rad)
        x3 = self.center_x + outer_radius * math.cos(end_rad)
        y3 = self.center_y + outer_radius * math.sin(end_rad)
        x4 = self.center_x + inner_radius * math.cos(end_rad)
        y4 = self.center_y + inner_radius * math.sin(end_rad)
        
        large_arc = "1" if end_angle - start_angle > 180 else "0"
        
        path = f"M {x1} {y1} L {x2} {y2} A {outer_radius} {outer_radius} 0 {large_arc} 1 {x3} {y3} L {x4} {y4} A {inner_radius} {inner_radius} 0 {large_arc} 0 {x1} {y1} Z"
        
        opacity = 0.7 - ring_index * 0.2
        elements.append(f'<path d="{path}" fill="url(#neon-{category})" opacity="{opacity}" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>')
        
        return elements

    def _create_glitch_elements(self, categories: list) -> list:
        """Create glitch effect elements"""
        elements = []
        
        # Add random glitch rectangles
        import random
        random.seed(42)
        
        for i in range(8):
            x = random.randint(50, self.width - 100)
            y = random.randint(50, self.height - 50)
            width = random.randint(20, 80)
            height = random.randint(2, 8)
            
            category = random.choice([cat[0] for cat in categories]) if categories else "crypto"
            colors = self.category_colors.get(category, ["#00FF41"])
            
            elements.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{colors[0]}" opacity="0.6" filter="url(#glitch)"/>')
        
        # Add scanline effect
        for y in range(0, self.height, 4):
            elements.append(f'<line x1="0" y1="{y}" x2="{self.width}" y2="{y}" stroke="rgba(0,255,65,0.03)" stroke-width="1"/>')
        
        return elements

    def _create_symmetric_patterns(self, categories: list) -> list:
        """Create symmetric pattern elements"""
        elements = []
        
        # Create radial symmetry with category data
        for i, (category, percentage) in enumerate(categories[:6]):  # Limit to 6 for symmetry
            angle = i * 60
            radius = self.max_radius * 0.8
            
            # Create symmetric elements at each angle
            for reflection in [0, 180]:  # Create mirrored elements
                actual_angle = angle + reflection
                rad = math.radians(actual_angle)
                
                x = self.center_x + radius * math.cos(rad)
                y = self.center_y + radius * math.sin(rad)
                
                # Create small decorative elements
                colors = self.category_colors.get(category, ["#FFFFFF"])
                elements.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{colors[0]}" opacity="0.8" filter="url(#neon-glow)"/>')
                elements.append(f'<circle cx="{x}" cy="{y}" r="2" fill="white" opacity="0.6"/>')
        
        return elements

    def _create_data_breakdown(self, categories: list) -> str:
        """Create data breakdown display in corner with proper spacing"""
        breakdown_x = self.width - 140  # Moved left to provide more space
        breakdown_y = 30
        
        breakdown = f'<g transform="translate({breakdown_x}, {breakdown_y})">'
        
        # Background panel - made wider to accommodate percentage values
        breakdown += f'<rect x="-10" y="-10" width="130" height="{len(categories) * 18 + 20}" fill="rgba(0,0,0,0.7)" stroke="rgba(255,255,255,0.2)" stroke-width="1" rx="5"/>'
        
        # Title
        breakdown += f'<text x="0" y="5" font-family="monospace" font-size="10" fill="rgba(255,255,255,0.9)">BREAKDOWN</text>'
        
        # Category data with proper spacing
        y_offset = 20
        for category, percentage in categories:
            colors = self.category_colors.get(category, ["#FFFFFF"])
            breakdown += f'<circle cx="5" cy="{y_offset}" r="3" fill="{colors[0]}" opacity="0.8"/>'
            breakdown += f'<text x="15" y="{y_offset + 3}" font-family="monospace" font-size="8" fill="rgba(255,255,255,0.8)">{category.upper()[:8]}</text>'
            # Moved percentage further right to prevent overlap
            breakdown += f'<text x="100" y="{y_offset + 3}" font-family="monospace" font-size="8" fill="rgba(255,255,255,0.6)" text-anchor="end">{percentage:.1f}%</text>'
            y_offset += 18
        
        breakdown += '</g>'
        return breakdown

    def _generate_empty_pattern(self, trader_address: str) -> str:
        """Generate empty pattern for traders with no data"""
        return self._generate_empty_mandala(trader_address)

    def _create_animated_background(self) -> str:
        """Create animated matrix-style background"""
        return f'''
            <rect width="{self.width}" height="{self.height}" fill="url(#matrix-bg)"/>
            <rect width="{self.width}" height="{self.height}" fill="url(#flowing-circuit)" opacity="0.6">
                <animateTransform attributeName="transform" type="translate" values="0,0;-60,0;0,0" dur="20s" repeatCount="indefinite"/>
            </rect>
        '''

    def _create_dynamic_grid(self, categories: list) -> list:
        """Create dynamic grid that adapts to category data"""
        elements = []
        
        # Base grid with category colors
        primary_category = categories[0] if categories else ("crypto", 100)
        primary_colors = self.category_colors.get(primary_category[0], ["#00FF41", "#33FF66", "#66FF88"])
        
        # Animated grid lines
        for i in range(0, self.width, 50):
            elements.append(f'''
                <line x1="{i}" y1="0" x2="{i}" y2="{self.height}" 
                      stroke="{primary_colors[0]}" stroke-width="0.5" opacity="0.3">
                    <animate attributeName="opacity" values="0.1;0.5;0.1" dur="4s" begin="{i*0.1}s" repeatCount="indefinite"/>
                </line>
            ''')
        
        for i in range(0, self.height, 50):
            elements.append(f'''
                <line x1="0" y1="{i}" x2="{self.width}" y2="{i}" 
                      stroke="{primary_colors[1]}" stroke-width="0.5" opacity="0.3">
                    <animate attributeName="opacity" values="0.1;0.5;0.1" dur="4s" begin="{i*0.1}s" repeatCount="indefinite"/>
                </line>
            ''')
        
        return elements

    def _create_fluid_visualization(self, categories: list, total_volume: float) -> list:
        """Create fluid visualization that works well for single or multiple categories"""
        elements = []
        
        if len(categories) == 1:
            # Single category - create flowing artistic pattern
            elements.extend(self._create_single_category_flow(categories[0], total_volume))
        elif len(categories) == 2:
            # Two categories - create dual flowing pattern
            elements.extend(self._create_dual_category_flow(categories, total_volume))
        elif len(categories) == 3:
            # Three categories - create triple flowing pattern
            elements.extend(self._create_triple_category_flow(categories, total_volume))
        else:
            # Multiple categories - create interconnected network pattern
            elements.extend(self._create_multi_category_network(categories, total_volume))
            
        return elements

    def _create_single_category_flow(self, category_data: tuple, total_volume: float) -> list:
        """Create flowing pattern for single category traders"""
        elements = []
        category, percentage = category_data
        colors = self.category_colors.get(category, ["#00FF41", "#33FF66", "#66FF88"])
        
        # Create flowing spiral pattern
        num_spirals = 3
        for spiral in range(num_spirals):
            radius_offset = spiral * 40
            points = []
            
            for t in range(0, 360, 5):
                angle = math.radians(t)
                radius = (self.max_radius - radius_offset) * (0.6 + 0.4 * math.sin(angle * 3))
                x = self.center_x + radius * math.cos(angle)
                y = self.center_y + radius * math.sin(angle)
                points.append(f"{x},{y}")
            
            path_data = "M " + " L ".join(points) + " Z"
            elements.append(f'''
                <path d="{path_data}" fill="none" stroke="{colors[spiral % len(colors)]}" 
                      stroke-width="2" opacity="0.7" filter="url(#neon-glow)">
                    <animateTransform attributeName="transform" type="rotate" 
                                    values="0 {self.center_x} {self.center_y};360 {self.center_x} {self.center_y}" 
                                    dur="{15 + spiral * 5}s" repeatCount="indefinite"/>
                </path>
            ''')
        
        # Add flowing particles
        for i in range(12):
            angle = i * 30
            radius = self.max_radius * 0.8
            x = self.center_x + radius * math.cos(math.radians(angle))
            y = self.center_y + radius * math.sin(math.radians(angle))
            
            elements.append(f'''
                <circle cx="{x}" cy="{y}" r="4" fill="{colors[0]}" opacity="0.8" filter="url(#pulse-glow)">
                    <animateTransform attributeName="transform" type="rotate" 
                                    values="0 {self.center_x} {self.center_y};360 {self.center_x} {self.center_y}" 
                                    dur="20s" repeatCount="indefinite"/>
                    <animate attributeName="r" values="2;6;2" dur="3s" repeatCount="indefinite"/>
                </circle>
            ''')
        
        return elements

    def _create_dual_category_flow(self, categories: list, total_volume: float) -> list:
        """Create flowing pattern for two categories - yin/yang style flows"""
        elements = []
        cat1, percent1 = categories[0]
        cat2, percent2 = categories[1]
        
        colors1 = self.category_colors.get(cat1, ["#00FF41", "#33FF66", "#66FF88"])
        colors2 = self.category_colors.get(cat2, ["#FF0040", "#FF3366", "#FF6699"])
        
        # Create two interwoven spiral flows
        for side in range(2):
            category = categories[side]
            colors = colors1 if side == 0 else colors2
            percentage = percent1 if side == 0 else percent2
            
            # Adjust flow intensity based on percentage
            flow_intensity = percentage / 100
            spiral_count = max(2, int(3 * flow_intensity))
            
            for spiral in range(spiral_count):
                points = []
                base_angle_offset = side * 180  # Offset second category by 180 degrees
                
                for t in range(0, 360, 4):
                    angle = math.radians(t + base_angle_offset)
                    # Create flowing wave pattern
                    radius_variation = math.sin(angle * 4 + spiral * math.pi/3) * 0.3 * percentage/100
                    radius = (self.max_radius * (0.8 - spiral * 0.15)) * (0.6 + 0.4 * flow_intensity + radius_variation)
                    
                    x = self.center_x + radius * math.cos(angle)
                    y = self.center_y + radius * math.sin(angle)
                    points.append(f"{x},{y}")
                
                path_data = "M " + " L ".join(points) + " Z"
                opacity = 0.6 * flow_intensity
                
                elements.append(f'''
                    <path d="{path_data}" fill="none" stroke="{colors[spiral % len(colors)]}" 
                          stroke-width="{2 + flow_intensity}" opacity="{opacity}" filter="url(#neon-glow)">
                        <animateTransform attributeName="transform" type="rotate" 
                                        values="0 {self.center_x} {self.center_y};{360 if side == 0 else -360} {self.center_x} {self.center_y}" 
                                        dur="{12 + spiral * 3}s" repeatCount="indefinite"/>
                    </path>
                ''')
        
        # Add flowing particles for each category
        for side in range(2):
            colors = colors1 if side == 0 else colors2
            percentage = percent1 if side == 0 else percent2
            particle_count = max(6, int(12 * percentage / 100))
            
            for i in range(particle_count):
                angle = (i * 360 / particle_count) + (side * 180)
                radius = self.max_radius * (0.7 + 0.2 * percentage / 100)
                x = self.center_x + radius * math.cos(math.radians(angle))
                y = self.center_y + radius * math.sin(math.radians(angle))
                
                particle_size = 3 + (percentage / 100) * 3
                
                elements.append(f'''
                    <circle cx="{x}" cy="{y}" r="{particle_size}" fill="{colors[0]}" 
                            opacity="0.8" filter="url(#pulse-glow)">
                        <animateTransform attributeName="transform" type="rotate" 
                                        values="0 {self.center_x} {self.center_y};{360 if side == 0 else -360} {self.center_x} {self.center_y}" 
                                        dur="{18 + side * 2}s" repeatCount="indefinite"/>
                        <animate attributeName="r" values="{particle_size-1};{particle_size+2};{particle_size-1}" 
                                 dur="3s" repeatCount="indefinite"/>
                    </circle>
                ''')
        
        return elements

    def _create_triple_category_flow(self, categories: list, total_volume: float) -> list:
        """Create flowing pattern for three categories - trinity flow"""
        elements = []
        
        # Create three interwoven flows at 120-degree intervals
        for i in range(3):
            category, percentage = categories[i]
            colors = self.category_colors.get(category, ["#FFFFFF", "#CCCCCC", "#999999"])
            
            flow_intensity = percentage / 100
            base_angle_offset = i * 120
            
            # Create flowing patterns for each category
            spiral_count = max(1, int(2 * flow_intensity))
            
            for spiral in range(spiral_count):
                points = []
                
                for t in range(0, 360, 5):
                    angle = math.radians(t + base_angle_offset)
                    # Create trinity wave pattern with interaction between categories
                    wave1 = math.sin(angle * 3 + spiral * math.pi/2) * 0.2
                    wave2 = math.cos(angle * 2 + i * math.pi/3) * 0.15
                    radius_variation = (wave1 + wave2) * percentage/100
                    
                    radius = (self.max_radius * (0.75 - spiral * 0.1)) * (0.5 + 0.5 * flow_intensity + radius_variation)
                    
                    x = self.center_x + radius * math.cos(angle)
                    y = self.center_y + radius * math.sin(angle)
                    points.append(f"{x},{y}")
                
                path_data = "M " + " L ".join(points) + " Z"
                opacity = 0.5 + 0.3 * flow_intensity
                stroke_width = 1.5 + flow_intensity * 1.5
                
                elements.append(f'''
                    <path d="{path_data}" fill="none" stroke="{colors[spiral % len(colors)]}" 
                          stroke-width="{stroke_width}" opacity="{opacity}" filter="url(#neon-glow)">
                        <animateTransform attributeName="transform" type="rotate" 
                                        values="0 {self.center_x} {self.center_y};360 {self.center_x} {self.center_y}" 
                                        dur="{15 + i * 2 + spiral * 3}s" repeatCount="indefinite"/>
                    </path>
                ''')
        
        # Add orbital particles for each category
        for i in range(3):
            category, percentage = categories[i]
            colors = self.category_colors.get(category, ["#FFFFFF"])
            
            particle_count = max(4, int(8 * percentage / 100))
            base_angle = i * 120
            
            for j in range(particle_count):
                angle = base_angle + (j * 120 / particle_count)
                orbit_radius = self.max_radius * (0.6 + 0.3 * percentage / 100)
                x = self.center_x + orbit_radius * math.cos(math.radians(angle))
                y = self.center_y + orbit_radius * math.sin(math.radians(angle))
                
                particle_size = 2.5 + (percentage / 100) * 2.5
                
                elements.append(f'''
                    <circle cx="{x}" cy="{y}" r="{particle_size}" fill="{colors[0]}" 
                            opacity="0.7" filter="url(#pulse-glow)">
                        <animateTransform attributeName="transform" type="rotate" 
                                        values="0 {self.center_x} {self.center_y};360 {self.center_x} {self.center_y}" 
                                        dur="{20 + i * 3}s" repeatCount="indefinite"/>
                        <animate attributeName="r" values="{particle_size-0.5};{particle_size+1.5};{particle_size-0.5}" 
                                 dur="4s" repeatCount="indefinite"/>
                    </circle>
                ''')
        
        return elements

    def _create_multi_category_network(self, categories: list, total_volume: float) -> list:
        """Create network pattern for multiple categories"""
        elements = []
        
        # Create nodes for each category
        angle_step = 360 / len(categories)
        nodes = []
        
        for i, (category, percentage) in enumerate(categories):
            angle = i * angle_step
            radius = self.max_radius * 0.7
            x = self.center_x + radius * math.cos(math.radians(angle))
            y = self.center_y + radius * math.sin(math.radians(angle))
            
            colors = self.category_colors.get(category, ["#FFFFFF"])
            
            # Much more dramatic scaling based on percentage
            # Small categories (0-10%): 4-8px, Medium (10-30%): 8-16px, Large (30%+): 16-28px
            if percentage < 10:
                base_size = 4 + (percentage / 10) * 4  # 4-8px
            elif percentage < 30:
                base_size = 8 + ((percentage - 10) / 20) * 8  # 8-16px
            else:
                base_size = 16 + ((percentage - 30) / 70) * 12  # 16-28px
            
            # Reduce pulsation range to maintain size differences
            pulse_range = max(1, base_size * 0.15)  # Much smaller pulse range
            
            nodes.append((x, y, colors[0], base_size, category))
            
            # Create category node with reduced pulsation
            elements.append(f'''
                <circle cx="{x}" cy="{y}" r="{base_size}" fill="{colors[0]}" 
                        opacity="0.8" filter="url(#cyber-glow)">
                    <animate attributeName="r" values="{base_size-pulse_range};{base_size+pulse_range};{base_size-pulse_range}" 
                             dur="4s" repeatCount="indefinite"/>
                </circle>
            ''')
        
        # Create connections between nodes with thickness based on combined percentages
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                # Line thickness based on combined importance of connected nodes
                combined_percentage = categories[i][1] + categories[j][1]
                line_width = max(0.5, min(3, combined_percentage / 50))
                
                elements.append(f'''
                    <line x1="{node1[0]}" y1="{node1[1]}" x2="{node2[0]}" y2="{node2[1]}" 
                          stroke="rgba(255,255,255,0.3)" stroke-width="{line_width}" opacity="0.5">
                        <animate attributeName="opacity" values="0.2;0.7;0.2" dur="6s" repeatCount="indefinite"/>
                    </line>
                ''')
        
        return elements

    def _create_volume_display(self, portfolio: PortfolioSummary) -> str:
        """Create volume and trade count display in bottom left corner"""
        volume_x = 30
        volume_y = self.height - 50
        
        return f'''
            <g transform="translate({volume_x}, {volume_y})">
                <rect x="-15" y="-25" width="150" height="40" fill="rgba(0,0,0,0.7)" 
                      stroke="rgba(255,255,255,0.2)" stroke-width="1" rx="5"/>
                <text x="0" y="-10" font-family="'Segoe UI', Arial, sans-serif" 
                      font-size="9" font-weight="600" fill="rgba(255,255,255,0.9)">
                      TOTAL VOLUME</text>
                <text x="0" y="2" font-family="'Segoe UI', Arial, sans-serif" 
                      font-size="14" font-weight="700" fill="rgba(0,255,155,0.9)" filter="url(#neon-glow)">
                      ${portfolio.total_volume:,.0f}</text>
                <text x="0" y="12" font-family="'Segoe UI', Arial, sans-serif" 
                      font-size="8" fill="rgba(255,255,255,0.7)">
                      {portfolio.trade_count} trades executed</text>
            </g>
        '''

    def _create_ambient_effects(self, categories: list) -> list:
        """Create ambient floating effects with neutral colors"""
        elements = []
        
        import random
        random.seed(42)
        
        # Neutral ambient colors to avoid category confusion
        ambient_colors = [
            "rgba(255,255,255,0.6)",  # White
            "rgba(200,200,255,0.5)",  # Light blue
            "rgba(255,255,200,0.4)",  # Light yellow
            "rgba(200,255,255,0.5)"   # Light cyan
        ]
        
        # Create floating orbs with neutral colors
        for i in range(15):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            
            # Avoid center area and volume display area
            if (abs(x - self.center_x) < 100 and abs(y - self.center_y) < 100) or \
               (x < 150 and y > self.height - 100):
                continue
                
            color = random.choice(ambient_colors)
            size = random.uniform(1.5, 3.5)
            duration = random.uniform(4, 8)
            
            elements.append(f'''
                <circle cx="{x}" cy="{y}" r="{size}" fill="{color}" opacity="0.4" filter="url(#neon-glow)">
                    <animate attributeName="opacity" values="0.2;0.6;0.2" dur="{duration}s" repeatCount="indefinite"/>
                    <animate attributeName="r" values="{size};{size*1.3};{size}" dur="{duration}s" repeatCount="indefinite"/>
                    <animateTransform attributeName="transform" type="translate" 
                                    values="0,0;{random.randint(-15,15)},{random.randint(-15,15)};0,0" 
                                    dur="{duration*2}s" repeatCount="indefinite"/>
                </circle>
            ''')
        
        return elements