# Urban Map Services

Urban Map Services is a web application built with Python Django framework and PostgreSQL database management system to provide map-based services to users. The application employs model-view-controller (MVC) architecture where the models are relational tables stored in a database, the views are created with SQL queries for presenting the data, and the controller contains logic for updating the database and making corresponding changes in the views. Some of the services provided by the application include-
* Showing nearby restaurants, malls, ATMs and pharmacies
* Searching for a location with partial name
* Finding routes and schedules of buses and trains between two locations
* Finding all bus or trains from a particular station 

## Directory structure

```
app-config - application configurations
source
|- models.py - Models corresponding to database table schema
|- views.py - Functions to convert HTTP API calls to SQL queries to retrieve and present data
|- forms.py - HTML fields to take user input
|- admin.py - Models to show in administration page
|- urls.py - All supported URLs for the application
|- templates - HTML templates for the application
|- static - CSS and Javascript files
|- migrations - Database checkpoints
```
