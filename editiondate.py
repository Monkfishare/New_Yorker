import re

issue_date = "2024/01/01"  # For past edition, for example, issue_date = "2024/01/29" [format:yyyy/mm/dd (Monday)]

insert_lines = """
                date_match = re.search(r'/(\d{4}_\d{2}_\d{2})\.jpg', self.cover_url)            
                if date_match:
                    raw_date = date_match.group(1)
                    edition_date = raw_date.replace("_", "-")
                    self.log('Edition date:', edition_date)
                    self.timefmt = ' [' + edition_date + ']'
                """

file_path = "new_yorker.recipe"
with open(file_path, 'r') as file:
    content = file.read()

# Pattern for self.cover_url = cover_img.get('src')
objective_line_pattern = re.compile(r'self\.cover_url = cover_img\.get\(\'src\'\)\s*')

replace_patterns = [
    (r'/w_\d{3}', r'/w_960'),
    (r'"w_\d{3}"', r'"w_960"'),
]

if issue_date:
    replace_patterns.extend([
        (r'MagazineSection__cover', r'MagazineCover__cover'),
        (r'https://www\.newyorker\.com/magazine', rf'https://www.newyorker.com/magazine/{issue_date}'),
        (r'https://www\.newyorker\.com/archive', rf'https://www.newyorker.com/magazine/{issue_date}')
    ])

match = objective_line_pattern.search(content)

if match:
    insert_position = match.end()
    modified_content = content[:insert_position].rstrip() + insert_lines + content[insert_position:]

    for pattern, replacement in replace_patterns:
        modified_content = re.sub(pattern, replacement, modified_content)

    separator = '\u2550' * 20
    print(separator + "  👇RECIPE👇  " + separator)
    print(modified_content)
    print(separator + "  👆RECIPE👆  " + separator)

    with open(file_path, 'w') as file:
        file.write(modified_content)
    print(separator + "  👏SUCESS👏  " + separator)
else:
    print(separator + "  ⚠ERRORS⚠  " + separator)
    print("Error: Pattern not found in the new_yorker.recipe. Check the latest recipe structure or update the regular expression.")
    print("self.cover_url = cover_img.get('src')")
    print("https://raw.githubusercontent.com/kovidgoyal/calibre/master/recipes/new_yorker.recipe")
    print(separator + "  ⚠ERRORS⚠  " + separator)
