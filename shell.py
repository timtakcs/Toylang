import language as lang

while True:
    text = input(": ")
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
