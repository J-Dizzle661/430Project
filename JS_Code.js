class Animal {
    constructor() {

    }
    speak() {
        console.log(0);
    }
}

class Cat extends Animal {
    constructor() {
        super();
    }
    speak() {
        console.log(1);
    }
}

class Dog extends Animal {
    constructor() {
        super();
    }
    speak() {
        console.log(2);
    }
}

let cat;
let dog;
cat = new Cat();
dog = new Dog();
cat.speak();
dog.speak();
