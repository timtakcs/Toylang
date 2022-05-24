import language as lang

while True:
    text = input(">>> ")

    # text = """
    #         var1 = 5 * (3 - 1);
    #         var2 = 4 / 2 + 6;

    #         IF var1 > var2 {
    #             var1 = "Im greater";
    #         };
    #         ELIF var1 == var2 {
    #             var1 = "were the same";
    #             var2 = "were the same";
    #         };
    #         ELSE {
    #             var2 = "im greater";
    #         };
    #         """

    # text = """
    #         var1 = 1;

    #         FOR (i = 0; i < 10; i++) {
    #             var1 = var1 + i;
    #         };
    # """

    # text = """
    #         var1 = 1;
    #         var2 = 6;

    #         WHILE var1 < var2 {
    #             var1 = var1 + 1;
    #         };
    # """
    # text = """
    #         var1 = 1;
    #         var1++;
    # """

    text = """
            FUNC add (num1, num2) {
                FOR (i = 0; i < num2; i++) {
                    num1 = num1 + i;
                };
            };

            add(1, 10);
    """
   
    result, error = lang.run(text)

    if error:
        print(error.asString())
    else:
        print(result)
