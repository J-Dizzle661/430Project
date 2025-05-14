# Language Documentation: pOOP Improved Syntax

## 1. Why this language, and why this language design?
We chose to create pOOP Improved Syntax because we were familiar with JavaScript as a target language and wanted to explore how object-oriented programming languages work under the hood. Java, while popular and widely taught, can be verbose and lacks some of the flexibility found in JavaScript. Our compiler aims to:
- Make a Java-like language more readable and concise.
- Add features to Java that are easier to implement or more powerful in JavaScript (e.g., more flexible inheritance, dynamic features).
- Help us learn about language design, parsing, type checking, and code generation by building a language from scratch.

We intentionally designed the language to be class-based and object-oriented, with a syntax similar to Java but compiling to JavaScript. This allows us to leverage JavaScript's prototype-based inheritance while providing a more familiar, structured syntax for users.

## 2. Code snippets in your language highlighting features and limitations, with short explanations

### Example: Class Definition and Inheritance
```poop
class Animal {
    init() { }
    method speak() Void { println("PC Noises"); }
    }
class Cat extends Animal {
    init() { super(); }
    method speak() Void { println("Meow"); }
    }
class Dog extends Animal {
    init() { super(); }
    method speak() Void { println("Bark"); }
    }
}
```
*Explanation:* This shows how to define classes, constructors , and methods. `Cat` inherits from `Animal` and overrides the `speak` method.

### Example: Variable Declaration and Assignment
```poop
Animal cat;
cat = new Cat();
```
*Explanation:* Variables are declared with their type, and objects are instantiated with `new`.

### Example: Method Calls and Polymorphism
```poop
cat = new Cat();
c.speak(); // prints "Meow"

```
*Explanation:* Method calls use dot notation. The correct method is called based on the object's runtime type (polymorphism).

### Limitation Example: No Comments
```poop
// This is not allowed in pOOP
/* Nor is this */
```
*Explanation:* The language does not support comments or advanced type features beyond basic class-based types.

## 3. Knowing what you know now, what would you do differently?
Our biggest challenges while working on this project was the parser. This was due to 2 reasons:
- We were lacking knoweledge on the return types of our AST and we spent most of development time trying to figure this out.
- By the time we started coding the parser, we were still unaware of the full scope of our project. As a result, many tokens were missing from the lexer and tests constantly failed until we made sure to cover all scenarios. 
I would argue that what we needed to do differently was spend more time undertanding the low-level code and truly understand the goal of our compiler before we started to write the parser.

## 4. How do I compile your compiler?
- Make sure you have the latests version of python downloaded onto you computer: 
https://www.python.org/downloads/
- Once that is done, and since python is an interpreted language, compiling never occurs
- If you are using vs code, I also recommend downlaoding the python and python debugger extensions. 

## 5. How do I run your compiler?
- First, make sure that in the terminal you have used cd (change directory) to change the directory folder to COMP430 Project
- Edit the input code to you liking
- Then run the following command:
```poop
python Main.py
```
- Afterward run this in node.js:
```poop
JS_Code.js
```

## 6. Formal syntax definition
Concrete Syntax:
```
var is a variable
classname is the name of a class
methodname is the name of a method
str is a string
i is an integer

type ::= `Int` | `Boolean` | `Void` | Built-in types
         classname class type; includes Object and String

comma_exp ::= [exp (`,` exp)*]

primary_exp ::=
  var | str | i | Variables, strings, and integers are     
                  expressions
  `(` exp `)` | Parenthesized expressions
  `this` | Refers to my instance
  `true` | `false` | Booleans
  `println` `(` exp `)` | Prints something to the terminal
  `new` classname `(` comma_exp `)` Creates a new object

call_exp ::= primary_exp (`.` methodname `(` comma_exp `)`)*

mult_exp ::= call_exp ((`*` | `/`) call_exp)*

add_exp ::= mult_exp ((`+` | `-`) mult_exp)*

exp ::= add_exp

vardec ::= type var

stmt ::= exp `;` | Expression statements
         vardec `;` | Variable declaration
         var `=` exp `;` | Assignment
         `while` `(` exp `)` stmt | while loops
         `break` `;` | break
         `return` [exp] `;` | return, possibly void
         if with optional else
         `if` `(` exp `)` stmt [`else` stmt] | 
         `{` stmt* `}` Block

comma_vardec ::= [vardec (`,` vardec)*]

methoddef ::= `method` methodname `(` comma_vardec `)` type
              `{` stmt* `}`

constructor ::= `init` `(` comma_vardec `)` `{`
                [`super` `(` comma_exp `)` `;` ]
                stmt*
                `}`
classdef ::= `class` classname [`extends` classname] `{`
             (vardec `;`)*
             constructor
             methoddef*
             `}`

program ::= classdef* stmt+  stmt+ is the entry point
```