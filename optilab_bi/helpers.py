import collections
from datetime import datetime
from flask_restless.helpers import to_dict as flask_to_dict, is_like_list
from sqlalchemy.orm import Query


def input_audit_data_on_insert(mapper, connection, target):
    """Atualiza a data de criação (create_at) na inclusão da entidade."""

    if hasattr(target, 'created_at'):
        target.created_at = datetime.utcnow()


def input_audit_data_on_update(mapper, connection, target):
    """Atualiza a data de atualização (create_at) na alteração da entidade."""

    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.utcnow()

def to_dict(instance, deep=None, exclude=None, global_exclude=None):
    if not instance:
        return [] if type(instance) == list else None

    exclude = exclude or {}
    global_exclude = global_exclude or []
    deep = deep or {}

    model = type(instance)

    real_exclude = global_exclude
    real_exclude.extend(exclude.get(model, []))

    if isinstance(instance, collections.Iterable):
        result = [to_dict(_inst, deep, exclude=exclude, global_exclude=global_exclude) for _inst in instance]
        return result

    result = flask_to_dict(instance, exclude=real_exclude)

    for relation, rdeep in deep.items():
        related_inst = getattr(instance, relation)
        if related_inst is None:
            result[relation] = None
            continue

        if is_like_list(instance, relation):
            result[relation] = [to_dict(inst, rdeep, exclude=exclude, global_exclude=global_exclude) for inst in
                                related_inst]
            continue

        if isinstance(related_inst, Query):
            related_inst = related_inst.one()

        result[relation] = to_dict(related_inst, rdeep, exclude=exclude, global_exclude=global_exclude)

    return result
