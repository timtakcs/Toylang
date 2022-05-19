import language as lang

while True:
    text = input(">>> ")

    text = """
            var1 = 6 * (3 - 1);
            var2 = 4 / 2 + 6;

            IF var1 < var2 {
                var1 = 1;
            }
            ELIF var1 == var2 {
                var1 = 0;
                var2 = 0;
            }
            ELSE {
                var2 = 1;
            }"""
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
