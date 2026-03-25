import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Diploma App"

    defect = ft.TextField(label="Тип дефекта")
    zone = ft.TextField(label="Зона")

    result_text = ft.Text(value="", selectable=True)

    def analyze_click(e):
        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "defect": defect.value,
                "zone": zone.value
            }
        )
        result_text.value = response.json()["result"]
        page.update()

    page.add(
        defect,
        zone,
        ft.ElevatedButton("Анализ", on_click=analyze_click),
        result_text
    )


ft.app(target=main)
