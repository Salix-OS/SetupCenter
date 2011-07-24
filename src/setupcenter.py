#!/usr/bin/env python

# version = '0.9-alpha'

### Import & internationalization

import commands
import gtk
import os
import pango
import shutil
import subprocess
import sys
import xdg.DesktopEntry as d

import locale
import gettext
import gtk.glade
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("setupcenter", "/usr/share/locale")
gettext.textdomain("setupcenter")
gettext.install("setupcenter", "/usr/share/locale", unicode=1)
gtk.glade.bindtextdomain("setupcenter", "/usr/share/locale")
gtk.glade.textdomain("setupcenter")

# Path of the configuration file
#pref_path = ""
pref_path = "/etc/setupcenter/"
sys.path.append(pref_path)
import setupcenter_pref as pref

### Global functions

def get_value_list_from_liststore(liststore,column) :
    """
    Retrieve the list of values from a given column in a given liststore
    """
    global liststore_content
    liststore_content = list ()
    item = liststore.get_iter_first ()
    while ( item != None ):
        liststore_content.append (liststore.get_value (item, column))
        item = liststore.iter_next(item)

def liststore_content_backup(liststore,int):
    """
    Make a backup of a liststore content.
    int is the number of columns in the liststore
    """
    global liststore_backup
    liststore_backup = list ()
    distribution = list ()
    feedline = list ()
    i = -1
    while i < int - 1 :
        i += 1
        get_value_list_from_liststore(liststore,i)
        distribution.append(liststore_content)
        feedline.append(eval('distribution[i]'))
    y = -1
    while y < len(distribution[0]) -1 :
        y += 1
        liststore_backup.append([])
        for item in feedline:
            liststore_backup[y].append(item[y])

def get_icon(name, icon_name, size):
    """
    Get icon specifics to feed iconview list stores
    """
    theme = gtk.icon_theme_get_default()
    try:
        return theme.load_icon(icon_name, size, 0)
    except :
        return theme.load_icon('image-missing', size, 0)

def error_dialog(message, parent = None):
    """
    Display an error message.
    """
    dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE, flags = gtk.DIALOG_MODAL)
    dialog.set_markup(message)
    global result_error
    result_error = dialog.run()
    dialog.destroy()

### Initialisation

# Retrieve the available administrator utilities from the users' system
utility_list = []
for i in os.listdir('/usr/share/applications') :
    if i.endswith('.desktop') :
        exec_line = d.DesktopEntry('/usr/share/applications/' + i).getExec()
        if 'gksu'in exec_line:
            utility_list.append(i.replace('.desktop', ''))
        # Add ati configuration tool if available
        elif 'amdxdg-su'in exec_line:
            utility_list.append(i.replace('.desktop', ''))
        # Add CUPS if available
        elif 'http://localhost:631' in exec_line:
            utility_list.append(i.replace('.desktop', ''))

class SetupCenter:
    """
    Main application class.
    """
    def __init__(self):
        
        builder = gtk.Builder()
        if os.path.exists('setupcenter.glade'):
            builder.add_from_file('setupcenter.glade')
        elif os.path.exists('/usr/share/setupcenter/setupcenter.glade'):
            builder.add_from_file('/usr/share/setupcenter/setupcenter.glade')
        elif os.path.exists('../share/setupcenter/setupcenter.glade') :
            builder.add_from_file('../share/setupcenter/setupcenter.glade')

        # Get a handle on the glade file widgets we want to interact with
        self.MainWindow = builder.get_object('main_window')
        self.AboutImage = builder.get_object('about_image')
        self.DisplayedCategoryListStore = builder.get_object('displayed_category_liststore')
        self.AvailableCategoryListStore = builder.get_object('available_category_liststore')
        self.ActivatedCategoryListStore = builder.get_object('activated_category_liststore')
        self.CategoriesTreeview = builder.get_object('categories_treeview')
        self.Category_Name_Column = builder.get_object('category_name_column')
        self.Category_Icon_Column = builder.get_object('category_icon_column')
        self.UtilitiesTreeview = builder.get_object('utilities_treeview')
        self.ApplicationListStore = builder.get_object('application_liststore')
        self.UtilitiesTreeViewColumn = builder.get_object('utilities_treeviewcolumn')
        self.Cat1ListStore = builder.get_object('cat1_liststore')
        self.Cat2ListStore = builder.get_object('cat2_liststore')
        self.Cat3ListStore = builder.get_object('cat3_liststore')
        self.Cat4ListStore = builder.get_object('cat4_liststore')
        self.Cat5ListStore = builder.get_object('cat5_liststore')
        self.Cat6ListStore = builder.get_object('cat6_liststore')
        self.CategoryIconView = builder.get_object('category_iconview')
        self.Cat1IconView = builder.get_object('cat1_iconview')
        self.Cat2IconView = builder.get_object('cat2_iconview')
        self.Cat3IconView = builder.get_object('cat3_iconview')
        self.Cat4IconView = builder.get_object('cat4_iconview')
        self.Cat5IconView = builder.get_object('cat5_iconview')
        self.Cat6IconView = builder.get_object('cat6_iconview')
        self.Cat1Label = builder.get_object('cat1_label')
        self.Cat2Label = builder.get_object('cat2_label')
        self.Cat3Label = builder.get_object('cat3_label')
        self.Cat4Label = builder.get_object('cat4_label')
        self.Cat5Label = builder.get_object('cat5_label')
        self.Cat6Label = builder.get_object('cat6_label')
        self.Cat1IconView2 = builder.get_object('cat1_iconview2')
        self.Cat2IconView2 = builder.get_object('cat2_iconview2')
        self.Cat3IconView2 = builder.get_object('cat3_iconview2')
        self.Cat4IconView2 = builder.get_object('cat4_iconview2')
        self.Cat5IconView2 = builder.get_object('cat5_iconview2')
        self.Cat6IconView2 = builder.get_object('cat6_iconview2')
        self.Cat1globalbox = builder.get_object('cat1_global_box')
        self.Cat2globalbox = builder.get_object('cat2_global_box')
        self.Cat3globalbox = builder.get_object('cat3_global_box')
        self.Cat4globalbox = builder.get_object('cat4_global_box')
        self.Cat5globalbox = builder.get_object('cat5_global_box')
        self.Cat6globalbox = builder.get_object('cat6_global_box')
        self.Cat1Label = builder.get_object('cat1_label')
        self.Cat2Label = builder.get_object('cat2_label')
        self.Cat3Label = builder.get_object('cat3_label')
        self.Cat4Label = builder.get_object('cat4_label')
        self.Cat5Label = builder.get_object('cat5_label')
        self.Cat6Label = builder.get_object('cat6_label')
        self.UtilityCellRendererCombo = builder.get_object("utility_cellrenderercombo")
        self.CategoryCellRendererText = builder.get_object("category_cellrenderertext")
        self.AboutDialog = builder.get_object("about_dialog")
        self.PreferencesDialog = builder.get_object("preferences_dialog")
        self.GlobalViewRadioButton = builder.get_object("global_view_radiobutton")
        self.PanedViewRadioButton = builder.get_object("paned_view_radiobutton")
        self.PanedView = builder.get_object("paned_view")
        self.GlobalView = builder.get_object("global_view")
        self.UtilityActivationToggle = builder.get_object("utility_cellrenderertoggle")
        self.CategoryActivationToggle = builder.get_object("category_cellrenderertoggle")
        self.PrefNulButton = builder.get_object("preferences_nul_button")
        self.PanedView = builder.get_object("paned_view")
        self.CategoryPanedView = builder.get_object("category_iconview_cellrenderer")

        # Connect signals
        builder.connect_signals(self)

### GUI INITIALIZATION ###

        global available_categories
        available_categories = [pref.cat1_list,pref.cat2_list,pref.cat3_list,pref.cat4_list,pref.cat5_list,pref.cat6_list]
        global stores
        stores = (self.Cat1ListStore,self.Cat2ListStore,self.Cat3ListStore,self.Cat4ListStore,self.Cat5ListStore,self.Cat6ListStore)
        global global_view_cat
        global_view_cat = (self.Cat1globalbox,self.Cat2globalbox,self.Cat3globalbox,self.Cat4globalbox,self.Cat5globalbox,self.Cat6globalbox)
        global cat_labels
        cat_labels = (self.Cat1Label,self.Cat2Label,self.Cat3Label,self.Cat4Label,self.Cat5Label,self.Cat6Label)
        global paned_category_views
        paned_category_views = (self.Cat1IconView,self.Cat2IconView,self.Cat3IconView,self.Cat4IconView,self.Cat5IconView,self.Cat6IconView)
        global global_category_views
        global_category_views = (self.Cat1IconView2,self.Cat2IconView2,self.Cat3IconView2,self.Cat4IconView2,self.Cat5IconView2,self.Cat6IconView2)
        global utility_process_list
        utility_process_list = []

        # Ensure the following liststores are empty to start with
        self.ApplicationListStore.clear()
        self.DisplayedCategoryListStore.clear()
        self.AvailableCategoryListStore.clear()
        self.ActivatedCategoryListStore.clear()

        # Personnalize the main window
        self.AboutImage.set_from_icon_name(pref.icon_name, pref.about_icon_size)
        self.MainWindow.set_icon(get_icon(gtk.STOCK_OPEN, pref.icon_name, pref.title_icon_size))
        self.AboutDialog.set_logo(get_icon(gtk.STOCK_OPEN, pref.icon_name, pref.about_icon_size))
        self.MainWindow.set_title(pref.setupcenter_name)
        self.MainWindow.resize(pref.main_window_size[0], pref.main_window_size[1])
        self.MainWindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.PanedView.set_position(0)

        # Set the utility combocell
        self.UtilityCellRendererCombo.set_property("model", self.ActivatedCategoryListStore)
        self.UtilityCellRendererCombo.set_property('text-column', 1)
        self.UtilityCellRendererCombo.set_property('editable', True)
        self.UtilityCellRendererCombo.set_property("has-entry", False)
        self.UtilityCellRendererCombo.set_property('cell_background', '#CCCCCC')
        self.UtilitiesTreeViewColumn.set_attributes(self.UtilityCellRendererCombo, text = 2)

        # Set the category CellRendereText
        self.CategoryCellRendererText.set_property('editable', True)
        self.CategoryCellRendererText.set_property('cell_background', '#CCCCCC')

        # Center the labels of the categories in the paned view
        self.CategoryPanedView.set_property("alignment", pango.ALIGN_CENTER)
        self.CategoryPanedView.set_property("xalign", 0.5)

        global get_category_content_feedline
        def get_category_content_feedline (utility) :
            """
            Get the utility feedline to append to one of the cat*_liststore
            """
            # Get the application human-readable name
            desktop_file = d.DesktopEntry(filename='/usr/share/applications/' + utility + '.desktop')
            global name_feed
            name_feed = desktop_file.getName().split(',')[0]
            exec_feed = desktop_file.getExec().rstrip("%f")
            term_feed = desktop_file.getTerminal()
            global icon_name
            icon_name = desktop_file.getIcon()
            if icon_name :
                global show_cat
                show_cat = 'yes'
                icon_feed = get_icon(gtk.STOCK_OPEN, icon_name, 48)
                global cat_feedline
                cat_feedline = (name_feed, icon_feed, exec_feed, term_feed, utility)

        global set_applications
        def set_applications (i) :
            """
            Put each utility found in the user's system in its given category (set in preference file).
            """
            # Ensure each category liststore is empty to start with
            stores[i].clear()
            for proposed_application_name in available_categories [i] :
                # Only use an application if it is present in the user system:
                if proposed_application_name in utility_list:
                    global show_cat
                    show_cat = 'no'
                    get_category_content_feedline (proposed_application_name)
                    if show_cat == 'yes' :
                        stores[i].append(cat_feedline)
                        # Only show an activated and non-empty category
                        if pref.category_list[i][3] :
                            global_view_cat[i].show()
                        # Starts feeding the available applications' liststore
                        utility_feedline = (name_feed, proposed_application_name, pref.category_list[i][1], 'gtk-properties', True)
                        self.ApplicationListStore.append(utility_feedline)
                        #  Remove the application from the list to ensure it is only fed once
                        utility_list.remove(proposed_application_name)

        global set_categories
        def set_categories (i) :
            """
            Initialize the default category application list
            """
            # Open & parse the default categories list
            try :
                cat_feed = pref.category_list[i][0]
                name_feed = pref.category_list[i][1]
                global icon_name
                icon_name = pref.category_list[i][2]
                icon_feed = get_icon(gtk.STOCK_OPEN, icon_name, 48)
                state_feed = pref.category_list[i][3]
                category_feedline = (cat_feed, name_feed, icon_feed, state_feed, 'gtk-properties', icon_name)
                cat_labels[i].set_text(name_feed)
                get_value_list_from_liststore(self.AvailableCategoryListStore,0)
                # Set the available category liststore (there should be no doublon):
                if category_feedline[0] not in liststore_content :
                    self.AvailableCategoryListStore.append(category_feedline)
                    # Also set the activated categories liststores
                    if state_feed == True :
                        self.ActivatedCategoryListStore.append((cat_feed[-1], name_feed))
                # Check if the category is empty, and if not, set the displayed category liststore:
                try :
                    if state_feed == True :
                        displayed_category_feedline = category_feedline[:3]
                        stores[i].get_iter(0) # if it throws an exception we'll pass
                        self.DisplayedCategoryListStore.append(displayed_category_feedline)
                except ValueError :
                    pass
            except IndexError :
                pass

        global refresh_displayed_categories
        def refresh_displayed_categories():
            """
            Previously hidden category boxes will have to be displayed if they now have content
            while newly emptied category boxes will have to be hidden
            """
            self.DisplayedCategoryListStore.clear()
            for i in (0,1,2,3,4,5) :
                set_categories (i)
                # Refresh the global view as well
                if pref.category_list[i][3]:
                    try :
                        stores[i].get_iter(0) # if it throws an exception we'll hide the category from global view
                        global_view_cat[i].show()
                    except :
                        global_view_cat[i].hide()
            # Set the cursor on the first row and show the first non-empty category
            self.CategoryIconView.select_path(0)

        global anulate_preferences
        def anulate_preferences():
            """
            Anulate any settings that was performed in the current preferences dialog box
            """
           # Restore the preference file
            shutil.move(pref_path + 'setupcenter_pref.old', pref_path + 'setupcenter_pref.py')
            # Restore the categories content liststore
            for i in [0,1,2,3,4,5] :
                stores[i].clear()
                for y in cat_lists_backup[i] :
                    stores[i].append(y)
            # Restore the previous liststores
            self.ApplicationListStore.clear()
            for i in app_list_backup :
                self.ApplicationListStore.append(i)
            self.AvailableCategoryListStore.clear()
            for i in available_cat_list_backup :
                self.AvailableCategoryListStore.append(i)
            self.DisplayedCategoryListStore.clear()
            for i in displayed_cat_list_backup :
                self.DisplayedCategoryListStore.append(i)
            self.ActivatedCategoryListStore.clear()
            for i in activated_cat_list_backup :
                self.ActivatedCategoryListStore.append(i)
            refresh_displayed_categories()

        global update_displayed_categories_labels
        def update_displayed_categories_labels(new_text, which_category,cat_number):
            """
            Update all displayed category labels
            """
            liststore_content_backup(self.DisplayedCategoryListStore,3)
            counter = -1
            for i in liststore_backup :
                counter += 1
                if which_category in i :
                    break
            self.DisplayedCategoryListStore.clear()
            old_text = liststore_backup[counter][1]
            liststore_backup[counter][1] = new_text
            for i in liststore_backup :
                self.DisplayedCategoryListStore.append(i)
            # Update the categories in the utility list as well
            get_value_list_from_liststore(self.ApplicationListStore,2)
            cat_list = liststore_content
            liststore_content_backup(self.ApplicationListStore,5)
            counter = -1
            for i in cat_list :
                counter += 1
                if old_text in i :
                    liststore_backup[counter][2] = new_text
            self.ApplicationListStore.clear()
            for i in liststore_backup :
                self.ApplicationListStore.append(i)
            # And finally, update the labels in the global view
            cat_labels[cat_number-1].set_text(new_text)

        # Finalize categories/utilities (we can have application for up to 6 categories)
        for i in (0,1,2,3,4,5) :
            set_applications (i)
        refresh_displayed_categories()

        # Feed the rest of the available applications' liststore (the ones with no assigned category)
        while utility_list :
            i = utility_list.pop()
            # Blacklist SetupCenter
            if i != 'setupcenter':
                 # Get the application human-readable name
                desktop_file = d.DesktopEntry(filename='/usr/share/applications/' + i + '.desktop')
                human_readable = desktop_file.getName().split(',')[0]
                utility_feedline = (human_readable, i, 'Select...', 'gtk-properties', False)
                # And populate the GUI system category iconview
                self.ApplicationListStore.append(utility_feedline)

        # Sets the preferred viewing mode
        if pref.viewing_mode =='paned' :
            self.GlobalView.hide()
            self.PanedView.show()
            # Set the check in the appropriate preference box
            self.PanedViewRadioButton.set_active(True)
        if pref.viewing_mode =='global' :
            self.GlobalView.show()
            self.PanedView.hide()
            # Set the check in the appropriate preference box
            self.GlobalViewRadioButton.set_active(True)

### Catching signals from the GUI

    def on_about_button_clicked(self, widget, data=None):
        """
        Action when the About button is clicked
        """
        self.AboutDialog.show()

    def on_about_dialog_close(self, widget, data=None):
        """
        Action when the About dialog quit button is clicked
        """
        self.AboutDialog.hide()
        return True

    def on_preferences_button_clicked(self, widget, data=None):
        """
        Action when the Preferences button is clicked
        """
        self.PreferencesDialog.show()
        # save a copy of the preference file
        shutil.copyfile(pref_path + 'setupcenter_pref.py', pref_path + 'setupcenter_pref.old')
        # save a copy of cat*_liststore content
        global cat_lists_backup
        cat_lists_backup = list ()
        for cat in stores :
            liststore_content_backup(cat,5)
            cat_lists_backup.append(liststore_backup)
        # save a copy of the liststores
        liststore_content_backup(self.ApplicationListStore,5)
        global app_list_backup
        app_list_backup = liststore_backup
        liststore_content_backup(self.AvailableCategoryListStore,6)
        global available_cat_list_backup
        available_cat_list_backup = liststore_backup
        liststore_content_backup(self.DisplayedCategoryListStore,3)
        global displayed_cat_list_backup
        displayed_cat_list_backup = liststore_backup
        liststore_content_backup(self.ActivatedCategoryListStore,2)
        global activated_cat_list_backup
        activated_cat_list_backup = liststore_backup

    def on_category_cellrenderertoggle_toggled(self, widget, path):
        """
        Action when the activated check is toggled in the utilities preferences
        """
        # Activate the toggling
        self.AvailableCategoryListStore[path][3] = not self.AvailableCategoryListStore[path][3]
        # Retrieve the bolean value
        value = str(self.AvailableCategoryListStore[path][3])
        # Retrieve toggled iter
        iter = self.AvailableCategoryListStore.get_iter(path)
        # Retrieve the name of the category
        category_name = self.AvailableCategoryListStore.get_value(iter, 1)
        # Retrieve the category
        toggled_category = self.AvailableCategoryListStore.get_value(iter, 0)
        # Update the configuration file
        update_cat_status = """sed "s|\('Category """ + str(int(path) +1) + """',_('.*'),'.*'\),.*]|\\1,""" + value + """]|" -i """ + pref_path + 'setupcenter_pref.py'
        subprocess.call(update_cat_status, shell=True)
        cat_number = int(toggled_category[-1])
        get_value_list_from_liststore(stores[cat_number-1],0)
        if self.AvailableCategoryListStore[path][3] == True :
            # Append the category to the activated category liststore
            liststore_content_backup(self.ActivatedCategoryListStore,2)
            self.ActivatedCategoryListStore.clear()
            new_feedline = [str(int(path) +1),category_name]
            liststore_backup.append(new_feedline)
            liststore_backup.sort()
            for i in liststore_backup :
                self.ActivatedCategoryListStore.append(i)
            # Display the category if it is activated and if it holds utilities
            if liststore_content != []:
                # Display in global view
                global_view_cat[cat_number-1].show()
                # insert in displayed category liststore
                liststore_content_backup(self.DisplayedCategoryListStore,3)
                self.DisplayedCategoryListStore.clear()
                new_feedline = [toggled_category,category_name,self.AvailableCategoryListStore.get_value(iter, 2)]
                if new_feedline not in liststore_backup :
                    liststore_backup.append(new_feedline)
                liststore_backup.sort()
                for i in liststore_backup :
                    self.DisplayedCategoryListStore.append(i)
        else :
            # Hide in global view
            global_view_cat[cat_number-1].hide()
            # Remove from the displayed category liststore
            liststore_content_backup(self.DisplayedCategoryListStore,3)
            self.DisplayedCategoryListStore.clear()
            new_feedline = [toggled_category,category_name,self.AvailableCategoryListStore.get_value(iter, 2)]
            try :
                liststore_backup.remove(new_feedline)
            except ValueError :
                pass
            for i in liststore_backup :
                self.DisplayedCategoryListStore.append(i)
            # Remove the category from the activated category liststore
            liststore_content_backup(self.ActivatedCategoryListStore,2)
            self.ActivatedCategoryListStore.clear()
            new_feedline = [str(int(path) +1),category_name]
            try :
                liststore_backup.remove(new_feedline)
            except ValueError:
                pass
            for i in liststore_backup :
                self.ActivatedCategoryListStore.append(i)
            # Also remove all utilites it contains
            update_cat_content = """sed "s|\(cat""" + str(int(path) +1) + """_list = \[\)'.*,|\\1'',|" -i """ + pref_path + 'setupcenter_pref.py'
            subprocess.call(update_cat_content, shell=True)
            # Remove from its own category liststore
            stores[int(path)].clear()
            # Remove from the utility liststore
        # Refresh the utility liststore
        get_value_list_from_liststore(self.ApplicationListStore,2)
        cat_list = liststore_content
        liststore_content_backup(self.ApplicationListStore,5)
        counter = -1
        for i in cat_list :
            counter += 1
            if category_name in i :
                if self.AvailableCategoryListStore[path][3] == False :
                    liststore_backup[counter][2] = "Select..."
                liststore_backup[counter][4] = self.AvailableCategoryListStore[path][3]
        self.ApplicationListStore.clear()
        for i in liststore_backup :
            self.ApplicationListStore.append(i)
        refresh_displayed_categories()
        self.CategoryIconView.select_path(0)

    def on_category_cellrenderertext_edited(self, widget, path_string, new_text):
        """
        Action to perform when a category name is edited in the categories preferences
        """
        # Retrieve the selected application liststore row_iter
        row_iter = self.CategoriesTreeview.get_selection().get_selected()[-1]
        # Set the new application row value on the liststore's second column (1)
        self.AvailableCategoryListStore.set_value(row_iter, 1, new_text)
        # Retrieve the value of the activation parameter
        category_activation = self.AvailableCategoryListStore.get_value(row_iter, 3)
        # Retrieve the value of the category
        which_category = self.AvailableCategoryListStore.get_value(row_iter, 0)
        # Update the configuration file
        update_cat_name = """sed "s|\('Category """ + str(int(path_string) +1) + """',\)_('.*')|\\1_('""" + new_text + """')|" -i """ + pref_path + 'setupcenter_pref.py'
        subprocess.call(update_cat_name, shell=True)
        # Update the displayed category liststore (only if activated)
        if category_activation == True :
            update_displayed_categories_labels(new_text,which_category,int(path_string) +1)
            # Also update the activated category liststore
            liststore_content_backup(self.ActivatedCategoryListStore,2)
            self.ActivatedCategoryListStore.clear()
            for i in liststore_backup :
                if i[0] == str(int(path_string) +1) :
                    i[1] = new_text
            liststore_backup.sort()
            for i in liststore_backup :
                self.ActivatedCategoryListStore.append(i)

    def on_categories_treeview_button_press_event(self,widget,event):
        x, y = event.get_coords()
        path = self.CategoriesTreeview.get_path_at_pos(int(x), int(y))[0][0]
        treeview_column = self.CategoriesTreeview.get_path_at_pos(int(x), int(y))[1]
        if treeview_column.get_title() == _('Set the icon: ') :
            icon_theme = gtk.icon_theme_get_default()
            try :
                icon_path = icon_theme.lookup_icon(self.AvailableCategoryListStore[path][5],48,gtk.ICON_LOOKUP_FORCE_SVG).get_filename()
                icon_directory = icon_path[:icon_path.rfind('/')]
            except AttributeError:
                icon_directory = '/usr/share/icons'
            new_icon_selection = gtk.FileChooserDialog(title=_('Choose another icon'), parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            new_icon_selection.set_current_folder(icon_directory)

            preview = gtk.Image()
            new_icon_selection.set_preview_widget(preview)
            def update_preview_cb(new_icon_selection, preview):
                filename = new_icon_selection.get_preview_filename()
                try:
                  pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 200, 200)
                  preview.set_from_pixbuf(pixbuf)
                  have_preview = True
                except:
                  have_preview = False
                new_icon_selection.set_preview_widget_active(have_preview)
                return
            new_icon_selection.connect("update-preview", update_preview_cb, preview)
            new_icon_selection.show()
            if(new_icon_selection.run() == gtk.RESPONSE_OK):
                new_icon_path = new_icon_selection.get_filename()
                new_icon_file = new_icon_path[new_icon_path.rfind('/')+1:]
                new_icon_name = new_icon_file[:new_icon_file.rfind('.')]
                # Retrieve the value of the activation parameter
                category_activation = self.AvailableCategoryListStore[path][3]
                # Update the Available category Liststore
                self.AvailableCategoryListStore[path][5] = new_icon_name
                new_icon_feed = get_icon(gtk.STOCK_OPEN, new_icon_name, 48)
                self.AvailableCategoryListStore[path][2] = new_icon_feed
                # Update the displayed category liststore (only if activated)
                if category_activation == True :
                    # Update the Available category Liststore
                    self.DisplayedCategoryListStore[path][2] = new_icon_feed
                 # Update the configuration file
                update_cat_icon = """sed "s|\('Category """ + str(int(path) +1) + """',_('.*'),\)'.*'|\\1'""" + new_icon_name + """'|" -i """ + pref_path + 'setupcenter_pref.py'
                subprocess.call(update_cat_icon, shell=True)
            new_icon_selection.destroy()

    def on_utility_cellrenderertoggle_toggled(self, widget, path):
        """
        Action when the activated check is toggled in the utilities preferences
        """
        # Activate the toggling
        self.ApplicationListStore[path][4] = not self.ApplicationListStore[path][4]
        # Retrieve toggled iter
        iter = self.ApplicationListStore.get_iter(path)
        # Retrieve the name of the selected application
        toggled_app = self.ApplicationListStore.get_value(iter, 1)
        # Retrieve the category name
        toggled_category = self.ApplicationListStore.get_value(iter, 2)
        for i in pref.category_list :
            if toggled_category in i :
                toggled_cat = i[0].replace('Category ', 'cat')+'_list'
                global toggled_cat_no
                toggled_cat_no = int(i[0].split()[-1])-1
        # If utility is deactivated, remove it from the preference file + liststore *if* category is already set
        if self.ApplicationListStore[path][4] == False and toggled_category != "Select...":
            # Remove the application from any of the cat*_list it was in
            remove_app_from_cat = """sed "s/'""" + toggled_app + """',//" -i """ + pref_path + 'setupcenter_pref.py'
            subprocess.call(remove_app_from_cat, shell=True)
            # Remove the application from any cat*_listore
            if toggled_cat :
                get_value_list_from_liststore(stores[toggled_cat_no],4)
                i = -1
                for cat in liststore_content :
                    i += 1
                    if cat == toggled_app :
                        break
                try :
                    stores[toggled_cat_no].remove(stores[toggled_cat_no].get_iter((i,)))
                except ValueError:
                    pass
            # Set the combobox line to "Select..."
            self.ApplicationListStore[path][2] = "Select..."    
        refresh_displayed_categories()

    def on_utility_cellrenderercombo_changed(self, widget, path_string, new_iter):
        """
        Action to perform when a combo line is changed in the utilities preferences
        """
        # Retrieve the selected application liststore row_iter
        row_iter = self.UtilitiesTreeview.get_selection().get_selected()[-1]
        # Retrieve the value of the activation parameter
        utility_activation = self.ApplicationListStore.get_value(row_iter, 4)
        if utility_activation == True :
            # Retrieve the combo new iter's value
            new_text = self.ActivatedCategoryListStore.get_value(new_iter, 1)
            # Retrieve the name of the selected application for further reference
            moved_app = self.ApplicationListStore.get_value(row_iter, 1)
            # Retrieve the name of the old category for further reference
            old_text = self.ApplicationListStore.get_value(row_iter, 2)
            # Work out the old and new category list
            new_cat = ''
            old_cat = ''
            for i in pref.category_list :
                if new_text in i :
                    new_cat = i[0].replace('Category ', 'cat')+'_list'
                    new_cat_no = int(i[0].split()[-1])-1
                if old_text in i :
                    old_cat = i[0].replace('Category ', 'cat')+'_list'
                    old_cat_no = int(i[0].split()[-1])-1
            # Only if the new category is activated:
            if self.AvailableCategoryListStore[new_cat_no][3] == True :
                # Set the new application row value on the liststore's third column (2)
                self.ApplicationListStore.set_value(row_iter, 2, new_text)
                # Remove the application from any of the cat*_list it was in
                remove_app_from_cat = """sed "s/'""" + moved_app + """',//" -i """ + pref_path + 'setupcenter_pref.py'
                subprocess.call(remove_app_from_cat, shell=True)
                # Remove the application from the old cat*_listore
                if old_cat :
                    get_value_list_from_liststore(stores[old_cat_no],4)
                    i = -1
                    for cat in liststore_content :
                        i += 1
                        if cat == moved_app :
                            break
                    stores[old_cat_no].remove(stores[old_cat_no].get_iter((i,)))
                # Append the application in the new cat*_list
                if new_cat :
                    move_app_to_new_cat = """sed "s/""" + new_cat + """ = \[/""" + new_cat + """ = \['""" + moved_app + """',/" -i """ + pref_path + 'setupcenter_pref.py'
                    subprocess.call(move_app_to_new_cat, shell=True)
                    # Append to the new cat*_listore
                    get_category_content_feedline (moved_app)
                    stores[new_cat_no].append(cat_feedline)

            refresh_displayed_categories()

    def on_preferences_ok_button_clicked(self, widget, data=None):
        """
        Action when the Preference Apply button is clicked
        """
        # Get the viewing choice and set it in the preference file
        if self.GlobalViewRadioButton.get_active() == True :
            set_viewmode = "sed 's/paned/global/' -i " + pref_path + "setupcenter_pref.py"
            subprocess.call(set_viewmode, shell=True)
            self.PanedView.hide()
            self.GlobalView.show()
        elif self.PanedViewRadioButton.get_active() == True :
            set_viewmode = "sed 's/global/paned/' -i " + pref_path + "setupcenter_pref.py"
            subprocess.call(set_viewmode, shell=True)
            self.GlobalView.hide()
            self.PanedView.show()
        # Erase unneeded backup files
        os.remove(pref_path + 'setupcenter_pref.old')
        self.PreferencesDialog.hide()

    def on_preferences_nul_button_clicked(self, widget, data=None):
        """
        Action when the Preference Annulate button is clicked
        """
        self.PreferencesDialog.hide()
        anulate_preferences()

    def on_preferences_dialog_close(self, widget, data=None):
        """
        Action when the Preference X cross button is clicked
        """
        self.PreferencesDialog.hide()
        return True
        anulate_preferences()

    def on_category_iconview_selection_changed(self, iconview):
        """
        Action when another category is selected in the paned view
        """
        try :
            path = self.CategoryIconView.get_selected_items()
            iter = self.DisplayedCategoryListStore.get_iter(path[0])
            new_cat_index = int(self.DisplayedCategoryListStore.get_value(iter, 0).split()[-1])-1
            for i in paned_category_views :
                i.hide()
            paned_category_views[new_cat_index].show()

        # If user's click misses a category:
        except IndexError :
            pass

    def on_iconview2_selection_changed(self, iconview) :
        """
        Action when the selection changes in the global view
        """
        for i in global_category_views :
            if iconview != i :
                i.unselect_all()

    def on_iconview_item_activated(self, iconview, path):
        """
        Action when an application is clicked on
        """
        path = [path]
        relevant_liststore = iconview.get_model()
        iter = relevant_liststore.get_iter(path[0])
        selected_action = relevant_liststore[int(path[0][0])][2]
        global to_execute
        to_execute = ""
        if 'gksu' in selected_action :
                to_execute = selected_action.replace('gksu ', '')
        else :
            # find out the user who executed setupcenter so it can run the command:
            for line in commands.getoutput("ps aux | grep 'su ' | grep setupcenter").splitlines() :
                if 'root' not in line :
                    reg_user = line.split(' ')[0]
                    to_execute = "su -l " + reg_user + ' -c "'  + selected_action + '"'
        if relevant_liststore.get_value(iter, 3) is False :
            utility_process = subprocess.Popen(to_execute, shell=True)
        if relevant_liststore.get_value(iter, 3) is True :
            utility_process = subprocess.Popen('xterm ' + to_execute, shell=True)
        # Get info for process cleanup on exit
        utility_process_list.append(utility_process)

    def on_main_window_destroy(self, widget):
        """
        Action when the exit X on the main window upper right is clicked
        """
        # Kill any utility still opened
        while utility_process_list :
            utility_process_list.pop(0).kill()
        # Window size to remember
        window_x, window_y = self.MainWindow.get_size()
        remembered_size = """sed "s|\(main_window_size = \)(.*)|\\1(""" + str(window_x) + "," + str(window_y) + """)|" -i """ + pref_path + 'setupcenter_pref.py'
        subprocess.call(remembered_size, shell=True)
        gtk.main_quit()

    def on_quit_button_clicked(self, widget):
        """
        Action when the quit button is clicked
        """
        # Kill any utility still opened
        while utility_process_list :
            utility_process_list.pop(0).kill()
        # Window size to remember
        window_x, window_y = self.MainWindow.get_size()
        remembered_size = """sed "s|\(main_window_size = \)(.*)|\\1(""" + str(window_x) + "," + str(window_y) + """)|" -i """ + pref_path + 'setupcenter_pref.py'
        subprocess.call(remembered_size, shell=True)
        gtk.main_quit()

# Launch the main application
if __name__ == '__main__':
    # Checks for root privileges
    if os.getuid() != 0:
        error_dialog(_("<b>Sorry!</b> \n\nRoot privileges are required to access the Setup Center. "))
        sys.exit(1)
    # Executes the main program
    SetupCenter()
    gtk.main()