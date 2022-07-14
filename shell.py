import language as lang


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

    #Function calls and declaration

    # text = """
    #         FUNC fact(n) {
    #             num = 1;

    #             FOR (i = 1; i < n; i++){
    #                 num = num * i;
    #             };

    #             RETURN num;
    #         };

    #         result = fact(5);
    # """

    # text = """
    #     array = [1, 2, 3, 5, 0];
    #     num = array[3];
    #     array[2] = 10;
    # """

    #Bubblesort
    # text = """
    #     FUNC bubblesort(array, length) {
    #         FOR (i = 0; i < length; i++) {
    #             FOR (j = 0; j < length - i - 1; j++) { 
    #                 IF array[j] > array[j + 1] {
    #                     temp = array[j];
    #                     array[j] = array[j + 1];
    #                     array[j + 1] = temp;
    #                 };
    #             };
    #         };

    #         RETURN array;
    #     };

    #     testarr = [3, 12, 0, 1, 7, 6];
    #     testarr = bubblesort(testarr, 6);
    # """

with open('sorts.gs', 'r') as f:
    text = f.read()

result, error = lang.run(text)

if error:
    print(error.asString())
else:
    print(result)
