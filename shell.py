import language as lang

while True:
    text = input(">>> ")

    text = """IF var1 == 2 + 3"""
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
