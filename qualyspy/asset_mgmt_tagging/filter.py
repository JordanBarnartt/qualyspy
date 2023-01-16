import collections

Filter = collections.namedtuple("Filter", ["field", "operator", "value"])


def make_filter(field: str, operator: str, value: str) -> Filter:
    """Generate a filter indicating the field to be searched on, the operator to use, and the value
    to search against.

    Args:
        field:
            The name of the field for which the filter should apply.

            For Tags, the searchable fields are: "id", "name", "parent", "ruleType", "provider",
            "color".

            For Assets, the searchable fields are: One of "id", "name", "created", "updated",
            "type", "tagName", "tagId".
        operator:
            The operator applied to the filter.  One of "equals", "not equals", "greater", "lesser",
            "in", "contains".
        value:
            The value for the field to be compared to.
    """

    return Filter(field, operator.upper(), value)
