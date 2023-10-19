"""Utility functions for qualyspy.  Primarily for internal use."""


import importlib
import inspect
import re
import copy
from typing import Any, TypeVar
import dataclasses

_D = TypeVar("_D")
_RE_QUALYSPY_CLASSNAME = re.compile(r"(qualyspy[\w._]*)")
_RE_SA_CLASSNAME = re.compile(r"sqlalchemy.orm")


def _get_cls_inst_from_annot(mapped_cls: str) -> Any:
    """Get an instance of a class from a string annotation.

    Args:
        mapped_cls (str): The string annotation of the class.

    Returns:
        Any: An instance of the class.

    Raises:
        ValueError: If the annotation is not a Mapped class.
    """
    m = _RE_QUALYSPY_CLASSNAME.search(mapped_cls)
    if m is not None:
        child_cls_strs = m.group(1).split(".")
        child_cls_package = ".".join(child_cls_strs[:-1])
        mod = importlib.import_module(child_cls_package)
        child_cls = getattr(mod, child_cls_strs[-1])
        return child_cls
    else:
        if _RE_SA_CLASSNAME.search(mapped_cls):
            return None
        else:
            raise ValueError("Annotation is not a Mapped class.")


def to_orm_object(
    obj: Any,
    out_cls: type[_D],
) -> _D:
    """Convert a dataclass instance of a Qualys object to an ORM object.

    Args:
        obj (dict[str, Any]): The dataclass instance of a Qualys object.
        out_cls (type[_D]): The ORM class to convert to.

    Returns:
        _D: The ORM object.
    """

    def _to_orm_object(
        obj: dict[str, Any],
        out_cls: type[_D],
    ) -> _D:
        """Helper function for to_orm_object.  Recursively converts a dataclass instance of a Qualys
        object to an ORM object.  This separate function allows obj to be converted from a
        dataclass to a dict before the recursive calls."""
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

    try:  # Type is Pydantic dataclass
        obj_dict = dataclasses.asdict(obj)
    except TypeError:  # Type is Pydantic model
        obj_dict = obj.dict()
    return _to_orm_object(obj_dict, out_cls)


def from_orm_object(obj: Any, output_class: Any) -> Any:
    """Convert an ORM object to a dataclass instance of a Qualys object.

    Args:
        obj (Any): The ORM object.

    Returns:
        Any: The dataclass instance of a Qualys object.
    """

    # Since the ORM objects relationships are bidirectional, we need to keep track of which
    # classes we've already processed to avoid infinite recursion.
    processed_classes: set[Any] = set()

    builtin_types = (str, int, float, bool, type(None))

    def get_attributes(obj: Any) -> dict[str, Any]:
        """Get the attributes of an ORM object.

        Args:
            obj (Any): The ORM object.

        Returns:
            dict[str, Any]: The attributes of the ORM object.
        """
        nonlocal processed_classes
        processed_classes.add(type(obj))

        result: dict[str, Any] = {}
        keys = obj.__mapper__.attrs.keys()  # List of attributes of the ORM object
        for key in keys:
            value = getattr(obj, key)

            # Check for bultin types first so they don't get added to processed_classes
            if isinstance(value, builtin_types):
                result[key] = value
                continue

            # Skip classes we've already processed so we don't go back up the hierarchy
            if type(value) in processed_classes:
                continue
            else:
                processed_classes.add(type(value))

            if callable(value):  # Skip methods
                continue
            elif isinstance(value, list):
                result[key] = [_from_orm_object(v) for v in value]
            else:
                result[key] = _from_orm_object(value)
        return result

    def _from_orm_object(
        obj: Any,
    ) -> Any:
        """Helper function for from_orm_object.  Recursively converts an ORM object to a dataclass
        instance of a Qualys object.
        """
        if isinstance(obj, list):
            return [_from_orm_object(item) for item in obj]
        elif not hasattr(obj, "__dict__"):
            return obj
        return get_attributes(obj)

    return output_class(**_from_orm_object(obj))


def snake_to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    # capitalize the first component and join the rest
    return components[0] + "".join(x.title() for x in components[1:])


def clean_dict(d: dict[str, Any]) -> dict[str, str]:
    """Remove None values from a dictionary and convert values to strings.

    Args:
        d (dict[str, Any]): The dictionary to clean.

    Returns:
        dict[str, str]: The cleaned dictionary.
    """

    def _clean_dict(v: Any) -> str:
        # if l is a list, return a comma-separated string of the list items
        if isinstance(v, list):
            return ",".join([str(item) for item in v])
        elif isinstance(v, bool):
            return "1" if v else "0"
        else:
            return str(v)

    return {k: _clean_dict(v) for k, v in d.items() if v is not None}
