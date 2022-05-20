import language as lang

while True:
    text = input(">>> ")

    # text = """
    #         var1 = 6 * (3 - 1);
    #         var2 = 4 / 2 + 6;

    #         IF var1 < var2 {
    #             var2 = "Im greater";
    #         }
    #         ELIF var1 == var2 {
    #             var1 = "were the same";
    #             var2 = "were the same";
    #         }
    #         ELSE {
    #             var1 = "im greater";
    #         }"""

    text = """
            var1 = 1;

            FOR (i = 1; i < 5; i = i + 1) {
                var1 = var1 * i;
            }
            """
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
