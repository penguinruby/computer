import { MdDeleteForever,MdEdit } from "react-icons/md";
import EditForm from "./EditForm";



function Todo ({todo, deleteTodo, toggleCompleted, toggleIsEditing, editTodo}) {
    return todo.isEditing ?( 
        <EditForm todo ={todo} editTodo={editTodo} />)
        :( <div className={'todo ${todo.isCompleted ? "completed" : ""}'}>
          <p onClick={()=>{toggleCompleted(todo.id)}}> {todo.content} </p>
          <div>
            <MdEdit onClick ={() =>{toggleIsEditing(todo.id)}}  style={{cursor: "pointer", marginRight: "7px" }} />
            <MdDeleteForever onClick ={() =>{deleteTodo(todo.id)}} 
            style={{cursor: "pointer"}} />
        </div>
      </div>
    );
}
export default Todo