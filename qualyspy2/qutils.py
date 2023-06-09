import importlib
import inspect
import re
import copy
from typing import Any, TypeVar

import sqlalchemy.orm as orm

_D = TypeVar("_D")
_re_classname = re.compile(r"(qualyspy[\w._]*)")
_re_sa_class = re.compile(r"sqlalchemy.orm")


def get_cls_inst_from_annot(mapped_cls: str) -> Any:
    m = _re_classname.search(mapped_cls)
    if m is not None:
        child_cls_strs = m.group(1).split(".")
        child_cls_package = ".".join(child_cls_strs[:-1])
        mod = importlib.import_module(child_cls_package)
        child_cls = getattr(mod, child_cls_strs[-1])
        return child_cls
    else:
        if _re_sa_class.search(mapped_cls):
            return None
        else:
            raise ValueError("Annotation is not a Mapped class.")


def to_orm_object(
    obj: dict[str, Any],
    out_cls: type[_D],
) -> _D:
    obj_copy = copy.deepcopy(obj)
    annots = inspect.get_annotations(out_cls)
    for k, v in obj_copy.items():
        if isinstance(v, dict):
            mapped_cls = str(annots[k])
            child_cls = get_cls_inst_from_annot(mapped_cls)
            if child_cls is None:
                continue
            obj_copy[k] = to_orm_object(v, child_cls)
        elif isinstance(v, list) and len(v) > 0:
            if not all(isinstance(item, orm.DeclarativeBase) for item in v):
                mapped_cls = str(annots[k])
                child_cls = get_cls_inst_from_annot(mapped_cls)
                if child_cls is None:
                    continue
                if isinstance(v[0], dict):
                    v = [to_orm_object(item, child_cls) for item in v]
                else:
                    child_annots = inspect.get_annotations(child_cls)
                    param = next(iter(child_annots))
                    v = [child_cls(**{param: item}) for item in v]
            obj_copy[k] = v

    out_cls_mapper = orm.class_mapper(out_cls)
    mapped_dict = {
        k: v for k, v in obj_copy.items() if k in out_cls_mapper.attrs.keys()
    }
    ret = out_cls(**mapped_dict)
    return ret
