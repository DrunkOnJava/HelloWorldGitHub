"""Compound management menu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import CompoundData

def show_compound_menu(ui) -> None:
    """Compound management submenu."""
    while True:
        ui.print_header(
            "Compound Manager",
            "Manage Compound Data and Pages"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create Compound',
                description='Create new compound data and page',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='edit',
                label='Edit Compound',
                description='Edit existing compound data',
                icon='✏️',
                shortcut='e'
            ),
            MenuItem(
                key='validate',
                label='Validate Data',
                description='Validate compound data structure',
                icon='✓',
                shortcut='v'
            ),
            MenuItem(
                key='generate',
                label='Generate Pages',
                description='Generate compound pages',
                icon='🔄',
                shortcut='g'
            ),
            MenuItem(
                key='back',
                label='Back to Project Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'create':
            create_compound(ui)
        elif choice == 'edit':
            edit_compound(ui)
        elif choice == 'validate':
            validate_compounds(ui)
        elif choice == 'generate':
            generate_compound_pages(ui)

def create_compound(ui) -> None:
    """Interactive compound creation process."""
    ui.print_header(
        "Create Compound",
        "Enter compound information"
    )

    try:
        # Basic information
        name = ui.get_input("Compound name", required=True)
        category = ui.get_input("Category (e.g., Anabolic Steroid)", required=True)
        description = ui.get_input("Description", required=True)

        # Ratings
        anabolic_rating = int(ui.get_input("Anabolic Rating (0-1000)", required=True))
        androgenic_rating = int(ui.get_input("Androgenic Rating (0-1000)", required=True))

        # Timing information
        half_life = ui.get_input("Half Life (e.g., '2-3 days')", required=True)
        detection_time = ui.get_input("Detection Time (e.g., '3-4 months')", required=True)

        # Dosage ranges
        print("\nDosage Ranges (in mg/week):")
        dosage_ranges = {
            "beginner": {
                "min": int(ui.get_input("Beginner minimum dose", required=True)),
                "max": int(ui.get_input("Beginner maximum dose", required=True)),
                "unit": "mg/week"
            },
            "intermediate": {
                "min": int(ui.get_input("Intermediate minimum dose", required=True)),
                "max": int(ui.get_input("Intermediate maximum dose", required=True)),
                "unit": "mg/week"
            },
            "advanced": {
                "min": int(ui.get_input("Advanced minimum dose", required=True)),
                "max": int(ui.get_input("Advanced maximum dose", required=True)),
                "unit": "mg/week"
            }
        }

        # Side effects
        print("\nSide Effects (comma-separated lists):")
        side_effects = {
            "common": ui.get_input("Common side effects", required=True).split(','),
            "uncommon": ui.get_input("Uncommon side effects", required=True).split(','),
            "rare": ui.get_input("Rare side effects", required=True).split(',')
        }

        # PCT requirements
        print("\nPCT Requirements:")
        pct_required = ui.get_input("PCT Required? (yes/no)", required=True).lower() == 'yes'
        pct_requirements = {
            "required": pct_required,
            "protocol": ui.get_input("PCT Protocol", required=pct_required),
            "duration": ui.get_input("PCT Duration", required=pct_required)
        }

        # Lists
        print("\nOther Information (comma-separated lists):")
        interactions = ui.get_input("Drug Interactions", required=True).split(',')
        references = ui.get_input("References/Studies", required=True).split(',')

        # Create compound data object
        compound_data = CompoundData(
            name=name,
            category=category,
            description=description,
            anabolic_rating=anabolic_rating,
            androgenic_rating=androgenic_rating,
            half_life=half_life,
            detection_time=detection_time,
            dosage_ranges=dosage_ranges,
            side_effects=side_effects,
            pct_requirements=pct_requirements,
            interactions=[i.strip() for i in interactions],
            references=[r.strip() for r in references]
        )

        # Add compound to database
        if ui.project.add_compound(compound_data):
            ui.status_bar.update(f"Successfully created compound: {name}", 3)
        else:
            ui.status_bar.update("Failed to create compound", 3)

    except ValueError as e:
        ui.status_bar.update(f"Invalid input: {str(e)}", 3)
    except Exception as e:
        ui.status_bar.update(f"Error creating compound: {str(e)}", 3)

def edit_compound(ui) -> None:
    """Edit an existing compound."""
    ui.print_header(
        "Edit Compound",
        "Edit existing compound data"
    )

    # Get list of compounds
    compounds = ui.project.get_compounds()
    if not compounds:
        ui.status_bar.update("No compounds found", 3)
        return

    # Display compound list
    print("\nAvailable compounds:")
    for i, compound in enumerate(compounds, 1):
        print(f"{i}. {compound['name']}")

    # Get compound selection
    try:
        selection = int(ui.get_input("\nSelect compound number", required=True)) - 1
        if selection < 0 or selection >= len(compounds):
            ui.status_bar.update("Invalid selection", 3)
            return

        compound = compounds[selection]
        compound_name = compound['name']

        # Get updated information
        print(f"\nEditing {compound_name}")
        print("Press Enter to keep current values, or enter new value")

        name = ui.get_input(f"Name [{compound['name']}]") or compound['name']
        category = ui.get_input(f"Category [{compound['category']}]") or compound['category']
        description = ui.get_input(f"Description [{compound['description']}]") or compound['description']

        anabolic_rating = int(ui.get_input(f"Anabolic Rating [{compound['anabolicRating']}]") or compound['anabolicRating'])
        androgenic_rating = int(ui.get_input(f"Androgenic Rating [{compound['androgenicRating']}]") or compound['androgenicRating'])

        half_life = ui.get_input(f"Half Life [{compound['halfLife']}]") or compound['halfLife']
        detection_time = ui.get_input(f"Detection Time [{compound['detectionTime']}]") or compound['detectionTime']

        # Create updated compound data
        updated_data = CompoundData(
            name=name,
            category=category,
            description=description,
            anabolic_rating=anabolic_rating,
            androgenic_rating=androgenic_rating,
            half_life=half_life,
            detection_time=detection_time,
            dosage_ranges=compound['dosageRanges'],  # Keep existing
            side_effects=compound['sideEffects'],    # Keep existing
            pct_requirements=compound['pctRequirements'],  # Keep existing
            interactions=compound['interactions'],    # Keep existing
            references=compound['references']        # Keep existing
        )

        # Update compound
        if ui.project.edit_compound(compound_name, updated_data):
            ui.status_bar.update(f"Successfully updated {compound_name}", 3)
        else:
            ui.status_bar.update(f"Failed to update {compound_name}", 3)

    except ValueError as e:
        ui.status_bar.update(f"Invalid input: {str(e)}", 3)
    except Exception as e:
        ui.status_bar.update(f"Error editing compound: {str(e)}", 3)

def validate_compounds(ui) -> None:
    """Validate all compound data."""
    ui.print_header(
        "Validate Data",
        "Validate compound data structure"
    )

    compounds = ui.project.get_compounds()
    if not compounds:
        ui.status_bar.update("No compounds found", 3)
        return

    print("\nValidating compounds...")
    has_errors = False

    for compound in compounds:
        errors = ui.project.validate_compound_data(compound)
        if errors:
            has_errors = True
            print(f"\n{ui.theme.COLORS['ERROR']}Errors in {compound['name']}:{ui.theme.COLORS['ENDC']}")
            for error in errors:
                print(f"  - {error}")

    if not has_errors:
        print(f"\n{ui.theme.COLORS['SUCCESS']}All compounds are valid!{ui.theme.COLORS['ENDC']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def generate_compound_pages(ui) -> None:
    """Generate pages for compounds."""
    ui.print_header(
        "Generate Pages",
        "Generate compound pages"
    )

    compounds = ui.project.get_compounds()
    if not compounds:
        ui.status_bar.update("No compounds found", 3)
        return

    print("\nGenerating compound pages...")
    success_count = 0
    error_count = 0

    for compound in compounds:
        if ui.project.generate_compound_page(compound['name']):
            success_count += 1
        else:
            error_count += 1

    if error_count == 0:
        print(f"\n{ui.theme.COLORS['SUCCESS']}Successfully generated {success_count} pages!{ui.theme.COLORS['ENDC']}")
    else:
        print(f"\n{ui.theme.COLORS['WARNING']}Generated {success_count} pages with {error_count} errors{ui.theme.COLORS['ENDC']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()
