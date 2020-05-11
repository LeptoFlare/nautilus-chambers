"""Contains mutation resolvers."""
from ariadne import MutationType
from nautilus import utils
from nautilus.validators import validate_profileinput

mutation_type = MutationType()


@mutation_type.field("createProfile")
def resolve_create_profile(*_, discord, profile):
    """mutation createProfile"""
    utils.logger.debug(f"createProfile | discord={discord}")
    if not (error := utils.errors.check_for([utils.errors.exists], discord)):
        payload = validate_profileinput(profile)
        if payload['status'] is True:
            payload['status'], payload['profile'] = utils.dbh.insert_profile(discord, profile)
        return payload
    else:
        return {"status": False, "error": error}


@mutation_type.field("updateProfile")
def resolve_update_profile(*_, discord, profile):
    """mutation updateProfile"""
    utils.logger.debug(f"updateProfile | discord={discord}")
    if not (error := utils.errors.check_for([utils.errors.missing], discord)):
        payload = validate_profileinput(profile)
        if payload['status'] is True:
            payload['status'], payload['profile'] = utils.dbh.update_profile(discord, profile)
        return payload
    else:
        return {"status": False, "error": error}


@mutation_type.field("deleteProfile")
def resolve_delete_profile(*_, discord):
    """mutation deleteProfile"""
    utils.logger.debug(f"deleteProfile | discord={discord}")
    payload = {}

    if not (error := utils.errors.check_for([utils.errors.missing], discord)):
        payload['status'] = utils.dbh.delete_profile(discord)
    else:
        payload['status'], payload['error'] = False, error
    return payload
