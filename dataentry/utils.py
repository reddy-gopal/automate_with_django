from django.core.management.base import BaseCommand, CommandError

import csv
from django.apps import apps
from django.db import DataError

def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission']
    custom_models = []
    for model in apps.get_models():
        if model.__name__ in default_models:
            continue
        custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path , model_name):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label , model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f"There is no model with name {model_name} in any app")

    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    print(model_fields)
    try:
        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            if csv_header !=  model_fields:
                raise DataError(f"CSV file does not match with {model_name} fields..")
    except Exception as e:
        raise Exception(f"Import data failed: {e}") from e

    return model

import datetime
from awd_main import settings
import os
def exported_file(model_name):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    exported_dir = 'exported_data'
    file_path = os.path.join(settings.MEDIA_ROOT ,exported_dir ,  file_name)
    return file_path
