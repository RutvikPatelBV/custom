/** @odoo-module **/
import { Component,useState } from "@odoo/owl";
import { Todolist } from "./todo_list";
export class Todoo extends Component {
  static template = "oxp.Todoo";
  static components = { Todolist };
   setup() {
    this.id = 1;
    this.lists = useState([]);
  }
  addNewList(){
    const id = this.id++;
    this.lists.push({ id, name: `List ${id}` });
  }
}