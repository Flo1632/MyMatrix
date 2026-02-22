import flet as ft
import os
import json
from datetime import datetime
from dataclasses import dataclass


class MatrixContainer(ft.Container):
    def __init__(self,title,color, inhalte, change_view=None, is_mobile=False):

        self.inhalte_text = ft.Text(inhalte, size=16)
        self.title = ft.Text(title, size=20, weight=ft.FontWeight.BOLD)
        self.content_column = ft.ListView(
            controls=[
                self.inhalte_text
            ],
            spacing=2,
            padding=10,
            expand=True
        )
        super().__init__(
        border_radius = ft.BorderRadius.all(20),
        width=None if is_mobile else 600,
        height=150 if is_mobile else 200,
        bgcolor = color,
        expand = True,
        padding = 20,
        content = ft.Column([self.title, self.content_column],
                            expand=True),

        on_click=change_view,
        ink=True
        #self.inhalte = ft.Text(value=inhalte, size=12)
        )

@dataclass
class Task:
    text: str
    checked: bool = False

async def main(page: ft.Page):
    page.title = 'Task Matrix'
    page.padding = 10 if page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.ANDROID] else 20
    page.scroll = ft.ScrollMode.AUTO
    headline = ft.Text(value='Your Matrix', size=20)
    date_display = ft.Text(value='', size=16, color='blue')
    notification_text=ft.Text(value='',size=16, color=ft.Colors.RED)

    prefs = ft.SharedPreferences()

    # Listenvariablen
    list_dringend_wichtig = []
    list_nicht_wichtig_dringend = []
    list_nicht_wichtig_nicht_dringend = []
    list_wichtig_nicht_dringend = []

    # Gespeicherte Daten laden
    saved_urgent = await prefs.get("tasks_urgent")
    if saved_urgent:
        list_dringend_wichtig = [Task(text=t) for t in json.loads(saved_urgent)]

    saved_not_urgent = await prefs.get("tasks_not_urgent")
    if saved_not_urgent:
        list_nicht_wichtig_dringend = [Task(text=t) for t in json.loads(saved_not_urgent)]

    saved_eliminate = await prefs.get("tasks_eliminate")
    if saved_eliminate:
        list_nicht_wichtig_nicht_dringend = [Task(text=t) for t in json.loads(saved_eliminate)]

    saved_schedule = await prefs.get("tasks_schedule")
    if saved_schedule:
        list_wichtig_nicht_dringend = [Task(text=t) for t in json.loads(saved_schedule)]


    def update_matrix_display(container, task_list):
        """Aktualisiert die Anzeige eines Matrix-Containers"""
        container.content_column.controls = [
            ft.Column([
                ft.Checkbox(
                    label=task.text,
                    value=task.checked,
                    on_change=lambda e, t=task: handle_checkbox_change(e, t)
                )
                for task in reversed(task_list)
            ])
        ]

    def handle_input(e):
        # Wir prüfen, ob das Feld nicht leer ist
        if e.control.value:
            # Aktuelles Datum/Uhrzeit formatieren
            now = datetime.now().strftime("%d.%m.%Y - %H:%M")
            date_display.value = f"{now}"
        else:
            date_display.value = "Feld wurde geleert."

        # UI aktualisieren
        page.update()

    display_text = 'Your tasks will be displayed here'

    def handle_checkbox_change(e, task):
        task.checked = e.control.value
        # Optional: UI aktualisieren falls nötig
        page.update()

    # ✅ Detail View Creation
    def create_detail_view(category_name, task_list, bgcolor):

        return ft.View(
            route="/detail",
            controls=[
                ft.AppBar(
                    title=ft.Text(category_name, size=20, weight=ft.FontWeight.BOLD),
                    bgcolor=bgcolor,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_to_main)
                ),
                ft.ListView(
                    controls=[
                        ft.Checkbox(
                            label=task.text,
                            value=task.checked,
                            on_change=lambda e, t=task: handle_checkbox_change(e, t),
                            label_style=ft.TextStyle(size=16)
                        )
                        for task in reversed(task_list)
                    ],
                    expand=True,
                    spacing=10,
                    padding=20
                )
            ]
        )

    # ✅ Explanation Variables

    do = """
STRATEGY: DO IMMEDIATELY
Description: These are critical tasks that require immediate attention. They usually involve deadlines, crises, or pressing problems. Leaving these undone leads to immediate negative consequences.
    """
    schedule = """
STRATEGY: SCHEDULE / DECIDE
Description: This is the 'Growth' quadrant. These tasks are vital for long-term success but don't have a ticking clock. If ignored, they eventually become IMPORTANT & URGENT (DO IMMEDIATELY) crises.
    """
    delegate = """
STRATEGY: DELEGATE
Description: The 'Deception' quadrant. These tasks feel pressing but are actually not part of your responsibility or work. They are often interruptions or the part of the work of others.
    """

    eliminate = """
STRATEGY: ELIMINATE / DELETE
Description: These are time-wasting activities. They offer no value and usually serve as a form of procrastination. Aim to minimize or remove these entirely from your schedule.
    """


    headline_dringend_wichtig=ft.Text(value='Do First (Urgent & Important)', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,text_align=ft.TextAlign.LEFT)
    text_dringend_wichtig=ft.Text(value=do, text_align=ft.TextAlign.LEFT)
    headline_dringend_nicht_wichtig=ft.Text(value='Delegate (Urgent & Not Important)', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align=ft.TextAlign.LEFT)
    text_dringend_nicht_wichtig=ft.Text(value=delegate, text_align=ft.TextAlign.LEFT)
    headline_nicht_dringend_wichtig=ft.Text(value='Schedule (Not Urgent & Important)', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align=ft.TextAlign.LEFT)
    text_nicht_dringend_wichtig=ft.Text(value=schedule, text_align=ft.TextAlign.LEFT)
    headline_nicht_dringend_nicht_wichtig=ft.Text(value='Eliminate/Delete (Not Urgent & Not Important)', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align=ft.TextAlign.LEFT)
    text_nicht_dringend_nicht_wichtig=ft.Text(value=eliminate, text_align=ft.TextAlign.LEFT)

    # ✅ Info View Creation
    def create_info_view():

        return ft.View(
            route="/info",
            controls=[
                ft.AppBar(
                    title=ft.Text(value='How to use'),
                    bgcolor=ft.Colors.PURPLE,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_to_main)
                ),
                ft.ListView(
                    controls=[
                        headline_dringend_wichtig,
                        text_dringend_wichtig,
                        headline_dringend_nicht_wichtig,
                        text_dringend_nicht_wichtig,
                        headline_nicht_dringend_wichtig,
                        text_nicht_dringend_wichtig,
                        headline_nicht_dringend_nicht_wichtig,
                        text_nicht_dringend_nicht_wichtig
                    ],
                    expand = True,
                    spacing = 10,
                    padding = 20
                )
            ]
        )

    def back_to_main(e):
        page.views.pop()
        # ✅ Hier alle Container aktualisieren
        update_matrix_display(dringend_wichtig, list_dringend_wichtig)
        update_matrix_display(nicht_wichtig_dringend, list_nicht_wichtig_dringend)
        update_matrix_display(nicht_wichtig_nicht_dringend, list_nicht_wichtig_nicht_dringend)
        update_matrix_display(wichtig_nicht_dringend, list_wichtig_nicht_dringend)
        page.update()


    def open_info_view(e):
        page.views.append(
            create_info_view()
        )
        page.update()

    def open_detail_view(category_name, task_list, bgcolor):
        page.views.append(
            create_detail_view(category_name, task_list, bgcolor)
        )
        page.update()

    # is_mobile definieren
    is_mobile = page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.ANDROID]

    #MatrixContainer wird mit Entry verknüpft, damit die Eingabe in der Matrix angezeigt wird + on_click Events
    dringend_wichtig = MatrixContainer('Important & Urgent', ft.Colors.RED_ACCENT, display_text, change_view=lambda e: open_detail_view(
            'Important & Urgent',
            list_dringend_wichtig,
            ft.Colors.RED_ACCENT
        ), is_mobile=is_mobile)
    nicht_wichtig_dringend = MatrixContainer('Not Important, but Urgent', ft.Colors.LIGHT_BLUE, display_text,
                                             change_view=lambda e: open_detail_view(
                                                 'Not Important, but Urgent',
                                                 list_nicht_wichtig_dringend,
                                                 ft.Colors.LIGHT_BLUE
                                             ), is_mobile=is_mobile
                                             )
    nicht_wichtig_nicht_dringend = MatrixContainer('Not Important, Not Urgent', ft.Colors.GREY, display_text,change_view=lambda e: open_detail_view(
            'Not Important, Not Urgent',
            list_nicht_wichtig_nicht_dringend,
            ft.Colors.GREY
        ), is_mobile=is_mobile)
    wichtig_nicht_dringend = MatrixContainer('Important, but not Urgent', ft.Colors.ORANGE_ACCENT, display_text, change_view=lambda e: open_detail_view(
            'Important, but not Urgent',
            list_wichtig_nicht_dringend,
            ft.Colors.ORANGE_ACCENT
        ), is_mobile=is_mobile)


    # Dropdown Options in Funktion setzen
    def get_options():
        options = [
            dringend_wichtig,
            nicht_wichtig_dringend,
            nicht_wichtig_nicht_dringend,
            wichtig_nicht_dringend,
        ]
        return [
            ft.DropdownOption(
                key=option.title.value,
                content=ft.Text(value=option.title.value, color=option.bgcolor),
            )
            for option in options
        ]

    # Dropdown Event Handler
    def handle_dropdown_select(e: ft.Event[ft.Dropdown]):
        #e.control kann genutzt werden, weil e vom Eventhandler verwendet wird
        e.control.color = e.control.value
        notification_text.value=''
        page.update()


    dropdown = ft.Dropdown(
            editable=True,
            label="Options",
            options=get_options(),
            on_select=handle_dropdown_select,
        )

    async def list_construct(e):
        selected_category = dropdown.value
        task = Task(text=task_entry.value + ' - ' + date_display.value)
        if date_display.value and task_entry.value:
            match selected_category:
                case 'Important & Urgent':
                    list_dringend_wichtig.append(task)
                    update_matrix_display(dringend_wichtig, list_dringend_wichtig)
                    await prefs.set("tasks_urgent", json.dumps([t.text for t in list_dringend_wichtig]))
                case 'Not Important, but Urgent':
                    list_nicht_wichtig_dringend.append(task)
                    update_matrix_display(nicht_wichtig_dringend, list_nicht_wichtig_dringend)
                    await prefs.set("tasks_not_urgent", json.dumps([t.text for t in list_nicht_wichtig_dringend]))
                case 'Not Important, Not Urgent':
                    list_nicht_wichtig_nicht_dringend.append(task)
                    update_matrix_display(nicht_wichtig_nicht_dringend, list_nicht_wichtig_nicht_dringend)
                    await prefs.set("tasks_eliminate", json.dumps([t.text for t in list_nicht_wichtig_nicht_dringend]))
                case 'Important, but not Urgent':
                    list_wichtig_nicht_dringend.append(task)
                    update_matrix_display(wichtig_nicht_dringend, list_wichtig_nicht_dringend)
                    await prefs.set("tasks_schedule", json.dumps([t.text for t in list_wichtig_nicht_dringend]))
                case _:
                    notification_text.value = 'Choose an Option'  # Hier nochmal was anderes eingeben
        page.update()
        return list_dringend_wichtig, list_nicht_wichtig_dringend, list_nicht_wichtig_nicht_dringend, list_wichtig_nicht_dringend


    async def remove_task (e):

        selected_category = dropdown.value
        # hier noch logik einfügen, falls es keine Werte in den Kategorien gibt

        match selected_category:
            case 'Important & Urgent':
                list_dringend_wichtig[:] = [t for t in list_dringend_wichtig if not t.checked]
                update_matrix_display(dringend_wichtig, list_dringend_wichtig)
                await prefs.set("tasks_urgent", json.dumps([t.text for t in list_dringend_wichtig]))
            case 'Not Important, but Urgent':
                list_nicht_wichtig_dringend [:] = [t for t in list_nicht_wichtig_dringend if not t.checked]
                update_matrix_display(nicht_wichtig_dringend, list_nicht_wichtig_dringend)
                await prefs.set("tasks_not_urgent", json.dumps([t.text for t in list_nicht_wichtig_dringend]))
            case 'Not Important, Not Urgent':
                list_nicht_wichtig_nicht_dringend[:]= [t for t in list_nicht_wichtig_nicht_dringend if not t.checked]
                update_matrix_display(nicht_wichtig_nicht_dringend, list_nicht_wichtig_nicht_dringend)
                await prefs.set("tasks_eliminate", json.dumps([t.text for t in list_nicht_wichtig_nicht_dringend]))
            case 'Important, but not Urgent':
                list_wichtig_nicht_dringend[:] = [t for t in list_wichtig_nicht_dringend if not t.checked]
                update_matrix_display(wichtig_nicht_dringend, list_wichtig_nicht_dringend)
                await prefs.set("tasks_schedule", json.dumps([t.text for t in list_wichtig_nicht_dringend]))
            case _:
                print('Oh man, das funktioniert nicht')
                notification_text.value ='Choose an Option'
        page.update()
        return list_dringend_wichtig, list_nicht_wichtig_dringend, list_nicht_wichtig_nicht_dringend, list_wichtig_nicht_dringend

    # Entry wird mit Datum verknüpft
    # Entry mit Datum setzen
    task_entry = ft.TextField(label='Enter your task here', on_change=handle_input)
    send_button = ft.Button('Submit', on_click=list_construct)
    remove_button = ft.Button('Remove Task', on_click=remove_task)
    info_button = ft.Button('Info', icon=ft.Icons.INFO, on_click=open_info_view)
    # Baut Matrix basierend auf der Platform

    if is_mobile:
        meine_matrix = ft.Column(
            controls=[
                dringend_wichtig,
                nicht_wichtig_dringend,
                wichtig_nicht_dringend,
                nicht_wichtig_nicht_dringend
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    else:
        meine_matrix = ft.Container(
            content =ft.Row(
                controls=[
                ft.Column(controls=
                        [dringend_wichtig,
                         ft.Divider(color=ft.Colors.BLACK),
                        nicht_wichtig_dringend],
                    expand=True
                ),
                ft.Container(bgcolor=ft.Colors.GREY, width=2, height=450),
                ft.Column(
                    controls=
                    [nicht_wichtig_nicht_dringend,
                     ft.Divider(color=ft.Colors.BLACK),
                     wichtig_nicht_dringend],
                    expand=True
                ),
            ],
                expand=True
            )

        )

    if is_mobile:
        main_view = ft.View(
            route="/",
            controls=[headline,
                      task_entry,
                      ft.Row(controls=[dropdown, info_button]),
                      ft.Row(controls=[send_button, remove_button],
                             spacing=10),
                      notification_text,
                      meine_matrix
                      ]
        )
    else:
        main_view = ft.View(
            route="/",
            controls=[headline,
                task_entry,
                ft.Row(controls=[dropdown,info_button,notification_text]),
                ft.Row(controls=[send_button, remove_button],
                       spacing=10),
                meine_matrix
            ]
        )
    def route_change(route):
        page.views.clear()
        page.views.append(main_view)
        if page.route == "/detail":
            # Wird vom Detail-View selbst gehandhabt
            pass
        elif page.route == "/info":
            pass
        page.update()

    page.on_route_change = route_change
    page.views.append(main_view)
    page.go(page.route)
port = int(os.environ.get("PORT", 8080))
ft.run(main, view=ft.AppView.WEB_BROWSER, port=8080)
