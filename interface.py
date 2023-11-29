from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from collections import defaultdict
import ast

# Suponiendo que trasladaste la lógica de búsqueda a un módulo separado
def search_and_rank(words, inverted_index):
    results = defaultdict(int)

    for word in words:
        for url, count in inverted_index[raiz(word)]:
            results[url] += count

    ranked_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return ranked_results

# Implementa la lógica para obtener la raíz de una palabra
def raiz(word):
    pass

class SearchForm(forms.Form):
    query = forms.CharField(label='Ingrese palabras clave:', max_length=100, required=True)

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            words = query.split()

            # Carga el índice invertido desde el archivo
            with open('path/to/raiz_ind_inv.txt', 'r') as file:
                data = file.read()
                inverted_index = ast.literal_eval(data)

            results = search_and_rank(words, inverted_index)

            context = {'results': results}
            return render(request, 'search_results.html', context)
    else:
        form = SearchForm()

    return render(request, 'search_form.html', {'form': form})
