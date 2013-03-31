
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

import os, re, subprocess

import pyalpm
from pycman import config, transaction

def run_command(*args):
	out = b""
	#err = b""
	proc = subprocess.Popen(args, stdout=subprocess.PIPE) #, stderr=subprocess.PIPE)

	while(proc.returncode == None):
		out += proc.communicate()[0]
		#err += proc.communicate()[1]

	return out #,err

def get_devices():
	lst = []
	out = run_command("blkid").decode("utf-8")
	lines = out.split("\n")
	regex = re.compile(r"^(.*):.*TYPE=\"(.*?)\".*")
	for line in lines:
		x = regex.match(line)
		if x:
			lst.append( (x.group(1), x.group(2)))

	return lst

def get_filesystem_types():
	paths = os.environ["PATH"].split(":")
	stdpaths = ["/bin", "/usr/bin", "/sbin", "/usr/sbin"]
	types = []

	for stdpath in stdpaths:
		if not stdpath in paths:
			paths.append(stdpath)

	for path in paths:
		for line in run_command("find", path , "-name", "mkfs.*").decode().split("\n"):
			types.append(line.split(".")[-1])
	types.sort()
	return list(filter(None, types))


class Pacman(object):

	def __init__(self):
		self.handle  = config.init_with_config("/etc/pacman.conf")

		for db in self.handle.get_syncdbs(): # do a -Sy on start
			t = transaction.init_from_options(self.handle, None)
			db.update(False) # dont force update
			t.release()

		self.update_members()


	def update_members(self):
		self.syncdbs     = { p.name:p for p in self.handle.get_syncdbs() }
		self.repos       = [ p.name   for p in self.handle.get_syncdbs() ]
		self.groupcaches = [ (db,self.syncdbs[db].grpcache) for db in self.syncdbs ]
		self.groups      = { gc[0]:[ g[0]      for g in gc[1]] for gc in self.groupcaches }
		self.group_pkgs  = { gc[0]:{ g[0]:g[1] for g in gc[1]} for gc in self.groupcaches }

	def get_repos(self):
		return self.repos

	def get_groups(self):
		return self.groups

	def get_package_list(self, repo, group=None):
		if not group:
			return [ (False, p.name, p.version, p.desc) for p in self.syncdbs[repo].pkgcache]
		else:
			return [ (False, p.name, p.version, p.desc) for p in self.group_pkgs[repo][group]]

	#~ def get_repo_of_group(self, group):
		#~ for repo in self.groups:
			#~ if group in self.groups[repo]:
				#~ return repo

	def get_repos_of_group(self, group):
		return [repo for repo in self.groups if group in self.groups[repo]]

	def get_groups_of_repo(self, repo):
		return self.groups[repo];

	def get_repos_of_pkg(self, pkg):
		lst = []
		for repo in self.repos:
			if pkg in [p.name for p in self.syncdbs[repo].pkgcache]:
				lst.append(repo);
		return lst

	def get_groups_of_pkg(self, pkg):
		for repo in self.get_repos():
			for p in self.syncdbs[repo].pkgcache:
				if p.name == pkg:
					return p.groups;


def main():
	#~ devs = get_devices()
	#~ for dev,typ in devs:
		#~ print(dev,typ)
	#print(get_filesystem_types())
	pacman = Pacman()
	#~ print(pacman.get_repos())
	#~ print(pacman.get_package_list("core"))
	#print(pacman.get_groups())
	#print(pacman.get_package_list("core", "base"))
	print(pacman.get_repo_of_group("unity"))

if __name__ == "__main__":
	main()
