FUNC factorial(n) {
    IF n == 1 {
        RETURN n;
    };
    ELSE {
        RETURN n * factorial(n - 1);
    };
};

num = factorial(4);
