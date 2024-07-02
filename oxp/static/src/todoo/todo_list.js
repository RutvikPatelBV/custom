/** @odoo-module **/
import { Component, useState , useRef , onMounted} from "@odoo/owl";
import { Todoitem } from "@oxp/todoo/todo_item";
import {useAutofocus} from "../utils"
export class Todolist extends Component {
  static template = "oxp.TodoList";
  static components = { Todoitem };
  static props={name: String}
  setup() {
    this.nextId = 4;
    this.todos = useState([]);
    useAutofocus("for_focus")
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
        this.todos.push({
          id: this.nextId++,
          description: ev.target.value,
          isCompleted: false,
        });
        ev.target.value = "";
    }
  }

  toggleTodo(id){
    const todo=this.todos.find((todo)=>todo.id===id)
    if(todo){
        todo.isCompleted=!todo.isCompleted;
    }
  }
  removeTodo(id){
    const todoIndex=this.todos.findIndex((todo)=>todo.id===id)
    if (todoIndex >= 0) {
//      this.todos.splice(todoIndex, 1);
      this.todos.pop(todoIndex);
    }
  }
}
