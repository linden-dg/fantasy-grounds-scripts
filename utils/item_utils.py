from shutil import copyfile
import re


def get_text(ele, fallback=""):
    return ele.text if (ele is not None and ele.text is not None) else fallback


ARMOR_TYPES = {
    'Leather': "Light Armor",
    'Padded': "Light Armor",
    'Studded Leather': "Light Armor",
    'Hide': "Medium Armor",
    'Chain Shirt': "Medium Armor",
    'Breastplate': "Medium Armor",
    'Scale Mail': "Medium Armor",
    'Half Plate': "Medium Armor",
    'Ring Mail': "Heavy Armor",
    'Chain Mail': "Heavy Armor",
    'Splint': "Heavy Armor",
    'Plate': "Heavy Armor",
    'Shield': "Shield Armor",
}

WEAPON_TYPES = {
    ('Spear', 'Greatclub', 'Dagger', 'Handaxe', 'Javelin', 'Club', 'Sickle', 'Light Hammer',
     'Quarterstaff', 'Mace'): "Simple Melee Weapons",

    ('Sling', 'Shortbow', 'Crossbow, Light', 'Dart'): "Simple Ranged Weapons",

    ('Rapier', 'Pike', 'Morningstar', 'Longsword (S)', 'War Pick', 'Halberd', 'Warhammer',
     'Flail', 'Greatsword', 'Lance', 'Glaive', 'Longsword', 'Whip', 'Trident', 'Maul', 'Battleaxe',
     'Scimitar', 'Shortsword', 'Greataxe'): "Martial Weapons",

    ('Blowgun', 'Net', 'Longbow', 'Crossbow, Hand',
     'Crossbow, Heavy'): "Martial Ranged Weapons",

    ('Blowgun Needles (50)', 'Crossbow Bolts (20)', 'Arrows (20)', 'Sling Bullet (5)', 'Crossbow Bolt',
     'Blowgun Needle', 'Arrow', 'Sling Bullets (20)'): "Ammunition"
}


def misc_items_category(item):
    subtype = get_text(item.find("subtype"))
    name = get_text(item.find("name"))

    if "Bag" in name or "Sack" in name or "Backpack" in name:
        return {
            "category": "Equipment",
            "type": "Container",
            "subtype": "Bag"
        }

    elif "Quiver" in name:
        return {
            "category": "Equipment",
            "type": "Container",
            "subtype": "Ammunition"
        }

    elif "Wand" in name or "Rod" in name:
        return {
            "category": "Weapon",
            "type": "Arcane Focus",
            "subtype": name
        }

    elif "Amulet" in name \
            or "Medallion" in name \
            or "Necklace" in name \
            or "Periapt" in name \
            or "Talisman" in name:
        return {
            "category": "Equipment",
            "type": "Jewelery",
            "subtype": "Amulet"
        }

    elif "Belt" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Belt"
        }

    elif "Cloak" in name or "Cape " in name or "Mantle" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Cloak"
        }

    elif "Robe" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Robe"
        }
    elif "Clothes" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Clothes"
        }

    elif "Boot" in name or "Slippers" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Footwear"
        }

    elif "Bracers" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Bracers"
        }

    elif "Gauntlet" in name or "Glove" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Hands"
        }

    elif "Brooch" in name:
        return {
            "category": "Equipment",
            "type": "Jewelery",
            "subtype": "Brooch"
        }

    elif "Instrument" in name or "Pipes" in name or "Horn of" in name:
        return {
            "category": "Tools",
            "type": "Musical Instrument",
            "subtype": item.find('spells').find('id-00002').find('name').text
        }

    elif "Cap " in name \
            or "Circlet " in name \
            or "Eyes of " in name \
            or "Goggles" in name \
            or "Hat" in name \
            or "Headband" in name \
            or "Helm" in name \
            or "Ioun" in name:
        return {
            "category": "Equipment",
            "type": "Clothing",
            "subtype": "Headwear"
        }

    elif "Tome" in name or "Manual of" in name:
        return {
            "category": "Consumable",
            "type": "Tome",
            "subtype": None
        }

    elif "Book" in name:
        return {
            "category": "Equipment",
            "type": "Book",
            "subtype": None
        }

    elif "Poison" in subtype:
        return {
            "category": "Consumable",
            "type": subtype,
            "subtype": None
        }

    elif "Potion" in name:
        return {
            "category": "Consumable",
            "type": "Potion",
            "subtype": None
        }

    elif "Ammunition" in subtype:
        return {
            "category": "Weapon",
            "type": subtype,
            "subtype": name.split("s (")[0]
        }

    return {
        "category": "Misc",
        "type": "Trinket",
        "subtype": None
    }


def categories(item):
    item_type = get_text(item.find('type'))
    subtype = get_text(item.find('subtype'))

    print(f'name -> {item.find("name").text}')

    if (item_type == "Armor"):
        return {
            "category": item_type,
            "type": ARMOR_TYPES[subtype],
            "subtype": subtype
        }
    elif (item_type == "Weapon"):
        new_type = "Misc"
        for key in WEAPON_TYPES:
            if subtype in key:
                new_type = WEAPON_TYPES[key]
        return {
            "category": "Weapon",
            "type": new_type,
            "subtype": subtype.split("s (")[0]
        }
    elif (item_type == "Staff"):
        return {
            "category": "Weapon",
            "type": "Simple Melee",
            "subtype": item_type
        }
    elif (item_type == "Rod" or item_type == "Wand"):
        return {
            "category": "Weapon",
            "type": "Arcane Focus",
            "subtype": item_type
        }

    elif (item_type == "Wondrous Item"):
        return misc_items_category(item)

    elif (item_type == "Ring"):
        return {
            "category": "Equipment",
            "type": "Jewelery",
            "subtype": item_type
        }
    elif (item_type == "Potion"):
        return {
            "category": "Consumable",
            "type": item_type,
            "subtype": None
        }
    elif (item_type == "Scroll"):
        return {
            "category": "Consumable",
            "type": item_type,
            "subtype": None
        }


def mundane_categories(item):
    item_type = get_text(item.find("type"))
    subtype = get_text(item.find("subtype"))
    name = get_text(item.find("name"))

    print(f'name -> {name}')

    if item_type == "Adventuring Gear":
        return misc_items_category(item)

    elif item_type == "Treasure":
        return treasure_categories(item)

    elif item_type == "Weapon":
        return mundane_weapon_categories(item)

    return {
        "category": item_type,
        "type": subtype,
        "subtype": name.split(" (")[0]
    }


def treasure_categories(item):
    type_comp = get_text(item.find("subtype")).split(" (")
    return {
        "category": "Treasure",
        "type": type_comp[0],
        "subtype": type_comp[1][:-1]
    }


def mundane_weapon_categories(item):
    subtype = get_text(item.find("subtype"))
    name = get_text(item.find("name"))

    if "Firearms" in subtype:
        return {
            "category": "Weapon",
            "type": "Firearms",
            "subtype": subtype.split(" Firearms")[0]
        }

    elif "Renaissance" in subtype:
        return {
            "category": "Weapon",
            "type": subtype.split("Renaissance ")[1],
            "subtype": "Renaissance"
        }

    elif "Modern" in subtype:
        return {
            "category": "Weapon",
            "type": subtype.split("Modern ")[1],
            "subtype": "Modern"
        }

    else:
        return {
            "category": "Weapon",
            "type": subtype,
            "subtype": name.split(" (")[0]
        }


def fetch_img_link(link_ele, img_links):
    q = re.search('reference.imagedata.(.*)\\@\\*', link_ele.attrib['recordname'])
    img_link = q.group(1)
    # ele = img_links_xml.find(img_link)
    link = img_links[img_link]  # ele.find('image').find('bitmap').text
    src = link.replace("\\", "/")
    dst = src.replace("images", "dmg")
    copyfile(f'./items/{src}', f'./items/{dst}')
    return dst
