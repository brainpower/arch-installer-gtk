
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

import os, time, threading
from gi.repository import Gtk, Vte, GLib, Gio, GObject

import utils

class ArchInstallerGui(Gtk.Assistant):
	"""main GUI of the arch installer"""

	def __init__(self):
		Gtk.Assistant.__init__(self)

		self.pacman = utils.Pacman()
		self.gsett = Gio.Settings("org.gnome.desktop.interface")
		self.prefix = "/mnt"
		self.scriptfn = "/tmp/ai_install_commands.sh"

		self.create_page1()
		self.create_page2()
		self.create_page3()
		self.create_page3_5()
		self.create_page4()
		self.create_page5()

		self.create_page_summary()

		self.connect("prepare", self.on_page_change)

################################################################################
                                # pages #
                                #########


	def create_page1(self):
		""" creates the welcoming page """
		self.page1 = Gtk.Grid()

		text = Gtk.Label("\nArch Install Wizard\n"
		                 "\n"
		                 "This GUI will guide you through the installation of arch linux.\n\n"
		                 "It is advised to read the 'Installation Guide' on wiki.archlinux.org beforehand,\n"
		                 "since the installer does not cover all parts of the installation (yet).\n\n"
		                 "Whenever this 'Installer' does something other than gathering information,\n"
		                 "it'll do that using a vte, so you can see, what happens to your system.\n"
		                 "\n"
		                 "There are a few things you should pay attention to:\n"
		                 "\n"
		                 " - Don't forget to select a bootloader package, for example 'grub-bios' \n"
		                 "   and to configure the bootloader after this 'Installer' is done.\n"
		                 "\n"
		                 " - Please make sure you're connected to the internet.\n"
		                 "\n"
		                 " - You should run this 'Installer' with superuser powers, it won't work otherwise.\n"
		                 "\n"
		                 "Have Fun\n"
		                 " oi_wtf (aka. brainpower)" )

		self.page1.add(text)

		self.append_page(   self.page1)
		self.set_page_title(self.page1, "Welcome")
		self.set_page_type( self.page1, Gtk.AssistantPageType.INTRO)

		self.set_page_complete(self.page1, True)



	def create_page2(self):
		""" creates page2, partitioning """
		self.page2 = Gtk.Grid()

		text = Gtk.Label("\nPartitioning\n"
		                  "\n"
		                  "Go to the main menu on the left and start \"gparted\".\n"
		                  "Use it to partition your harddisk to your liking.\n"
		                  "Of course you can also use any other application to do this.\n"
		                  "And if you\'ve already suitable partitions, you can skip this and hit \'Continue\'.\n"
		                  "\n"
		                  "Most people create two partitions, one smaller of at least 25GB for the / (root-) partition \n"
		                  "and another, usually much bigger one, for the /home partition.\n"
		                  "\n"
		                  "Think about it carefully, since changing partitions once the system is installed, is a pain in the ass.\n"
		                  "\n"
		                  "If you have suitable partitions, click \'Continue\'.")

		self.page2.add(text)

		self.append_page(   self.page2)
		self.set_page_title(self.page2, "Partitioning")
		self.set_page_type( self.page2, Gtk.AssistantPageType.CONTENT)

		self.set_page_complete(self.page2, True)



	def create_page3(self):
		""" creates page3, mount points """
		self.page3 = Gtk.Grid()

		self.page3_ls = Gtk.ListStore(bool, str, str, bool, str)
		type_lst = Gtk.ListStore(str)
		bl_lst = Gtk.ListStore(str)
		for x in utils.get_filesystem_types():
			type_lst.append([x])

		tv = Gtk.TreeView(self.page3_ls)
		text = Gtk.Label("Set your partitions mountpoints.\n"
		                 "The / (root) mountpoint is required.\n ")
		cb = Gtk.ComboBox()
		text.set_hexpand(True)
		text.set_alignment(.0,.0)

		self.add_toggle_column_to_tv(tv, "use", 0, self.on_page3_use_toggled)
		self.add_text_column_to_tv  (tv, "device", 1)
		self.add_combo_column_to_tv (tv, "type", 2, type_lst, self.on_page3_type_changed)
		self.add_toggle_column_to_tv(tv, "format", 3, self.on_page3_format_toggled)
		self.add_text_column_to_tv  (tv, "mountpoint", 4, self.on_page3_mountpoint_edited)

		self.page3.attach(text, 0, 0, 1, 1)
		self.page3.attach(tv, 0, 1, 1, 1)

		self.append_page(   self.page3)
		self.set_page_title(self.page3, "mount points")
		self.set_page_type( self.page3, Gtk.AssistantPageType.CONTENT)

		#DEBUG:
		self.set_page_complete(self.page3, True)


	def create_page3_5(self):
		""" creates page3.5, configure system"""
		self.page3_5 = Gtk.Grid()
		self.page3_5.set_row_spacing(5)

		label = Gtk.Label("Enter some common settings\n\n"
		                  "For information on the values of the following settings, visit: \n"
		                  "https://wiki.archlinux.org/index.php/Installation_Guide#Configure_the_system \n\n"
		                  "If you leave them empty, you'll have to set them yourself later.")
		label.set_alignment(.0,.0)

		label1 = Gtk.Label("Hostname: ")
		self.e_host = Gtk.Entry()

		label2 = Gtk.Label("Timezone: ")
		label3 = Gtk.Label("( 'Zone/Subzone', e.g. 'Europe/Berlin') ")
		self.e_tz = Gtk.Entry()

		label4 = Gtk.Label("Locale: ")
		label5 = Gtk.Label("( e.g. 'en_US.UTF-8') ")
		self.e_loc = Gtk.Entry()

		self.page3_5.attach(label,       0, 0, 4, 1)
		self.page3_5.attach(label1,      0, 2, 1, 1)
		self.page3_5.attach(self.e_host, 1, 2, 1, 1)
		self.page3_5.attach(label2,      0, 3, 1, 1)
		self.page3_5.attach(self.e_tz,   1, 3, 1, 1)
		self.page3_5.attach(label3,      2, 3, 1, 1)
		self.page3_5.attach(label4,      0, 4, 1, 1)
		self.page3_5.attach(self.e_loc,  1, 4, 1, 1)
		self.page3_5.attach(label5,      2, 4, 1, 1)

		self.append_page(   self.page3_5)
		self.set_page_title(self.page3_5, "configure system")
		self.set_page_type( self.page3_5, Gtk.AssistantPageType.CONTENT)

		self.set_page_complete(self.page3_5, True)

	def create_page4(self):
		""" creates page4, packages """
		self.page4 = Gtk.Grid()
		self.page4.set_column_homogeneous(False)
		text = Gtk.Label("Select packages to be installed now. Packages in base are preselected.\nHit 'Apply' to start installation.")
		text.set_hexpand(True)
		text.set_alignment(.0,.0)

		self.page4_ls2 = Gtk.ListStore(str)
		self.page4_ls3 = Gtk.ListStore(bool,str)
		self.page4_tv = Gtk.TreeView(self.page4_ls2)
		self.page4_tv2 = Gtk.TreeView()
		self.page4_tv3 = Gtk.TreeView(self.page4_ls3)

		sw = Gtk.ScrolledWindow()
		sw.set_hexpand(True)
		sw.set_vexpand(True)
		sw.add(self.page4_tv2)
		sw2 = Gtk.ScrolledWindow()
		sw2.set_vexpand(True)
		sw2.set_size_request(150,100)
		sw2.add(self.page4_tv3)

		self.page4_ls = {}
		for repo in self.pacman.get_repos():
			it = self.page4_ls2.append([repo])
			self.page4_ls[repo] = Gtk.ListStore(bool,str,str,str);
			for p in self.pacman.get_package_list(repo):
				self.page4_ls[repo].append(p)

			for group in self.pacman.get_groups()[repo]:
				self.page4_ls3.append([False, group])


		self.page4_activate_all_pkgs_of("core", "base")

		self.add_toggle_column_to_tv(self.page4_tv2, " ", 0, self.on_page4_install_toggled)
		self.add_text_column_to_tv  (self.page4_tv2, "name", 1)
		self.add_text_column_to_tv  (self.page4_tv2, "version", 2)
		self.add_text_column_to_tv  (self.page4_tv2, "description", 3)

		self.add_text_column_to_tv  (self.page4_tv, "   repos", 0)
		self.add_toggle_column_to_tv(self.page4_tv3, "", 0, self.on_page4_group_toggled)
		self.add_text_column_to_tv  (self.page4_tv3, "groups", 1)

		self.page4_tv.get_selection().connect("changed", self.on_page4_tv_selection_changed)

		self.page4.attach(text,          0, 0, 10, 1)
		self.page4.attach(self.page4_tv, 0, 1, 1, 1)
		self.page4.attach(sw2,           0, 2, 1, 1)
		self.page4.attach(sw,            1, 1, 9, 2)
		self.page4.set_column_spacing(5)

		self.append_page(   self.page4)
		self.set_page_title(self.page4, "select packages")
		self.set_page_type( self.page4, Gtk.AssistantPageType.CONFIRM)



	def create_page5(self):
		""" creates page5, package installing """

		self.term = Vte.Terminal()

		self.term.set_font_from_string(self.gsett.get_string("monospace-font-name"))
		self.term.set_emulation("xterm")
		self.term.set_scrollback_lines(-1)

		self.page5 = self.term

		self.append_page(   self.page5)
		self.set_page_title(self.page5, "install packages")

		self.set_page_type( self.page5, Gtk.AssistantPageType.PROGRESS)

	def create_page_summary(self):
		""" creates summary page """
		self.pagex = Gtk.Grid()

		text = Gtk.Label()
		text.set_text("\nFinished!\n"
		              "\n"
		              " - Don't forget to configure your bootloader!\n\n"
		              " - All devices mounted by this installer will stay mounted, \n"
		              "   so you can make changes to your system after closing this 'Installer'.\n"
		              "   So, umount them yourself when you're done.\n"
		              "\n"
		              "See wiki.archlinux.org for further guidance.\n\n"
		              "Have Fun with your freshly installed ArchLinux!" )

		self.pagex.add(text)
		self.append_page(self.pagex)
		self.set_page_title(self.pagex, "Finished")
		self.set_page_type(self.pagex, Gtk.AssistantPageType.SUMMARY)



################################################################################
                   # page-related helper functions #
                   #################################

# page3, mountpoints:

	def page3_check_mountpoints(self):
		complete = False
		for x in self.page3_ls:
			if x[0] and x[4] == "/":
				complete = True
				break
		self.set_page_complete(self.page3, complete )

	def page3_prepare(self):
		self.page3_ls.clear()
		for dev,_type in utils.get_devices():
			self.page3_ls.append([False, dev, _type, False, ""])


# page4, packages:

	def page4_activate_all_pkgs_of(self, repo, group):
		plist = [ p[1] for p in self.pacman.get_package_list(repo, group)]
		for row in self.page4_ls[repo]:
			if row[1] in plist:
				row[0] = True
		for row in self.page4_ls3:
			if row[1] == group:
				row[0] = True

	def page4_deactivate_all_pkgs_of(self, repo, group):
		plist = [ p[1] for p in self.pacman.get_package_list(repo, group)]
		for row in self.page4_ls[repo]:
			if row[1] in plist:
				row[0] = False
		for row in self.page4_ls3:
			if row[1] == group:
				row[0] = False

	def page4_get_all_pkgs_of_group(self, group):
		pkgs = []
		repos = self.pacman.get_repos_of_group(group);
		for repo in repos:
			pkgs += [ p[1] for p in self.pacman.get_package_list(repo, group)]
		return pkgs

	def page4_check_group(self, group):
		pkgs    = self.page4_get_all_pkgs_of_group(group);
		repos   = self.pacman.get_repos_of_group(group)
		pkgs_ls = self.page4_ls;

		all_pkgs_selected = True

		for repo in repos:
			for pkg in pkgs_ls[repo]:
				if pkg[1] in pkgs and not pkg[0]: # if pkg in group, if pkg not selected
					all_pkgs_selected = False

		for g in self.page4_ls3:
			if group == g[1]:
				g[0] = all_pkgs_selected;

	def page4_check_base_group(self):
		for grp in self.page4_ls3:
			if grp[1] == "base" and grp[0]:
				self.set_page_complete(self.page4, True)

	def page4_get_group_by_name(self, name):
		for grp in self.page4_ls3:
			if grp[1] == name:
				return grp


# page5, install process

	def page5_prepare(self, widget, page):
		self.commit()

		self.isf = open(self.scriptfn, "w")
		self.isf.write("function error_msg(){\n"
		               "	echo 'Something went wrong, check the output of the command above for further information'\n"
		               "	echo 'Installation abborted!'\n"
		               "	exit 1\n"
		               "}\n")
		self.isf.write("echo -e '\\nInstalling ArchLinux...'\n")

		self.isf.write("echo -e '\\nMaking filesystems...'\n")
		self.page5_format()

		self.isf.write("echo -e '\\nMounting filesystems...'\n")
		self.page5_mount()

		self.isf.write("echo -e '\\nRunning pacstrap...'\n")
		self.page5_pacstrap()

		self.isf.write("echo -e '\\nInstalling additional packages...'\n")
		self.page5_pacman()

		self.isf.write("echo -e '\\nConfiguring system...'\n")
		self.page5_configure()

		self.isf.write("echo -e '\\n\\nAll done.'\n")

		self.isf.close()
		# run all gathered commands
		self.run_command_in_term(self.term, ["/bin/sh", self.scriptfn,], self.on_page5_exec_complete)

	def page5_pacstrap(self):
		self.base_pkgs = "base"
		if self.page4_get_group_by_name("base-devel")[0]:
			self.base_pkgs += " base-devel"
		self.isf.write("echo '# pacstrap %s %s'\n" % (self.prefix, self.base_pkgs))
		self.isf.write("pacstrap %s %s\n" % (self.prefix, self.base_pkgs))

	def page5_pacman(self):
		pkglst = ""
		pkgign = [ x[1] for x in self.pacman.get_package_list("core", "base")]
		if "base-devel" in self.base_pkgs.split(" "):
			pkgign += [ x[1] for x in self.pacman.get_package_list("core", "base-devel")]

		for repo in self.page4_ls:
			for x in self.page4_ls[repo]:
				if x[0] and not x[1] in pkgign:
					pkglst += " " + x[1]

		if pkglst:
			self.isf.write("echo '# arch-chroot %s pacman -S --noconfirm %s'\n" % (self.prefix,pkglst))
			self.isf.write("arch-chroot %s pacman -S --noconfirm %s\n" % (self.prefix,pkglst))

	def page5_configure(self):
		self.isf.write("echo '# genfstab -p %s >> %s/etc/fstab'\n" % (self.prefix, self.prefix))
		self.isf.write("genfstab -p %s >> %s/etc/fstab\n" % (self.prefix, self.prefix))

		hostname = self.e_host.get_text()
		if hostname:
			self.isf.write("echo '# echo %s > %s/etc/hostname'\n" % (hostname,self.prefix))
			self.isf.write("echo '%s' > %s/etc/hostname\n" % (hostname, self.prefix))

		tz = self.e_tz.get_text()
		if tz:
			self.isf.write("echo '# arch-chroot %s ln -s /usr/share/zoneinfo/%s /etc/localtime'\n" % (self.prefix,tz))
			self.isf.write("arch-chroot %s ln -s /usr/share/zoneinfo/%s /etc/localtime\n" % (self.prefix,tz))

		loc = self.e_loc.get_text()
		if loc:
			self.isf.write("echo '# echo \"LANG=%s\" > %s/etc/locale.conf '\n" % (loc,self.prefix))
			self.isf.write("echo 'LANG=%s' > %s/etc/locale.conf\n" % (loc,self.prefix))

			self.isf.write("echo \# sed -i \\'s/^#\\(%s\\)/\\1/\\' %s/etc/locale.gen\n" % (loc, self.prefix))
			self.isf.write("sed -i 's/^#\\(%s\\)/\\1/' %s/etc/locale.gen\n" % (loc, self.prefix))

			self.isf.write("echo '# arch-chroot %s locale-gen'\n" % self.prefix )
			self.isf.write("arch-chroot %s locale-gen \n" % self.prefix )

		self.isf.write("echo '# arch-chroot %s mkinitcpio -p linux'\n" % self.prefix)
		self.isf.write("arch-chroot %s mkinitcpio -p linux \n" % self.prefix)

		self.isf.write("echo -e '\\nChoose a root password...'\n")
		self.isf.write("echo '# arch-chroot %s passwd'\n" % self.prefix)
		self.isf.write("arch-chroot %s passwd \n" % self.prefix)

	def page5_mount(self):
		#mount all devices as specified on page3

		for x in self.page3_ls: # mount root first
			if x[0] and x[4] == "/":
				self.isf.write("echo '# mount -t %s %s %s%s'\n" %(x[2],x[1],self.prefix,x[4]))
				self.isf.write("mount -t %s %s %s%s || error_msg\n" %(x[2],x[1],self.prefix,x[4]))
				break

		for x in self.page3_ls: # mount all others
			if x[0] and x[4] != "/":
				self.isf.write("echo '# mount -t %s %s %s%s'\n" %(x[2],x[1],self.prefix,x[4]))
				self.isf.write("mount -t %s %s %s%s || error_msg\n" %(x[2],x[1],self.prefix,x[4]))


	def page5_format(self):
		# make filesystems as specified on page3
		for x in self.page3_ls:
			if x[0] and x[3]:
				self.isf.write("echo '# mkfs.%s %s'\n" % (x[2], x[1]))
				self.isf.write("mkfs.%s %s || error_msg\n" % (x[2], x[1]))


	def on_page5_exec_complete(self, t):
		#when done, set complete:
		self.set_page_complete(t, True)



################################################################################
                                # slots #
                                #########

	def on_page_change(self, widget, page):
		if page == self.page3:
			self.page3_prepare()
		elif page == self.page4:
			self.page4_check_base_group()
		elif page == self.page5:
			GObject.timeout_add(10, self.page5_prepare, widget, page)
			#self.page5_prepare(widget, page)

	#def on_page3_device_edited(self, widget, path, text):
	#	self.page3_ls[path][1] = text

	def on_page3_use_toggled(self, widget, path):
		self.page3_ls[path][0] = not self.page3_ls[path][0]
		self.page3_check_mountpoints()


	def on_page3_format_toggled(self, widget, path):
		self.page3_ls[path][3] = not self.page3_ls[path][3]

	def on_page3_type_changed(self, widget, path, text):
		self.page3_ls[path][2] = text

	def on_page3_mountpoint_edited(self, widget, path, text):
		self.page3_ls[path][4] = text
		self.page3_check_mountpoints()

	#~ def on_page3_tv_selection_changed(self, selection):
		#~ pass

	def on_page4_install_toggled(self, widget, path):
		model = self.page4_tv2.get_model()
		model[path][0] = not model[path][0]

		#~ for r in self.pacman.get_repos_of_pkg(model[path][1]):
			#~ self.check_groups(r)
		for g in self.pacman.get_groups_of_pkg(model[path][1]):
			self.page4_check_group(g)

		self.page4_check_base_group()

	def on_page4_tv_selection_changed(self, selection):
		model,it = selection.get_selected()
		repo = model[it][0]
		self.page4_tv2.set_model(self.page4_ls[repo])


	def on_page4_group_toggled(self, widget, path):
		group = self.page4_ls3[path][1];
		repos  = self.pacman.get_repos_of_group(group)
		if self.page4_ls3[path][0]:
			for r in repos:
				self.page4_deactivate_all_pkgs_of(r, group)
		else:
			for r in repos:
				self.page4_activate_all_pkgs_of(r, group)

		self.page4_check_base_group()



################################################################################
                             # static members #
                             ##################

	@staticmethod
	def add_text_column_to_tv(tv, title, column, on_edit=None):
		r = Gtk.CellRendererText()
		if on_edit: # if on_edit provided, text is editable, if not, it's not
			r.set_property("editable", True)
			r.connect("edited", on_edit)
		c = Gtk.TreeViewColumn(title, r, text=column)
		tv.append_column(c)

	@staticmethod
	def add_toggle_column_to_tv(tv, title, column, on_toggle=None):
		r = Gtk.CellRendererToggle()
		if on_toggle:
			r.connect("toggled", on_toggle)
		c = Gtk.TreeViewColumn(title, r, active=column)
		tv.append_column(c)

	@staticmethod
	def add_combo_column_to_tv(tv, title, column, lst_m, on_change=None):
		r = Gtk.CellRendererCombo()
		r.set_property("model", lst_m)
		r.set_property("text-column", 0)
		r.set_property("has-entry", False)
		if on_change:
			r.set_property("editable", True)
			r.connect("edited", on_change)
		c = Gtk.TreeViewColumn(title, r, text=column)
		tv.append_column(c)


	@staticmethod
	def create_term(shell=Vte.get_user_shell(), emulation="xterm", pwd=os.environ['HOME']):
		term = Vte.Terminal()
		pid  = term.fork_command_full(Vte.PtyFlags.DEFAULT, pwd, [shell],
		                              [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None, )
		term.set_emulation(emulation)
		term.watch_child(pid[1])

		return term,pid

	@staticmethod
	def run_command_in_term(term, command, on_complete=None):
		pid = term.fork_command_full(Vte.PtyFlags.DEFAULT, ".", command,
		                             [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None, )
		term.watch_child(pid[1])
		if on_complete:
			term.connect("child-exited", on_complete)

		return pid
