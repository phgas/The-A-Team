To solve the typeguard problem in ydata-profiling:
- Just comment out decorator @typechecked for Class ProfileReport in C:\ProgramData\anaconda3\Lib\site-packages\ydata_profiling\profile_report.py on Line 53.

To solve the problem, where numbers aren't being displayed on the chart:
- Downgrade matplotlib: pip install matplotlib==3.7.3

To cre-create the process of creating the Django-API:
- django-admin startproject the_a_team
- cd the_a_team
- python manage.py startapp the_a_team
- pip install djangorestframework (needed for backend)
