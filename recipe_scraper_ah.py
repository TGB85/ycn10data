import requests
from bs4 import BeautifulSoup
import re

#haalt alle links uit de recepten kaarten van een pagina zoals: 'https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht',
#geeft een lijst met deel urls die 'https://www.ah.nl' ervoor missen
def get_urls(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a',class_="display-card_root__o17AY card_root__VNG0M card_roundCorners__dYaFu display-card_anchor__cTFon"):
        urls.append(link.get('href'))
    return urls

def get_title(soup):
    s = "typography_root__Om3Wh typography_variant-superhero__239x3 typography_hasMargin__4EaQi recipe-header_title__tG0JE"
    for i in soup.find_all(class_=s):
        title = i.text
    return title

def get_tags(soup):
    s = "typography_root__Om3Wh typography_variant-paragraph__T5ZAU typography_weight-strong__uEXiN recipe-tag_text__aKcWG"
    tags = []
    for i in soup.find_all(class_=s):
        tags.append(i.text)
    return list(set(tags))

def get_time(soup):
    s = 'recipe-header-time_timeLine__nn84w'
    time = []
    for i in soup.find_all(class_=s):
        time.append(i.text)
    return time

def get_ingredients(soup):
    s1 = "typography_root__Om3Wh typography_variant-paragraph__T5ZAU typography_weight-strong__uEXiN typography_hasMargin__4EaQi ingredient_unit__-ptEq"
    s2 = "typography_root__Om3Wh typography_variant-paragraph__T5ZAU typography_hasMargin__4EaQi ingredient_name__WXu5R"
    ingredients = []
    for i, j in zip(soup.find_all(class_=s1),soup.find_all(class_=s2)):
        ingredients.append((i.text, j.text))
    return ingredients

def get_steps(soup):
    s = "recipe-steps_step__FYhB8"
    steps = []
    for i in soup.find_all(class_=s):
        steps.append(i.text)
    return steps

def get_img(soup):
    s = "figure_imageObjectFit__6Atjm lazyload"
    srcset = soup.find(class_=s).get("data-srcset")
    img = srcset.split(" ")[0]
    return img

def get_persons(soup):
    s = "typography_root__Om3Wh typography_variant-paragraph__T5ZAU typography_hasMargin__4EaQi recipe-ingredients_count__zS2P-"
    persons = soup.find(class_=s)
    return persons.text

#gebruikt alle voorgaande functies en voegt de resultaten samen in een dictionary
def get_food(url):
    reqs= requests.get(url)
    soup= BeautifulSoup(reqs.text, 'html.parser')
    
    title = get_title(soup)
    tags = get_tags(soup) 
    print(split_tags(tags))
    time = get_time(soup)
    persons = get_persons(soup)
    ingredients = get_ingredients(soup)
    steps = get_steps(soup)
    img = get_img(soup)
    return {'title': title, 'time':time, 'tags':tags, 'persons':persons, 'ingredients':ingredients, 'steps': steps, 'img': img}

def split_tags(tags):
    #check_seizoen(i)
    g = check_gluten(tags)
    return g

# def check_seizoen(tag):
#     s = ["lente","zomer","herfst","winter"]
#     if tag in s:

def check_gluten(tags):
    s = "gluten"
    for tag in tags:
        if s in tag:
            return True
    return False




if __name__ == "__main__":
    url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
    urls = get_urls(url)
    recipes = []
    for i in urls:
        url_recept = "https://www.ah.nl"+i
        recipes.append(get_food(url_recept))
    print(recipes[10])
