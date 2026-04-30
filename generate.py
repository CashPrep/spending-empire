import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def load_template(name):
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def generate_state_page(row, base_tpl, state_tpl):
    state_name = row["name"]
    slug = row["slug"]
    rent = int(row["avg_rent"])
    food = int(row["avg_food"])
    social = int(row["avg_social"])
    transport = int(row["avg_transport"])
    total = rent + food + social + transport

    low_range = int(total * 0.8)
    high_range = int(total * 1.2)

    page_title = f"College Student Budget in {state_name} | spending.college"
    meta_description = f"See a realistic monthly college student budget for {state_name}, including housing, food, going out, and transportation, plus tools to plan job hours."

    content = state_tpl
    content = content.replace("{STATE_NAME}", state_name)
    content = content.replace("{AVG_RENT}", str(rent))
    content = content.replace("{AVG_FOOD}", str(food))
    content = content.replace("{AVG_SOCIAL}", str(social))
    content = content.replace("{AVG_TRANSPORT}", str(transport))
    content = content.replace("{TOTAL_MONTHLY}", str(total))
    content = content.replace("{LOW_RANGE}", str(low_range))
    content = content.replace("{HIGH_RANGE}", str(high_range))

    full_html = base_tpl.replace("{page_title}", page_title)\
                        .replace("{meta_description}", meta_description)\
                        .replace("{content}", content)

    out_dir = os.path.join(OUTPUT_DIR, "states")
    ensure_dir(out_dir)
    filename = f"{slug}-college-student-budget.html"
    out_path = os.path.join(out_dir, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    return f"states/{filename}"

def main():
    base_tpl = load_template("base.html")
    state_tpl = load_template("state.html")

    ensure_dir(OUTPUT_DIR)

    generated_paths = []

    csv_path = os.path.join(BASE_DIR, "locations.csv")
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_type = row["type"].strip().lower()
            if row_type == "state":
                rel_path = generate_state_page(row, base_tpl, state_tpl)
                generated_paths.append(rel_path)

    links_html = "<h1>Generated pages</h1><ul>"
    for p in generated_paths:
        links_html += f'<li><a href="{p}">{p}</a></li>'
    links_html += "</ul>"

    index_html = base_tpl.replace("{page_title}", "Spending College – Local Generator")\
                         .replace("{meta_description}", "Local content generator index for spending.college.")\
                         .replace("{content}", links_html)

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Generated pages:")
    for p in generated_paths:
        print(" -", p)
    print("Done. Open output/index.html in a browser, or run a local server to preview.")

if __name__ == "__main__":
    main()
