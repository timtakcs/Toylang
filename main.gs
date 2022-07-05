FUNC bubblesort(array, length) {
    FOR (i = 0; i < length; i++) {
        FOR (j = 0; j < length - i - 1; j++) { 
            IF array[j] > array[j + 1] {
                temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            };
        };
    };

    RETURN array;
};

testarr = [3, 12, 0, 1, 7, 6];
testarr = bubblesort(testarr, 6);