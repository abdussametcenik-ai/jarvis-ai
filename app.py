from flask import Flask, request, jsonify
from brain import think
import os


app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS</title>

<style>
body{
    margin:0;
    background:#000;
    font-family: Arial, sans-serif;
    color:white;
}

#container{
    max-width:720px;
    height:100vh;
    margin:auto;
    display:flex;
    flex-direction:column;
}

header{
    text-align:center;
    padding:18px;
    background:#000;
    font-weight:900;
    letter-spacing:4px;
    color:#ff7a00;
    font-size:20px;
    border-bottom:1px solid #222;
}

#chat{
    flex:1;
    overflow-y:auto;
    padding:20px;
}

.msg{
    max-width:80%;
    padding:16px 20px;
    margin:12px 0;
    border-radius:18px;
    font-weight:600;
    font-size:17px;
    animation:fade 0.25s ease-in;
}

.user{
    background:#ff7a00;
    color:white;
    margin-left:auto;
    border-bottom-right-radius:6px;
}

.bot{
    background:#ff7a00;
    color:white;
    margin-right:auto;
    border-bottom-left-radius:6px;
    opacity:0.9;
}

footer{
    display:flex;
    gap:10px;
    padding:14px;
    background:#000;
    border-top:1px solid #222;
}

input{
    flex:1;
    padding:18px;
    background:#000;
    color:white;
    border:1px solid #ff7a00;
    border-radius:16px;
    outline:none;
    font-size:17px;
    font-weight:600;
}

input::placeholder{
    color:#aaa;
}

button{
    padding:18px 24px;
    background:#ff7a00;
    border:none;
    border-radius:16px;
    font-weight:900;
    font-size:18px;
    color:black;
}

@keyframes fade{
    from{opacity:0; transform:translateY(8px)}
    to{opacity:1; transform:translateY(0)}
}
</style>
</head>

<body>
<div id="container">

<header>J A R V I S</header>

<div id="chat"></div>

<footer>
    <input id="text" placeholder="Bir şey yaz Hacım..." />
    <button onclick="send()">➤</button>
</footer>

</div>

<script>
const input = document.getElementById("text");
const chat = document.getElementById("chat");

input.addEventListener("keydown", function(e){
    if(e.key === "Enter"){
        e.preventDefault();
        send();
    }
});

function send(){
    let text = input.value.trim();
    if(!text) return;

    chat.innerHTML += `<div class="msg user">${text}</div>`;
    chat.scrollTop = chat.scrollHeight;

    fetch("/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:text})
    })
    .then(r => r.json())
    .then(d => {
        chat.innerHTML += `<div class="msg bot">${d.reply}</div>`;
        chat.scrollTop = chat.scrollHeight;
    });

    input.value = "";
}
</script>

</body>
</html>
"""

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"]
    reply = think(msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 3000))
    )
