import mysql.connector

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NameForm, ContactForm, TreatmentForm

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
    # return HttpResponse("search reached")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        form_data = request.POST.copy()
        name = form_data['your_name']
        print('name: ', name)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print('test')
            # redirect to a new URL:
            return HttpResponse("Query results go here.")

    # if a GET (or any other method) we'll create a blank form
    else:
        print('Visiting search page.')
        form = NameForm()

    return render(request, 'shopper/name.html', {'form': form})

def search2(request):
    '''Accept the query strings from the user.'''

    if request.method == "POST":
        form = TreatmentForm(request.POST)
        if form.is_valid():
            #Extract query strings from form
            form_data = request.POST.copy()
            condition = form_data['condition']
            price_high = form_data['price_high']
            print('condition: ' , condition)

            # context gets passed to the html template
            context = {'form': form, 'condition': condition}

            conn = Connection() #Crecte db connection
            #Construct query to get treatments
            cmd = f'''
            SELECT p.name prod_name, 
                (SELECT d.name
                FROM drug.drug d
                WHERE d.id = p.drug_id) drug_name,
                p.avg_price
            FROM drug.product p
            WHERE p.source_id = 1 #wiki
            AND p.drug_id IN (SELECT t.drug_id
                            FROM drug.treatment t
                            WHERE t.source_id = 1 #wiki
                            AND t.condition_id IN (SELECT c.id
                                                    FROM drug.condition c
                                                    WHERE c.name = "{condition}"
                                                    AND c.source_id = 1 #wiki
                                )
                            )
            AND p.avg_price < {price_high}
            ORDER BY p.avg_price
            '''
            conn.cursor.execute(cmd)
            results = conn.cursor.fetchall()
            print('result: ', results)

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
            return render(request, 'shopper/search2.html', context)
    else:
        form = TreatmentForm()
        context = {'form': form}

    return render(request, 'shopper/search2.html', context)

def prod_page(request, prod_details):
    return HttpResponse("Good job.")
    # pass


