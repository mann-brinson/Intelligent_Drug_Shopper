import mysql.connector

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TreatmentForm
from . import queries

class Connection():
    def __init__(self):
        self.mydb = self.create_db()
        self.cursor = self.create_cursor()

    def create_db(self): #called by __init__
        mydb = mysql.connector.connect(host="localhost",user="inf551",password='inf551',database='drug',auth_plugin='mysql_native_password')
        return mydb

    def create_cursor(self): #called by __init__
        cursor = self.mydb.cursor(buffered=True)
        return cursor

def default(request):
    return HttpResponse("Hello, world. You're at the shopper default.")

def search(request):
    '''Accept the query strings from the user.'''

    if request.method == "POST":
        form = TreatmentForm(request.POST)
        if form.is_valid():
            #Extract query strings from form
            form_data = request.POST.copy()
            condition = form_data['condition']
            price_high = form_data['price_high']
            current_med = form_data['current_med']

            print('current_med: ' , current_med == '')

            # context gets passed to the html template
            context = {'form': form, 'condition': condition}

            conn = Connection() #Crecte db connection
            #Construct query to get treatments
            if current_med == '': 
                cmd = queries.search_cond(condition, price_high)
            else: 
                cmd = queries.search_cond_currmed(condition, price_high, current_med)

            conn.cursor.execute(cmd)
            results = conn.cursor.fetchall()
            # print('result: ', results)

            #Add each result to the context
            result_list = []
            features = ['Product', 'Active Ingredient', 'Average Price']
            for row in results:
                ent = dict()
                for idx, feat in enumerate(features):
                    ent[feat] = row[idx]
                prod = row[0]
                ent['link'] = f'{prod}'
                result_list.append(ent)
            context['results'] = result_list
            #return HttpResponse("Good job.")
            return render(request, 'shopper/search.html', context)
    else:
        form = TreatmentForm()
        context = {'form': form}

    return render(request, 'shopper/search.html', context)

def prod_page(request, prod_details):
    items = prod_details.split('&')
    print('items: ', items)
    # items = ['source_id:1', 'prod_name:Advil']
    source_id = int(items[0].split(':')[1])
    prod_name = items[1].split(':')[1]

    # context gets passed to the html template
    context = {'prod_name': prod_name}

    conn = Connection() #Crecte db connection
    cmd = queries.search_prod_prices(source_id, prod_name)
    conn.cursor.execute(cmd)
    results = conn.cursor.fetchall()
    # print('result: ', results)

    #Add each result to the context
    result_list = []
    features = ['Store', 'Type', 'Price', 'Link']
    for row in results:
        ent = dict()
        for idx, feat in enumerate(features):
            ent[feat] = row[idx]
        result_list.append(ent)
    context['results'] = result_list

    # return HttpResponse("Good job.")
    return render(request, 'shopper/prod_page.html', context)


