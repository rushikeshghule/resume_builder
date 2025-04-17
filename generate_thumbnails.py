from PIL import Image, ImageDraw, ImageFont
import os

# Create the directory if it doesn't exist
os.makedirs("static/images/templates", exist_ok=True)

# Template designs with their colors
templates = {
    "modern": {
        "primary": "#3498db",
        "secondary": "#ffffff",
        "accent": "#2c3e50",
        "layout": "sidebar"
    },
    "minimal": {
        "primary": "#555555",
        "secondary": "#ffffff",
        "accent": "#cccccc",
        "layout": "simple"
    },
    "executive": {
        "primary": "#002D62",
        "secondary": "#ffffff",
        "accent": "#B8860B",
        "layout": "classic"
    },
    "creative": {
        "primary": "#ff5252",
        "secondary": "#ffffff",
        "accent": "#6c63ff",
        "layout": "colorful"
    },
    "technical": {
        "primary": "#4285F4",
        "secondary": "#ffffff",
        "accent": "#34A853",
        "layout": "code"
    },
    "elegant": {
        "primary": "#8A2BE2",
        "secondary": "#F8F8FF",
        "accent": "#B8860B",
        "layout": "sidebar"
    },
    "corporate": {
        "primary": "#00396F",
        "secondary": "#ffffff",
        "accent": "#2F80ED",
        "layout": "classic"
    },
    "academic": {
        "primary": "#1B3A57",
        "secondary": "#ffffff",
        "accent": "#82211D",
        "layout": "formal"
    },
    "compact": {
        "primary": "#333333",
        "secondary": "#ffffff",
        "accent": "#3498db",
        "layout": "dense"
    },
    "bold": {
        "primary": "#111111",
        "secondary": "#ffffff",
        "accent": "#FF3E41",
        "layout": "statement"
    },
    "contemporary": {
        "primary": "#3D5A80",
        "secondary": "#ffffff",
        "accent": "#EE6C4D",
        "layout": "modern"
    }
}

def create_thumbnail(template_name, colors, size=(300, 400)):
    # Create a blank white image
    img = Image.new('RGB', size, color=colors["secondary"])
    draw = ImageDraw.Draw(img)
    
    # Draw the template based on layout type
    if colors["layout"] == "sidebar":
        # Draw sidebar
        draw.rectangle([(0, 0), (size[0] * 0.3, size[1])], fill=colors["primary"])
        
        # Draw header
        draw.rectangle([(size[0] * 0.3, 0), (size[0], size[1] * 0.2)], fill=colors["secondary"])
        
        # Draw name line
        draw.rectangle([(size[0] * 0.35, size[1] * 0.05), (size[0] * 0.9, size[1] * 0.08)], fill=colors["primary"])
        
        # Draw content lines
        for i in range(5):
            y_pos = size[1] * 0.25 + i * size[1] * 0.1
            draw.rectangle([(size[0] * 0.35, y_pos), (size[0] * 0.9, y_pos + size[1] * 0.02)], fill=colors["accent"])
            
            # Shorter lines for details
            for j in range(2):
                draw.rectangle([
                    (size[0] * 0.35, y_pos + size[1] * 0.03 + j * size[1] * 0.015),
                    (size[0] * 0.75, y_pos + size[1] * 0.04 + j * size[1] * 0.015)
                ], fill="#dddddd")
    
    elif colors["layout"] == "simple":
        # Draw header
        draw.rectangle([(0, 0), (size[0], size[1] * 0.2)], fill=colors["secondary"])
        
        # Draw name line
        draw.rectangle([(size[0] * 0.1, size[1] * 0.05), (size[0] * 0.9, size[1] * 0.08)], fill=colors["primary"])
        
        # Draw section titles and content
        for i in range(4):
            section_y = size[1] * 0.25 + i * size[1] * 0.15
            
            # Section title
            draw.rectangle([(size[0] * 0.1, section_y), (size[0] * 0.5, section_y + size[1] * 0.03)], fill=colors["primary"])
            
            # Section content
            for j in range(3):
                line_y = section_y + size[1] * 0.05 + j * size[1] * 0.025
                draw.rectangle([(size[0] * 0.1, line_y), (size[0] * 0.9, line_y + size[1] * 0.015)], fill="#dddddd")
    
    elif colors["layout"] == "classic":
        # Draw header
        draw.rectangle([(0, 0), (size[0], size[1] * 0.22)], fill=colors["primary"])
        
        # Draw name line (white on dark background)
        draw.rectangle([(size[0] * 0.1, size[1] * 0.08), (size[0] * 0.9, size[1] * 0.12)], fill=colors["secondary"])
        
        # Draw content sections
        for i in range(3):
            section_y = size[1] * 0.25 + i * size[1] * 0.18
            
            # Section title
            draw.rectangle([(size[0] * 0.1, section_y), (size[0] * 0.9, section_y + size[1] * 0.03)], fill=colors["accent"])
            
            # Item headers
            draw.rectangle([
                (size[0] * 0.1, section_y + size[1] * 0.06),
                (size[0] * 0.9, section_y + size[1] * 0.08)
            ], fill="#eeeeee")
            
            # Content lines
            for j in range(3):
                draw.rectangle([
                    (size[0] * 0.1, section_y + size[1] * 0.1 + j * size[1] * 0.02),
                    (size[0] * 0.9, section_y + size[1] * 0.11 + j * size[1] * 0.02)
                ], fill="#dddddd")
    
    elif colors["layout"] == "colorful":
        # Draw diagonal header
        points = [(0, 0), (size[0], 0), (size[0], size[1] * 0.3), (0, size[1] * 0.4)]
        draw.polygon(points, fill=colors["primary"])
        
        # Draw accent shape
        accent_points = [(size[0], size[1] * 0.3), (size[0], size[1] * 0.5), (size[0] * 0.7, size[1] * 0.4)]
        draw.polygon(accent_points, fill=colors["accent"])
        
        # Draw name (white on colored background)
        draw.rectangle([(size[0] * 0.1, size[1] * 0.1), (size[0] * 0.7, size[1] * 0.15)], fill="white")
        
        # Draw content lines with alternating background
        for i in range(4):
            y_pos = size[1] * 0.45 + i * size[1] * 0.12
            if i % 2 == 0:
                draw.rectangle([(0, y_pos), (size[0], y_pos + size[1] * 0.1)], fill="#f8f9fa")
            
            # Content lines
            draw.rectangle([(size[0] * 0.1, y_pos + size[1] * 0.02), (size[0] * 0.9, y_pos + size[1] * 0.04)], fill="#dddddd")
            draw.rectangle([(size[0] * 0.1, y_pos + size[1] * 0.06), (size[0] * 0.7, y_pos + size[1] * 0.07)], fill="#eeeeee")
    
    elif colors["layout"] == "code":
        # Draw top bar
        draw.rectangle([(0, 0), (size[0], size[1] * 0.15)], fill=colors["primary"])
        
        # Draw code window frame
        draw.rectangle([(size[0] * 0.1, size[1] * 0.2), (size[0] * 0.9, size[1] * 0.35)], fill="#f1f3f4")
        
        # Draw code lines
        for i in range(3):
            draw.rectangle([
                (size[0] * 0.15, size[1] * 0.22 + i * size[1] * 0.035),
                (size[0] * 0.85, size[1] * 0.24 + i * size[1] * 0.035)
            ], fill=colors["accent"] if i == 1 else colors["primary"])
        
        # Draw content sections
        for i in range(3):
            section_y = size[1] * 0.4 + i * size[1] * 0.15
            
            # Section title with code symbol
            draw.rectangle([(size[0] * 0.1, section_y), (size[0] * 0.4, section_y + size[1] * 0.03)], fill=colors["primary"])
            
            # Content with indentation like code
            for j in range(3):
                draw.rectangle([
                    (size[0] * 0.15, section_y + size[1] * 0.05 + j * size[1] * 0.025),
                    (size[0] * 0.85, section_y + size[1] * 0.065 + j * size[1] * 0.025)
                ], fill="#eeeeee")
    
    elif colors["layout"] == "formal":
        # Draw centered header
        draw.rectangle([(0, 0), (size[0], size[1] * 0.2)], fill="#f5f5f5")
        
        # Draw name line (centered)
        draw.rectangle([(size[0] * 0.2, size[1] * 0.05), (size[0] * 0.8, size[1] * 0.08)], fill=colors["primary"])
        
        # Draw formal dividers
        draw.rectangle([(size[0] * 0.3, size[1] * 0.2), (size[0] * 0.7, size[1] * 0.205)], fill=colors["accent"])
        
        # Draw content in an academic style
        for i in range(3):
            section_y = size[1] * 0.25 + i * size[1] * 0.18
            
            # Section title (centered)
            draw.rectangle([(size[0] * 0.3, section_y), (size[0] * 0.7, section_y + size[1] * 0.03)], fill=colors["primary"])
            draw.rectangle([(size[0] * 0.4, section_y + size[1] * 0.035), (size[0] * 0.6, section_y + size[1] * 0.038)], fill=colors["accent"])
            
            # Content with indentation
            for j in range(4):
                draw.rectangle([
                    (size[0] * 0.15, section_y + size[1] * 0.06 + j * size[1] * 0.022),
                    (size[0] * 0.85, section_y + size[1] * 0.075 + j * size[1] * 0.022)
                ], fill="#eeeeee")
    
    elif colors["layout"] == "dense":
        # Draw compact header
        draw.rectangle([(0, 0), (size[0], size[1] * 0.12)], fill=colors["primary"])
        
        # Draw name and contact side by side
        draw.rectangle([(size[0] * 0.05, size[1] * 0.03), (size[0] * 0.6, size[1] * 0.06)], fill="white")
        draw.rectangle([(size[0] * 0.65, size[1] * 0.03), (size[0] * 0.95, size[1] * 0.06)], fill="white")
        
        # Draw dense content with more sections
        section_heights = [0.08, 0.07, 0.1, 0.07, 0.08, 0.1]
        current_y = size[1] * 0.14
        
        for height in section_heights:
            # Section title
            draw.rectangle([(size[0] * 0.05, current_y), (size[0] * 0.5, current_y + size[1] * 0.02)], fill=colors["accent"])
            
            # Dense content
            line_height = size[1] * 0.015
            spacing = size[1] * 0.02
            num_lines = int((height * size[1] - size[1] * 0.03) / (line_height + spacing * 0.5))
            
            for j in range(num_lines):
                draw.rectangle([
                    (size[0] * 0.05, current_y + size[1] * 0.03 + j * (line_height + spacing * 0.5)),
                    (size[0] * 0.95, current_y + size[1] * 0.03 + j * (line_height + spacing * 0.5) + line_height)
                ], fill="#eeeeee")
            
            current_y += size[1] * height
    
    elif colors["layout"] == "statement":
        # Draw statement header with accent line
        draw.rectangle([(0, 0), (size[0], size[1] * 0.25)], fill="white")
        draw.rectangle([(0, 0), (size[0] * 0.03, size[1] * 0.25)], fill=colors["accent"])
        
        # Draw bold name
        draw.rectangle([(size[0] * 0.08, size[1] * 0.05), (size[0] * 0.7, size[1] * 0.1)], fill="black")
        draw.rectangle([(size[0] * 0.08, size[1] * 0.12), (size[0] * 0.5, size[1] * 0.14)], fill=colors["accent"])
        
        # Draw content with timeline style dots
        for i in range(3):
            section_y = size[1] * 0.3 + i * size[1] * 0.2
            
            # Section title with underline
            draw.rectangle([(size[0] * 0.08, section_y), (size[0] * 0.4, section_y + size[1] * 0.03)], fill="black")
            draw.rectangle([(size[0] * 0.08, section_y + size[1] * 0.035), (size[0] * 0.15, section_y + size[1] * 0.04)], fill=colors["accent"])
            
            # Timeline dot
            dot_y = section_y + size[1] * 0.08
            draw.ellipse([(size[0] * 0.08, dot_y), (size[0] * 0.1, dot_y + size[1] * 0.02)], fill=colors["accent"])
            
            # Content line next to dot
            draw.rectangle([
                (size[0] * 0.12, dot_y),
                (size[0] * 0.9, dot_y + size[1] * 0.02)
            ], fill="#eeeeee")
            
            # Detail lines
            for j in range(2):
                draw.rectangle([
                    (size[0] * 0.12, dot_y + size[1] * 0.03 + j * size[1] * 0.02), 
                    (size[0] * 0.8, dot_y + size[1] * 0.04 + j * size[1] * 0.02)
                ], fill="#dddddd")
    
    elif colors["layout"] == "modern":
        # Draw modern header with gradient effect
        draw.rectangle([(0, 0), (size[0], size[1] * 0.2)], fill=colors["primary"])
        draw.rectangle([(0, size[1] * 0.2), (size[0], size[1] * 0.22)], fill=colors["accent"])
        
        # Draw name and title
        draw.rectangle([(size[0] * 0.1, size[1] * 0.05), (size[0] * 0.9, size[1] * 0.09)], fill="white")
        draw.rectangle([(size[0] * 0.1, size[1] * 0.11), (size[0] * 0.5, size[1] * 0.13)], fill="white")
        
        # Draw content in a modern layout
        left_col_width = size[0] * 0.55
        right_col_width = size[0] * 0.3
        
        # Left column content
        for i in range(3):
            section_y = size[1] * 0.25 + i * size[1] * 0.15
            
            # Section title with accent bar
            draw.rectangle([(size[0] * 0.1, section_y), (size[0] * 0.1 + left_col_width * 0.8, section_y + size[1] * 0.03)], fill=colors["primary"])
            draw.rectangle([(size[0] * 0.1, section_y), (size[0] * 0.1 + size[0] * 0.02, section_y + size[1] * 0.03)], fill=colors["accent"])
            
            # Content lines
            for j in range(3):
                draw.rectangle([
                    (size[0] * 0.1, section_y + size[1] * 0.05 + j * size[1] * 0.02),
                    (size[0] * 0.1 + left_col_width * 0.9, section_y + size[1] * 0.06 + j * size[1] * 0.02)
                ], fill="#eeeeee")
        
        # Right column skills/bars
        right_col_x = size[0] * 0.1 + left_col_width + size[0] * 0.05
        for i in range(5):
            skill_y = size[1] * 0.3 + i * size[1] * 0.07
            
            # Skill name
            draw.rectangle([(right_col_x, skill_y), (right_col_x + right_col_width * 0.9, skill_y + size[1] * 0.02)], fill="#dddddd")
            
            # Skill bar
            draw.rectangle([
                (right_col_x, skill_y + size[1] * 0.03),
                (right_col_x + right_col_width * 0.9, skill_y + size[1] * 0.045)
            ], fill="#eeeeee")
            
            # Skill level
            fill_width = right_col_width * 0.9 * (0.3 + (i % 3) * 0.2)
            draw.rectangle([
                (right_col_x, skill_y + size[1] * 0.03),
                (right_col_x + fill_width, skill_y + size[1] * 0.045)
            ], fill=colors["accent"])
    
    else:  # Fallback to simple layout
        # Draw header
        draw.rectangle([(0, 0), (size[0], size[1] * 0.2)], fill=colors["primary"])
        
        # Draw content lines
        for i in range(8):
            y_pos = size[1] * 0.25 + i * size[1] * 0.08
            draw.rectangle([(size[0] * 0.1, y_pos), (size[0] * 0.9, y_pos + size[1] * 0.03)], fill="#dddddd")
    
    # Save the thumbnail
    output_path = f"static/images/templates/{template_name}.jpg"
    img.save(output_path, quality=95)
    print(f"Generated thumbnail: {output_path}")

# Generate thumbnails for all templates
for template_name, colors in templates.items():
    create_thumbnail(template_name, colors)

print("All thumbnails generated successfully!")
