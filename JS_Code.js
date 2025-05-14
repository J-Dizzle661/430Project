class Animal {
    age;
    weight;
    constructor(age, weight) {
        this.age = age;
        this.weight = weight;

    }
    speak() {
        console.log("PC Noises");
    }
    getAge() {
        return this.age;
    }
    getWeight() {
        return this.weight;
    }
}

class Cat extends Animal {
    constructor(age, weight) {
        super(age, weight);
    }
    speak() {
        console.log("Meow");
    }
}

class Dog extends Animal {
    constructor(age, weight) {
        super(age, weight);
    }
    speak() {
        console.log("Bark");
    }
}

let cat;
let dog;
cat = new Cat(5, 30);
dog = new Dog(6, 60);
cat.speak();
dog.speak();
i = 0;
if (i < 1) {
    i = 5;
}
else {
    console.log("Failure");
}
{
    j = 10;
    bool = false;
    otherBool = true;
}
while (i > 0) {
    i = i - 1;
    }
console.log(i);
console.log(cat.getAge());
console.log(dog.getAge());
console.log(cat.getWeight());
console.log(dog.getWeight());
