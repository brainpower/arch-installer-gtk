Requirements
------------
 - python3
 - python-gobject
 - pycman (included)
 - pyalpm (x86_64 binary included, i686 here: https://www.archlinux.org/packages/extra/i686/pyalpm/download/ )
 - libalpm

Installation
------------
not necessary

Usage
-----
run as root:

    # python3 main.py

It is advised to read the [Installation Guide](https://wiki.archlinux.org/index.php/Installation_Guide) beforehand/whilst installing, since the installer does not cover all parts of the installation (yet).
For example not all configuration files are covered and no bootloader will be written to your HDD's MBR.
It also contains no partitioning manager, you'll have to use gparted, parted, fdisk or a similar programm to create your partitions before installing.

Please make sure you're connected to the internet before installing, the installer won't check for it.

Now, as for what is covered by the installer:
 - creating filesystems using mkfs and mounting them to selectable mountpoints
 - installing base and optionally base-devel using pacstrap
 - selecting & installing additional packages
 - setting hostname, locale and timezone
 - locale-gen
 - genfstab
 - mkinitcpio
 - setting a root password

All those steps will be run in an embedded vte, so you'll have full transparency of what happens to your system.
All comands executed in the vte are written to /tmp/ai_install_commands.sh ,
so if you'd run it as a shell script you'd get the same installation process again.
(In fact, the installer does run that file to install the system in the first place)

All devices mounted by the installer will stay mounted after it's done,
so you don't have to remount them if you want to further customize your freshly installed system.

License
-------
GPLv3, see LICENSE file
