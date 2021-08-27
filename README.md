# URLcounter

Setup:

1. Start PostreSQL server, add credentials and connection information into URLtagsCounter\settings.py
2. run "python manage.py migrate" to apply migrations
3. run "python manage.py runserver" to start debug server

Endpoints:

1. "/add" adds new URL and starts counting process. Returns url_id
2. "/get/<int:url_id>" returns counting result or message if counting isn't finished
3. "/update/<int:url_id>" repeats counting process for URL. Returns url_id
