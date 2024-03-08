import re

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

objective_line_pattern = re.compile(r'self\.cover_url = cover_img\.get\(\'src\'\)\s*')  # self.cover_url = cover_img.get('src')
match = objective_line_pattern.search(content)

if match:
    insert_position = match.end()
    modified_content = content[:insert_position].rstrip() + insert_lines + content[insert_position:]

    print("object_line_pattern found; added successfully!!")
    
    with open(file_path, 'w') as file:
        file.write(modified_content)
else:
    print("Error: Pattern not found in the new_yorker.recipe. Check the latest recipe structure or update the regular expression.")
    print("self.cover_url = cover_img.get('src')")
    print("https://raw.githubusercontent.com/kovidgoyal/calibre/master/recipes/new_yorker.recipe")
