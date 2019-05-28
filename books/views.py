from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from books.forms import ConnexionForm
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required




from books.models import Book

class BookList(ListView):
    model = Book

class BookView(DetailView):
    model = Book

class BookCreate(CreateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')

class BookUpdate(UpdateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages']

def book_list(request, template_name='books/book_list.html'):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, template_name, data)

def book_view(request, pk, template_name='books/book_detail.html'):
    book= get_object_or_404(Book, pk=pk)
    return render(request, template_name, {'object':book})

def book_create(request, template_name='books/book_form.html'):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})

def book_update(request, pk, template_name='books/book_form.html'):
    book= get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})

def book_delete(request, pk, template_name='books/book_confirm_delete.html'):
    book= get_object_or_404(Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, template_name, {'object':book})

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request,'books/connexion.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse_lazy(connexion))

@login_required(login_url='/connexion/')
def reconnexion(request):
    if request.method != "POST":
        return render(request, 'books/connexions.html')
    #...
