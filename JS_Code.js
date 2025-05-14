class Animal {
    age;
    constructor(age) {
this.age = age
    }
    speak() {
        console.log("PC Noises");
    }
    getAge() {
        return this.age;
    }
}

class Cat extends Animal {
    constructor(age) {
        super(age);
    }
    speak() {
        console.log("Meow");
    }
}

class Dog extends Animal {
    constructor(age) {
        super(age);
    }
    speak() {
        console.log("Bark");
    }
}

let cat;
let dog;
cat = new Cat(5);
dog = new Dog(6);
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
console.log(cat.getAge());
console.log(dog.getAge());
