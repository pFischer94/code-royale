from pathlib import Path
from sys import exception

project: str = "src"
paths: list[str] = [
    # PARAMS
    "params.py",
    
    # ENUMS
    "sites/Side.py",
    "sites/SiteType.py",
    "units/UnitType.py",
    "owner/Owner.py",
    
    # CLASSES
    "sites/Site.py",
    "sites/SitesAccessBuilder.py",
    "sites/SitesManager.py",
    "units/Unit.py",
    "units/UnitsAccessBuilder.py",
    "units/UnitsManager.py",
    "game/GameManager.py",
    
    # MAIN
    "main.py",
]

imports: list[str] = []
output_lines: list[str] = []
    
for path in paths:
    with open(Path(f"{project}/{path}"), "r") as file:
        output_lines.append(f"# {path}\n")
        input_lines = file.readlines()
        for line in input_lines:
            if line.startswith("import "):
                if not line in imports:
                    imports.append(line)
            elif not line.startswith("from"):
                output_lines.append(line)
        output_lines.append("\n\n\n")
            
with open(Path(f"output/{project}.py"), "w") as file:
    for line in imports:
        file.write(line)
    file.write("\n\n\n")
    for line in output_lines:
        file.write(line)
    
print("Files merged successfully!")