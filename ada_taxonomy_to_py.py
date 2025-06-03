import json
import os.path
import re
import subprocess
from typing import Dict

import click

def read_file(path: str) -> str:
    # Execute a command
    process = subprocess.Popen(['sh', '-c', f"cat {path}| grep -v 'package' | grep -vE '^-' | grep -vE 'version\\s*:\\s*' | grep -v 'end Avionomy' | sed -E 's/\\s*--(\\s*.*)$//g' | perl -0777 -pe 's/is\\s*\\(/\\n      /g' | sed 's/type/enum/g' | sed -E 's/^\\s+$//g' | sed -E 's/)*;|,/\\n/g' | sed -E 's/^[ ]+//g' | sed 's/^[ \\n]$//g' | awk 'NF'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error
    stdout, stderr = process.communicate()

    return stdout.decode("utf-8")

def write_file(path: str, content: str) -> None:
    with open(path, 'w') as f:
        f.write(content)

@click.command()
@click.option("--in_dir", help="The directory path of Ada taxonomy file to convert", required=True)
@click.option("--out_dir", help="The directory where the output taxonomy.py file will be placed", required=True)
def command(in_dir, out_dir):

    taxonomy: Dict[str, Dict[str, int]] = {}

    ada_taxonomy_path = os.path.join(in_dir, "avionomy.ads")
    py_taxonomy_path = os.path.join(out_dir, "taxonomy.py")

    ada_taxonomy_content = read_file(ada_taxonomy_path)

    for line in ada_taxonomy_content.split("\n"):
        clean_line = line.strip()
        if clean_line:
            taxon_match = re.match(r"enum\s.+_Taxonomy", clean_line)
            if taxon_match:
                taxon = taxon_match.string.replace("enum", "").replace("Taxonomy", "").replace("_", "").strip()
                taxon_split = list(taxon.lower())
                taxon_split[0] = (taxon_split[0]).upper()
                taxon = "".join(taxon_split)
                taxonomy[taxon] = {}
            else:
                split_line = clean_line.split("_")
                value = "_".join(split_line[:-1]).upper()
                taxon_split = list(split_line[-1].lower())
                taxon_split[0] = (taxon_split[0]).upper()
                taxon = "".join(taxon_split)
                if taxon in taxonomy:
                    taxonomy[taxon][value] = len(list(taxonomy[taxon].keys()))

    with open("taxonomy.json", "w+") as f:
        f.write(json.dumps(taxonomy))

    output_py_lines = ["from enum import IntEnum, auto"]
    for taxon in taxonomy.keys():
        output_py_lines.append(f"\nclass Ax{taxon}(IntEnum):")
        for key, value in taxonomy[taxon].items():
            output_py_lines.append(f"   {key} = auto()")
        output_py_lines.append(f"\nAv{taxon} = Ax{taxon}\n")

    write_file(py_taxonomy_path, "\n".join(output_py_lines))


if __name__ == "__main__":
    command()