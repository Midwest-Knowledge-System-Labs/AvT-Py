import json
import re
from typing import Dict, List

def generate_py_taxonomy(path: str, taxonomy: Dict[str, List[str]]):
    content = ""
    header = '''"""
Copyright (c) [Midwest Knowledge System Labs & Plex - Alexander Larkin] [2025-2026]
Copyright (c) [LEDR Technologies Inc.] [2024-2025]
This file is part of the Orchestra library, which helps developer use our Orchestra technology which is based on AvesTerra, owned and developed by Georgetown University, under license agreement with LEDR Technologies Inc.
The Orchestra library is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
The Orchestra library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along with the Orchestra library. If not, see <https://www.gnu.org/licenses/>.
If you have any questions, feedback or issues about the Orchestra library, you can contact us at support@midwksl.net.
"""

import sys
from enum import IntEnum, auto


'''

    content += header
    taxons = []
    for key in taxonomy.keys():
        content += f"class Ax{key}(IntEnum):\n"
        for value in taxonomy[key]:
            if value == "NULL":
                content += f"   {value} = 0\n"
            else:
                content += f"   {value} = auto()\n"
        content += f"\nAv{key} = Ax{key}\n\n\n"

        taxons.append(f"Av{key}")

    content += f"AvTaxon = {' | '.join(taxons)}"

    content += """

def taxon(taxon_name, code):
    current_module = sys.modules[__name__]
    try:
        enum_class = getattr(current_module, taxon_name)
        if issubclass(enum_class, IntEnum):
            return list(enum_class)[code]
        else:
            raise TypeError(f"{taxon_name} is not an Enum class.")
    except AttributeError as e:
        raise ValueError(f"Enum class or member not found: {e}")"""

    with open(path, "w") as f:
        f.write(content)


def load_taxonomy_ads(path: str) -> Dict[str, List[str]]:
    output = {}
    with open(path, "r") as f:
        content = f.read()
        new = re.sub(r"\s*--.*", "", content)
        new = re.sub(",\s+", ",", new, flags=re.MULTILINE)
        new = re.sub("is\n\s+", "is ", new)
        new = re.sub("^\n$", "", new, flags=re.MULTILINE)
        new = re.sub("^\s+", "", new, flags=re.MULTILINE)
        new = re.sub("^(?!type).*", "", new, flags=re.MULTILINE)
        new = re.sub("\n\s+", "\n", new)
        new = re.sub("[ ][ ]+", " ", new)
        new = re.sub("\(.+\)", lambda match: match.group(0).upper(), new)
        new = re.sub("type( .)", lambda match: match.group(0)[:-1] + match.group(0)[-1].upper(), new)
        new = new.replace("type ", "")
    for line in new.split("\n"):
        if line:
            m = re.match(r"(.+_Taxonomy) is (\(.+\))", line)
            if m is not None:
                name = m.group(1).replace("_Taxonomy", "")
                upper_name = name.upper()
                output[name] = json.loads(m.group(2).replace(f"_{upper_name}", "").replace("(", '["').replace(")", '"]').replace(",", '","'))
    return output



if __name__ == '__main__':
    taxonomy = load_taxonomy_ads("avionomy.ads")

    with open("taxonomy.json", "w") as f:
        json.dump(taxonomy, f, indent=2)

    generate_py_taxonomy("src/avesterra/taxonomy.py", taxonomy)
