from lxml import etree
from utils.zip_utils import zip_folder, extract_to_directory


def format_class_data(xml_root):
    reference = xml_root.find('reference')
    classdata = reference.find('classdata')[0]
    for c in classdata:
        classname = c.find('name').text.lower()
        if classname in BASE_CLASSES:
            c.tag = classname
            print(f'Formatted tag for {classname}')


BASE_CLASSES = (
    'artificer',
    'barbarian',
    'bard',
    'cleric',
    'druid',
    'fighter',
    'monk',
    'paladin',
    'ranger',
    'rogue',
    'sorcerer',
    'warlock',
    'wizard',
)

filename = 'Zen-player'

extract_to_directory(filename)

xmlfolder = f'./modules/unpacked/{filename}'
xmlfile = 'client.xml'

tree = etree.parse(open(f'{xmlfolder}/{xmlfile}', 'r'))
root = tree.getroot()

format_class_data(root)

export_tree = etree.tostring(tree, pretty_print=True)
f = open(f'{xmlfolder}/{xmlfile}', "wb")
f.write(export_tree)
f.close()

zip_folder(filename)

