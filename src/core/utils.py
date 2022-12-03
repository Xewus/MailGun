import csv
import os

from validate_email import validate_email

from src.settings import (ALLOWED_EXTENSIONS, EMAIL_TEMPLATES_DIR,
                               UPLOAD_DIR)


def save_uploaded_file(file, user_id):
    """Check the file extension, rename it and save it.

    #### Args:
    - file (str): The path to file.
    - user_id (int): User`s Id to rename the file.
    """
    ext = None
    if '.' in file.filename:
        _, ext = file.filename.rsplit('.')
    if ext in ALLOWED_EXTENSIONS:
        file.filename = '%d.%s' % (user_id , ext)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(file_path)
        return file_path
    return
    

def get_contact_from_csv(file_name, user_id):
    """Cet unique emails and bound names from `.csv` file.

    #### Args:
    - filename (str): The path to file.csv with contacts.
    - user_id (int): The id of contact`s owner.

    #### Returns:
    - list[dict['email': str, 'name': str, 'user_id': user_id]]
    - None if file not found
    """
    try:
        with open(file_name) as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                if not validate_email(row[0], verify=False):
                    continue
                data.append(
                    {
                        'email': row[0],
                        'name': row[-1],
                        'user_id':user_id
                    }
                )
        return data
    except IOError:
        raise ValueError('File %s wasn`t opened' % file_name)


def get_list_email_templates(dir=EMAIL_TEMPLATES_DIR):
    """
    ### Args:
    - dir (str): The directory with templates.
    #### Returns
    - list: The list of email templates from directory.
    """
    return [
        t for t in os.listdir(dir) if os.path.isfile(os.path.join(dir, t))
    ]
