#!/usr/bin/env python3

# Copyright (C) 2013 anonymous <brainpower@gulli.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#TODO:
# - make every page of installergui a own class
# - noconfirm when installing additional pkgs?


import sys, os, threading

from gi.repository import Gtk, Vte, GLib, Gdk, GObject
from archinstallergui import ArchInstallerGui


def feed_command(cmd):
	return term.feed_child(cmd, len(cmd))

def feed_archey(bt):
	feed_command("archey\n")

def main():
	GObject.threads_init()
	Gdk.threads_init()
	win = ArchInstallerGui()

	win.resize(600,700)
	win.set_size_request(1024,756)
	win.connect("cancel", Gtk.main_quit)
	win.connect("close", Gtk.main_quit)
	win.show_all()

	sys.exit(Gtk.main())


if __name__ == "__main__":
	main()
