#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Authors: Pierrick Le Brun <akuna~AT~salixos~org>
#          Frédéric Galusik <fredg~AT~salixos~org>
#
# License: GPL v3 (see COPYING for details).
#

# CONFIGURATION FILE FOR SETUPCENTER PREFERENCES
# (if you do modify this configuration manually please respect its syntaxe
# which should be self-explanatory)

# This first section can be configured manually by any distribution
# integrating SetupCenter:

# SetupCenter displayed name
setupcenter_name = _('Salix Control Center')

# SetupCenter displayed icon
icon_name = 'setupcenter'
title_icon_size = 24
about_icon_size = 128

# Remembering sizes
main_window_size = (850,550)

# After the above initial configuration by a distribution integrating
# SetupCenter, the following section shouldn't need further manual
# modification from then on, it will be automatically managed by
# the Preferences dialog box.

# Preferred viewing mode
viewing_mode = 'paned'

# Categories' names, categories icons and their activation status:
category_list = [
    ['Category 1',_('Desktop'),'display-capplet',True],
    ['Category 2',_('Hardware'),'xvkbd',True],
    ['Category 3',_('Software'),'emblem-package',True],
    ['Category 4',_('System'),'preferences-system',True],
    ['Category 5',_('Other'),'bum',True],
    ['Category 6',_('Unused'),'xfce-utils',False],
    ]

# Syntaxe is => ['Category no',_('Name of the category'),'icon',bolean
# value for activation state],\
# There should be no unset categories!
# For the moment only 6 categories are supported.

# Set the utilities that should be in some (or all) of the categories:
cat1_list = [
    'gtkiconrefresh',
    ]
cat2_list = [
    'gtkclocksetup',
    'gtkkeyboardsetup',
    'gparted',
    'gtkalsasetup',
    'ndisgtk',
    'cups',
    ]
cat3_list = [
    'gslapt',
    'dotnew',
    'sourcery',
    ]
cat4_list = [
    'gtkhostsetup',
    'gtkusersetup',
    'gtkservicesetup',
    'lilosetup',
    'gtklocalesetup',
    ]
cat5_list = [
    'persistence-wizard',
    ]
cat6_list = [
    '',
    ]

# Syntaxe is => cat_no_list = ['utility1','utility2','utility3','etc...']
# If a category is empty [], it will not be displayed.
