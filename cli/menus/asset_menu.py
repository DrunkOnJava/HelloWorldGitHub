"""Asset management menu implementation."""

from typing import List
from ..models.menu_item import MenuItem
from ..project.asset_manager import AssetManager

class AssetMenu:
    """Menu interface for asset management tools."""

    def __init__(self, ui, project_manager):
        """Initialize asset menu.

        Args:
            ui: UI instance for terminal interaction
            project_manager: Project manager instance
        """
        self.ui = ui
        self.project_manager = project_manager
        self.asset_manager = AssetManager(project_manager.project_path)

    def get_menu_items(self) -> List[MenuItem]:
        """Get asset management menu items.

        Returns:
            List[MenuItem]: List of menu items
        """
        return [
            MenuItem(
                key="scan",
                label="Scan Assets",
                description="Scan project for image and font assets",
                handler=self.scan_assets
            ),
            MenuItem(
                key="optimize_images",
                label="Optimize Images",
                description="Optimize project images while maintaining quality",
                handler=self.optimize_images
            ),
            MenuItem(
                key="convert_images",
                label="Convert Images",
                description="Convert images to different formats (WebP, AVIF)",
                handler=self.convert_images
            ),
            MenuItem(
                key="responsive_images",
                label="Generate Responsive Images",
                description="Create responsive image variants",
                handler=self.generate_responsive_images
            ),
            MenuItem(
                key="font_subset",
                label="Subset Fonts",
                description="Create optimized font subsets",
                handler=self.subset_fonts
            ),
            MenuItem(
                key="optimize_fonts",
                label="Optimize Font Loading",
                description="Generate optimized font variants for different browsers",
                handler=self.optimize_fonts
            ),
            MenuItem(
                key="analyze",
                label="Analyze Assets",
                description="Get detailed metadata about project assets",
                handler=self.analyze_assets
            )
        ]

    def scan_assets(self) -> bool:
        """Scan project for assets and display results."""
        self.ui.print_status("Scanning project for assets...")
        assets = self.asset_manager.scan_project_assets()

        self.ui.print_header("Asset Scan Results", "Found assets in project")
        self.ui.print_info(f"Images found: {len(assets['images'])}")
        self.ui.print_info(f"Fonts found: {len(assets['fonts'])}")

        if assets['images']:
            self.ui.print_header("Images", "List of image files")
            for image in assets['images']:
                self.ui.print_info(f"- {image}")

        if assets['fonts']:
            self.ui.print_header("Fonts", "List of font files")
            for font in assets['fonts']:
                self.ui.print_info(f"- {font}")

        return True

    def optimize_images(self) -> bool:
        """Optimize all images in the project."""
        assets = self.asset_manager.scan_project_assets()
        if not assets['images']:
            self.ui.print_warning("No images found in project")
            return False

        self.ui.print_status("Optimizing images...")
        optimized_count = 0
        for image in assets['images']:
            if self.asset_manager.optimize_image(image):
                optimized_count += 1
                self.ui.print_success(f"Optimized: {image}")
            else:
                self.ui.print_info(f"Skipped: {image} (already optimized)")

        self.ui.print_success(f"Optimized {optimized_count} images")
        return True

    def convert_images(self) -> bool:
        """Convert images to different formats."""
        assets = self.asset_manager.scan_project_assets()
        if not assets['images']:
            self.ui.print_warning("No images found in project")
            return False

        formats = ['WEBP', 'AVIF']
        format_choice = self.ui.get_choice("Select target format", formats)

        self.ui.print_status(f"Converting images to {format_choice}...")
        converted_count = 0
        for image in assets['images']:
            if new_path := self.asset_manager.convert_image_format(image, format_choice):
                converted_count += 1
                self.ui.print_success(f"Converted: {new_path}")
            else:
                self.ui.print_error(f"Failed to convert: {image}")

        self.ui.print_success(f"Converted {converted_count} images to {format_choice}")
        return True

    def generate_responsive_images(self) -> bool:
        """Generate responsive image variants."""
        assets = self.asset_manager.scan_project_assets()
        if not assets['images']:
            self.ui.print_warning("No images found in project")
            return False

        widths = [320, 640, 1024, 1920]  # Common responsive breakpoints

        self.ui.print_status("Generating responsive images...")
        for image in assets['images']:
            results = self.asset_manager.generate_responsive_images(image, widths)
            if results:
                self.ui.print_success(f"Generated variants for: {image}")
                for width, path in results.items():
                    self.ui.print_info(f"- {width}px: {path}")
            else:
                self.ui.print_error(f"Failed to generate variants for: {image}")

        return True

    def subset_fonts(self) -> bool:
        """Create optimized font subsets."""
        assets = self.asset_manager.scan_project_assets()
        if not assets['fonts']:
            self.ui.print_warning("No fonts found in project")
            return False

        text = self.ui.get_input("Enter text for font subset (or leave empty for basic Latin)", required=False)
        if not text:
            text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        self.ui.print_status("Creating font subsets...")
        for font in assets['fonts']:
            if subset_path := self.asset_manager.subset_font(font, text):
                self.ui.print_success(f"Created subset: {subset_path}")
            else:
                self.ui.print_error(f"Failed to create subset for: {font}")

        return True

    def optimize_fonts(self) -> bool:
        """Generate optimized font variants."""
        assets = self.asset_manager.scan_project_assets()
        if not assets['fonts']:
            self.ui.print_warning("No fonts found in project")
            return False

        self.ui.print_status("Optimizing fonts for web...")
        for font in assets['fonts']:
            results = self.asset_manager.optimize_font_loading(font)
            if results:
                self.ui.print_success(f"Generated variants for: {font}")
                for format_type, path in results.items():
                    self.ui.print_info(f"- {format_type}: {path}")
            else:
                self.ui.print_error(f"Failed to generate variants for: {font}")

        return True

    def analyze_assets(self) -> bool:
        """Display detailed asset metadata."""
        assets = self.asset_manager.scan_project_assets()

        if assets['images']:
            self.ui.print_header("Image Analysis", "Detailed image metadata")
            for image in assets['images']:
                metadata = self.asset_manager.get_image_metadata(image)
                if metadata:
                    self.ui.print_info(f"\nImage: {metadata['path']}")
                    self.ui.print_info(f"Format: {metadata['format']}")
                    self.ui.print_info(f"Mode: {metadata['mode']}")
                    self.ui.print_info(f"Dimensions: {metadata['width']}x{metadata['height']}")
                    self.ui.print_info(f"Size: {metadata['size_bytes'] / 1024:.1f}KB")

        if assets['fonts']:
            self.ui.print_header("Font Analysis", "Detailed font metadata")
            for font in assets['fonts']:
                metadata = self.asset_manager.get_font_metadata(font)
                if metadata:
                    self.ui.print_info(f"\nFont: {metadata['path']}")
                    self.ui.print_info(f"Format: {metadata['format']}")
                    self.ui.print_info(f"Family: {metadata['family_name']}")
                    self.ui.print_info(f"Full Name: {metadata['full_name']}")
                    self.ui.print_info(f"Version: {metadata['version']}")
                    self.ui.print_info(f"Size: {metadata['size_bytes'] / 1024:.1f}KB")

        return True
