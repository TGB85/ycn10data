import requests
from bs4 import BeautifulSoup
import pandas as pd
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

def get_rating(soup):
    s1 = "allerhande-icon svg svg--svg_star"
    s2 = "allerhande-icon svg svg--svg_star-half"
    full_stars = soup.find_all(class_=s1)
    half_stars = soup.find_all(class_=s2)
    return len(full_stars)+0.5*len(half_stars)

#gebruikt alle voorgaande functies en voegt de resultaten samen in een dictionary
def get_food(url):
    reqs= requests.get(url)
    soup= BeautifulSoup(reqs.text, 'html.parser')
    titel = get_title(soup)
    tags = get_tags(soup) 
    tags_split = split_tags(tags)
    time = get_time(soup)
    bereidingstijd, oventijd = split_time(time)
    aantal_personen = get_persons(soup)
    ingredienten = get_ingredients(soup)
    bereidings_stappen = get_steps(soup)
    rating = get_rating(soup)
    img = get_img(soup)
    dic = {'titel': titel, 'bereidingstijd':bereidingstijd, 'oventijd':oventijd, 'aantal_personen':aantal_personen, 'ingredienten':ingredienten, 'bereidings_stappen': bereidings_stappen, 'rating':rating, 'img': img}
    dic.update(tags_split)
    return dic

def check_gluten(tags):
    s = "gluten"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_vegetarisch(tags):
    s = "vegetarisch"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_lactose(tags):
    s = "lactose"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_veganistisch(tags):
    s = "veganistisch"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_zonder_vlees_vis(tags):
    s = "zonder vlees/vis"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_kerst(tags):
    s = "kerst"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_bbq(tags):
    s = "barbecue"
    for tag in tags:
        if s in tag:
            return True
    return False

def check_seizoen(tags):
    s = ["lente","zomer","herfst","winter"]
    seasons = [False,False,False,False]
    for tag in tags:
        if tag in s[0]:
            seasons[0]=True
        if tag in s[1]:
            seasons[1]=True
        if tag in s[2]:
            seasons[2]=True
        if tag in s[3]:
            seasons[3]=True
    return seasons

def check_region(tags):
    regions = ["aziatisch","mediterraan","zuid-amerikaans","amerikaans","midden-oosters","midden-amerika"]
    for tag in tags:
        if tag in regions:
            return tag
    return None

def check_country(tags):
    countries = ["italiaans","hollands","frans","mexicaans","indiaas","thais","spaans","chinees","indonesisch","japans","marokkaans",
    "grieks","engels","turks","scandinavisch","argentijns","vietnamees","oost-europees"]
    for tag in tags:
        if tag in countries:
            return tag
    return None

def check_recipe_type(tags):
    recipe_types = ["pasta","rijst","salade","soep","stamppot","quiche","brood/sandwiches","couscous","wrap","noedels"]
    for tag in tags:
        if tag in recipe_types:
            return tag
    return None

def split_tags(tags):
    glutenvrij = check_gluten(tags)
    vegetarisch = check_vegetarisch(tags)
    lactosevrij = check_lactose(tags)
    veganistisch = check_veganistisch(tags)
    zonder_vlees_vis = check_zonder_vlees_vis(tags)
    kerst = check_kerst(tags)
    bbq = check_bbq(tags)

    seizoenen = check_seizoen(tags)
    keuken1 = check_region(tags)
    keuken2 = check_country(tags)
    soort_recept = check_recipe_type(tags)
    dic = {"glutenvrij":glutenvrij,"vegetarisch":vegetarisch,"lactosevrij":lactosevrij,"veganistisch":veganistisch,"zonder_vlees_vis":zonder_vlees_vis,"kerst":kerst,"bbq":bbq,
    "lente":seizoenen[0],"zomer":seizoenen[1],"herfst":seizoenen[2],"winter":seizoenen[3],"keuken1":keuken1,"keuken2":keuken2,"soort_recept":soort_recept}
    return dic

def split_time(time):
    bereidingstijd = None
    oventijd = None
    for i in time:
        if "bereiden" in i:
            bereidingstijd = i.replace("bereiden","")
        if "oventijd" in i:
            oventijd = i.replace("oventijd","")
    return (bereidingstijd,oventijd)

def recipes_page(url):
    #url = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
    urls = get_urls(url)
    recipes = []
    n = 1
    k = len(urls)
    for i in urls:
        print(f'recipe {n} out of {k}.')
        n+=1
        url_recept = "https://www.ah.nl"+i
        recipes.append(get_food(url_recept))
    return pd.DataFrame(recipes)

if __name__ == "__main__":
    start = 240
    end = start+18
    url_base = "https://www.ah.nl/allerhande/recepten-zoeken?menugang=hoofdgerecht"
    df = pd.DataFrame()
    for i in range(start,end):
        url = url_base + f"&page={i}"
        print(url)
        df = pd.concat([df,recipes_page(url)])
    name = f"ah_recipes_{start}-{end}.csv"
    df.to_csv(name)

