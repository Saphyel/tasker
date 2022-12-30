import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from src.TreeViewWindow import TreeViewWindow

from gi.repository import Adw, Gtk, Gio

Adw.init()


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
