#!/usr/bin/env python
import random
import numpy as np
from nicegui import ui

# ============= CUSTOMIZATION =============
CUSTOM_FONT = (
    "'Open Sans', 'Inter', 'Segoe UI', 'Roboto', sans-serif"  # Change this to your preferred font
)
LOGO_IMAGE_PATH = "CCElogo.png"  # Set to your logo image path e.g., 'logo.png' or leave as None for text logo
INPUT_BOX_WIDTH = 80  # Width of input boxes in pixels (default: 70)
# =========================================
# Theme Colors
THEMES = {
    "dark": {
        "bg": "#0a0a0a",
        "surface": "#1a1a1a",
        "card": "#2a2a2a",
        "text": "#ffffff",
        "text_secondary": "#a0a0a0",
        "border": "#404040",
        "neon_primary": "#00ff88",
        "neon_secondary": "#00ddff",
        "neon_error": "#ff0055",
        "neon_warning": "#ffaa00",
        "input_bg": "#151515",
        "input_text": "#ffffff",
    },
    "light": {
        "bg": "#f5f5f5",
        "surface": "#ffffff",
        "card": "#fafafa",
        "text": "#1a1a1a",
        "text_secondary": "#666666",
        "border": "#d0d0d0",
        "neon_primary": "#006432",
        "neon_secondary": "#006080",
        "neon_error": "#cc0044",
        "neon_warning": "#dd8800",
        "input_bg": "#ffffff",
        "input_text": "#1a1a1a",
    },
}

class CramersRuleSolver:
    def __init__(self):
        self.n = 3
        self.matrix_inputs = []
        self.vector_inputs = []
        self.solution_container = None
        self.current_theme = "dark"
        self.main_container = None
        self.theme_button = None
        self.last_solution_data = None
        self.n_select = None

    def get_theme(self):
        return THEMES[self.current_theme]

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.rebuild_ui()

    def clear_inputs(self):
        """Clear all input fields"""
        for i in range(self.n):
            for j in range(self.n):
                self.matrix_inputs[i][j].value = None
            self.vector_inputs[i].value = None

        self.solution_container.clear()
        self.last_solution_data = None
        ui.notify("All inputs cleared", type="positive")

    def fill_random(self):
        """Fill all input fields with random integers (no decimals, max 3 digits)"""
        for i in range(self.n):
            for j in range(self.n):
                self.matrix_inputs[i][j].value = random.randint(-999, 999)
            self.vector_inputs[i].value = random.randint(-999, 999)

        ui.notify("Random values generated", type="positive")

    def rebuild_ui(self):
        """Rebuild the entire UI with new theme"""
        # ADDED: Save current input values before rebuilding
        saved_matrix_values = []
        saved_vector_values = []

        for i in range(self.n):
            row_values = []
            for j in range(self.n):
                if i < len(self.matrix_inputs) and j < len(self.matrix_inputs[i]):
                    row_values.append(self.matrix_inputs[i][j].value)
                else:
                    row_values.append(None)
            saved_matrix_values.append(row_values)

            if i < len(self.vector_inputs):
                saved_vector_values.append(self.vector_inputs[i].value)
            else:
                saved_vector_values.append(None)

        theme = self.get_theme()

        # Update body
        ui.query("body").style(
            f"background: {theme['bg']}; margin: 0; padding: 0; font-family: {CUSTOM_FONT}; "
            f"display: flex; flex-direction: column; min-height: 100vh"
        )

        # Update header
        header_container.clear()
        with header_container:
            with ui.row().classes("items-center gap-4 md:gap-6 flex-1 flex-wrap"):

                # ============= MODIFIED LOGO SECTION =============
                # NOTE: This assumes 'logo.png' is in the SAME directory as main.py
                ui.image(LOGO_IMAGE_PATH).style('max-width: 200px; height: auto;')
                # If logo.png is missing, NiceGUI will show an error message
                # instead of silently falling back to a text logo.
                # =================================================

                # Title
                with ui.column().classes("gap-0"):
                    ui.label("Cramer's Rule Solver").classes(
                        "text-lg md:text-2xl font-bold"
                    ).style(f"color: {theme['text']}")
                    ui.label("SAVIO PRINCE | CCE25EC053").classes(
                        "text-xs md:text-sm"
                    ).style(f"color: {theme['text_secondary']}")

            # Theme toggle button - emoji only
            icon = "🌙" if self.current_theme == "light" else "☀️"
            self.theme_button = (
                ui.button(icon, on_click=self.toggle_theme)
                .props("rounded flat")
                .classes("px-3 md:px-4")
                .style(
                    f"background: #8B5DFF; color: #000; "
                    f"font-weight: bold; font-size: 20px;"
                )
            )

        header_container.style(
            f"background: {theme['surface']}; box-shadow: 0 2px 8px rgba(0,0,0,0.2)"
        )

        # Update footer
        footer_container.style(
            f"background: {theme['surface']}; color: {theme['text_secondary']}"
        )
        footer_label.style(f"color: {theme['text_secondary']}")

        # Rebuild main content
        self.main_container.clear()
        with self.main_container:
            # Control Panel
            with (
                ui.card()
                .classes("w-full max-w-4xl mx-auto p-4 md:p-6 rounded-lg")
                .style(f"background: {theme['card']}")
            ):
                # Variable selector and buttons - all in one responsive row
                with ui.row().classes("items-center gap-3 md:gap-4 flex-wrap"):
                    ui.label("Number of Variables (N):").classes(
                        "text-base md:text-lg font-semibold whitespace-nowrap"
                    ).style(f"color: {theme['text']}")

                    self.n_select = (
                        ui.number(value=self.n, min=2, max=18, step=1)
                        .classes("rounded-lg no-spinner")
                        .style(
                            f"background: {theme['input_bg']}; color: {theme['input_text']} !important; "
                            f"border: 2px solid {theme['neon_secondary']}; width: 100px"
                        )
                        .props(
                            'dense outlined input-style="color: '
                            + theme["input_text"]
                            + ' !important"'
                        )
                    )

                    # Vertical separator for larger screens
                    with (
                        ui.element("div")
                        .classes("hidden md:block")
                        .style(
                            f"width: 2px; height: 32px; background: {theme['border']}"
                        )
                    ):
                        pass

                    # Action buttons - wrap to new line on small screens (no shadows)
                    ui.button(
                        "Update Grid",
                        on_click=lambda: self.update_grid(int(self.n_select.value)),
                    ).props("rounded flat").classes(
                        "px-4 md:px-6 text-sm md:text-base"
                    ).style(
                        f"background: #31ccec; color: #000; "
                        f"font-weight: bold; transition: all 0.2s;"
                    )

                    ui.button("🗑️ Clear", on_click=self.clear_inputs).props(
                        "rounded flat"
                    ).classes("px-4 md:px-6 text-sm md:text-base").style(
                        f"background: #FF004D; color: #000; "
                        f"font-weight: bold; transition: all 0.2s;"
                    )

                    ui.button("🎲 Random", on_click=self.fill_random).props(
                        "rounded flat"
                    ).classes("px-4 md:px-6 text-sm md:text-base").style(
                        f"background: #F57D1F; color: #000; "
                        f"font-weight: bold; transition: all 0.2s;"
                    )

            # Matrix Input Grid
            self.render_grid()

            # ADDED: Restore saved values after grid is rendered
            for i in range(self.n):
                for j in range(self.n):
                    if i < len(saved_matrix_values) and j < len(saved_matrix_values[i]):
                        self.matrix_inputs[i][j].value = saved_matrix_values[i][j]
                if i < len(saved_vector_values):
                    self.vector_inputs[i].value = saved_vector_values[i]

            # Solve Button (no shadow)
            with ui.row().classes("w-full justify-center mt-4"):
                ui.button("🧮 Solve System", on_click=self.solve_system).props(
                    "rounded size=lg"
                ).classes("px-8 md:px-12 py-3").style(
                    f"background: {theme['neon_primary']}; color: #000; "
                    f"font-size: 16px md:font-size: 18px; font-weight: bold; transition: all 0.2s;"
                )

            # Solution Display
            self.solution_container = ui.column().classes("w-full mt-6")

            # If we had a previous solution, redisplay it
            if self.last_solution_data:
                self.show_solution_with_data(self.last_solution_data)

    def solve_system(self):
        """Solve the linear system using Cramer's Rule"""
        try:
            # Get matrix A
            A = np.zeros((self.n, self.n))
            for i in range(self.n):
                for j in range(self.n):
                    val = self.matrix_inputs[i][j].value
                    if val is None or val == "":
                        ui.notify("Please fill all coefficient values", type="warning")
                        return
                    A[i][j] = float(val)

            # Get vector B
            B = np.zeros(self.n)
            for i in range(self.n):
                val = self.vector_inputs[i].value
                if val is None or val == "":
                    ui.notify("Please fill all constant values", type="warning")
                    return
                B[i] = float(val)

            # Calculate det(A)
            det_A = np.linalg.det(A)

            if abs(det_A) < 1e-10:
                self.show_error("System has no unique solution (det(A) ≈ 0)")
                return

            # Apply Cramer's Rule and store all intermediate values
            solutions = []
            det_Ai_list = []

            for i in range(self.n):
                A_i = A.copy()
                A_i[:, i] = B
                det_A_i = np.linalg.det(A_i)
                det_Ai_list.append(det_A_i)
                x_i = det_A_i / det_A
                solutions.append(x_i)

            # Verification
            verification = A @ np.array(solutions)

            # Store solution data
            self.last_solution_data = {
                "A": A,
                "B": B,
                "det_A": det_A,
                "det_Ai_list": det_Ai_list,
                "solutions": solutions,
                "verification": verification,
            }

            self.show_solution_with_data(self.last_solution_data)

        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def show_solution_with_data(self, data):
        """Display solution with all data"""
        theme = self.get_theme()
        self.solution_container.clear()

        with self.solution_container:
            # Quick Solution Display
            with (
                ui.card()
                .classes("w-full p-4 md:p-6 rounded-lg")
                .style(
                    f"background: {theme['card']}; border: 2px solid {theme['neon_primary']};"
                )
            ):
                ui.label("✓ Solution Found").classes(
                    "text-xl md:text-2xl font-bold mb-4"
                ).style(f"color: {theme['neon_primary']}")

                ui.label(f"det(A) = {data['det_A']:.6f}").classes("text-sm mb-4").style(
                    f"color: {theme['text_secondary']}"
                )

                ui.separator().style(f"background: {theme['border']}")

                for i, sol in enumerate(data["solutions"]):
                    with ui.row().classes("items-center gap-2 mt-3 flex-wrap"):
                        ui.label(f"x{i + 1}").classes(
                            "text-base md:text-lg font-mono font-bold"
                        ).style(f"color: {theme['neon_secondary']}; min-width: 40px")
                        ui.label("=").style(f"color: {theme['text']}")
                        ui.label(f"{sol:.6f}").classes(
                            "text-base md:text-lg font-mono"
                        ).style(f"color: {theme['text']}")

            # Detailed Explanation (Expandable)
            with (
                ui.expansion("📊 Show Detailed Solution Steps", icon="calculate")
                .classes("w-full mt-4")
                .style(
                    f"background: {theme['card']}; border: 2px solid {theme['neon_warning']}; "
                    f"border-radius: 8px; color: {theme['text']}"
                )
            ):
                with (
                    ui.column()
                    .classes("w-full p-4 gap-4 font-mono")
                    .style(
                        f"background: {theme['input_bg']}; color: {theme['text']}; overflow-x: auto"
                    )
                ):
                    # System of Equations
                    ui.label("SYSTEM OF EQUATIONS:").classes("text-lg font-bold").style(
                        f"color: {theme['neon_secondary']}"
                    )
                    ui.label("=" * 60).style(f"color: {theme['border']}")

                    for i in range(self.n):
                        eq_parts = []
                        for j in range(self.n):
                            eq_parts.append(f"{data['A'][i][j]:.2f}x{j + 1}")
                        eq_str = " + ".join(eq_parts) + f" = {data['B'][i]:.2f}"
                        ui.label(eq_str).style(f"color: {theme['text']}")

                    ui.label(f"\nDeterminant of [A] = {data['det_A']:.6f}").classes(
                        "font-bold"
                    ).style(f"color: {theme['neon_primary']}")
                    ui.label("=" * 60).style(f"color: {theme['border']}")

                    # Calculating Solutions
                    ui.label("\nCALCULATING SOLUTIONS:").classes(
                        "text-lg font-bold mt-4"
                    ).style(f"color: {theme['neon_secondary']}")
                    ui.label("=" * 60).style(f"color: {theme['border']}")

                    for i, sol in enumerate(data["solutions"]):
                        ui.label(f"\nx{i + 1} = det(A{i + 1}) / det(A)").style(
                            f"color: {theme['text']}"
                        )
                        ui.label(
                            f"x{i + 1} = {data['det_Ai_list'][i]:.6f} / {data['det_A']:.6f}"
                        ).style(f"color: {theme['text_secondary']}")
                        ui.label(f"x{i + 1} = {sol:.6f}").classes("font-bold").style(
                            f"color: {theme['neon_primary']}"
                        )

                    # Final Solution
                    ui.label("\n" + "=" * 60).style(f"color: {theme['border']}")
                    ui.label("FINAL SOLUTION:").classes("text-lg font-bold mt-4").style(
                        f"color: {theme['neon_secondary']}"
                    )
                    ui.label("=" * 60).style(f"color: {theme['border']}")

                    for i, sol in enumerate(data["solutions"]):
                        ui.label(f"x{i + 1} = {sol:.6f}").classes("font-bold").style(
                            f"color: {theme['neon_primary']}"
                        )

                    # Verification
                    ui.label("\n" + "=" * 60).style(f"color: {theme['border']}")
                    ui.label("VERIFICATION (AX = B):").classes(
                        "text-lg font-bold mt-4"
                    ).style(f"color: {theme['neon_secondary']}")
                    ui.label("=" * 60).style(f"color: {theme['border']}")

                    for i in range(self.n):
                        match = (
                            "="
                            if abs(data["verification"][i] - data["B"][i]) < 0.01
                            else "≈"
                        )
                        ui.label(
                            f"{data['verification'][i]:.6f} {match} {data['B'][i]:.6f}"
                        ).style(f"color: {theme['text']}")

                    ui.label("\n" + "=" * 60).style(f"color: {theme['border']}")
                    ui.label("Created by @oivas000").classes(
                        "text-sm mt-4 text-center"
                    ).style(f"color: {theme['text_secondary']}")

    def show_error(self, message):
        """Display error message"""
        theme = self.get_theme()
        self.solution_container.clear()
        with self.solution_container:
            with (
                ui.card()
                .classes("w-full p-4 md:p-6 rounded-lg")
                .style(
                    f"background: {theme['card']}; border: 2px solid {theme['neon_error']};"
                )
            ):
                ui.label("✗ Error").classes("text-xl md:text-2xl font-bold mb-2").style(
                    f"color: {theme['neon_error']}"
                )
                ui.label(message).classes("text-sm md:text-base").style(
                    f"color: {theme['text']}"
                )

    def update_grid(self, new_n):
        """Update the matrix grid when N changes"""
        self.n = new_n
        self.matrix_inputs = []  # Make sure this is here
        self.vector_inputs = []  # Make sure this is here
        self.last_solution_data = None
        self.rebuild_ui()

    def render_grid(self):
        """Render the coefficient matrix and constant vector grid"""
        self.matrix_inputs = []
        self.vector_inputs = []
        theme = self.get_theme()

        # Calculate required width for the grid
        grid_width = self.n * (INPUT_BOX_WIDTH + 2) + 112  # input width + 2px gap + equals + B column

        # Determine max-width based on number of variables
        # Use responsive widths for smaller systems, full width for larger ones
        if self.n <= 5:
            max_width_class = "max-w-4xl"  # ~896px
        elif self.n <= 8:
            max_width_class = "max-w-6xl"  # ~1152px
        else:
            max_width_class = "max-w-full"  # Full width for 9+ variables

        with (
            ui.card()
            .classes(f"w-full {max_width_class} mx-auto p-4 md:p-6 rounded-lg")
            .style(
                f"background: {theme['card']}; overflow-x: auto; overflow-y: visible;"
            )
        ):
            ui.label("Linear System").classes(
                "text-lg md:text-xl font-bold mb-4"
            ).style(f"color: {theme['neon_secondary']}")

            # Container for the grid - always in a single row (no line breaks)
            with ui.column().classes("gap-2").style(f"min-width: {grid_width}px;"):
                # Header row
                with ui.row().classes("items-center gap-2 mb-2"):
                    # Column headers for variables
                    for j in range(self.n):
                        ui.label(f"x{j + 1}").classes(
                            "text-sm md:text-base font-bold text-center"
                        ).style(
                            f"color: {theme['neon_secondary']}; width: {INPUT_BOX_WIDTH}px; flex-shrink: 0"
                        )

                    # Equal sign header
                    ui.label("").classes("text-sm md:text-base font-bold").style(
                        f"color: {theme['text']}; width: 40px; flex-shrink: 0"
                    )

                    # B column header
                    ui.label("B").classes(
                        "text-sm md:text-base font-bold text-center"
                    ).style(
                        f"color: {theme['neon_primary']}; width: {INPUT_BOX_WIDTH}px; flex-shrink: 0"
                    )

                # Data rows
                for i in range(self.n):
                    with ui.row().classes("items-center gap-2 mb-2"):
                        row_inputs = []

                        # Coefficient inputs with colored border
                        for j in range(self.n):
                            inp = (
                                ui.number(
                                    value=None,
                                    format="%.2f",
                                    placeholder=f"a{i + 1}{j + 1}",
                                )
                                .classes("rounded-lg no-spinner")
                                .style(
                                    f"background: {theme['input_bg']}; color: {theme['input_text']} !important; "
                                    f"border: 2px solid {theme['neon_secondary']}; width: {INPUT_BOX_WIDTH}px; flex-shrink: 0"
                                )
                                .props(
                                    'dense outlined input-style="color: '
                                    + theme["input_text"]
                                    + ' !important"'
                                )
                            )
                            row_inputs.append(inp)

                        # Equal sign
                        ui.label("=").classes(
                            "text-base md:text-lg font-bold text-center"
                        ).style(
                            f"color: {theme['neon_primary']}; width: 40px; flex-shrink: 0"
                        )

                        # Constant input
                        b_inp = (
                            ui.number(
                                value=None, format="%.2f", placeholder=f"b{i + 1}"
                            )
                            .classes("rounded-lg no-spinner")
                            .style(
                                f"background: {theme['input_bg']}; color: {theme['input_text']} !important; "
                                f"border: 2px solid {theme['neon_primary']}; width: {INPUT_BOX_WIDTH}px; flex-shrink: 0"
                            )
                            .props(
                                'dense outlined input-style="color: '
                                + theme["input_text"]
                                + ' !important"'
                            )
                        )

                        self.matrix_inputs.append(row_inputs)
                        self.vector_inputs.append(b_inp)


# Initialize solver
solver = CramersRuleSolver()

# Page setup
theme = solver.get_theme()
ui.query("body").style(
    f"background: {theme['bg']}; margin: 0; padding: 0; font-family: {CUSTOM_FONT}; "
    f"display: flex; flex-direction: column; min-height: 100vh"
)

# Add responsive meta tag and CSS to hide number input spinners
ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <style>
        /* Hide number input spinners */
        input[type=number]::-webkit-inner-spin-button,
        input[type=number]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        input[type=number] {
            -moz-appearance: textfield;
            appearance: textfield;
        }
    </style>
''')

# Header
header_container = (
    ui.header()
    .classes("items-center justify-between px-4 md:px-6 py-4")
    .style(f"background: {theme['surface']}; box-shadow: 0 2px 8px rgba(0,0,0,0.2)")
)

with header_container:
    with ui.row().classes("items-center gap-4 md:gap-6 flex-1 flex-wrap"):
        ui.image(LOGO_IMAGE_PATH).style('max-width: 240px; height: auto;')

        # Title
        with ui.column().classes("gap-0"):
            ui.label("Cramer's Rule Solver").classes(
                "text-lg md:text-2xl font-bold"
            ).style(f"color: {theme['text']}")
            ui.label("SAVIO PRINCE | CCE25EC053").classes("text-xs md:text-sm").style(
                f"color: {theme['text_secondary']}"
            )

    # Theme toggle button - emoji only
    solver.theme_button = (
        ui.button("☀️", on_click=solver.toggle_theme)
        .props("rounded flat")
        .classes("px-3 md:px-4")
        .style(
            f"background: #8B5DFF; color: #000; "
            f"font-weight: bold; font-size: 20px;"
        )
    )

# Main content
solver.main_container = (
    ui.column()
    .classes("w-full px-4 md:px-6 gap-6 flex-grow")
    .style("max-width: 100vw;")
)

with solver.main_container:
    # Control Panel
    with (
        ui.card()
        .classes("w-full max-w-4xl mx-auto p-4 md:p-6 rounded-lg")
        .style(f"background: {theme['card']}")
    ):
        # Variable selector and buttons - all in one responsive row
        with ui.row().classes("items-center gap-3 md:gap-4 flex-wrap"):
            ui.label("Number of Variables (N):").classes(
                "text-base md:text-lg font-semibold whitespace-nowrap"
            ).style(f"color: {theme['text']}")

            solver.n_select = (
                ui.number(value=3, min=2, max=18, step=1)
                .classes("rounded-lg")
                .style(
                    f"background: {theme['input_bg']}; color: {theme['input_text']} !important; "
                    f"border: 2px solid {theme['neon_secondary']}; width: 100px"
                )
                .props(
                    'dense outlined input-style="color: '
                    + theme["input_text"]
                    + ' !important"'
                )
            )

            # Vertical separator for larger screens
            with (
                ui.element("div")
                .classes("hidden md:block")
                .style(f"width: 2px; height: 32px; background: {theme['border']}")
            ):
                pass

            # Action buttons - wrap to new line on small screens (no shadows)
            ui.button(
                "Update Grid",
                on_click=lambda: solver.update_grid(int(solver.n_select.value or 3)),
            ).props("rounded flat").classes("px-4 md:px-6 text-sm md:text-base").style(
                f"background: #31ccec; color: #000; "
                f"font-weight: bold; transition: all 0.2s;"
            )

            ui.button("🗑️ Clear", on_click=solver.clear_inputs).props(
                "rounded flat"
            ).classes("px-4 md:px-6 text-sm md:text-base").style(
                f"background: #FF004D; color: #000; "
                f"font-weight: bold; transition: all 0.2s;"
            )

            ui.button("🎲 Random", on_click=solver.fill_random).props(
                "rounded flat"
            ).classes("px-4 md:px-6 text-sm md:text-base").style(
                f"background: #F57D1F; color: #000; "
                f"font-weight: bold; transition: all 0.2s;"
            )

    # Matrix Input Grid
    solver.render_grid()

    # Solve Button (no shadow)
    with ui.row().classes("w-full justify-center mt-4"):
        ui.button("🧮 Solve System", on_click=solver.solve_system).props(
            "rounded size=lg"
        ).classes("px-8 md:px-12 py-3").style(
            f"background: {theme['neon_primary']}; color: #000; "
            f"font-size: 16px md:font-size: 18px; font-weight: bold; transition: all 0.2s;"
        )

    # Solution Display
    solver.solution_container = ui.column().classes("w-full mt-6")

# Footer
footer_container = (
    ui.footer()
    .classes("w-full py-4")
    .style(f"background: {theme['surface']}; margin-top: auto")
)

with footer_container:
    with ui.row().classes("w-full justify-center"):
        footer_label = (
            ui.label("© 2025 SAVIO PRINCE")
            .classes("text-sm")
            .style(f"color: {theme['text_secondary']}")
        )
ui.colors(primary='#004488')
ui.run(title="Cramer's Rule Solver", port=8000)

