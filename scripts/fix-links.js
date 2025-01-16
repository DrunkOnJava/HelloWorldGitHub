import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname, relative } from 'path';
import { fileURLToPath } from 'url';

// For colored console output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m'
};

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Track broken and fixed links
const brokenLinks = new Map(); // source -> [broken links]
const fixedLinks = new Map();  // source -> [fixed links]

// Directories that should have index.html files
const requiredPaths = [
  'resources/calculators',
  'resources/research',
  'guides/success-stories',
  'guides/compounds',
  'legal/disclaimer',
  'legal/terms',
  'health',
  'training',
  'nutrition',
  'protocols',
  'compounds'
];

const BASE_PATH = '';

// Map of special routes that should be handled differently
const specialRoutes = {
  'pages/compounds/index.html': 'compounds/index.html',
  '/pages/compounds/index.html': 'compounds/index.html',
  '/compounds/index.html': 'compounds/index.html',
  '/compounds/database': 'compounds/index.html',
  '/compounds': 'compounds/index.html',
  'pages/compounds/testosterone/testosterone.html': 'compounds/testosterone/index.html',
  'pages/compounds/nandrolone/nandrolone.html': 'compounds/nandrolone/index.html',
  'pages/compounds/trenbolone/trenbolone.html': 'compounds/trenbolone/index.html',
  '/guides/first-cycle': 'guides/first-cycle/index.html',
  '/guides/success-stories': 'guides/success-stories/index.html',
  '/guides/compounds': 'guides/compounds/index.html',
  '/safety/bloodwork': 'safety/bloodwork/index.html',
  '/safety/pct': 'safety/pct/index.html',
  '/safety/side-effects': 'safety/side-effects/index.html',
  '/resources/research': 'resources/research/index.html',
  '/legal/disclaimer': 'legal/disclaimer/index.html',
  '/legal/terms': 'legal/terms/index.html'
};

// Function to convert file system path to URL path
const toUrlPath = (path) => {
    return path.replace(/\\/g, '/');
};

// Function to handle Astro routes
const handleAstroRoute = (path) => {
    // Convert Astro routes to HTML paths
    if (path.endsWith('.astro')) {
        return path.replace('.astro', '/index.html');
    }
    // If path doesn't end in .html or /, assume it needs index.html
    if (!path.endsWith('.html') && !path.endsWith('/')) {
        return `${path}/index.html`;
    }
    // If path ends with /, append index.html
    if (path.endsWith('/')) {
        return `${path}index.html`;
    }
    return path;
};

// Function to get the correct path with base and validate it exists
const getPath = (path, sourceFile = '') => {
    // Remove query parameters and hashes
    path = path.split('?')[0].split('#')[0];

    // Handle special routes first
    if (specialRoutes[path]) {
        path = specialRoutes[path];
    }

    // Handle Astro routes
    path = handleAstroRoute(path);

    // Remove leading slash and clean path
    const cleanPath = path.replace(/^\/+/, '');

    // Convert the path to a file system path and URL path
    const fsPath = join(process.cwd(), cleanPath);
    const urlPath = toUrlPath(cleanPath);

    // Check if path exists
    if (!existsSync(fsPath)) {
        // Track broken link
        const links = brokenLinks.get(sourceFile) || [];
        links.push(urlPath);
        brokenLinks.set(sourceFile, links);

        // Create missing directory and index.html if needed
        if (requiredPaths.includes(cleanPath.split('/')[0])) {
            const dir = dirname(fsPath);
            if (!existsSync(dir)) {
                mkdirSync(dir, { recursive: true });
                console.log(`${colors.green}Created directory:${colors.reset} ${dir}`);
            }

            // If path doesn't end in .html, assume it needs an index.html
            const filePath = fsPath.endsWith('.html') ? fsPath : join(fsPath, 'index.html');
            if (!existsSync(filePath)) {
                const title = cleanPath.split('/').pop().replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                writeFileSync(filePath, createIndexTemplate(title));
                console.log(`${colors.green}Created file:${colors.reset} ${filePath}`);

                // Track fixed link
                const fixed = fixedLinks.get(sourceFile) || [];
                fixed.push(fullPath);
                fixedLinks.set(sourceFile, fixed);
            }
        }
    }

    return urlPath;
};

// Basic template for index pages
const createIndexTemplate = (title) => `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">${title}</h1>
        <p class="text-gray-600">Content coming soon...</p>
    </div>
</body>
</html>
`;

// Create missing directories and index files
requiredPaths.forEach(dirPath => {
    const fullPath = join(process.cwd(), dirPath);

    // Create directory if it doesn't exist
    if (!existsSync(fullPath)) {
        mkdirSync(fullPath, { recursive: true });
    }

    // Create index.html if it doesn't exist
    const indexPath = join(fullPath, 'index.html');
    if (!existsSync(indexPath)) {
        const title = dirPath.split('/').pop().charAt(0).toUpperCase() +
                     dirPath.split('/').pop().slice(1);
        writeFileSync(indexPath, createIndexTemplate(title));
    }
});

// Function to normalize path for comparison
const normalizePath = (path) => {
    // Remove leading slash and normalize to forward slashes
    return path.replace(/^\/+/, '').replace(/\\/g, '/');
};

// Function to fix links in a file
const fixLinksInFile = (filePath) => {
    if (!existsSync(filePath)) return;

    let content = readFileSync(filePath, 'utf8');

    // Fix various link patterns
    content = content
        // Fix HelloWorldGitHubcompounds issue
        .replace(/\/HelloWorldGitHub\/HelloWorldGitHubcompounds/g, '/compounds')
        // Fix compound links with pages prefix
        .replace(/href="(?:\/)?(?:pages\/)?compounds/g, (match) => `href="compounds`)
        // Handle special routes
        .replace(/href="([^"]*)"([^>]*>Compound\s+Database)/g, (match, p1, p2) => `href="${getPath('compounds')}"${p2}`)
        .replace(/href="([^"]*)"([^>]*>Compound\s+Guide)/g, (match, p1, p2) => `href="${getPath('compounds')}"${p2}`)
        // Replace placeholder # links with appropriate paths
        .replace(/href="#"([^>]*>Blood\s*Work)/g, (match, p1) => `href="${getPath('safety/bloodwork')}"${p1}`)
        .replace(/href="#"([^>]*>Calculators)/g, (match, p1) => `href="${getPath('resources/calculators')}"${p1}`)
        .replace(/href="#"([^>]*>Side\s*Effects)/g, (match, p1) => `href="${getPath('safety/side-effects')}"${p1}`)
        .replace(/href="#"([^>]*>Success\s*Stories)/g, (match, p1) => `href="${getPath('guides/success-stories')}"${p1}`)
        .replace(/href="#"([^>]*>Research)/g, (match, p1) => `href="${getPath('resources/research')}"${p1}`)
        .replace(/href="#"([^>]*>Disclaimer)/g, (match, p1) => `href="${getPath('legal/disclaimer')}"${p1}`)
        .replace(/href="#"([^>]*>Terms)/g, (match, p1) => `href="${getPath('legal/terms')}"${p1}`)
        .replace(/href="#"([^>]*>Compound\s*Guide)/g, (match, p1) => `href="${getPath('guides/compounds')}"${p1}`)
        // Preserve template variables
        .replace(/href="#\${([^}]+)}"/g, (match) => {
            // Keep the original template syntax
            return match;
        })
        // Fix triple-nested HelloWorldGitHub paths
        .replace(/\/HelloWorldGitHub\/HelloWorldGitHub\/HelloWorldGitHub\//g, `${BASE_PATH}/`)
        // Fix double-nested HelloWorldGitHub paths
        .replace(/\/HelloWorldGitHub\/HelloWorldGitHub\//g, `${BASE_PATH}/`)
        // Fix compound-specific routes
        .replace(/href="([^"]+)\/compounds\/([^"]+)\.html"/g, (match, prefix, compound) => {
            return `href="${getPath(`compounds/${compound}`)}"`;
        })
        // Fix root links (but not external links)
        .replace(/href="(?:\/HelloWorldGitHub)?\/([^"]+)"/g, (match, path) => {
            // Don't modify external links
            if (path.startsWith('http://') || path.startsWith('https://')) {
                return match;
            }
            return `href="${path}"`;
        })
        // Fix Astro routes
        .replace(/href="([^"]+)\.html"/g, (match, p1) => {
            const normalizedPath = normalizePath(p1);
            // Check if the path or its variations exist in specialRoutes
            const routeKey = Object.keys(specialRoutes).find(key =>
                normalizePath(key) === normalizedPath ||
                normalizePath(key) === normalizedPath + '/index'
            );
            return routeKey ? `href="${getPath(specialRoutes[routeKey])}"` : match;
        });

    writeFileSync(filePath, content);
};

// Get all HTML files recursively
const getAllFiles = (dir) => {
    let results = [];
    const list = readdirSync(dir);

    list.forEach(file => {
        const filePath = join(dir, file);
        const stat = statSync(filePath);

        if (stat.isDirectory()) {
            results = results.concat(getAllFiles(filePath));
        } else if (file.endsWith('.html')) {
            results.push(filePath);
        }
    });

    return results;
};

// Fix links in all HTML files
const htmlFiles = getAllFiles(process.cwd());
htmlFiles.forEach(fixLinksInFile);

// Print report
console.log('\n=== Link Validation Report ===\n');

if (brokenLinks.size > 0) {
    console.log(`${colors.yellow}Found broken links in ${brokenLinks.size} files:${colors.reset}`);
    for (const [source, links] of brokenLinks) {
        console.log(`\n${colors.blue}${relative(process.cwd(), source)}:${colors.reset}`);
        links.forEach(link => {
            const fixed = fixedLinks.get(source)?.includes(link);
            console.log(`  ${fixed ? colors.green + '✓' : colors.red + '✗'} ${link}${colors.reset}`);
        });
    }
} else {
    console.log(`${colors.green}No broken links found!${colors.reset}`);
}

console.log('\nLink fixing complete!');
