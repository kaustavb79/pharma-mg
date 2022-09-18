from datetime import datetime
from django import template
from rest_framework.utils import json

register = template.Library()

@register.filter
def list_at_index(data, index):
    index = int(index) - 1
    return data[index]


# this template is use for getting the value in a dict by passing dict and key
@register.filter
def dict_at_key(dict_data, key):
    value = dict_data[key]
    return value

@register.simple_tag
def check_if_key_present(dict_data, key):
    if key in dict_data:
        return True
    else:
        False

@register.filter
def get_type(value):
    return str(type(value))

@register.filter
def get_object_length(value):
    return len(value)

@register.filter
def is_empty_strings(value):
    if value:
        if len(value) == 0:
            return False
        else:
            return True
    return False

@register.filter
def string_list_to_list_obj(string_list):
    list_obj = json.loads(string_list)
    return list_obj

@register.filter
def multiply(number, multiply_by, *args, **kwargs):
    # you would need to do any localization of the result here
    number = float(number)
    multiply_by = float(multiply_by)
    result = int(number * multiply_by)
    return result

@register.filter
def one_more(_1, _2):
    return _1, _2

@register.filter
def get_dict_value(input_key_company_id, input_dict):
    input_key, company_id = input_key_company_id
    input_dict = json.loads(input_dict)
    result = ''
    if company_id and input_key and input_dict:
        input_key = str(input_key)
        company_id = str(company_id)
        result = input_dict[company_id][input_key]
    return result


@register.filter
def is_past_due(given_date):
    current_time = datetime.now()
    return given_date < current_time


@register.filter
def get_filename(path):
    print("---path---",path)
    filename = ""
    if path:
        filename = path.split('/')[-1]
    print("---filename---", filename)

    return filename
