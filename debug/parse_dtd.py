import re
import string
from collections import OrderedDict

ELEMENT_RE = re.compile("<!ELEMENT (?P<name>.+) \\((?P<attributes>[\\s\\S]+?)\\)>")

with open("debug/dtd.txt", "r") as f:
    text = f.read()
    matches = ELEMENT_RE.findall(text)

classes = OrderedDict()

for (name, attributes) in matches:
    parsed = attributes.replace("\n", "").replace(" ", "").lower()
    parsed = parsed.split(",")
    classes[name.lower()] = parsed

with open("debug/output.txt", "w") as f:
    for c in reversed(classes):
        if classes[c][0] != "#pcdata":
            f.write("\n@dataclasses.dataclass\n")
            cl = string.capwords(c, sep="_")
            f.write(f"class {cl}:\n")
            for a in classes[c]:
                if a == "is_default?":
                    pass
                if a.strip("*?+") in classes and classes[a.strip("*?+")][0] == "#pcdata":
                    if a.endswith("*"):
                        x = a.strip("*")
                        f.write(f"    {x}: Optional[MutableSequence[str]] = None\n")
                    elif a.endswith("?"):
                        x = a.strip("?")
                        f.write(f"    {x}: Optional[str] = None\n")
                    elif a.endswith("+"):
                        x = a.strip("+")
                        f.write(f"    {x}: MutableSequence[str]\n")
                    else:
                        f.write(f"    {a}: str\n")
                elif a.endswith("*"):
                    x = a.strip("*")
                    cl = string.capwords(x, sep="_")
                    f.write(f"    {x}: Optional[MutableSequence[{cl}]] = None\n")
                elif a.endswith("?"):
                    x = a.strip("?")
                    cl = string.capwords(x, sep="_")
                    f.write(f"    {x}: Optional[{cl}] = None\n")
                elif a.endswith("+"):
                    x = a.strip("+")
                    cl = string.capwords(x, sep="_")
                    f.write(f"    {x}: MutableSequence[{cl}]\n")
                else:
                    cl = string.capwords(a, sep="_")
                    f.write(f"    {a}: {cl}\n")
