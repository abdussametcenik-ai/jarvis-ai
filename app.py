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

/* 🔥 IRON MAN BACKGROUND */
.ironman-bg {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 0;
    opacity: 0.15;
}

.ironman-bg svg {
    width: 320px;
    height: 320px;
}

.ironman-bg path {
    fill: none;
    stroke: orange;
    stroke-width: 3;
    filter: drop-shadow(0 0 10px orange);
}

/* CHAT ÜSTTE KALSIN */
#container{
    max-width:900px;
    height:100vh;
    margin:auto;
    display:flex;
    flex-direction:column;
    position:relative;
    z-index:2;
}

header{
    text-align:center;
    padding:18px;
    background:#000;
    font-weight:900;
    letter-spacing:4px;
    color:#ff7a00;
    font-size:22px;
    border-bottom:1px solid #222;
}

#chat{
    flex:1;
    overflow-y:auto;
    padding:24px;
}

.msg{
    max-width:85%;
    padding:18px 22px;
    margin:14px 0;
    border-radius:18px;
    font-weight:700;
    font-size:18px;
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
    padding:16px;
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
    font-size:18px;
    font-weight:700;
}

input::placeholder{
    color:#aaa;
}

button{
    padding:18px 26px;
    background:#ff7a00;
    border:none;
    border-radius:16px;
    font-weight:900;
    font-size:18px;
    color:black;
    cursor:pointer;
}

@keyframes fade{
    from{opacity:0; transform:translateY(8px)}
    to{opacity:1; transform:translateY(0)}
}
</style>
</head>

<body>

<!-- 🔥 IRON MAN SVG -->
<div class="ironman-bg">
<svg viewBox="0 0 200 200">
  <path d="M50 40 L150 40 L170 90 L150 150 L50 150 L30 90 Z" />
  <path d="M70 80 L90 80 L90 100 L70 100 Z" />
  <path d="M110 80 L130 80 L130 100 L110 100 Z" />
  <path d="M80 120 L120 120 L110 140 L90 140 Z" />
</svg>
</div>

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
