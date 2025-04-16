import { useState } from "react";

function CreateForm({ addTodo }) {
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    if (content.trim()==="") {
      setError("Enter something before click the button");
        return;
    }
    addTodo(content);
    setContent("");
    setError("");
  };

  return (
    <form className="create-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="enter your list here"
        value={content}
        onChange={(e) => {
          setContent(e.target.value);
          if (error) setError(""); 
        }}
      />
      {! error && <button type="submit">add</button>}
      {error && <p className="error-message"> {error}</p>}
    </form>
  );
}

export default CreateForm;
