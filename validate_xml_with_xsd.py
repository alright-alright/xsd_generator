from lxml import etree
import sys

def validate_xml_with_xsd(xml_file, xsd_file):
    """Validates an XML file against an XSD schema."""
    try:
        # Parse the XSD schema
        with open(xsd_file, 'r') as f:
            xsd_root = etree.XML(f.read())
        schema = etree.XMLSchema(xsd_root)

        # Parse the XML file
        xml_doc = etree.parse(xml_file)

        # Validate the XML against the XSD
        if schema.validate(xml_doc):
            print("XML file is valid according to the XSD.")
        else:
            print("XML file is invalid. Errors:")
            for error in schema.error_log:
                print(error)

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
    except etree.DocumentInvalid as e:
        print(f"Document Invalid: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_xml_with_xsd.py path/to/your/xml_file.xml path/to/your/xsd_file.xsd")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    xsd_file_path = sys.argv[2]
    validate_xml_with_xsd(xml_file_path, xsd_file_path)

