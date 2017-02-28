from bs4 import BeautifulSoup
import dryscrape
import re
import requests


#def get_ingredients_for_recipe(recipe_url):
    # ingredients_to_quantities = {}

    # campsites = soup.find("table", {"class": "items"}, id="calendar")


def get_recipes(html_doc):
    recipes = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    recipe_links = soup.findAll("div", {"class": "recipe-thumb"})
    for recipe in recipe_links:
        link = recipe.find("a")['href']
        recipes.append("https://www.blueapron.com{0}".format(link))
    return recipes


def main():
    recipes_to_parse = ['recipes_blueapron_fish', 'recipes_blueapron_vegetarian']
    with open('cookbook', 'w') as cb:
        recipes_to_store = []
        for recipe in recipes_to_parse:
            with open(recipe) as f:
                recipes_to_store = recipes_to_store + get_recipes(f)
        for recipe in recipes_to_store:
            cb.write(recipe + "\n")

if __name__ == '__main__':
    main()
