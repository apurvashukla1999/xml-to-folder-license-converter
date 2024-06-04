import os
import shutil
import xml.etree.ElementTree as ET


def process_xml(file_path):
    # parse XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    for dependencies in root:
        for dependency in dependencies:
            process_dependency(dependency)


def process_dependency(dependency):
    # Constructing dependency name using group_id and artifact_id
    group_id_element = dependency.find('groupId')
    group_id = group_id_element.text if group_id_element is not None else ''

    artifact_id_elem = dependency.find('artifactId')
    artifact_id = artifact_id_elem.text if artifact_id_elem is not None else ''

    package = f'{group_id}.{artifact_id}'

    # Create package directory regardless of whether a license file exists
    package_dir_path = f'packages/{package}'
    os.makedirs(package_dir_path, exist_ok=True)

    for licenses in dependency:
        for license in licenses:
            license_file_elem = license.find('file')

            # Skip to next iteration if license_file_elem is None
            if license_file_elem is None:
                continue

            license_file = license_file_elem.text
            license_path = f'licenses/{license_file}'

            if os.path.exists(license_path):
                destination_path = f'{package_dir_path}/{license_file}'
                shutil.copy(license_path, destination_path)  # This line copies the file


# Call the function
process_xml('licenses.xml')
