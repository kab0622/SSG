def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            title = markdown.lstrip("#").lstrip(" ")
            return title
        continue
    raise Exception("No title in markdown")