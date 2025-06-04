from lxml import etree
from datetime import datetime


def process_document_lxml(input_file: str, output_file: str):
    """Process the pain.001.001.03 XML file according to specifications."""
    ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03'}
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
    tree = etree.parse(input_file, parser)
    root = tree.getroot()

    for cd_elem in root.xpath('.//ns:SvcLvl/ns:Cd', namespaces=ns):
        if cd_elem.text == 'NORM':
            cd_elem.text = 'SEPA'

    for pmt_tp_inf in root.xpath('.//ns:PmtTpInf', namespaces=ns):
        parent = pmt_tp_inf.getparent()
        idx = parent.index(pmt_tp_inf)
        new_elem = etree.Element("{urn:iso:std:iso:20022:tech:xsd:pain.001.001.03}ReqdExctnDt")
        new_elem.text = datetime.today().strftime('%Y-%m-%d')
        parent.insert(idx + 1, new_elem)

    for tag in ['StrtNm', 'PstCd', 'TwnNm']:
        for elem in root.xpath(f'.//ns:{tag}', namespaces=ns):
            parent = elem.getparent()
            parent.remove(elem)

    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    print(f"{output_file} saved")


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: python main.py input.xml output.xml')
    else:
        process_document_lxml(sys.argv[1], sys.argv[2])
