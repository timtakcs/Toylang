
<h2>Toylang</h2>
Toylang is an imperative toy language written in Python. This project was used as a learning experience for interpreters and compilers so that I could understand how they work and build more sophisticated projects in the future.

This is the first version of the language and includes some basic features, however, it is still a work in progress. 

<h3>Syntax for v1.0</h3>
```
factor: PLUS factor
      | MINUS factor
      | INT
      | LPAR expression RPAR
      | VAR

term: factor ((PLUS|MINUS) factor)*

expression: term ((MULT|DIV) term)*

logic-expression: expression LOGIC expression

increment-expression: factor (INC|DEC|INCBY|DECBY)

arr-expression: [expression (, expression)*?]

arr-index: arr[expression]

assignment: var ASSGN expression
          | var INC
          | var INCBY factor

if: if logic-expression { body } (elif logic-expression { body })*? (else { body })?

for: FOR (assignment, logic-expression, increment-expression) { loop body }

while: while condition { loop body }

func: func var ((expression, )*?) { func body }

func-call: var((expression, )*?)

statement: compound_statement
         | increment-expression
         | assignment
         | if
         | while
         | for
         | func
         | func-call

        
compound_statement: statement; (statement;)*?
```
<h3>Features</h3>

- This language is weakly typed as it takes advantage of Python's single type. In the future I plan to make it strongly typed to perform semantic analysis and various optimizations.

- It has garbage collection for local function variables.

- It has built in functions: print(), len(), and append()

- It supports recursion and catches stack overflows

<h3>Examples</h3>
**Hello World**

```
print("Hello World");
```
**If statements**
```

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

```
**Loops**
```

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

print(num1);
print(num2);
```

**Functions and Recursion**

```
func factorial(n) {
    if n == 1 {
        return n;
    }
    else {
        return n * factorial(n - 1);
    }
}
```

<h4>Algorithms</h4>

**Quicksort**
```
func part(array, low, high) {
    pivot = array[high];
    i = low - 1;

    for (j = low; j < high; j++) {
        if array[j] <= pivot {
            i++;
            temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }

    temp = array[i + 1];
    array[i + 1] = array[high];
    array[high] = temp;

    return i + 1;
}

func quicksort(array, low, high, part) {
    if low < high {
        index = part(array, low, high);
        quicksort(array, low, index - 1);
        quicksort(array, index + 1, high);
    }
}

somearray = [6, 71, 8, 61, 3, 9, 13];
quicksort(somearray, 0, len(somearray) - 1, part);
```

**Binary Search**
```
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
```

<h3>Future Development</h3>

- [ ] Type checking and semantic analysis

- [ ] Rewrite in a compiled language

<h3>Notes</h3>

This language is not bug free nor is it fast. It includes a few optimizations which also act as error handling. Again, it was made for a learning experience and to build a mental framework for future projects.
