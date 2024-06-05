// Parent constructor function
function Animal(name) {
    this.name = name;
}

// Method shared by all instances of Animal
Animal.prototype.speak = function() {
    console.log(this.name + ' makes a noise.');
};

// Child constructor function
function Dog(name) {
    Animal.call(this, name); // Call the parent constructor
}

// Create prototype chain between Dog and Animal
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

// Method specific to Dog
Dog.prototype.bark = function() {
    console.log(this.name + ' barks.');
};

let dog = new Dog('Buddy');
dog.speak(); // Output: Buddy makes a noise.
dog.bark();  // Output: Buddy barks.
