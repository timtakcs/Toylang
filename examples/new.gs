print("Hello World");

num1 = 10;
num2 = 6;

if num1 > num2 {
    print("num1 is greater");
}
elif num1 == num2 {
    print("num1 and num2 are the same");
}
else {
    print("num2 is greater");
}

array = [];

for (i = 0; i < 10; i++) {
    append(array, i);
}

num1 = 10;
num2 = 20;

while num2 > num1 {
    num1++;
    num2--;
}

func factorial(n) {
    if n == 1 {
        return n;
    }
    else {
        return n * factorial(n - 1);
    }
}

func binarysearch(array, n, low, high) {
    middle = (high - low) // 2;
    
    if array[middle] == n {
        return middle;
    }
    else {
        if array[middle] > n {
            return binarysearch(array, n, middle + 1, high);
        }
        else {
            return binarysearch(array, n, low, middle - 1);
        }
    }
}