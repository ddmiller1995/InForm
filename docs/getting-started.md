# InForm

*InForm* is an information managment system with three main functions:

* **Pertinent data at-a-glance**

    Non-sensitive case data is displayed on the homepage to give a quick overview of current residents. 

* **Clear form tracking**

    For each youth, all required forms are displayed and given a status of either To-Do, In Progress, or Complete.

* **Comprehensive Admin functionality**

    An admin page is included that allows basic CRUD operations - creates, reads, updates, and deletes.


## User Guide

This tutorial will guide you through the general user flow for *InForm*. 

### Main

* [Reading the front page](#reading-the-front-page)

* [Presentation View](#presentation-view)

* [Marking a youth exited](#marking-a-youth-as-exited)

* [Extending exit dates and changing placement types](#extending-exit-dates-and-changing-placement-types)

* [Viewing and moving forms](#viewing-and-moving-forms)

### Admin

* [Data overview](#data-overview)

* [Adding admin user accounts](#adding-admin-user-accounts)

* [Entering a new youth or editing and existing youth data](#entering-a-new-youth-or-editing-and-existing-youth-data)

* [Changing columns on the homepage youth tracker](#changing-columns)

* [Import/Export](#import-and-export)

### Server Restart (in case of system shutdown)
* [Restarting the server](#restarting-the-server)

### Reading the front page
![homepage](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/homepage.png)

Our homepage, by default, provides an overview of all current residents and their most pertinent case details. If you wish to view more details on a particular youth, you can click their name to be taken to their case profile. If you want to view youth that are no longer current residents, uncheck the `show active` checkbox near the top right corner. This will expand the youth chart to show all youth in the system, active or not. The `add youth` button can be used for adding a new youth visit into the sytem. See the [entering a new youth](#Entering-a-new-youth-or-editing-and-existing-youth-data) section for more information.

The color displayed for a youth's estimated exit date will change depending on how close we are to that date. If the estimated exit date is within the following three days, the date will be displayed as red. If it's within seven days, the date will be orange.

![homepage upcoming exits](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/homepage-colors.png)

### Presentation View
![presentation view](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/presentation.png)

This page can be accessed from the homepage by clicking on `Presentation View`. The primary purpose of this page is to provide a non-clickable view of current residents. This ensures that, if this page were to be presented on a client-facing monitor, a staff member could not unintentionally click on a given youth and reveal sensitive case data.

### Marking a youth as exited
<img src="https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/exit-modal.png" alt="youth exit modal" width="400"/>

The exit modal appears when you click the `Add` button under Exit Date from the homepage. 

`Exit Date` will default to today's date, but can be modified to any other calendar date. Fill out the other fields as appropriate, or leave them alone if you wish to use their default values. These can always be changed later through the Admin page. Once you hit Save, the youth will be marked as exited and disappear from the active listing on the homepage.

As the popup specifies, this should only be used when the youth has left the shelter. Any extensions or bed changes must be done through the youth's case profile. 

### Extending exit dates and changing placement types
![youth profile](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/youth-profile-short.png)

Extend Stay | Switch Beds
:-----------:|:-----------:
<img src="https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/extend-modal.png" alt="extend youth visit modal" width="400"/>  | <img src="https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/placement-modal.png" alt="change placement type modal" width="400"/>

Clicking on a youth from the homepage will bring you to that youth's case profile. A snippet of the case profile is shown above with the two update actions highlighted. 

Note that if the youth has multiple visits, you can view past visits by clicking through the dropdown menu in the top left corner.

The extend modal only requires one field `number of extension days`. This will default to 15 days, but can be modified. As you change the number of extension days, the `new estimated exit` date will update accordingly, but these changes *will not* be saved until you click Save. 

The modal used to switch beds has two fields `new placement type` and `transfer date`. Use the dropdown to select the new placement type. If you don't see a bed type listed, you must go to the Admin page to add it. `transfer date` will default to today's date, but can modified to any calendar date.

### Viewing and moving forms
![forms](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/forms.png)

Our form management tool can be found in the youth's case profile. This tool is used to track all forms required for a particular youth throughout their stay in the shelter. Form categories (here depicted as Intake and Psychosocial) can be collapsed using the ^ icons. Click on the info icon to see details for a particular form.

By default, all forms will be in the leftmost column but can be moved around using the arrows provided. Forms that get moved into the Done column will be reflected in the homepage's `Form Progress` column.

### Data overview
<img src="https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/admin-tables.png" alt="admin page data" width="600"/>

1. **Groups** - Groups allow you to define a set of access roles that will be applied to any user within that group. For example, I can define an Admin group and enable all permissions. Any user that is adding to the Admin group will also be given all permissions.

2. **Users** - Users are those that have a username and password to access this system. Users can be added to different groups and be given different permissions and restrictions.

3. **Form Types** - Think of Form Types as form categories. These are the overarching buckets that various forms fall into i.e. Intake Forms, Psychosocial Forms, etc. Every form must have a Form Type. 

4. **Form Youth Visits** - As the required forms may vary from youth to youth or youth visit to youth visit, this is where you can add or modify the forms that are required for a particular youth's stay in the shelter.

5. **Forms** - Here you can find all the forms that exist in the system.

6. **Placement Types** - Similar to Form Types, Placement Types represent the various bed types that can be assigned to youth. Every youth must have a Placement Type.

7. **School** - All schools that have ever been added into the system along with their district and phone number. We store this data to save you time when you enter new youth into the system.

8. **Youth Visits** - All youth visit data. A youth's name will appear one time for every visit they've ever had at this shelter. 

9. **Youth** - All youth in the system. This is separate from Youth Visits as it only displays the data that is non changing between different visits i.e. date of birth, ethnicity, etc.

### Adding admin user accounts
![admin accounts](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/admin-accounts.png)

To add new users, navigate to the Admin page and click `Users`. It's important to note that users are people that you want to have access to this system and the sensitive data it contains. The Admin page will prompt you for a username and password initially. After hitting save, you will be directed to a more robust user page that will allow you set strict permissions for this new user. These permissions are well-described on the page itself, but read them carefully as they permit users to perform various create, update, and delete actions.

### Entering a new youth or editing existing youth data
![admin youth visit](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/admin-youth-visit.png)

This page can be accessed either by clicking the `Add Youth` button off the homepage or through the admin page directly. If you're editing an existing youth's data, this page will look identical, but with the appropriate date fields already filled.

If the youth has been to the shelter before and has previous visit data in the system, start typing their name into the search box to autofill some of the required data. Otherwise, click the `add` button next to the youth field. 

The only fields required to enter a youth into the system are in **bold**. You are welcome to leave the remaining fields blank and return to edit them later. Be sure to click Save near the bottom of the page to finish the process. 

### Changing columns
![admin youth tracker columns](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/columns.png)

Use this page to modify the columns visible on the homepage. All available data fields will be listed, but you will have to select which ones will be displayed and in what order. Select a field name to change its ordering or its displayed name.

The ordering starts at 0, so given the example ordering in the screenshot above, `Youth Name` will be the first column shown in the homepage youth tracker.

### Import and Export
![admin import and export](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/import-export.png)

Near the bottom of the admin page, you should see options to both import and export your data. These functions are not intended to create or import full data backups and should only be used when importing a set of youth and youth visits (theoretically, this would only be necessary once, transfering current residents into the database after the system is deployed). 

`Export data` will download a CSV file with all current resident data. The format of this file will be the same one we expect on import. You can downlaod the template for the import format by clicking on `Download import template`. Once you have your data in the format specified, click `Choose file` to import your data into the system.

**NOTICE**:
Importing a new CSV file will overwrite all the youth visit data in the sytem. We recommend that this is only done for the initial onboard i.e. loading current resident data into the system when it's first deployed. If for reason you need to import a new set of youth visits, consider first backing up your data with the tool described in [this section](#restarting-the-server).

### Creating a Backup

This tool only exists on the server, and can only be accessed on the monitor attached to the server box. Once on the server, you should see an `InForm Database Backup Tool`. Clicking this will open the popup you see below:

![restart interface](https://github.com/ddmiller1995/InForm/blob/dev/docs/screenshots/restart-gui.png)

`Restart` will reboot *InForm* should it ever go down. We expect our tool to be back up and running in just a few minutes. `Download backup file` will export all of your data and prompt you to name the file and save it. As the name suggests, this should be used to create an entire backup of the system database. `Restore from a backup file` will prompt you the for the correct file. The backup file used here **must** be in the same format received when you download the backup file. You should never be restoring the system database with a file that was not directly downlaoded from this same popup.
