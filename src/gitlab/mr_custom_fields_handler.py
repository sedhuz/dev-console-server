import json

FILE_PATH = "mr_custom_fields.json"


def get_mr_custom_fields(project_id, mr_iid):
    with open(FILE_PATH, "r") as f:
        return json.load(f).get(str(project_id) + "_" + str(mr_iid), {})


def update_mr_custom_fields(project_id, mr_iid, custom_fields):
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    key = f"{project_id}_{mr_iid}"

    if key not in data:
        data[key] = {}

    data[key].update(custom_fields)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
