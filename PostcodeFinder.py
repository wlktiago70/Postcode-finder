import urllib.request
import json
import argparse
import codecs
key = "AIzaSyCbBq87dATXX-DQ8P98txk0ZCrxzwakhlQ"
def find_postal_code(str):
    # Getting data
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+urllib.parse.quote(str)+"&key="+key
    try:
        response = urllib.request.urlopen(url)
        response_content = response.read()
        response_json = json.loads(response_content)
        results = response_json["results"]
    except:
        print("An error occurred while getting data!")
    # Data classification
    number = "<NO DATA>"
    street = "<NO DATA>"
    neighborhood = "<NO DATA>"
    postalCode = "<NO DATA>"
    city = "<NO DATA>"
    state = "<NO DATA>"
    country = "<NO DATA>"
    for component in results[0]["address_components"]:
        if "street_number" in component["types"]:
            number = component["long_name"]
        elif "route" in component["types"]:
            street = component["long_name"]
        elif "sublocality" in component["types"]:
            neighborhood = component["long_name"]
        elif "postal_code" in component["types"]:
            postalCode = component["long_name"]
        elif "administrative_area_level_2" in component["types"]:
            city = component["long_name"]
        elif "administrative_area_level_1" in component["types"]:
            state = component["long_name"]
        elif "country" in component["types"]:
            country = component["long_name"]
    dict = {"Number":number}
    dict["Street"] = street
    dict["Neighborhood"] = neighborhood
    dict["Postalcode"] = postalCode
    dict["City"] = city
    dict["State"] = state
    dict["Country"] = country
    dict["Address"] = results[0]["formatted_address"]
    return dict
# Setup script arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--fin', nargs=1)
parser.add_argument('-o','--fout', nargs=1)
parser.add_argument('-l','--limit', nargs=1, default="0")
# Assign values from arguments to variables
fileIn = (parser.parse_args().fin)[0]
fileOut = (parser.parse_args().fout)[0]
limit = int((parser.parse_args().limit)[0])
# File handling
input = open("./"+fileIn)
content = input.read()
rows = content.split("\n")
output = codecs.open("./"+fileOut,"w","utf-8")
output.write("sep=,\n\"Establishment\",\"Partial Address\",\"Postal code\",\"Number\",\"Street\",\"Neighborhood\",\"City\",\"State\",\"Country\",\"Address\"\n")
count = 0
for row in rows:
    if count == limit:
        break
    data = [str.strip() for str in row.split(",")]
    dict = find_postal_code(data[1])
    print("Establishment..: "+data[0])
    print("Partial Address: "+data[1])
    print("Postal code....: "+dict["Postalcode"])
    print("Number.........: "+dict["Number"])
    print("Street.........: "+dict["Street"])
    print("Neighborhood...: "+dict["Neighborhood"])
    print("City...........: "+dict["City"])
    print("State..........: "+dict["State"])
    print("Country........: "+dict["Country"])
    print("Address........: "+dict["Address"])
    print("WRITING..................................................................................")
    output.write(data[0]+",=\""+data[1]+"\",=\""+dict["Postalcode"]+"\",=\""+dict["Number"]+"\",\""+dict["Street"]+"\",\""+dict["Neighborhood"]+"\",\""+dict["City"]+"\",\""+dict["State"]+"\",\""+dict["Country"]+"\",\""+dict["Address"]+"\"\n")
    count+=1
output.close()