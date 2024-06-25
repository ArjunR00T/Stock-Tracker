from django.shortcuts import render, redirect
from .models import product, purchases
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import recordForm

# Create your views here.
bag = {}
l = {}
name = ''
cp = ''
sp = ''
qty = ''


def all_products(request):

    data = purchases.objects.all
    total_cost_price, total_selling_price, profit = statistics()

    return render(request, 'stats.html', {'product': data, 'cp': total_cost_price, 'sp': total_selling_price, 'profit': profit})


def base(request):
    global bag
    global l

    if request.method == 'POST' and 'search' in request.POST:
        l = product.objects.filter(name__contains=request.POST['pname'])
        return render(request, 'base.html', {"product": l, "bag": bag, "total": gettotal(bag)})

    elif request.method == 'POST' and 'all' in request.POST:
        return HttpResponseRedirect('all_products')

    elif request.method == 'POST' and 'admin' in request.POST:
        return HttpResponseRedirect('admin')

    elif request.method == 'POST' and 'table' in request.POST:
        return HttpResponseRedirect('records')

    elif request.method == 'POST' and 'add' in request.POST:
        item = request.POST['add'].split(',')[0]
        price = request.POST['add'].split(',')[1]
        available_qty = product.objects.filter(
            name__contains=item).values('nos')[0].get('nos')
        if item in bag:
            c = int(bag.get(item)[0])
            if c < available_qty:
                c = c+1
            newPrice = float(price) * int(c)
            bag.update({item: [c, newPrice]})
        else:
            bag.update({item: [1, price]})
        return render(request, 'base.html', {"product": l, "bag": bag, "total": gettotal(bag)})

    elif request.method == 'POST' and 'delete' in request.POST:
        if len(bag) != 0:
            item = request.POST['delete']
            price = bag.get(item)[1]
            qty = bag.get(item)[0]

            if qty != 1:
                price_for_one = price / qty
                new_qty = qty-1
                new_price = new_qty * price_for_one
                updated_items = {item: [new_qty, new_price]}
                bag.update(updated_items)
            else:
                del bag[item]
        return render(request, 'base.html', {"product": l, "bag": bag, "total": gettotal(bag)})

    elif request.method == 'POST' and 'Confirm' in request.POST:
        updateDatabase(bag)
        bag.clear()
        return render(request, 'base.html', {"product": product.objects.all, "bag": gettotal(bag)})

    data = product.objects.all
    return render(request, 'base.html', {"product": data, "bag": bag, "total": gettotal(bag)})


def updateDatabase(bag):
    nos = 0
    for k, v in bag.items():
        p = product.objects.filter(name=k)
        for i in p:
            nos = i.nos
            product.objects.filter(name=k).update(nos=nos-int(v[0]))
        purchases.objects.create(name=k, cost=v[1], nos=int(
            v[0]), payment=True, date=datetime.now())


def gettotal(bag):
    total = 0
    for k, v in bag.items():
        prices = v[1]
        total = total + float(prices)
    return total


def statistics():
    total_cost_price = 0
    total_selling_price = 0
    profit = 0
    items_bought = []
    available_items = []

    sellingprice = purchases.objects.values('name', 'cost')
    costprice = product.objects.values('name', 'cp')

    for sp in sellingprice:
        total_selling_price = total_selling_price + float(sp.get('cost'))
        items_bought.append(sp.get('name'))

    for cp in costprice:
        available_items.append((cp.get('name')))

    for item in items_bought:
        if (item in available_items):
            cost = product.objects.filter(name=item).values('cp')
            total_cost_price += float(cost[0].get('cp'))

    profit = total_selling_price - total_cost_price

    return total_cost_price, total_selling_price, profit


def records(request):
    data = product.objects.all()

    if request.method == 'POST' and 'add' in request.POST:
        form = recordForm(request.POST)
        name = form['name'].value()
        cp = form['cp'].value()
        sp = form['sp'].value()
        qty = form['qty'].value()

        product.objects.create(name=name, cp=cp, sp=sp, nos=qty)
        return render(request, 'records.html', {'product': data, 'form': form})

    if request.method == 'POST' and 'delete' in request.POST:

        name = request.POST['delete']
        form = recordForm()
        product.objects.filter(name=name).delete()
        return render(request, 'records.html', {'product': data, 'form': form})

    if request.method == 'POST' and 'edit' in request.POST:
        info = (request.POST['edit']).split(',')
        name = info[0]
        cp = info[1]
        sp = info[2]
        qty = info[3]

        form = recordForm(
            initial={'name': name, 'cp': cp, 'sp': sp, 'qty': qty})

        set_edit(form['name'].value(), form['cp'].value(),
                 form['sp'].value(), form['qty'].value())

        return HttpResponseRedirect('editrecords')
        # return render(request, 'editrecords.html',{'product':data,'form':form})

    return render(request, 'records.html', {'product': data, 'form': recordForm()})


def editrecords(request):
    name, cp, sp, qty = get_edit()
    form = recordForm(
        initial={'name': name, 'cp': cp, 'sp': sp, 'qty': qty})

    name = form['name'].value()
    cp = form['cp'].value()
    sp = form['sp'].value()
    qty = form['qty'].value()

    
    if 'add' in request.POST:
        form = recordForm(request.POST)
        newname = form['name'].value()
        newcp = form['cp'].value()
        newsp = form['sp'].value()
        newqty = form['qty'].value()

        product.objects.filter(name=name, cp=cp, sp=sp, nos=qty).delete()
        product.objects.create(name=newname, cp=newcp, sp=newsp, nos=newqty)

    return render(request, 'editrecords.html', {'form': form})


def set_edit(itemname, itemcp, itemsp, itemqty):
    global name
    global cp
    global sp
    global qty

    name = itemname
    cp = itemcp
    sp = itemsp
    qty = itemqty


def get_edit():
    global name
    global cp
    global sp
    global qty
    return name, cp, sp, qty
