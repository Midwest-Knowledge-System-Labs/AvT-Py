import json

def write_file(path: str, content: str) -> None:
    with open(path, 'w+') as f:
        f.write(content.strip())

if __name__ == "__main__":
    output_lines = ["#ifndef AVESTERRA_TAXONOMY_H", "#define AVESTERRA_TAXONOMY_H"]
    with open("taxonomy.json", "r") as f:
        taxonomy = json.loads(f.read())

    for taxon in taxonomy.keys():

        # Enum gen
        output_lines.append("\ntypedef enum {")
        for key, value in taxonomy[taxon].items():
            output_lines.append(f"  {taxon.upper()}_{key},")
        output_lines.append(f"}} Ax{taxon};")
        output_lines.append(f"\ntypedef Ax{taxon} Av{taxon};\n")

        # Enum# to char* code
        output_lines.append(f"\nstatic const char *{taxon.upper()}_STR[] = {{")
        for key, value in taxonomy[taxon].items():
            output_lines.append(f'  "{key}",')
        output_lines.append(f"}};")

    output_lines.append("#endif")

    write_file("taxonomy.h", "\n".join(output_lines))