function table(name,price){
    this.name=name
    this.price=price
}

table.prototype.showPrice=function(){
    console.log(`price of ${this.name} is ${this.price}`)
}
const table1= new table('wood',2222)
table1.showPrice()





