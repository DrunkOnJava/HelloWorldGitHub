"""Component management menu implementation."""

from ...models.menu_item import MenuItem

def show_component_menu(ui) -> None:
    """Component tools submenu."""
    while True:
        ui.print_header(
            "Component Tools",
            "Create and Manage Components"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create Component',
                description='Create new React component',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='test',
                label='Generate Tests',
                description='Generate component tests',
                icon='🧪',
                shortcut='t'
            ),
            MenuItem(
                key='stories',
                label='Create Stories',
                description='Create Storybook stories',
                icon='📚',
                shortcut='s'
            ),
            MenuItem(
                key='docs',
                label='Generate Docs',
                description='Generate component documentation',
                icon='📝',
                shortcut='d'
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
            create_component(ui)
        elif choice == 'test':
            component_name = ui.get_input("Component name", required=True)
            generate_test(ui, component_name, [])
        elif choice == 'stories':
            component_name = ui.get_input("Component name", required=True)
            generate_story(ui, component_name, [])
        elif choice == 'docs':
            component_name = ui.get_input("Component name", required=True)
            description = ui.get_input("Component description", required=True)
            generate_docs(ui, component_name, description, [])

def create_component(ui) -> None:
    """Component creation wizard."""
    try:
        ui.print_header(
            "Create Component",
            "Component Creation Wizard"
        )

        # Get component details
        name = ui.get_input("Component name", required=True)
        description = ui.get_input("Component description", required=True)
        component_type = ui.get_input("Component type (functional/class)", required=True).lower()

        # Get props
        props = []
        while True:
            add_prop = ui.get_input("Add a prop? (y/n)").lower()
            if add_prop != 'y':
                break

            prop_name = ui.get_input("Prop name", required=True)
            prop_type = ui.get_input("Prop type (e.g., string, number)", required=True)
            prop_required = ui.get_input("Is prop required? (y/n)").lower() == 'y'
            prop_description = ui.get_input("Prop description")

            props.append({
                'name': prop_name,
                'type': prop_type,
                'required': prop_required,
                'description': prop_description
            })

        # Create component
        if ui.project.create_component(name, description, component_type, props):
            ui.status_bar.update(f"Component '{name}' created successfully", 2)

            # Ask about generating additional files
            if ui.get_input("Generate test file? (y/n)").lower() == 'y':
                generate_test(ui, name, props)
            if ui.get_input("Generate story file? (y/n)").lower() == 'y':
                generate_story(ui, name, props)
            if ui.get_input("Generate documentation? (y/n)").lower() == 'y':
                generate_docs(ui, name, description, props)
        else:
            ui.status_bar.update("Failed to create component", 2, error=True)

    except Exception as e:
        ui.status_bar.update(f"Error creating component: {str(e)}", 2, error=True)

def generate_test(ui, component_name: str, props: list) -> None:
    """Generate test file for component."""
    try:
        if ui.project.generate_component_test(component_name, props):
            ui.status_bar.update(f"Test file generated for {component_name}", 2)
        else:
            ui.status_bar.update("Failed to generate test file", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error generating test: {str(e)}", 2, error=True)

def generate_story(ui, component_name: str, props: list) -> None:
    """Generate Storybook story for component."""
    try:
        if ui.project.generate_component_story(component_name, props):
            ui.status_bar.update(f"Story file generated for {component_name}", 2)
        else:
            ui.status_bar.update("Failed to generate story file", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error generating story: {str(e)}", 2, error=True)

def generate_docs(ui, component_name: str, description: str, props: list) -> None:
    """Generate documentation for component."""
    try:
        if ui.project.generate_component_docs(component_name, description, props):
            ui.status_bar.update(f"Documentation generated for {component_name}", 2)
        else:
            ui.status_bar.update("Failed to generate documentation", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error generating documentation: {str(e)}", 2, error=True)
