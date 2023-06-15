import importlib
import inspect
import re
import copy
from typing import Any, TypeVar
import dataclasses

from .models.vmdr import host_list_vm_detection_output

_D = TypeVar("_D")
_re_classname = re.compile(r"(qualyspy[\w._]*)")
_re_sa_class = re.compile(r"sqlalchemy.orm")


def _get_cls_inst_from_annot(mapped_cls: str) -> Any:
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


def _to_orm_object(
    obj: dict[str, Any],
    out_cls: type[_D],
) -> _D:
    obj_copy = copy.deepcopy(obj)
    annots = inspect.get_annotations(out_cls)
    for k, v in obj_copy.items():
        if isinstance(v, dict):
            mapped_cls = str(annots[k])
            child_cls = _get_cls_inst_from_annot(mapped_cls)
            if child_cls is None:
                continue
            obj_copy[k] = _to_orm_object(v, child_cls)
        elif isinstance(v, list) and len(v) > 0:
            mapped_cls = str(annots[k])
            child_cls = _get_cls_inst_from_annot(mapped_cls)
            if child_cls is None:
                continue
            if isinstance(v[0], dict):
                v = [_to_orm_object(item, child_cls) for item in v]
            else:
                child_annots = inspect.get_annotations(child_cls)
                param = next(iter(child_annots))
                v = [child_cls(**{param: item}) for item in v]
            obj_copy[k] = v

    return out_cls(**obj_copy)


def to_orm_object(
    obj: dict[str, Any],
    out_cls: type[_D],
) -> _D:
    obj_dict = dataclasses.asdict(obj)  # type: ignore
    return _to_orm_object(obj_dict, out_cls)


def from_orm_object(obj: Any) -> Any:
    processed_classes: set[Any] = set()

    def get_attributes(obj: Any) -> dict[str, Any]:
        result: dict[str, Any] = {}
        keys = obj.__mapper__.attrs.keys()
        nonlocal processed_classes
        for key in keys:
            value = getattr(obj, key)
            if type(value) in processed_classes:
                continue
            else:
                processed_classes.add(type(obj))

            if callable(value):
                continue
            if isinstance(value, (str, int, float, bool, type(None))):
                result[key] = value
            elif isinstance(value, list):
                result[key] = [_from_orm_object(v) for v in value]
            else:
                result[key] = _from_orm_object(value)
        return result

    def _from_orm_object(
        obj: Any,
    ) -> Any:
        if isinstance(obj, list):
            return [_from_orm_object(item) for item in obj]
        elif not hasattr(obj, "__dict__"):
            return obj
        return get_attributes(obj)

    output_class = getattr(host_list_vm_detection_output, obj.__class__.__name__)
    return output_class(**_from_orm_object(obj))
