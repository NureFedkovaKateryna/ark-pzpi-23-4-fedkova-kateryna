def save_with_organisation(request, data, model):
    user = request.user
    organisation_id = user.organisation_id
    data['organisation_id'] = organisation_id
    obj = model(**data)
    obj.save()
    return obj
