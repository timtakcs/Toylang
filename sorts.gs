func bubblesort(array, lenght) {
    for (i = 0; i < length; i++) {
        for (j = 0; j < length - i - 1; j++) { 
            if array[j] > array[j + 1] {
                temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            };
        };
    };
};

testarr = [3, 12, 0, 1, 7, 6];
bubblesort(testarr, 6);

func part(array, low, high) {
    pivot = array[high];
    i = low - 1;

    for (j = low; j < high; j++) {
        if array[j] <= pivot {
            i++;
            temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        };
    };

    temp = array[i + 1];
    array[i + 1] = array[high];
    array[high] = temp;

    return i + 1;
};

func quicksort(array, low, high, part) {
    if low < high {
        index = part(array, low, high);
        quicksort(array, low, index - 1);
        quicksort(array, index + 1, high);
    };
};

newtestarr = [6, 71, 8, 61, 3, 9, 13];
quicksort(newtestarr, 0, 6, part);



