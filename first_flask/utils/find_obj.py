def find_obj_by_id(obj_list, id):
    return next((obj for obj in obj_list if obj['id'] == id), None)
