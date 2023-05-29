import json

filename = input("Input a file path here:\n$ ")

f = open(filename, "r")
title, theme, content = None, None, ""
cs, done = False, False
for line in f:
    lineS = line.split(" ")
    if lineS[0] == "/TITLE":
        title = lineS[1]
    elif lineS[0] == "/THEME":
        theme = lineS[1]
    elif lineS[0] == "/START-CONTENT\n":
        cs = True
    elif lineS[0] == "/END-CONTENT\n":
        cs = False
        done = True
    else:
        if cs and not done:
            content += line
# remove newlines
title = title[:-1]
if theme.endswith("\n"):
    theme = theme[:-1]
f.close()

# make dict and convert
newJsonData = json.dumps({"TITLE": title, "THEME": theme, "CONTENT": content})
print(newJsonData)
# write new data in the form of a JSON
f = open(filename, "w")
f.write(newJsonData)
f.close()

print("DONE")
