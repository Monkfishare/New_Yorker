import re
import os

insert_lines_template = """
            date_match = re.search(r'/(\d{4}_\d{2}_\d{2})\.(jpg|gif)', self.cover_url)
            if date_match:
                raw_date = date_match.group(1)
                edition_date = raw_date.replace("_", "-")
                self.log('Edition date:', edition_date)
                self.timefmt = ' [' + edition_date + ']'
            """

replace_patterns = [
    (r'/w_\d{3}', r'/w_960'),
    (r'"w_\d{3}"', r'"w_960"'),
]

def process_date(issue_date, content):
    if issue_date:
        replace_patterns_extended = [
            (r'MagazineSection__cover', r'MagazineCover__cover'),
            (r'https://www\.newyorker\.com/magazine', rf'https://www.newyorker.com/magazine/{issue_date}'),
            (r'https://www\.newyorker\.com/archive', rf'https://www.newyorker.com/magazine/{issue_date}')
        ]
        replace_patterns_extended.extend(replace_patterns)

        modified_content = content

        for pattern, replacement in replace_patterns_extended:
            modified_content = re.sub(pattern, replacement, modified_content)

        separator = '\u2550' * 20
        print(separator + f"  👇RECIPE for issue date {issue_date}👇  " + separator)
        print(modified_content)
        print(separator + f"  👆RECIPE for issue date {issue_date}👆  " + separator)

        # Write modified content back to file
        with open(file_path, 'w') as file:
            file.write(modified_content)
        print(separator + "  👏SUCCESS👏  " + separator)
    else:
        print(separator + "  ⚠ERRORS⚠  " + separator)
        print("Error: Issue date not provided.")
        print(separator + "  ⚠ERRORS⚠  " + separator)

def remove_date_from_issue_dates(date):
    with open("issue_dates.txt", "r") as file:
        lines = file.readlines()
    with open("issue_dates.txt", "w") as file:
        for line in lines:
            if line.strip() != date:
                file.write(line)

file_path = "new_yorker.recipe"

with open("issue_dates.txt", 'r') as dates_file:
    issue_date = dates_file.readline().strip()  # Read one line from the file

if issue_date:  # Check if the issue date is not empty
    with open(file_path, 'r') as file:
        content = file.read()

    # Pattern for self.cover_url = cover_img.get('src')
    objective_line_pattern = re.compile(r'self\.cover_url = cover_img\.get\(\'src\'\)\s*')
    match = objective_line_pattern.search(content)

    if match:
        insert_position = match.end()
        insert_lines = insert_lines_template.replace('\n', '\n    ')  # Indent insert_lines
        modified_content = content[:insert_position].rstrip() + insert_lines + content[insert_position:]

        process_date(issue_date, modified_content)
else:
    print("Skipping empty issue date.")