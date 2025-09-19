

# Bookshelf Admin Integration

## Steps:

1. Registered the Book model in bookshelf/admin.py
2. Created BookAdmin class with:
   - list_display: 'title', 'author', 'publication_year'
   - list_filter: 'publication_year'
   - search_fields: 'title', 'author'
3. Registered the Book model with BookAdmin
4. Created superuser using python manage.py createsuperuser
5. Accessed Django admin at /admin and confirmed customized Book display
