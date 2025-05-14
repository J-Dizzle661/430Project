class Animal {
    constructor() {

    }
    speak() {
        console.log("PC Noises");
    }
}

class Cat extends Animal {
    constructor() {
        super();
    }
    speak() {
        console.log("Meow");
    }
}

class Dog extends Animal {
    constructor() {
        super();
    }
    speak() {
        console.log("Bark");
    }
}

let cat;
let dog;
cat = new Cat();
dog = new Dog();
cat.speak();
dog.speak();
i = 0;
if (i < 1) {
    i = 5;
}
else {
    console.log("Failure");
}
while (i > 0) {
    i = i - 1;
    }
console.log(i);
