# PED Knowledge Base

A comprehensive web-based knowledge base for performance enhancement information, providing detailed compound profiles, protocols, and safety guidelines.

## Overview

The PED Knowledge Base is a modular, component-based website built with HTML, Tailwind CSS, and JavaScript. It provides evidence-based information about performance enhancement compounds, protocols, and best practices for safety and effectiveness.

## Directory Structure

```
.
├── pages/              # Page-specific content
│   ├── home/          # Home page components
│   │   ├── navigation.html
│   │   ├── hero.html
│   │   ├── categories.html
│   │   ├── quick-access.html
│   │   └── footer.html
│   └── compounds/     # Compound-specific content
│       ├── index.html # Compounds database main page
│       ├── testosterone/
│       │   ├── testosterone.html
│       │   ├── components/
│       │   │   ├── breadcrumb.html
│       │   │   ├── table-of-contents.html
│       │   │   ├── overview.html
│       │   │   ├── dosage-calculator.html
│       │   │   ├── effects.html
│       │   │   ├── side-effects.html
│       │   │   ├── pct.html
│       │   │   └── studies.html
│       │   ├── data/
│       │   │   └── compound-data.js
│       │   └── js/
│       │       └── main.js
│       ├── nandrolone/  # Similar structure as testosterone
│       ├── trenbolone/  # Similar structure as testosterone
│       └── [compound-name]/  # Template for new compounds
├── templates/         # Page templates
│   └── compounds/
│       └── compound.html
├── index.html        # Main entry point
└── sitemap.md        # Site structure documentation
```

## Recent Updates

### Component Loading Changes

We've improved the site's reliability and performance by implementing direct component embedding instead of dynamic loading. This change:

1. Eliminates CORS issues during local development
2. Improves page load performance
3. Simplifies debugging
4. Ensures consistent rendering across all environments

Key changes made:

- Removed dynamic component loading scripts
- Embedded navigation and footer directly in HTML files
- Updated relative paths for proper linking
- Fixed compound database link functionality

Example of the new approach:

```html
<!-- Old approach (removed) -->
<div id="navigation"></div>
<script>
  loadComponent("navigation", "path/to/navigation.html");
</script>

<!-- New approach -->
<nav class="bg-gray-900 text-white shadow-lg">
  <!-- Navigation content directly embedded -->
</nav>
```

## Component Integration

### Direct Component Integration

Components are now directly embedded in pages for optimal performance and reliability. This approach:

1. Works seamlessly with local development
2. Reduces dependencies on external scripts
3. Improves page load times
4. Makes debugging easier
5. Ensures consistent behavior across different environments

### Adding New Compounds

To add a new compound to the database, follow these steps:

1. **Create Directory Structure**

   ```bash
   mkdir -p pages/compounds/[compound-name]/{components,data,js}
   ```

2. **Create Required Files**

   ```bash
   # Main compound page
   cp templates/compounds/compound.html pages/compounds/[compound-name]/[compound-name].html

   # Component files
   cd pages/compounds/[compound-name]/components
   touch breadcrumb.html table-of-contents.html overview.html \
         dosage-calculator.html effects.html side-effects.html \
         pct.html studies.html

   # Data and JavaScript
   touch ../data/compound-data.js
   touch ../js/main.js
   ```

3. **Update Compound Page Structure**

   - Edit `[compound-name].html`:

     ```html
     <!DOCTYPE html>
     <html lang="en">
       <head>
         <meta charset="UTF-8" />
         <meta
           name="viewport"
           content="width=device-width, initial-scale=1.0"
         />
         <title>[Compound Name] - PED Knowledge Base</title>
         <script src="https://cdn.tailwindcss.com"></script>
         <link
           rel="stylesheet"
           href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
         />
       </head>
       <body class="bg-gray-50">
         <!-- Navigation -->
         <nav class="bg-gray-900 text-white shadow-lg">
           <!-- Copy navigation content here -->
         </nav>

         <!-- Breadcrumb -->
         <nav class="bg-white border-b" aria-label="Breadcrumb">
           <!-- Update breadcrumb path -->
         </nav>

         <!-- Table of Contents -->
         <div class="table-of-contents">
           <!-- Add section links -->
         </div>

         <!-- Main Content -->
         <main>
           <!-- Include all component sections -->
           <section id="overview">
             <!-- Overview content -->
           </section>

           <section id="dosage">
             <!-- Dosage calculator -->
           </section>

           <!-- Additional sections -->
         </main>

         <!-- Footer -->
         <footer class="bg-gray-900 text-white">
           <!-- Copy footer content here -->
         </footer>
       </body>
     </html>
     ```

4. **Implement Component Files**

   - `breadcrumb.html`: Navigation path
   - `table-of-contents.html`: Quick section navigation
   - `overview.html`: General information, mechanism of action
   - `dosage-calculator.html`: Dosing guidelines and calculator
   - `effects.html`: Primary effects and benefits
   - `side-effects.html`: Potential side effects and mitigation
   - `pct.html`: Post-cycle therapy requirements
   - `studies.html`: Research references and studies

5. **Add Compound Data**

   - In `compound-data.js`:
     ```javascript
     const compoundData = {
       name: "[Compound Name]",
       category: "e.g., Anabolic, SARM, etc.",
       halfLife: "hours",
       detectionTime: "days/weeks",
       anabolicRating: 0,
       androgenicRating: 0,
       dosageRanges: {
         beginner: { min: 0, max: 0, unit: "mg" },
         intermediate: { min: 0, max: 0, unit: "mg" },
         advanced: { min: 0, max: 0, unit: "mg" },
       },
       sideEffects: {
         common: ["effect1", "effect2"],
         uncommon: ["effect3"],
         rare: ["effect4"],
       },
       pctRequirements: {
         required: true,
         protocol: "Standard PCT protocol",
         duration: "4-6 weeks",
       },
       interactions: ["compound1", "compound2"],
       references: ["study1", "study2"],
     };
     ```

6. **Update Compounds Index**

   - Add new compound card to `pages/compounds/index.html`:
     ```html
     <a
       href="[compound-name]/[compound-name].html"
       class="block bg-white rounded-lg border hover:shadow-md transition-shadow"
     >
       <div class="p-6">
         <h2 class="text-xl font-semibold text-gray-900">[Compound Name]</h2>
         <p class="mt-2 text-gray-500">Brief description of the compound</p>
         <div class="mt-4 flex items-center text-blue-600">
           <span>Learn more</span>
           <i class="fas fa-arrow-right ml-2"></i>
         </div>
       </div>
     </a>
     ```

7. **Testing Checklist**

   - [ ] All links work correctly
   - [ ] Responsive design functions on all viewports
   - [ ] Component integration is complete
   - [ ] Calculator functionality works
   - [ ] Navigation paths are correct
   - [ ] Data is properly loaded
   - [ ] Interactive elements function
   - [ ] Cross-browser compatibility
   - [ ] Local development works without CORS issues

### Content Guidelines

1. **Evidence-Based Information**

   - Include references to scientific studies
   - Link to relevant research papers
   - Provide dosage ranges based on clinical data
   - Document side effects with occurrence rates
   - Include confidence levels for each claim
   - Reference specific studies for key points

2. **Formatting**

   - Use consistent heading hierarchy (h1 -> h6)
   - Maintain uniform spacing (8px, 16px, 24px, 32px)
   - Follow color scheme:
     ```css
     :root {
       --primary: #007bff;
       --secondary: #6c757d;
       --success: #28a745;
       --warning: #ffc107;
       --danger: #dc3545;
     }
     ```
   - Implement responsive design patterns
   - Use consistent font sizes and weights

3. **Required Sections**

   - Overview and background
   - Mechanism of action
   - Dosage guidelines
   - Effects and benefits
   - Side effects and risks
   - PCT requirements
   - Drug interactions
   - Research references
   - Safety precautions
   - Legal considerations
   - Contraindications

4. **Interactive Elements**

   - Dosage calculators
   - Side effect probability charts
   - PCT protocol generators
   - Blood work timing calculators
   - Cycle planning tools
   - Progress tracking features

5. **Quality Standards**

   - All content must be evidence-based
   - Include primary sources
   - Regular content reviews
   - Version control for updates
   - Peer review process
   - User feedback integration

## Development Guidelines

### Code Style

1. **HTML**

   - Semantic markup
   - Proper indentation (2 spaces)
   - Descriptive class names
   - Accessibility attributes
   - Valid HTML5

2. **CSS (Tailwind)**

   - Utility-first approach
   - Custom components for reuse
   - Responsive design patterns
   - Dark mode support
   - Performance optimization

3. **JavaScript**
   - ES6+ syntax
   - Modular structure
   - Error handling
   - Type checking
   - Documentation

### Best Practices

1. **Performance**

   - Minimize HTTP requests
   - Optimize images
   - Lazy loading
   - Code splitting
   - Cache management

2. **Security**

   - Input validation
   - XSS prevention
   - CORS handling
   - Content security
   - Error handling

3. **Accessibility**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support
   - Color contrast
   - Focus management

## Live Demo

Visit the live site at: https://drunkonjava.github.io/HelloWorldGitHub/

## Setup and Installation

1. **Prerequisites**

   - Modern web browser
   - Python 3.x (for local development server)
   - GitHub CLI (gh) for deployment

2. **Local Development**

   ```bash
   # Start local development server
   python3 -m http.server 8080
   ```

   Then visit `http://localhost:8080` in your browser.

3. **Production Deployment**
   - The site is deployed using GitHub Pages
   - Deployment is configured from the main branch root directory
   - Changes pushed to main will automatically trigger deployment

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
