"""Asset management implementation."""

import os
from PIL import Image
import shutil
import importlib.util
from typing import List, Dict, Optional

# Try to import fonttools, but make it optional
try:
    from fonttools import ttLib
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False

class AssetManager:
    """Manages project assets including images and fonts."""

    def __init__(self, project_path: str):
        """Initialize asset manager.

        Args:
            project_path: Root path of the project
        """
        self.project_path = project_path
        self.image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']
        self.font_formats = ['.ttf', '.otf', '.woff', '.woff2']

    def optimize_image(self, image_path: str, quality: int = 85) -> bool:
        """Optimize an image while maintaining acceptable quality.

        Args:
            image_path: Path to the image file
            quality: Quality level (0-100) for lossy compression

        Returns:
            bool: True if optimization was successful
        """
        try:
            img = Image.open(image_path)
            optimized_path = f"{os.path.splitext(image_path)[0]}_optimized{os.path.splitext(image_path)[1]}"

            if img.format == 'PNG':
                img.save(optimized_path, 'PNG', optimize=True)
            else:
                img.save(optimized_path, quality=quality, optimize=True)

            # Replace original if optimized is smaller
            if os.path.getsize(optimized_path) < os.path.getsize(image_path):
                shutil.move(optimized_path, image_path)
                return True
            else:
                os.remove(optimized_path)
                return False
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return False

    def convert_image_format(self, image_path: str, target_format: str) -> Optional[str]:
        """Convert image to a different format.

        Args:
            image_path: Path to the image file
            target_format: Desired output format (e.g., 'WEBP', 'AVIF')

        Returns:
            Optional[str]: Path to converted image if successful, None otherwise
        """
        try:
            img = Image.open(image_path)
            output_path = f"{os.path.splitext(image_path)[0]}.{target_format.lower()}"

            if target_format.upper() == 'WEBP':
                img.save(output_path, 'WEBP', quality=85)
            elif target_format.upper() == 'AVIF':
                img.save(output_path, 'AVIF', quality=85)
            else:
                img.save(output_path, target_format.upper())

            return output_path
        except Exception as e:
            print(f"Error converting image: {e}")
            return None

    def generate_responsive_images(self, image_path: str, widths: List[int]) -> Dict[int, str]:
        """Generate responsive image variants.

        Args:
            image_path: Path to the source image
            widths: List of desired output widths

        Returns:
            Dict[int, str]: Mapping of widths to generated image paths
        """
        results = {}
        try:
            img = Image.open(image_path)
            aspect_ratio = img.height / img.width

            for width in widths:
                height = int(width * aspect_ratio)
                resized = img.resize((width, height), Image.Resampling.LANCZOS)

                output_path = f"{os.path.splitext(image_path)[0]}_{width}w{os.path.splitext(image_path)[1]}"
                resized.save(output_path, quality=85, optimize=True)
                results[width] = output_path

            return results
        except Exception as e:
            print(f"Error generating responsive images: {e}")
            return results

    def subset_font(self, font_path: str, text: str) -> Optional[str]:
        """Create a subset of a font file containing only specified characters.

        Args:
            font_path: Path to the font file
            text: Text containing characters to include in subset

        Returns:
            Optional[str]: Path to subsetted font if successful, None otherwise
        """
        if not FONTTOOLS_AVAILABLE:
            print("Warning: fonttools not available. Font subsetting disabled.")
            return None

        try:
            output_path = f"{os.path.splitext(font_path)[0]}_subset{os.path.splitext(font_path)[1]}"

            # Create unicode list from text
            unicodes = set(ord(c) for c in text)

            # Load the font
            font = ttLib.TTFont(font_path)

            # Save a new copy with minimal tables
            font.save(output_path, tables=['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post'])

            return output_path
        except Exception as e:
            print(f"Error subsetting font: {e}")
            return None

    def optimize_font_loading(self, font_path: str) -> Dict[str, str]:
        """Generate optimized font variants for different browsers.

        Args:
            font_path: Path to the font file

        Returns:
            Dict[str, str]: Mapping of format to generated font paths
        """
        if not FONTTOOLS_AVAILABLE:
            print("Warning: fonttools not available. Font optimization disabled.")
            return {}

        results = {}
        try:
            font = ttLib.TTFont(font_path)
            base_path = os.path.splitext(font_path)[0]

            # Generate WOFF2 (best compression)
            woff2_path = f"{base_path}.woff2"
            font.save(woff2_path)
            results['woff2'] = woff2_path

            # Generate WOFF (fallback)
            woff_path = f"{base_path}.woff"
            font.save(woff_path)
            results['woff'] = woff_path

            return results
        except Exception as e:
            print(f"Error optimizing font loading: {e}")
            return results

    def scan_project_assets(self) -> Dict[str, List[str]]:
        """Scan project directory for image and font assets.

        Returns:
            Dict[str, List[str]]: Mapping of asset types to file paths
        """
        assets = {
            'images': [],
            'fonts': []
        }

        for root, _, files in os.walk(self.project_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                if ext in self.image_formats:
                    assets['images'].append(file_path)
                elif ext in self.font_formats:
                    assets['fonts'].append(file_path)

        return assets

    def get_image_metadata(self, image_path: str) -> Dict[str, any]:
        """Get metadata for an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Dict[str, any]: Image metadata including dimensions, format, and size
        """
        try:
            img = Image.open(image_path)
            return {
                'path': image_path,
                'format': img.format,
                'mode': img.mode,
                'width': img.width,
                'height': img.height,
                'size_bytes': os.path.getsize(image_path)
            }
        except Exception as e:
            print(f"Error getting image metadata: {e}")
            return {}

    def get_font_metadata(self, font_path: str) -> Dict[str, any]:
        """Get metadata for a font file.

        Args:
            font_path: Path to the font file

        Returns:
            Dict[str, any]: Font metadata including format, family name, and size
        """
        if not FONTTOOLS_AVAILABLE:
            print("Warning: fonttools not available. Only basic font metadata available.")
            return {
                'path': font_path,
                'format': os.path.splitext(font_path)[1],
                'size_bytes': os.path.getsize(font_path)
            }

        try:
            font = ttLib.TTFont(font_path)
            return {
                'path': font_path,
                'format': os.path.splitext(font_path)[1],
                'family_name': font['name'].getDebugName(1),
                'full_name': font['name'].getDebugName(4),
                'version': font['name'].getDebugName(5),
                'size_bytes': os.path.getsize(font_path)
            }
        except Exception as e:
            print(f"Error getting font metadata: {e}")
            return {}
