# Fantasy Ground Custom Scripts

A collection of custom scripts to extract and modify data/xml from Fantasy Grounds.


### main.py
`main.py` can be used to modify the xml for player classes to match the PHB etc classes - allowing you to add custom features and subclasses to standard/existing classes. 
It does this by unpacking the a module in the `modules/raw` folder into `modules/unpacked`, then renaming the relevant xml tags based on the class name. It then repacks the module into the `modules/output` folder



### items.py
This takes the `db.xml` file from a FG module and extracts the items out of it. It then converts the xml items into a json format and adds additional categories to each item to allow better sorting etc.