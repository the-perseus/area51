function deleteNote(noteId) { //take the note id
  fetch("/delete-note", { //from delete-note function in views
    method: "POST", // send POST Req to db to remove the note
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/"; //refresh window
  });
}
