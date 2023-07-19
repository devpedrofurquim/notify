function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = '/';
    })
}

function editNote(noteId) {
    let noteText = document.getElementById('edit_note').value;
    let payload = {
        noteId: noteId,
        edit_note: noteText
    };
  
    fetch('/edit-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    }).then((_res) => {
        window.location.href = '/';
    });
}


window.onload = function() {
    function sendTimeToServer() {
        let time = new Date();
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/getTime?time=" + time, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                document.getElementById("time").innerHTML = xhr.responseText;
                if (time.getHours() >= 6 && time.getHours() < 12) {
                    document.getElementById("greet").innerHTML = '☕ Good Morning';
                } else if (time.getHours() >= 12 && time.getHours() < 18) {
                    document.getElementById("greet").innerHTML = '🌅 Good Afternoon';
                } else {
                    document.getElementById("greet").innerHTML = '🌃 Good Night';
                }

            }
        };
        xhr.send();
    }
    sendTimeToServer();
};

// Profile Page Dynamic Form

updateForm = document.getElementById("update-form")
updateUsername = document.getElementById("update-username")
updateEmail = document.getElementById("update-email")

console.log(updateUsername)
console.log(updateEmail)

//Submit Profile Picture

const input = document.getElementById("picture");
const preview = document.getElementById("preview");

input.addEventListener("change", updateImageDisplay);

function updateImageDisplay() {
    while (preview.firstChild) {
      preview.removeChild(preview.firstChild);
    }
  
    const curFiles = input.files;
    if (curFiles.length === 0) {
      const para = document.createElement("p");
      para.textContent = "No files currently selected for upload";
      preview.appendChild(para);
    } else {
      const list = document.createElement("ol");
      preview.appendChild(list);
  
      for (const file of curFiles) {
        const listItem = document.createElement("li");
        const para = document.createElement("p");
        if (validFileType(file)) {
          para.textContent = `File name ${file.name}, file size ${returnFileSize(
            file.size,
          )}.`;
          const image = document.createElement("img");
          image.src = URL.createObjectURL(file);

          image.style.maxWidth="100px"
          image.style.padding="10px"

  
          listItem.appendChild(image);
          listItem.appendChild(para);
        } else {
          para.textContent = `File name ${file.name}: Not a valid file type. Update your selection.`;
          listItem.appendChild(para);
        }
  
        list.appendChild(listItem);
      }
    }
  }
  
  const fileTypes = [
    "image/jpeg",
    "image/png",
    "image/jpg",
  ];
  
  function validFileType(file) {
    return fileTypes.includes(file.type);
  }
  
  function returnFileSize(number) {
    if (number < 1024) {
      return `${number} bytes`;
    } else if (number >= 1024 && number < 1048576) {
      return `${(number / 1024).toFixed(1)} KB`;
    } else if (number >= 1048576) {
      return `${(number / 1048576).toFixed(1)} MB`;
    }
  }