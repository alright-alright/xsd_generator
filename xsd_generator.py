import xml.etree.ElementTree as ET

def parse_xml_to_structure(xml_file):
    """Parses the XML file and extracts element details for XSD generation."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    element_structure = {}

    def traverse(element, path="root"):
        path = f"{path}/{element.tag}"
        if path not in element_structure:
            element_structure[path] = {
                'tag': element.tag,
                'attributes': list(element.attrib.keys()),
                'children': set(),
                'sample_data': element.text.strip() if element.text else ''
            }
        for child in element:
            element_structure[path]['children'].add(child.tag)
            traverse(child, path)

    traverse(root)
    return element_structure

def generate_xsd_template(element_structure):
    """Generates a basic XSD template based on the parsed XML structure."""
    xsd_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">'
    ]

    def create_xsd_element(path, details):
        indent = " " * (path.count('/') * 2)
        element_line = f'{indent}<xs:element name="{details["tag"]}"'
        if details['children']:
            element_line += '>'
            xsd_lines.append(element_line)
            xsd_lines.append(f'{indent}  <xs:complexType>')
            xsd_lines.append(f'{indent}    <xs:sequence>')
            for child in details['children']:
                xsd_lines.append(f'{indent}      <xs:element name="{child}" type="xs:string" minOccurs="0"/>')
            xsd_lines.append(f'{indent}    </xs:sequence>')
            xsd_lines.append(f'{indent}  </xs:complexType>')
            xsd_lines.append(f'{indent}</xs:element>')
        else:
            element_line += ' type="xs:string" minOccurs="0"/>'
            xsd_lines.append(element_line)

    for path, details in element_structure.items():
        create_xsd_element(path, details)

    xsd_lines.append('</xs:schema>')
    return "\n".join(xsd_lines)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python xsd_parser.py path/to/your/exported_health_record.xml")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    xml_structure = parse_xml_to_structure(xml_file_path)

    # Print out the structure for verification
    for path, details in xml_structure.items():
        print(f"Path: {path}, Tag: {details['tag']}, Attributes: {details['attributes']}, Sample: {details['sample_data']}")

    # Generate and print the XSD template
    xsd_template = generate_xsd_template(xml_structure)
    print("\nGenerated XSD Template:\n")
    print(xsd_template)

    # Optionally, write the XSD to a file
    with open("generated_schema.xsd", "w") as xsd_file:
        xsd_file.write(xsd_template)
        print("\nXSD template written to 'generated_schema.xsd'")

