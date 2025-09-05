from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from bson.objectid import ObjectId
from pymongo import MongoClient
from .forms import EmployeeForm

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["EmployeeDB"]
collection = db["employees"]

# ---------------- Authentication ----------------
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("employee_list")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("employee_list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

# ---------------- Employee CRUD ----------------
@login_required
def employee_list(request):
    employees = list(collection.find())
    for e in employees:
        e["id"] = str(e["_id"])
    return render(request, "employee_list.html", {"employees": employees})


@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if "salary" in data and data["salary"] is not None:
                data["salary"] = float(data["salary"])
            collection.insert_one(data)
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(request, "employee_form.html", {"form": form})


@login_required
def employee_update(request, emp_id):
    employee = collection.find_one({"_id": ObjectId(emp_id)})
    if not employee:
        return redirect("employee_list")

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if "salary" in data and data["salary"] is not None:
                data["salary"] = float(data["salary"])
            collection.update_one({"_id": ObjectId(emp_id)}, {"$set": data})
            return redirect("employee_list")
    else:
        form = EmployeeForm(initial=employee)

    return render(request, "employee_form.html", {"form": form})


@login_required
def employee_delete(request, emp_id):
    collection.delete_one({"_id": ObjectId(emp_id)})
    return redirect("employee_list")
