import language as lang

while True:
    text = input(">>> ")

    # text = """
    #         var1 = 6 * (3 - 1);
    #         var2 = 4 / 2 + 6;

    #         IF var1 > var2 {
    #             var2 = "Im greater";
    #         }
    #         ELIF var1 == var2 {
    #             var1 = "were the same";
    #             var2 = "were the same";
    #         }
    #         ELSE {
    #             var1 = "im greater";
    #         }
    #         """

    # text = """
    #         var1 = 1;

    #         FOR (i = 0; i < 10; i++) {
    #             var1 = var1 + i;
    #         }
    # """

    # text = """
    #         var1 = 1;
    #         var2 = 6;

    #         WHILE var1 < var2 {
    #             var1 = var1 + 1;
    #         }
    # """
    # text = """
    #         var1 = 1;
    #         var1++;
    # """

    text = """
            FUNC add (num1, num2) {
                num3 = num1 + num2;
            }
    """
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
