from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book, Library


# ---------------------------
# Function-based view
# ---------------------------
def list_books(request):
    books = Book.objects.all()
    
    # Plain text output (or switch to template if you prefer)
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")

    # Optional template version:
    # return render(request, "list_books.html", {"books": books})


# ---------------------------
# Class-based view
# ---------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"  # uses your template
    context_object_name = "library"        # name in template

