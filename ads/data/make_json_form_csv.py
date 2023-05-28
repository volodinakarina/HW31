import csv
import datetime
import json


def create_json(csv_path, json_path, model):
    with open(csv_path) as file:
        dict_ = csv.DictReader(file)
        result = []
        for object_ in dict_:
            object_dict = {
                'model': model,
                'pk': object_['id'],
                'fields': object_
            }
            del object_dict['fields']['id']

            if 'is_published' in object_dict['fields']:
                if object_dict['fields']['is_published'] == 'TRUE':
                    object_dict['fields']['is_published'] = True
                else:
                    object_dict['fields']['is_published'] = False

            if 'location_id' in object_dict['fields']:
                object_dict['fields']['locations'] = list()
                object_dict['fields']['locations'].append(int(object_dict['fields']['location_id']))
                del object_dict['fields']['location_id']

            if model == 'ads.category':
                object_dict['fields']['slug'] = f'slug_{object_dict["pk"]}'

            if model == 'authentication.user':
                object_dict['fields']['birth_date'] = datetime.date(2000, 1, 1).strftime('%Y-%m-%d')
                object_dict['fields']['email'] = f"{object_dict['fields']['username']}@mail.ru"

            result.append(object_dict)

    with open(f'../fixtures/{json_path}', 'w') as file:
        json.dump(result, file, ensure_ascii=False)


create_json('ad.csv', 'ad.json', 'ads.ad')
create_json('category.csv', 'category.json', 'ads.category')
create_json('location.csv', 'location.json', 'authentication.location')
create_json('user.csv', 'user.json', 'authentication.user')
