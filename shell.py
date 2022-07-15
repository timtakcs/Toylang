import language as lang

with open('examples/new.gs', 'r') as f:
    text = f.read()

result, error = lang.run(text)

if error:
    print(error.asString())
else:
    print(result)
