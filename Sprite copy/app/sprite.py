import flet as ft

COLOR_OFF = ft.Colors.BLUE_GREY_900
COLOR_ON = ft.Colors.GREEN_ACCENT_400
BITS_COUNT = 64
HEX_LENGTH = 16

def main(page: ft.Page):
    page.title = "Editor de Sprites 8x8 (8-Bits)"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 700
    page.window.height = 750
    page.window.resizable = False
    page.padding = 20

    grid_buttons = []

    hex_output_text = ft.Text(
        value="0" * HEX_LENGTH,
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_ACCENT,
        selectable=True
    )
    
    hex_input = ft.TextField(
        label="Código Hexadecimal (max 16 caracteres)",
        hint_text="Ej: FFFF0000FFFF0000",
        max_length=HEX_LENGTH,
        width=300,
        capitalization=ft.TextCapitalization.CHARACTERS
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED_400, size=12)

    def update_hex_from_grid():
        binary_str = "".join(["1" if btn.bgcolor == COLOR_ON else "0" for btn in grid_buttons])
        decimal_val = int(binary_str, 2)
        hex_val = hex(decimal_val)[2:].upper()
        hex_output_text.value = hex_val.zfill(HEX_LENGTH)
        page.update()

    def pixel_click(e):
        e.control.bgcolor = COLOR_OFF if e.control.bgcolor == COLOR_ON else COLOR_ON
        update_hex_from_grid()

    grid_view = ft.GridView(
        expand=False,
        runs_count=8,
        max_extent=45,
        child_aspect_ratio=1.0,
        spacing=4,
        run_spacing=4,
        width=390,
        height=390
    )

    for _ in range(BITS_COUNT):
        btn = ft.Container(
            bgcolor=COLOR_OFF,
            border_radius=4,
            on_click=pixel_click,
            animate=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT)
        )
        grid_buttons.append(btn)
        grid_view.controls.append(btn)

    def load_hex_to_grid(e):
        user_input = hex_input.value.strip()
        error_text.value = ""
        
        if not user_input:
            error_text.value = "Por favor, ingresa un valor Hexadecimal."
            page.update()
            return

        try:
            decimal_val = int(user_input, 16)
        except ValueError:
            error_text.value = "Entrada inválida. Usa solo caracteres Hexadecimales (0-9, A-F)."
            page.update()
            return

        binary_str = bin(decimal_val)[2:].zfill(BITS_COUNT)
        
        if len(binary_str) > BITS_COUNT:
            error_text.value = "El valor excede el límite de 64 bits (16 dígitos hex)."
            page.update()
            return

        for bit, btn in zip(binary_str, grid_buttons):
            btn.bgcolor = COLOR_ON if bit == "1" else COLOR_OFF

        hex_output_text.value = user_input.upper().zfill(HEX_LENGTH)
        hex_input.value = ""
        page.update()

    # Replaced text="Cargar Hex" with content=ft.Text("Cargar Hex")
    btn_load = ft.ElevatedButton(
        content=ft.Text("Cargar Hex"),
        icon=ft.Icons.DOWNLOAD,
        on_click=load_hex_to_grid,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    control_panel = ft.Column(
        controls=[
            ft.Text("Valor Hexadecimal Actual (64 bits):", size=14, color=ft.Colors.GREY_400),
            hex_output_text,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row(controls=[hex_input, btn_load], alignment=ft.MainAxisAlignment.CENTER),
            error_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("Editor de Sprites 8x8", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Electrónica Digital - CUL", color=ft.Colors.GREY_500),
                ft.Divider(height=20),
                grid_view,
                ft.Divider(height=20),
                control_panel
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)