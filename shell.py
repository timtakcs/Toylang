import language as lang

while True:
    text = input(": ")

    text = """var1 = 2 * (3 - 1)
              var2 = 2 * (4 - 1)
              var3 = var1 + var2"""
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
