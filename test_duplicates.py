import os
import ezdxf
from collections import defaultdict

def find_duplicates_and_incorrect_geometry(file_path):
    duplicates = defaultdict(int)
    incorrect_geometry = []

    try:
        doc = ezdxf.readfile(file_path)
        modelspace = doc.modelspace()

        for entity in modelspace:
            # Count duplicates
            duplicates[str(entity)] += 1

            # Check for incorrect geometry, add your specific checks here
            if entity.dxftype() == 'CIRCLE' and entity.dxf.radius <= 0:
                incorrect_geometry.append(str(entity))
            
            # Add other geometry checks here

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

    # Filter out non-duplicates
    duplicates = {k: v for k, v in duplicates.items() if v > 1}
    return duplicates, incorrect_geometry

def generate_html_dashboard(output_path, results):
    with open(output_path, 'w') as html_file:
        html_file.write("<h1>Files with Issues</h1>")
        for file_path, (duplicates, incorrect_geometry) in results.items():
            html_file.write(f"<h2>{file_path}</h2>")
            html_file.write("<h3>Duplicates</h3>")
            html_file.write("<ul>")
            for item, count in duplicates.items():
                html_file.write(f"<li>{item}: {count} duplicates</li>")
            html_file.write("</ul>")

            html_file.write("<h3>Incorrect Geometry</h3>")
            html_file.write("<ul>")
            for item in incorrect_geometry:
                html_file.write(f"<li>{item}</li>")
            html_file.write("</ul>")

def main():
    directory = "./dwg_files"  # Set the directory where DWG files are located
    results = {}

    for file_name in os.listdir(directory):
        if file_name.endswith(".dwg"):
            file_path = os.path.join(directory, file_name)
            duplicates, incorrect_geometry = find_duplicates_and_incorrect_geometry(file_path)
            if duplicates or incorrect_geometry:
                results[file_path] = (duplicates, incorrect_geometry)

    generate_html_dashboard('dashboard.html', results)
    print("Dashboard generated: dashboard.html")

if __name__ == "__main__":
    main()
