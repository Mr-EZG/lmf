import pandas as pd
import formatting as f
import lmf as l
import os
import re

def cleanse_dir(dir_of_listings):
    for d in os.listdir(dir_of_listings):
        full_path = os.path.join(dir_of_listings, d)
        if os.path.isdir(full_path):
            old_d = d
            new_d =  re.sub("[^0-9a-zA-Z, ]", ' ', str(old_d))
            new_full_path = os.path.join(dir_of_listings, new_d)
            os.rename(full_path, new_full_path)


def cleanse_input(input):
    input =  re.sub("[^0-9a-zA-Z, ]", ' ', str(input))
    return input


def format_inputs(row, dir_of_listings, main_image=None):
    address = cleanse_input(row["property_address"])
    street_address, city, state, zipcode = f.split_address(address)
    image_dir = os.path.join(dir_of_listings, address)
    try:
        image_path = os.path.join(image_dir, row["image_name"]+".webp")
        img = f.webp_to_jpg(image_path)
    except:
        image_path = os.path.join(image_dir, row["image_name"]+".jpg")
        img = f.load_jpg(image_path)
    if not main_image:
        x_s = (int(row["top_x"]), int(row["bottom_x"]))
        y_s = (int(row["top_y"]), int(row["bottom_y"]))
        img = f.crop_image(img, x_s, y_s)
    qty = int(row["quantity"])
    product_name = f.format_input(row["product_name"])
    category = f.format_input(row["category"])
    sub_category = f.format_input(row["sub_category"])
    return {"street_address": street_address, "city": city, "state": state,
            "zipcode": zipcode, "img": img, "qty": qty,
            "category": category, "sub_category": sub_category,
            "product_name": product_name}


def create_property(row, dir_of_listings, live=None):
    inputs = format_inputs(row, dir_of_listings, main_image=True)
    response = l.make_property(inputs["img"], inputs["street_address"], 
                    inputs["city"], inputs["state"], inputs["zipcode"], 
                    live)
    property_id = response.json()['response']['id']
    property_slug = response.json()['response']['slug']
    return {'id': property_id, 'slug': property_slug}


def main(dir_of_listings, columns, name_of_file, live=None):
    listings_excel = os.path.join(dir_of_listings, name_of_file)
    data = pd.read_excel(listings_excel)
    df = pd.DataFrame(data, columns=columns)
    visited_addresses= dict()
    succesful_properties = 0

    for index, row in df.iterrows():
        address = row["property_address"]
        if address not in visited_addresses:
            try:
                details = create_property(row, dir_of_listings,live)
                visited_addresses[address] = details
                succesful_properties += 1
            except Exception as e:
                pass

    succesfull_products = 0
    succesfull_images = 0

    for index, row in df.iterrows():
        address = row["property_address"]
        if address in visited_addresses:
            try:
                inputs = format_inputs(row, dir_of_listings, main_image=None)
                product_response = l.create_product(inputs["category"], inputs["sub_category"],
                                            visited_addresses[address]["id"], visited_addresses[address]["slug"], 
                                            inputs["qty"], live)
                succesfull_products += 1
                product_id = product_response.json()['response']['id']
                image_response = l.create_image(product_id, inputs["img"], live)
                succesfull_images += 1
            except Exception as e:
                pass

    return succesful_properties, succesfull_products, succesfull_images


if __name__ == '__main__':
    dir_of_listings = "/Users/ethangarza/Downloads/fixeddata_tab_v23-2.2"
    name_of_file = "fixeddata_tab_v23.2.xlsx"

    columns = ["property_address", "image_name", "product_name", "quantity", 
            "category", "sub_category", "top_x", "top_y", "bottom_x", "bottom_y"]

    # Only needs to be done once    
    cleanse_dir(dir_of_listings)

    # Is the automation / uploading code / process
    succesful_properties, succesfull_products, succesfull_images= main(dir_of_listings, columns, name_of_file)

    print("Uploading complete")
    print("Properties uploaded:", succesful_properties)
    print("Products uploaded:", succesfull_products)
    print("Images uploaded:", succesfull_images)
