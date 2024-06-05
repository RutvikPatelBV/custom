// Parent class
class Animal2 {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        console.log(this.name + ' makes a noise.');
    }
}

// Child class inheriting from Animal
class Dog2 extends Animal2 {
    constructor(name) {
        super(name); // Call the parent constructor
    }
    
    bark() {
        console.log(this.name + ' barks.');
    }
}

let dog2 = new Dog2('Buddy');
dog2.speak(); // Output: Buddy makes a noise.
dog2.bark();  // Output: Buddy barks.
