import json

FILE_PATH = "mr_custom_fields.json"


def get_mr_custom_fields(mr_iid):
    with open(FILE_PATH, "r") as f:
        return json.load(f).get(str(mr_iid), {})


def update_mr_custom_fields(mr_iid, custom_fields):
    with open(FILE_PATH, "r") as f:
        data = json.load(f)

    data[str(mr_iid)] = custom_fields

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)
