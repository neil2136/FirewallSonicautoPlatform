import xml.etree.ElementTree as ET
from definition.settings import *


def get_cert_from_xml():
    tree = ET.parse('/tmp/SAML.xml')
    root = tree.getroot()
    signature = root.find('{http://www.w3.org/2000/09/xmldsig#}Signature')
    if signature is not None:
        print('found signature element')
        # find KeyInfo element
        namespaces = {
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        key_info = signature.find('{http://www.w3.org/2000/09/xmldsig#}KeyInfo')
        if key_info is not None:
            print('found the KeyInfo element')

            # find X509Data
            X509Data = key_info.find('{http://www.w3.org/2000/09/xmldsig#}X509Data')
            if X509Data is not None:
                print('found the X509data element')

                # X509Certificate
                X509Certificate = X509Data.find('{http://www.w3.org/2000/09/xmldsig#}X509Certificate')
                if X509Certificate is not None:
                    print('found the X509Certificate')
                    cert_base64 = X509Certificate.text
                    logger.info(f'cert_base64 from XML is: {cert_base64}')
                    return X509Certificate.text
                else:
                    print('not found the X509Certificate')
            else:
                print('not found the X509data element')

        else:
            print('not found the KeyInfo element')
    else:
        print('not found Signature element')


def get_server_id_from_xml():
    tree = ET.parse('/tmp/SAML.xml')
    root = tree.getroot()

    RoleDescriptor_list = root.findall('{urn:oasis:names:tc:SAML:2.0:metadata}RoleDescriptor')
    print(RoleDescriptor_list)
    if len(RoleDescriptor_list) == 2:
        print('found the Second RoleDescriptor element')
        TargetScopes = RoleDescriptor_list[1].find('{http://docs.oasis-open.org/wsfed/federation/200706}TargetScopes')
        if TargetScopes is not None:
            print('found TargetScopes element')
            EndpointReference = TargetScopes.find('{http://www.w3.org/2005/08/addressing}EndpointReference')
            if EndpointReference is not None:
                print('found EndpointReference element')
                Address = EndpointReference.find('{http://www.w3.org/2005/08/addressing}Address')
                if Address is not None:
                    print('found Address element')
                    server_id = Address.text
                    logger.info(f'server_id is: {server_id}')
                    return Address.text
                else:
                    print('not found Address element')
            else:
                print('not found EndpointReference element')
        else:
            print('not found TargetScopes element')


def get_url_from_xml():
    out = get_server_id_from_xml()
    m = re.search(r'\d.*\d', out)
    id = m.group() if m else ''
    url = f'https://login.microsoftonline.com/{id}/saml2'
    logger.info(url)
    return url


def generate_pem_cert(file_path='/tmp/certificate.pem'):
    cert_base64 = get_cert_from_xml()
    pem_certificate = f"-----BEGIN CERTIFICATE-----\n{cert_base64}\n-----END CERTIFICATE-----"
    with open(file_path, 'w') as pem_file:
        pem_file.write(pem_certificate)

    print('PEM 证书已保存为 certificate.pem')

    if 'certificate.pem' in pc1_login.send_command('ls -l /tmp/'):
        print('证书保存成功')
        return True
    print('证书保存失败')
    return False


def change_cert_content_to_invalid():
    cert_base64 = get_cert_from_xml()
    damaged_cert_base64 = cert_base64[:len(cert_base64) - 10]
    logger.info(f'damaged_cert_base64 is :\n{damaged_cert_base64}')
    return damaged_cert_base64


def generate_invalid_pem_cert(file_path):
    cert_base64 = change_cert_content_to_invalid()
    pem_certificate = f"-----BEGIN CERTIFICATE-----\n{cert_base64}\n-----END CERTIFICATE-----"
    with open(file_path, 'w') as pem_file:
        pem_file.write(pem_certificate)

    print(f'PEM 证书已保存为 {file_path}')

    if file_path in pc1_login.send_command('ls -l /tmp/'):
        print('证书保存成功')
        return True
    print('证书保存失败')
    return False
