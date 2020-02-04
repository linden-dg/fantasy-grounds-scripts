from lxml import etree
from utils.item_utils import categories, fetch_img_link, get_text, mundane_categories

xmlfolder = f'./items'
xmlfile = 'db.xml'
img_link_xmlfile = 'DMG_item_img_links.xml'

tree = etree.parse(open(f'{xmlfolder}/{xmlfile}', 'r'))
root = tree.getroot()

magic_items_data = root.find('reference').find('magicitemdata')
equipment_data = root.find('reference').find('equipmentdata')

img_links = {}
for img_cat in root.find('reference').find('imagedata'):
    for img in img_cat:
        img_links.update({
            img.tag : img.find('image').find('bitmap').text
        })


def create_item(x, source, img_links, magic=True):
    link = None
    desc_div = etree.Element('div')

    rarity_components = get_text(x.find("rarity")).split(" (Requires Attunement")
    cat = categories(x) if magic else mundane_categories(x)
    desc = x.find("description")

    if desc is not None:
        links = desc.findall('link')
        desc_p = desc.findall('p')
        for p in desc_p:
            t = etree.SubElement(desc_div, "p")
            t.text = p.text

        for l in links:
            if l.attrib['class'] == "imagewindow":
                link = fetch_img_link(l, img_links)

    item = {
        "name": get_text(x.find("name")),
        "rarity": rarity_components[0] if magic else "Adventuring Gear",
        "category": cat["category"],
        "type": cat["type"],
        "subtype": cat["subtype"],
        "attunement": len(rarity_components) > 1,
        "img": link,
        "source": source,
        "data": {
            "nonid_name": get_text(x.find("nonid_name")),
            "appearance": get_text(x.find("nonidentified")),
            "description": etree.tostring(desc_div, encoding="unicode"),
            # "description_elements": description,
            "properties": get_text(x.find("properties")),
            "weight": get_text(x.find("weight")),
            "cost": get_text(x.find("cost")),
            "attune_text": None if len(rarity_components) <= 1 or rarity_components[
                1] == ")" else f'{rarity_components[1][1:-1]}',
        },
        "meta": {
            "fg_id": x.tag,
            "fg_category": "magicitemdata" if magic else "equipmentdata"
        }
    }
    if x.find('type').text == "Armor":
        item["data"].update({
            "ac": get_text(x.find("ac")),
            "dexbonus": get_text(x.find("dexbonus")),
            "strength": get_text(x.find("strength")),
            "stealth":  get_text(x.find("stealth")),
            "bonus": get_text(x.find("bonus")),
        })
    elif x.find('type').text == "Weapon":
        item["data"].update({
            "bonus": get_text(x.find("bonus")),
            "damage": get_text(x.find("damage")),
        })

    return item


magic_items = [
    create_item(i, "DMG", img_links) for i in magic_items_data
]

basic_items = [
    create_item(i, "DMG", img_links, magic=False) for i in equipment_data
]

items = basic_items + magic_items

basic_category = {c['category'] for c in basic_items}
magic_category = {c['category'] for c in magic_items}
