"""Compound management functionality."""

import json
import os
from typing import Dict, Any, List, Optional

class CompoundData:
    """Represents a compound with its properties."""
    def __init__(self, name: str, category: str, description: str,
                 anabolic_rating: int, androgenic_rating: int,
                 half_life: str, detection_time: str,
                 dosage_ranges: Dict, side_effects: Dict,
                 pct_requirements: Dict, interactions: List[str],
                 references: List[str]):
        self.name = name
        self.slug = name.lower().replace(' ', '-')
        self.category = category
        self.description = description
        self.anabolicRating = anabolic_rating
        self.androgenicRating = androgenic_rating
        self.halfLife = half_life
        self.detectionTime = detection_time
        self.dosageRanges = dosage_ranges
        self.sideEffects = side_effects
        self.pctRequirements = pct_requirements
        self.interactions = interactions
        self.references = references

    def to_dict(self) -> Dict:
        """Convert compound data to dictionary format."""
        return {
            "name": self.name,
            "slug": self.slug,
            "category": self.category,
            "description": self.description,
            "anabolicRating": self.anabolicRating,
            "androgenicRating": self.androgenicRating,
            "halfLife": self.halfLife,
            "detectionTime": self.detectionTime,
            "dosageRanges": self.dosageRanges,
            "sideEffects": self.sideEffects,
            "pctRequirements": self.pctRequirements,
            "interactions": self.interactions,
            "references": self.references
        }

class CompoundManager:
    """Handles compound-related operations."""
    def __init__(self, ui, npm_manager):
        self.ui = ui
        self.npm_manager = npm_manager
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"
        self.compounds_file = os.path.join(self.project_root, "src/data/compounds.ts")

    def get_compounds(self) -> List[Dict[str, Any]]:
        """Get list of all compounds."""
        try:
            with open(self.compounds_file, 'r') as f:
                content = f.read()

            # Extract compounds array
            compounds_start = content.find('export const compounds: Compound[] = [')
            compounds_end = content.rfind('];')

            if compounds_start == -1 or compounds_end == -1:
                return []

            # Extract compounds array content
            compounds_content = content[compounds_start:compounds_end+1]

            # Convert TypeScript syntax to valid JSON
            compounds_content = compounds_content.replace("export const compounds: Compound[] = ", "")
            compounds_content = compounds_content.replace("'", '"')

            try:
                compounds = json.loads(compounds_content)
                return compounds
            except json.JSONDecodeError:
                return []

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to get compounds: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return []

    def add_compound(self, compound_data: CompoundData) -> bool:
        """Add a new compound to the compounds.ts file."""
        try:
            # Read current compounds file
            with open(self.compounds_file, 'r') as f:
                content = f.read()

            # Parse existing compounds array
            compounds_start = content.find('export const compounds: Compound[] = [')
            compounds_end = content.rfind('];')

            if compounds_start == -1 or compounds_end == -1:
                print(f"\n{self.ui.theme.COLORS['ERROR']}Invalid compounds.ts file structure{self.ui.theme.COLORS['ENDC']}")
                return False

            # Convert compound to TypeScript object string
            new_compound = json.dumps(compound_data.to_dict(), indent=2)
            # Fix JSON to TypeScript syntax
            new_compound = new_compound.replace('"', "'")

            # Insert new compound into array
            updated_content = (
                content[:compounds_end] +
                ('  ' if content[compounds_end-1] != '[' else '') +
                (',' if content[compounds_end-1] != '[' else '') +
                '\n  ' + new_compound +
                '\n' + content[compounds_end:]
            )

            # Write updated content
            with open(self.compounds_file, 'w') as f:
                f.write(updated_content)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully added compound: {compound_data.name}{self.ui.theme.COLORS['ENDC']}")

            # Rebuild project to update UI
            self.npm_manager.run_npm_command('build')

            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to add compound: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def edit_compound(self, compound_name: str, updated_data: CompoundData) -> bool:
        """Edit an existing compound."""
        try:
            compounds = self.get_compounds()

            # Find compound index
            compound_index = -1
            for i, compound in enumerate(compounds):
                if compound['name'].lower() == compound_name.lower():
                    compound_index = i
                    break

            if compound_index == -1:
                print(f"\n{self.ui.theme.COLORS['ERROR']}Compound not found: {compound_name}{self.ui.theme.COLORS['ENDC']}")
                return False

            # Update compound
            compounds[compound_index] = updated_data.to_dict()

            # Convert to TypeScript
            compounds_str = json.dumps(compounds, indent=2).replace('"', "'")

            # Update file
            with open(self.compounds_file, 'r') as f:
                content = f.read()

            compounds_start = content.find('export const compounds: Compound[] = [')
            compounds_end = content.rfind('];')

            updated_content = (
                content[:compounds_start] +
                f'export const compounds: Compound[] = {compounds_str}' +
                content[compounds_end+1:]
            )

            with open(self.compounds_file, 'w') as f:
                f.write(updated_content)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully updated compound: {compound_name}{self.ui.theme.COLORS['ENDC']}")

            # Rebuild project
            self.npm_manager.run_npm_command('build')

            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to edit compound: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def validate_compound_data(self, compound: Dict[str, Any]) -> List[str]:
        """Validate compound data structure."""
        errors = []

        # Required fields
        required_fields = [
            'name', 'category', 'description', 'anabolicRating',
            'androgenicRating', 'halfLife', 'detectionTime',
            'dosageRanges', 'sideEffects', 'pctRequirements'
        ]

        for field in required_fields:
            if field not in compound:
                errors.append(f"Missing required field: {field}")

        # Type validation
        if 'anabolicRating' in compound and not isinstance(compound['anabolicRating'], int):
            errors.append("anabolicRating must be an integer")
        if 'androgenicRating' in compound and not isinstance(compound['androgenicRating'], int):
            errors.append("androgenicRating must be an integer")

        # Nested structure validation
        if 'dosageRanges' in compound:
            for level in ['beginner', 'intermediate', 'advanced']:
                if level not in compound['dosageRanges']:
                    errors.append(f"Missing {level} dosage range")
                else:
                    range_data = compound['dosageRanges'][level]
                    if not all(k in range_data for k in ['min', 'max', 'unit']):
                        errors.append(f"Invalid {level} dosage range structure")

        if 'sideEffects' in compound:
            for category in ['common', 'uncommon', 'rare']:
                if category not in compound['sideEffects']:
                    errors.append(f"Missing {category} side effects")
                elif not isinstance(compound['sideEffects'][category], list):
                    errors.append(f"{category} side effects must be a list")

        if 'pctRequirements' in compound:
            required_pct_fields = ['required', 'protocol', 'duration']
            for field in required_pct_fields:
                if field not in compound['pctRequirements']:
                    errors.append(f"Missing PCT field: {field}")

        return errors

    def generate_compound_page(self, compound_name: str) -> bool:
        """Generate or update compound page."""
        try:
            compounds = self.get_compounds()

            # Find compound
            compound = None
            for c in compounds:
                if c['name'].lower() == compound_name.lower():
                    compound = c
                    break

            if not compound:
                print(f"\n{self.ui.theme.COLORS['ERROR']}Compound not found: {compound_name}{self.ui.theme.COLORS['ENDC']}")
                return False

            # Create compound directory
            compound_dir = os.path.join(self.project_root, 'src/pages/compounds', compound['slug'])
            os.makedirs(compound_dir, exist_ok=True)

            # Generate index.astro file
            template = f"""---
import Layout from '../../../layouts/Layout.astro';
import CompoundTemplate from '../../../templates/CompoundTemplate/CompoundTemplate.astro';
import {{ compounds }} from '../../../data/compounds';

const compound = compounds.find(c => c.slug === '{compound['slug']}');
---

<Layout title="{compound['name']} Guide">
  <CompoundTemplate compound={{compound}} />
</Layout>
"""

            with open(os.path.join(compound_dir, 'index.astro'), 'w') as f:
                f.write(template)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully generated page for: {compound_name}{self.ui.theme.COLORS['ENDC']}")
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to generate compound page: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def get_compound_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get compound data by name."""
        compounds = self.get_compounds()
        for compound in compounds:
            if compound['name'].lower() == name.lower():
                return compound
        return None

    def get_compound_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get compound data by slug."""
        compounds = self.get_compounds()
        for compound in compounds:
            if compound['slug'] == slug:
                return compound
        return None
