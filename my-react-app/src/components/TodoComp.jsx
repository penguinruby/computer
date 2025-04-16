import { useState } from "react";
import CreateForm from "./CreateForm";
import Todo from "./Todo";

function TodoComp() {
    const [todos, setTodos ] = useState ([
        // {content: "Clean the room", id:Math.random(), 
        //     isCompleted: false,isEditing: false },
        // {content: "Work out", id:Math.random(), 
        //     isCompleted: false, isEditing: false},
    ]);
    
    const addTodo =(content) =>{
        setTodos([...todos, {content:content, id:Math.random(), 
            isCompleted: false, isEditing: false}])

    }

    const deleteTodo =(id) =>{
        setTodos(todos.filter((todo)=> {
            return todo.id !== id
        }))

    }

    const toggleIsEditing =(id)=>{
        setTodos(todos.map((todo) => {
            return todo.id == id
            ? {...todo, isEditing: !todo.isEditing}
            :todo
        }))
    }

    const toggleCompleted=(id) =>{
        setTodos(todos.map((todo)=> {
            return todo.id === id 
            ? {...todo, isCompleted: !todo.isCompleted}
            :todo
        }))

    }
    const editTodo =(id, newContent) => {
        setTodos(todos.map((todo) => {
            return todo.id === id
            ? {...todo, content: newContent, isEditing:false}
            : todo
        }))
    }



    return (
      <div className="wrapper">
        <h1>To Do List</h1>
        <CreateForm addTodo={addTodo} />
        {todos.map((todo) => {
          return <Todo toggleCompleted={toggleCompleted}
          toggleIsEditing={toggleIsEditing} editTodo={editTodo}
          todo ={todo} key={todo.id} deleteTodo = {deleteTodo}/>
        })}

    </div>
    );
}

export default TodoComp
