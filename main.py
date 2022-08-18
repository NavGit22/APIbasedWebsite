# Notes #
# 1. Get the list of all elephants - List All option
# https://elephant-api.herokuapp.com/elephants
# 2. Get the random elephant - Random option
# https://elephant-api.herokuapp.com/elephants/random
# 3. Fetch elephant based on Sex
# https://elephant-api.herokuapp.com/elephants/sex/{SEX}
# 4. Fetch elephant by Name
# https://elephant-api.herokuapp.com/elephants/name/{NAME}
# 5. Fetch elephant by Species
# https://elephant-api.herokuapp.com/elephants/species/{SPECIES}

import requests
from flask import Flask, render_template, request
from elephant import Elephant


# Initialize List to store objects
temp_objects = []
name_objects = []
species_objects = []
random_objects = []
gender_objects = []
elephant_objects = []
data_list = []

# API Endpoint URL
ALL_ELEPHANTS = 'https://elephant-api.herokuapp.com/elephants'
RANDOM_ELEPHANT = f"{ALL_ELEPHANTS}/random"


# Create elephant objects
def create_elephant_objects(elephants_data):
    temp_objects.clear()
    for elephant in elephants_data:
        try:
            elep_obj = Elephant(elephant['name'],
                                elephant['affiliation'],
                                elephant['species'],
                                elephant['sex'],
                                elephant['fictional'],
                                elephant['dob'],
                                elephant['dod'],
                                elephant['wikilink'],
                                elephant['image'],
                                elephant['note']
                                )
        except KeyError:
            pass
        else:
            temp_objects.append(elep_obj)
    return temp_objects


app = Flask(__name__)


@app.route('/')
def home():
    global elephant_objects
    response = requests.get(url=ALL_ELEPHANTS)
    response.raise_for_status()
    data = response.json()
    elephant_objects = create_elephant_objects(data)
    return render_template("index.html", elephants=elephant_objects)


@app.route('/random')
def random_home():
    global random_objects
    try:
        random_objects.clear()
    except ValueError:
        pass
    else:
        not_found = True
        while not_found:
            response = requests.get(url=RANDOM_ELEPHANT)
            response.raise_for_status()
            data = response.json()

            random_objects = create_elephant_objects(data)
            if len(random_objects) == 1:
                not_found = False
        return render_template("index.html", elephants=random_objects)


@app.route('/<gender>')
def gender_home(gender):
    global gender_objects
    try:
        gender_objects.clear()
    except ValueError:
        pass
    else:
        gender_elephant = f"{ALL_ELEPHANTS}/sex/{gender}"
        response = requests.get(url=gender_elephant)
        response.raise_for_status()
        data = response.json()
        gender_objects = create_elephant_objects(data)
        return render_template("index.html", elephants=gender_objects)


@app.route('/name', methods=['POST'])
def name_home():
    global name_objects
    global data_list

    name = request.form['name'].title()
    print(name)

    try:
        name_objects.clear()
        data_list.clear()
    except ValueError:
        pass
    else:
        name_elephant = f"{ALL_ELEPHANTS}/name/{name}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80'
        }
        response = requests.get(url=name_elephant, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            try:
                data_list.append(response.json())
            except:
                pass
            else:
                print(data_list)
                name_objects = create_elephant_objects(data_list)
                return render_template("index.html", elephants=name_objects)
    return render_template("index.html", elephants=elephant_objects)


@app.route('/species', methods=['POST'])
def species_home():
    global species_objects

    species = request.form['species'].title()
    print(species)

    try:
        species_objects.clear()
    except ValueError:
        pass
    else:
        species_elephant = f"{ALL_ELEPHANTS}/species/{species}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80'
        }
        response = requests.get(url=species_elephant, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            try:
                data = response.json()
            except:
                pass
            else:
                print(data)
                species_objects = create_elephant_objects(data)
                return render_template("index.html", elephants=species_objects)
    return render_template("index.html", elephants=elephant_objects)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")