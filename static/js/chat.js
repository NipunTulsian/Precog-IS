document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('chat-button').style.display = 'block';
    document.getElementById('chat-container').style.display = 'none';
});

// function toggleChat() {
//     const chatButton = document.getElementById('chat-button');
//     const chatContainer = document.getElementById('chat-container');
//     const isChatVisible = chatContainer.style.display === 'flex';

//     chatButton.style.display = isChatVisible ? 'block' : 'none';
//     chatContainer.style.display = isChatVisible ? 'none' : 'flex';
// }

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const userText = userInput.value.trim();
    if (userText) {
        addMessage('user', userText);
        userInput.value = '';
        fetch('/chatbot', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: userText })
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = data.message;
            simulateTyping(botMessage, 70);
           
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', "Sorry, I'm having trouble responding. Please try again later.");
        });
    }
}

function addMessage(sender, text,istyping = false, containsLink = true) {
    const messagesContainer = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + sender + '-message';
    const sanitizedText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">this link</a>');


    messageElement.innerHTML = sanitizedText;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addMessage(sender, text, isTyping = false, containsLink = true) {
    const messagesContainer = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + sender + '-message';

    if (containsLink) {
        const urlRegex = /(https?:\/\/[^\s]+)/g; // Regular expression to match URLs
        const replacedText = text.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');
        messageElement.innerHTML = replacedText;
    } else {
        messageElement.textContent = text;
    }

    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function inputKeyUp(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function simulateTyping(message, typingSpeed) {
    let i = 0;
    let isTypingDone = false;
    const messagesContainer = document.getElementById('messages');
    const typingElement = document.createElement('div');
    typingElement.className = 'message bot-message typing-indicator';
    messagesContainer.appendChild(typingElement);

    function typeChar() {
        if (i < message.length) {
            typingElement.textContent += message.charAt(i);
            i+=1;
            if (i < message.length) {
                setTimeout(typeChar, typingSpeed);
            } else {
                isTypingDone = true; 
                typingElement.classList.remove('typing-indicator');
                typingElement.textContent = message;
            }
        }
    }
    
    typeChar(); 
}
//////////////////////////////////////////////////////////////// List Document ////////////////////////////////////////////////////////////////

function listDocuments() {
    fetch('/list-documents')
    .then(response => response.json())
    .then(documents => {
        console.log(documents); // For debugging
        documents.forEach(doc => {
            addMessage('bot', `Document ID: ${doc.id}, Title: ${doc.title}, Content: ${doc.content.substring(0, 100)}...`);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('bot', "Error listing documents.");
    });
}

//////////////////////////////////////////////////////////////// Upload Document ////////////////////////////////////////////////////////////////
function deleteDocument(documentId,documentTitle) {
    if (!confirm("Are you sure you want to delete this document?")) {
        return;
    }

    // Make the fetch call to the Flask backend to delete the document
    fetch(`/delete-document/${documentId}/${encodeURIComponent(documentTitle)}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Process the response from the server
        alert('Document deleted successfully.',data); // Display a message to the user (optional
        // Remove the document from the list or refresh the page
        window.location.reload(); // Simplest approach is to reload the page
    })
    .catch(error => {
        console.error('Error deleting document:', error);
        // Display error message or handle accordingly
    });
}
// Handles when files are dropped onto the drop area
function dropHandler(event) {
    event.stopPropagation();
    event.preventDefault();
    const files = event.dataTransfer.files;
    document.getElementById('file-input').files = files;
    fileSelectedHandler();
}

// Handles when files are dragged over the drop area
function dragOverHandler(event) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy'; // Visual feedback to indicate a copy action
}

// This function will be triggered when files are selected or dropped
function fileSelectedHandler() {
    const uploadButton = document.getElementById('upload-files-btn');
    const files = document.getElementById('file-input').files;
    if (files.length > 0) {
        uploadButton.disabled = false;  // Enable the upload button
    } else {
        uploadButton.disabled = true;   // Disable the upload button if no files are selected
    }
}

/////////////////////////////////////////////// Multiple File Upload ///////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const fileDropArea = document.getElementById('file-drop-area');
    const uploadButton = document.getElementById('upload-btn');
    const fileListContainer = document.getElementById('file-list');
    let selectedFiles = [];

    const updateFileDisplay = () => {
        fileListContainer.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const listItem = document.createElement('div');
            listItem.textContent = file.name;
            fileListContainer.appendChild(listItem);
        });
        uploadButton.disabled = selectedFiles.length === 0;
    };

    fileDropArea.addEventListener('click', function () {
        fileInput.click();
    });

    fileDropArea.addEventListener('dragover', function (event) {
        event.stopPropagation();
        event.preventDefault();
        event.dataTransfer.dropEffect = 'copy';
    });

    fileDropArea.addEventListener('drop', function (event) {
        event.stopPropagation();
        event.preventDefault();
        selectedFiles = Array.from(event.dataTransfer.files); // Update selectedFiles with dropped files
        updateFileDisplay();

	//fileInput.files = event.dataTransfer.files;
        //showFiles(fileInput.files);
    });

    fileInput.addEventListener('change', function () {
        //showFiles(fileInput.files);
	selectedFiles = Array.from(fileInput.files); // Update selectedFiles with selected files
        updateFileDisplay();
    });

    function showFiles(files) {
        fileListContainer.innerHTML = '';
        for (const file of files) {
            const listItem = document.createElement('div');
            listItem.textContent = file.name;
            fileListContainer.appendChild(listItem);
        }
        uploadButton.disabled = files.length === 0;
    }

    window.uploadFiles = function () {
        console.log("file Input:",fileInput);
	console.log("Selected Files:",selectedFiles);
	const formData = new FormData();
	selectedFiles.forEach(file => {
          formData.append('files[]', file);
        });
	console.log("Form Data:",formData);
        //for (const file of fileInput.files) {
          //  formData.append('files[]', file);
        //}

        fetch('/upload-multiple-documents', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
            if (data.errors) {
                console.log(data.errors);
		let errorMessage = 'An error occurred while uploading files:\n';
                data.errors.forEach(error => {
                    errorMessage += `${error.filename}: ${error.error}\n`;
                });
                alert(errorMessage);
                //window.location.reload();
            }
            //   alert(data.message);
              fileListContainer.innerHTML = '';
              uploadButton.disabled = true;
              fileInput.value = '';
	      selectedFiles = [];
	      updateFileDisplay();
              window.location.reload();
          }).catch(error => {
              console.error('Error:', error);
              alert('An error occurred while uploading files.');
              //window.location.reload();
          });
     //    window.location.reload();
    };
});

//////////////////////////////////////////////////////////////// Download Document ////////////////////////////////////////////////////////////////
function downloadDocument(filename) {
    alert('Downloading ' + filename);
    window.location.href = `/download-document/${filename}`;
}

////////////////////////////////////////////////////////////////////// Expand Chat ////////////////////////////////////////////////////////////////

function expandChat() {
    const chatButton = document.getElementById('chat-button');
    const chatContainer = document.getElementById('chat-container');
    const expandIcon = document.getElementById('expand-chat');
    const isChatExpanded = chatContainer.classList.contains('expanded');

    // Toggle expanded class
    if (isChatExpanded) {
        chatContainer.classList.remove('expanded');
        expandIcon.style.display = 'block';
    } else {
        chatContainer.classList.add('expanded');
        expandIcon.style.display = 'none';
    }
    // Blur background when chat is expanded
    document.body.classList.toggle('blurred', !isChatExpanded);
}

function toggleChat() {
    const chatButton = document.getElementById('chat-button');
    const chatContainer = document.getElementById('chat-container');
    // const chatOverlay = document.getElementById('chat-overlay');
    const isChatVisible = chatContainer.style.display === 'flex';

    chatButton.style.display = isChatVisible ? 'block' : 'none';
    chatContainer.style.display = isChatVisible ? 'none' : 'flex';
    // chatOverlay.style.display = isChatVisible ? 'none' : 'block'; // Toggle overlay visibility

    if (isChatVisible && chatContainer.classList.contains('expanded')) {
        toggleExpandChat();
    }
}

function toggleExpandChat() {
    const chatContainer = document.getElementById('chat-container');
    const expandIcon = document.getElementById('expand-icon');
    const compressIcon = document.getElementById('compress-icon');
    const chatOverlay = document.getElementById('chat-overlay');
    const isChatExpanded = chatContainer.classList.toggle('expanded');

    expandIcon.style.display = isChatExpanded ? 'none' : 'block';
    compressIcon.style.display = isChatExpanded ? 'block' : 'none';
    chatOverlay.style.display = isChatExpanded ? 'block' : 'none';

    // No need to modify the overlay here since it's already displayed
}


// function toggleChat() {
//     const chatButton = document.getElementById('chat-button');
//     const chatContainer = document.getElementById('chat-container');
//     const isChatVisible = chatContainer.style.display === 'flex';

//     chatButton.style.display = isChatVisible ? 'block' : 'none';
//     chatContainer.style.display = isChatVisible ? 'none' : 'flex';
// }
