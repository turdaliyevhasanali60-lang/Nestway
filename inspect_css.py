import re

with open('static/css/output.css', 'r') as f:
    css = f.read()

# Let's search for anything related to header
for match in re.finditer(r'(?:^|\})([^\}]*?header[^\}]*?)\{([^\}]+)\}', css):
    print(f"Rule: {match.group(1).strip()} {{ {match.group(2).strip()} }}")

print("\n--- Searching for .h-20 ---")
for match in re.finditer(r'(?:^|\})([^\}]*?\.h-20[^\}]*?)\{([^\}]+)\}', css):
    print(f"Rule: {match.group(1).strip()} {{ {match.group(2).strip()} }}")

