import xml.etree.ElementTree as ET

# Example XML data
xml_data = '''
<root>
    <person>
        <name>John Doe</name>
        <age>30</age>
        <city>New York</city>
    </person>
    <person>
        <name>Jane Smith</name>
        <age>25</age>
        <city>London</city>
    </person>
</root>
'''

# Parse the XML data
root = ET.fromstring(xml_data)

# Access elements and attributes
for person in root.findall('person'):
    name = person.find('name').text
    age = int(person.find('age').text)
    city = person.find('city').text
    print(name, age, city)
