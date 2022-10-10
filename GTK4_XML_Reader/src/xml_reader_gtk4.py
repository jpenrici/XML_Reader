# -*- Mode: Python3; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-
'''
    Simple XML and SVG file reader.
'''

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio
from xml_reader import XmlReader

path = "./example.xml"

@Gtk.Template(filename='xml_reader_gtk4.ui')
class XmlReaderWindow(Gtk.ApplicationWindow):

    __gtype_name__ = 'XmlReaderWindow'

    lblStatus = Gtk.Template.Child("lblStatus")
    textView = Gtk.Template.Child("textview")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.props.title = "XML Reader - Experimental"


class XmlReaderApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='org.gnome.XmlReader',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('openFile', self.on_open_file_action)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = XmlReaderWindow(application=self)            
            self.win.present()

    def on_about_action(self, widget, _):
        about = AboutDialog(self.props.active_window)
        about.present()

    def on_open_file_action(self, widget, _):
        fchooser = OpenXml(self.props.active_window)
        btn_select = fchooser.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        btn_select.connect('clicked', self.update)

    def update(self, widget):
        global path
        self.win.lblStatus.set_text(path.split('/')[-1])
        print("Selected:", path)

        data = []
        buffer = ""
        f = path.strip().lower()
        if f.endswith(".svg"):
            xml = XmlReader(path, ['rect', 'path', 'ellipse'])
            data = xml.prepare()
            for i in data:
                buffer += "{0} : {1}\n".format(i['tag'], i['style'])
        if f.endswith(".xml"):
            xml = XmlReader(path)
            data = xml.prepare()
            for i in data:
                buffer += i + "\n"
        self.win.textView.get_buffer().set_text(buffer)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


class OpenXml(Gtk.FileChooserDialog):
    
    def __init__(self, parent):
        super().__init__(transient_for=parent, use_header_bar=True)
        self.set_title("Open File")
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.add_buttons("_Select", Gtk.ResponseType.OK)
        self.connect('response', self.select)
        self.set_select_multiple(False)
        self.set_modal(True)

        filter_xml = Gtk.FileFilter()
        filter_xml.set_name("Xml files")
        filter_xml.add_mime_type("text/xml")
        filter_xml.add_pattern("*.xml")

        filter_svg = Gtk.FileFilter()
        filter_svg.set_name("SVG files")
        filter_svg.add_mime_type("text/svg")
        filter_svg.add_pattern("*.svg")        

        self.add_filter(filter_xml)
        self.add_filter(filter_svg)

        self.show()

    def select(self, widget, response):
        global path
        if response == Gtk.ResponseType.OK:
            path = self.get_file().get_path()
            self.close()


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Xml Reader'
        self.props.version = "0.1.0"
        self.props.authors = ['jpenrici']
        self.props.copyright = '2022 jpenrici'
        self.props.logo_icon_name = 'org.gnome.XmlReader'
        self.props.modal = True
        self.set_transient_for(parent)            


def gui():
    app = XmlReaderApplication()
    return app.run()


if __name__ == '__main__':
    gui()
