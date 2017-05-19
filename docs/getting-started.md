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

* [Reading the front page](#Reading-the-front-page)

* [Presentation View](#presentation-view)

* [Marking a youth exited](#Marking-a-youth-as-exited)

* [Extending exit dates and changing placement types](#Extending-exit-dates-and-changing-placement-types)

* [Viewing and moving forms](#Viewing-and-moving-forms)

### Admin

* [Data overview](#data-overview)

* [Adding admin user accounts](#Adding-admin-user-accounts)

* [Entering a new youth or editing and existing youth data](#Entering-a-new-youth-or-editing-and-existing-youth-data)

### Reading the front page
![homepage](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/homepage.png)

Our homepage, by default, provides an overview of all current residents and their most pertinent case details. If you wish to view more details on a particular youth, you can click their name to be taken to their case profile. If you want to view youth that are no longer current residents, uncheck the `show active` checkbox near the top right corner. This will expand the youth chart to show all youth in the system, active or not. The `add youth` button can be used for adding a new youth visit into the sytem. See the [entering a new youth](#Entering-a-new-youth-or-editing-and-existing-youth-data) section for more information.

The color displayed for a youth's estimated exit date will change depending on how close we are to that date. If the estimated exit date is within the following three days, the date will be displayed as red. If it's within seven days, the date will be orange.

![homepage upcoming exits](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/homepage-colors.png)

### Marking a youth as exited
<img src="https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/exit-modal.png" alt="youth exit modal" width="200"/>

### Presentation View
![presentation view](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/presentation.png)

This page can be accessed from the homepage by clicking on `Presentation View`. The primary purpose of this page is to provide a non-clickable view of current residents. This ensures that, if this page were to be presented on a client-facing monitor, a staff member could not unintentionally click on a given youth and reveal sensitive case data.

### Marking a youth as exited
<img src="https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/exit-modal.png" alt="youth exit modal" width="400"/>

The exit modal appears when you click the `Add` button under Exit Date from the homepage. 

`Exit Date` will default to today's date, but can be modified to any other calendar date. Fill out the other fields as appropriate, or leave them alone if you wish to use their default values. These can always be changed later through the Admin page. Once you hit Save, the youth will be marked as exited and disappear from the active listing on the homepage.

As the popup specifies, this should only be used when the youth has left the shelter. Any extensions or bed changes must be done through the youth's case profile. 

### Extending exit dates and changing placement types
![youth profile](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/youth-profile-short.png)

<img src="https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/extend-modal.png" alt="extend youth visit modal" width="400"/>
<img src="https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/placement-modal.png" alt="change placement type modal" width="400"/>

Clicking on a youth from the homepage will bring you to that youth's case profile. A snippet of the case profile is shown above with the two update actions highlighted. 

Note that if the youth has multiple visits, you can view past visits by clicking through the dropdown menu in the top left corner.

The extend modal only requires one field `number of extension days`. This will default to 15 days, but can be modified. As you change the number of extension days, the `new estimated exit` date will update accordingly, but these changes *will not* be saved until you click Save. 

The modal used to switch beds has two fields `new placement type` and `transfer date`. Use the dropdown to select the new placement type. If you don't see a bed type listed, you must go to the Admin page to add it. `transfer date` will default to today's date, but can modified to any calendar date.

### Viewing and moving forms
![forms](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/forms.png)

Our form management tool can be found in the youth's case profile. This tool is used to track all forms required for a particular youth throughout their stay in the shelter. Form categories (here depicted as Intake and Psychosocial) can be collapsed using the ^ icons. Click on the info icon to see details for a particular form.

By default, all forms will be in the leftmost column but can be moved around using the arrows provided. Forms that get moved into the Done column will be reflected in the homepage's `Form Progress` column.

### Data overview
<img src="https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/admin-tables.png" alt="admin page data" width="600"/>

### Adding admin user accounts
![admin accounts](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/admin-accounts.png)

### Entering a new youth or editing existing youth data
![admin youth visit](https://github.com/ddmiller1995/InForm/blob/tessa-homepage/docs/screenshots/admin-youth-visit.png)

