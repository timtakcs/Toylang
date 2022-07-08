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
};

testarr = [3, 12, 0, 1, 7, 6];
bubblesort(testarr, 6);

FUNC part(array, low, high) {
    pivot = array[high];
    i = low - 1;

    FOR (j = low; j <= high; j++) {
        IF array[j] < pivot {
            i++;
            temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        };
    };
    temp = array[i + 1];
    array[i + 1] = array[high];
    array[high] = temp;
    RETURN i + 1;
};

FUNC quicksort(array, low, high) {
    IF low > high {
        index = part(array, low, high);
        quicksort(array, low, index - 1);
        quicksort(array, index + 1, high);
    };
};

newtestarr = [6, 71, 8, 9, 1, 13];
quicksort(newtestarr, 0, 6);

