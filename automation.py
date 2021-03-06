import pandas as pd
import formatting as f
import lmf as l
import os
import re
import json

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


def cleanse_phone(input):
    input =  re.sub("[^0-9]", '', str(input))
    return input


def format_categories(input_sub_category, live=None):
    response = l.get_categories(live).json().get('response')
    categories = response.get("categories", [])
    sub_categories = response.get('sub-categories', [])
    possible_categories = {c['Name']: c['_id'] for c in categories}
    # category, category_name = f.most_similar_output(input_category, possible_categories)
    possible_sub_categories = {sub_category['Name']: sub_category['_id'] for sub_category in sub_categories}
    # print("sub:", sub_categories)
    # print("---")
    # for sub in sub_categories:
    #     if 'Category' not in sub:
    #         print(sub)
    sub_categories_to_categories_name = {sub_category['Name']: sub_category['Category'] for sub_category in sub_categories}
    # print("Possible Sub Categories:", possible_sub_categories)
    sub_category, sub_category_name = f.most_similar_output(input_sub_category, possible_sub_categories)
    category = sub_categories_to_categories_name[sub_category_name]
    return category, sub_category


def format_inputs(row, dir_of_listings, main_image=None, live=None):
    address = cleanse_input(row["property_address"])
    street_address, city, state, zipcode = f.split_address(address)
    image_dir = os.path.join(dir_of_listings, address)
    try:
        image_path = os.path.join(image_dir, row["image_name"]+".webp")
        img = f.webp_to_jpg(image_path)
    except:
        image_path = os.path.join(image_dir, row["image_name"]+".jpg")
        img = f.load_jpg(image_path)
    orig_img = img
    if not main_image:
        x_s = (int(row["top_x"]), int(row["bottom_x"]))
        y_s = (int(row["top_y"]), int(row["bottom_y"]))
        img = f.buffer_crop(img, x_s, y_s)
        # img = f.crop_image(img, x_s, y_s)
    qty = int(row["quantity"])
    sub_category = f.format_input(row["sub_category"])
    product_name = f.format_input(row.get("product_name", sub_category))
    category, sub_category = format_categories(sub_category, live=live)
    return {"street_address": street_address, "city": city, "state": state,
            "zipcode": zipcode, "img": img, "qty": qty,
            "category": category, "sub_category": sub_category,
            "product_name": product_name, "original_image": orig_img}


def format_agent_inputs(row, dir_of_listings, live=None):
    address = cleanse_input(row["property_address"])
    try:
        name = f.format_input(row["listing_agents_name"])
    except:
        name = None
    try:
        firm = f.format_input(row["listing_agents_brokerage"])
    except:
        firm = None
    phone = str(cleanse_phone(str(row["listing_agents_phone"])))
    email = row["lisiting_agents_email"]
    property_id = row["property_id"]
    d = {"address": address, "name": name, "phone": phone, "email": email, 
            "property_id": property_id, "firm": firm}
    return {k: v if type(v) == str else '' for k, v in d.items()}


def create_property(row, dir_of_listings, live=None):
    inputs = format_inputs(row, dir_of_listings, main_image=True, live=live)
    # print(inputs)
    response = l.make_property(inputs["img"], inputs["street_address"], 
                    inputs["city"], inputs["state"], inputs["zipcode"], 
                    live)
    property_id = response.json()['response']['id']
    property_slug = response.json()['response']['slug']
    return {'id': property_id, 'slug': property_slug}


def create_agent(row, dir_of_listings, live=None):
    inputs = format_agent_inputs(row, dir_of_listings, live=live)
    response = l.create_agent(inputs["name"], inputs["email"], 
                    inputs["phone"], inputs["firm"], inputs["property_id"], live)
    agent_id = response.json()['response']['id']
    return agent_id


def main(dir_of_listings, property_columns, product_columns, name_of_file, live=None):
    listings_excel = os.path.join(dir_of_listings, name_of_file)
    data = pd.ExcelFile(listings_excel)
    # products = pd.read_excel(data, "Sheet1")
    # properties = pd.read_excel(data, "Sheet2")
    products = pd.read_excel(data, "Main (Classification&Location)")
    properties = pd.read_excel(data, "Realtor")
    df_properties = pd.DataFrame(properties, columns=property_columns)
    df_products = pd.DataFrame(products, columns=product_columns)
    visited_addresses= dict()
    succesful_properties = 0

    for index, row in df_products.iterrows():
        address = row["property_address"]
        if address not in visited_addresses:
            try:
                details = create_property(row, dir_of_listings,live)
                visited_addresses[address] = details
                succesful_properties += 1
            except Exception as e:
                # print("OOf")
                # print(str(e))
                # raise Exception("Ye")
                pass

    succesfull_products = 0
    succesfull_images = 0

    for index, row in df_products.iterrows():
        address = row["property_address"]
        if address in visited_addresses:
            try:
                inputs = format_inputs(row, dir_of_listings, main_image=None, live=live)
                product_response = l.create_product(inputs["product_name"], inputs["category"], inputs["sub_category"],
                                            visited_addresses[address]["id"], visited_addresses[address]["slug"], 
                                            inputs["qty"], live=live)
                succesfull_products += 1
                product_id = product_response.json()['response']['id']
                image_response = l.create_image(product_id, inputs["img"], live, original_img=inputs["original_image"])
                succesfull_images += 1
            except Exception as e:
                # print("Yikes:", str(e))
                pass

    succesful_agents = 0

    for index, row in df_properties.iterrows():
        address = row["property_address"]
        if address in visited_addresses:
            try:
                row["property_id"] = visited_addresses[address]["id"]
                details = create_agent(row, dir_of_listings, live=live)
                succesful_agents += 1
            except Exception as e:
                print(str(e))
                pass

    return succesful_properties, succesfull_products, succesfull_images, succesful_agents


if __name__ == '__main__':
    dir_of_listings = "/Users/ethangarza/Downloads/LMFData_Massachusetts_29_12_20"
    name_of_file = "LMFData_Massachusetts_29_12_2020.xlsx"

    # property_columns = ["property_address", "listing_agents_name", "listing_agents_phone", "lisiting_agents_email", "listing_agents_brokerage"]

    # products_columns = ["property_address", "image_name", "product_name", "quantity", 
    #         "category", "sub_category", "top_x", "top_y", "bottom_x", "bottom_y"]

    # dir_of_listings = "/Users/ethangarza/Downloads/LMF 8_12_2020"
    # name_of_file = "Master Excel Sheet (1).xlsx"

    products_columns = ["property_address", "image_name", "quantity", "sub_category", 
                        "top_x", "top_y", "bottom_x", "bottom_y", "costestimate",
                        "costestimate_1", "date"]

    property_columns =["S.No.", "property_address", "date_of_extraction",
            "cost_of_property", "URL", "listing_agents_name", "listing_agents_phone",
            "lisiting_agents_email", "listing_agents_brokerage"]

    # dir_of_listings = "/Users/ethangarza/Downloads/lmf tech"
    # name_of_file = "Master Excel Sheet lmf tech 123.xlsx" # Décor

    # products_columns = ["property edress", "image_name", "quantity", "Décor", "sub_category", 
    #                     "product_name", "top_x", "top_y", "bottom_x", "bottom_y", "cost"]

    # Only needs to be done once    
    cleanse_dir(dir_of_listings)

    # Is the automation / uploading code / process
    succesful_properties, succesfull_products, succesfull_images, succesful_agents = main(dir_of_listings, 
                                                                property_columns, products_columns, name_of_file)

    print("Uploading complete")
    print("Properties uploaded:", succesful_properties)
    print("Products uploaded:", succesfull_products)
    print("Images uploaded:", succesfull_images)
    print("Agents uploaded:", succesful_agents)
