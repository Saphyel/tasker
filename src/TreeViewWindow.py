from gi.repository import Gtk
# from pymongo import MongoClient

# from src.model import Search
# from src.repository import WorkRepository
# from src.settings import Settings
from src.widgets.NewTaskDialog import NewTaskDialog

# settings = Settings()
# client: MongoClient = MongoClient(settings.database_uri)

task_list_db = [
    ("random1", "2022-11-24 12:30:00", "Football", "Watch something"),
    ("random2", "2022-11-24 13:30:00", "Videogames", "Watch some gamers"),
    ("random3", "2022-11-25 12:30:00", "Python", "Python 4 release!"),
    ("random4", "2022-11-26 12:30:00", "Shop", "Buy chocolate"),
    ("random5", "2022-11-26 13:30:00", "Secret", "reveal the fire"),
]


def create_button(label: str, icon_name: str | None = None) -> Gtk.Button:
    button = Gtk.Button(label=label)
    if icon_name:
        button.set_icon_name(icon_name=icon_name)
    return button


class TreeViewWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.repository = WorkRepository(client.task)

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
        # task_list_db = self.repository.find(Search())
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
