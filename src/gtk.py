import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gtk, Gio

Adw.init()

task_list_db = [
    ("random1", "2022-11-24 12:30:00", "Football", "Watch something"),
    ("random2", "2022-11-24 13:30:00", "Videogames", "Watch some gamers"),
    ("random3", "2022-11-25 12:30:00", "Python", "Python 4 release!"),
    ("random4", "2022-11-26 12:30:00", "Shop", "Buy chocolate"),
    ("random5", "2022-11-26 13:30:00", "Secret", "reveal the fire"),
]


def create_entry(text: str) -> Gtk.Entry:
    entry = Gtk.Entry()
    entry.set_placeholder_text(text=text)
    return entry


def create_button(label: str, icon_name: str | None = None) -> Gtk.Button:
    button = Gtk.Button(label=label)
    if icon_name:
        button.set_icon_name(icon_name=icon_name)
    return button


class NewTaskDialog(Gtk.Dialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent = kwargs.get('transient_for')

        self.set_title(title='New task')
        self.use_header_bar = True
        self.connect('response', self.dialog_response)
        self.set_modal(modal=True)

        self.set_width = 683
        self.set_height = 384

        self.add_buttons('_Cancel', Gtk.ResponseType.CANCEL, '_Add', Gtk.ResponseType.OK)

        self.get_widget_for_response(response_id=Gtk.ResponseType.OK).get_style_context().add_class(
            class_name='suggested-action'
        )
        self.get_widget_for_response(response_id=Gtk.ResponseType.CANCEL).get_style_context().add_class(
            class_name='destructive-action'
        )

        content_area = self.get_content_area()
        content_area.set_orientation(orientation=Gtk.Orientation.VERTICAL)
        content_area.set_spacing(spacing=14)
        content_area.set_margin_top(margin=8)
        content_area.set_margin_end(margin=8)
        content_area.set_margin_bottom(margin=8)
        content_area.set_margin_start(margin=8)

        self.date_entry = create_entry("Date:")
        content_area.append(child=self.date_entry)

        self.tag_entry = create_entry("Tag:")
        content_area.append(child=self.tag_entry)

        self.detail_entry = create_entry("Details:")
        content_area.append(child=self.detail_entry)

    def dialog_response(self, dialog: Gtk.Dialog, response: int) -> None:
        if response == Gtk.ResponseType.OK:
            entry = (
                f"random{len(self.parent.task_list) + 1}",
                self.date_entry.get_text(),
                self.tag_entry.get_text(),
                self.detail_entry.get_text()
            )
            self.parent.task_list.append(entry)

        dialog.close()


class TreeViewWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='List of tasks')
        self.set_default_size(width=int(1360 / 2), height=int(764 / 2))
        self.set_size_request(width=int(1360 / 2), height=int(764 / 2))

        headerbar = Gtk.HeaderBar()
        self.set_titlebar(titlebar=headerbar)

        button_add_task = create_button('Add', 'list-add-symbolic')
        button_add_task.connect('clicked', self.add_task_dialog)
        headerbar.pack_start(child=button_add_task)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(margin=8)
        vbox.set_margin_end(margin=8)
        vbox.set_margin_bottom(margin=8)
        vbox.set_margin_start(margin=8)
        self.set_child(child=vbox)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox.append(child=hbox)

        scrolledwindow = Gtk.ScrolledWindow()
        vbox.append(child=scrolledwindow)

        self.task_list = Gtk.ListStore(str, str, str, str)
        for task in task_list_db:
            self.task_list.append(task)

        self.tree_view = Gtk.TreeView(model=self.task_list)
        self.tree_view.set_vexpand(expand=True)
        scrolledwindow.set_child(child=self.tree_view)

        for column_index, title in enumerate(('ID', 'Date', 'Tag', 'Detail')):
            tree_view_column = Gtk.TreeViewColumn(title=title, cell_renderer=Gtk.CellRendererText(), text=column_index)
            self.tree_view.append_column(tree_view_column)

        button_remove = create_button('Remove', 'user-trash-symbolic')
        hbox.append(child=button_remove)
        button_remove.connect('clicked', self.remove_task, self.tree_view.get_selection())

    def add_task_dialog(self, button: Gtk.Button) -> None:
        custom_dialog = NewTaskDialog(transient_for=self, use_header_bar=True)
        custom_dialog.present()

    def remove_task(self, button: Gtk.Button, selection: Gtk.TreeSelection) -> None:
        model, index = selection.get_selected()
        self.task_list.remove(index)


class TasksApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='tasks.app', flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = TreeViewWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)


app = TasksApplication()

if __name__ == '__main__':
    import sys

    app.run(sys.argv)
