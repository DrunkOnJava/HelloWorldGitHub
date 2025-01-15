# PED Knowledge Base

A comprehensive web-based knowledge base for performance enhancement information, providing detailed compound profiles, protocols, and safety guidelines.

## Overview

The PED Knowledge Base is a modular, component-based website built with HTML, Tailwind CSS, and JavaScript. It provides evidence-based information about performance enhancement compounds, protocols, and best practices for safety and effectiveness.

## Directory Structure

```
.
├── components/           # Reusable UI components
│   ├── navigation.html  # Main navigation bar
│   ├── hero.html       # Hero section
│   ├── categories.html # Main category grid
│   ├── quick-access.html # Quick access links
│   └── footer.html     # Footer component
├── compounds/           # Compound-specific pages
│   ├── index.html      # Compounds database main page
│   └── testosterone.html # Example compound page
├── templates/           # Page templates
│   └── compound.html   # Template for compound pages
├── index.html          # Main entry point
└── sitemap.md          # Site structure documentation
```

## Setup and Installation

1. **Prerequisites**

   - Modern web browser
   - Python 3.x (for local development server)

2. **Local Development**

   ```bash
   # Start local development server
   python3 -m http.server 8080
   ```

   Then visit `http://localhost:8080` in your browser.

3. **Production Deployment**
   - Replace CDN Tailwind CSS with a production build
   - Set up proper web server (nginx/Apache)
   - Configure proper URL routing

## Development Guidelines

### Component Structure

Components are designed to be modular and reusable. Each component follows these principles:

- Self-contained HTML structure
- Tailwind CSS for styling
- Clear semantic markup
- Accessibility considerations

### Adding New Components

1. Create component file in `/components` directory
2. Follow existing component patterns
3. Update main `index.html` to include new component
4. Test in isolation and integrated

### Creating Compound Pages

1. Copy `/templates/compound.html` as base
2. Update content sections:
   - Overview
   - Dosage information
   - Effects and benefits
   - Side effects
   - PCT requirements
   - Studies and research

### Styling Guidelines

- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
- Maintain consistent color scheme:
  - Primary: Blue (#007bff)
  - Secondary: Gray (#6c757d)
  - Success: Green (#28a745)
  - Warning: Yellow (#ffc107)
  - Danger: Red (#dc3545)

## Component Documentation

### Navigation Component

- Location: `/components/navigation.html`
- Features:
  - Responsive navigation bar
  - Search functionality
  - Brand logo

### Hero Component

- Location: `/components/hero.html`
- Features:
  - Main headline
  - Call-to-action buttons
  - Descriptive text

### Categories Component

- Location: `/components/categories.html`
- Features:
  - Grid layout
  - Category cards
  - Icon integration

### Quick Access Component

- Location: `/components/quick-access.html`
- Features:
  - Popular compounds
  - Latest research
  - Quick links

### Footer Component

- Location: `/components/footer.html`
- Features:
  - Site sections
  - Legal links
  - Copyright information

## Contributing

### Adding New Content

1. Follow appropriate template
2. Ensure all content is evidence-based
3. Include references where applicable
4. Follow formatting guidelines
5. Test all links and functionality

### Code Style

- Use 2 spaces for indentation
- Keep files under 300 lines
- Comment complex functionality
- Maintain semantic HTML structure

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is intended for educational purposes only. All content must be used in accordance with applicable laws and regulations.

## Contact

For questions, suggestions, or contributions, please open an issue in the repository.
