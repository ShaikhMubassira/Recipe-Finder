import requests
from django.shortcuts import render

# Create your views here.

def index(request):
    url = requests.get("https://dummyjson.com/recipes/tags")
    recipes = requests.get("https://dummyjson.com/recipes").json()
    response = url.json()
    data = recipes["recipes"]

    context = {
        "tags" : response,
        "data" : data
    }

    return render(request, "index.html",context)


def databytags(request, tag):
    tags = requests.get("https://dummyjson.com/recipes/tags").json()
    response = requests.get(f"https://dummyjson.com/recipes/tag/{tag}").json()

    data = response["recipes"]
    context = {
        "data":data,
        "tags":tags
    }

    return render(request,"index.html",context)

def mealtype(request, meal):
    response = requests.get(f"https://dummyjson.com/recipes/meal-type/{meal}").json()
    tags = requests.get("https://dummyjson.com/recipes/tags").json()

    data = response["recipes"]
    context = {
        "data": data,
        "tags": tags
    }

    return render(request, "index.html",context)

def search(request):
    query = request.POST.get("query")
    response = requests.get(f"https://dummyjson.com/recipes/search?q={query}").json()

    tags = requests.get("https://dummyjson.com/recipes/tags").json()

    data = response["recipes"]
    context = {
        "data": data,
        "tags": tags
    }

    return render(request, "index.html", context)


def recipe_detail(request, id):
    response = requests.get(f"https://dummyjson.com/recipes/{id}").json()  # Fetch recipe data by id
    tags = requests.get("https://dummyjson.com/recipes/tags").json()

    context = {
        "recipe": response,
        "tags": tags
    }

    return render(request, "recipe_detail.html", context)

def singlepage(request, id):
    response = requests.get(f"https://dummyjson.com/recipes/{id}").json()

    # Get all recipes
    all_data = requests.get("https://dummyjson.com/recipes?limit=100").json()
    all_recipes = all_data.get("recipes",[])

    # Get tags of current recipe
    current_tags = response.get("tags",[])

    # Find 3 related recipes based on matching tags
    related = []
    for recipe in all_recipes:
        if recipe["id"] != response["id"]:
            # Check if any tag matches
            if any(tag in recipe.get("tags", []) for tag in current_tags):
                related.append(recipe)
        if len(related) == 3:
            break

    context = {
        "data": response,
        "related": related
    }
    return render(request, "receipes.html",context)
