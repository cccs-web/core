"""
Go through the stored files and ensure that each one has a Document model (metadata object) supporting it.
Create or use categories matching the document folder.
This should never look at uploaded documents because they will already have metadata objects.
"""
import os
from storages.backends.s3boto import S3BotoStorage

import documents.models as dm


def upload_files(source_path, root_path='./'):
    """
    Copy files and folders in source path up to storage, preserving the folder structure
    :param source_path: path to search
    :param root_path: part of source_path that should be dropped from the name
    :return:
    """
    storage = S3BotoStorage()
    for dirpath, dirnames, filenames in os.walk(source_path):
        for filename in filenames:
            source_fpath = os.path.join(dirpath, filename)
            target_fpath = source_fpath.lstrip(root_path)
            if os.path.splitext(source_fpath)[1] != '.py':
                print("{0} -> {1}".format(source_fpath, target_fpath))
                with open(source_fpath, 'rb') as f:
                    storage.save(target_fpath, f)


def import_files():
    """
    Go through the stored files and ensure that each one has a Document model supporting it.
    Create or use categories matching the document folder structure unless the folder is numeric.
    :return:
    """
    storage = S3BotoStorage()
    for key in storage.bucket.list():
        if not dm.Document.objects.filter(source_file=key.name):  # No existing metadata object
            document = dm.Document(source_file=key.name,
                                   title=os.path.splitext(os.path.basename(key.name))[0])
            document.save()  # save here so m2m relations are possible

            filename, created = dm.FileName.objects.get_or_create(name=key.name)
            if created:
                filename.save()
            document.filenames.add(filename)

            category_names = os.path.split(key.name)[0].split(os.path.sep)
            if category_names:
                categories = dm.verify_categories(category_names, create_if_absent=True)
                document.categories.add(categories[-1])


def update_sha_values():
    """
    Go through all the documents and update their sha values
    :return: None
    """
    for document in dm.Document.objects.all():
        document.update_sha()
        document.save()