from gi.repository import Gtk

# from src.model import Work


def create_entry(text: str) -> Gtk.Entry:
    entry = Gtk.Entry()
    entry.set_placeholder_text(text=text)
    return entry


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
            # result = self.parent.repository.insert(Work(
            #     date=self.date_entry.get_text(), tag=self.tag_entry.get_text(), details=self.detail_entry.get_text()
            # ))
            entry = (
                f"random{len(self.parent.task_list) + 1}",
                self.date_entry.get_text(),
                self.tag_entry.get_text(),
                self.detail_entry.get_text()
            )
            self.parent.task_list.append(entry)

        dialog.close()
