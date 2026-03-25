import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):

    page.title = "Анализ объектов культурного наследия"
    page.window_width = 900
    page.window_height = 700

    current_user_id = 1  # временно

    # ---------------- AUTH ----------------

    username = ft.TextField(label="Имя пользователя", width=300)
    password = ft.TextField(label="Пароль", password=True, width=300)
    auth_message = ft.Text(color="red")

    def register(e):
        try:
            r = requests.post(f"{API_URL}/auth/register", json={
                "username": username.value,
                "password": password.value
            })

            if r.status_code == 200:
                auth_message.value = "Пользователь зарегистрирован"
            else:
                auth_message.value = r.json().get("detail", "Ошибка")

        except Exception as ex:
            auth_message.value = str(ex)

        page.update()

    def login(e):
        r = requests.post(f"{API_URL}/auth/login", json={
            "username": username.value,
            "password": password.value
        })

        if r.status_code == 200:
            page.clean()
            build_main_page()
        else:
            auth_message.value = "Неверный логин или пароль"
            page.update()

    # ---------------- FILE PICKER ----------------

    selected_file = ft.Text()
    result_text = ft.Text()

    image_preview = ft.Image(src="", width=350, height=250)

    def on_file_selected(e):
        if e.files:
            file = e.files[0]
            selected_file.value = file.name
            image_preview.src = file.path
            page.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_file_selected
    page.overlay.append(file_picker)

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False)

    # ---------------- ANALYZE ----------------

    def analyze(e):

        if not file_picker.result:
            result_text.value = "Сначала выберите изображение"
            page.update()
            return

        file = file_picker.result.files[0]

        files = {"file": open(file.path, "rb")}
        data = {"user_id": current_user_id}

        r = requests.post(f"{API_URL}/analyze", files=files, data=data)

        if r.status_code == 200:
            result_text.value = r.json().get("result")
        else:
            result_text.value = "Ошибка анализа"

        page.update()

    # ---------------- UI BLOCK ----------------

    def upload_block():
        return ft.Container(
            width=400,
            height=180,
            border=ft.border.all(2, "grey"),
            border_radius=10,
            content=ft.Column(
                [
                    ft.Text("Выберите изображение", size=16),
                    ft.ElevatedButton("Выбрать файл", on_click=pick_file),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    # ---------------- MAIN PAGE ----------------

    def build_main_page():

        page.add(

            ft.Column(

                [
                    ft.Text(
                        "Система анализа объектов культурного наследия",
                        size=22,
                        weight="bold"
                    ),

                    ft.Divider(),

                    ft.Text("Загрузка изображения", size=18),

                    upload_block(),

                    selected_file,

                    image_preview,

                    ft.ElevatedButton("Анализировать", on_click=analyze),

                    result_text,

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        )

    # ---------------- AUTH PAGE ----------------

    def build_auth_page():

        page.add(

            ft.Column(

                [
                    ft.Text("Авторизация", size=26, weight="bold"),

                    username,
                    password,

                    ft.Row(
                        [
                            ft.ElevatedButton("Регистрация", on_click=register),
                            ft.ElevatedButton("Войти", on_click=login),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),

                    auth_message

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        )

    build_auth_page()


ft.app(target=main)