import http.server
import json

class Message:
    message_counter = 1

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.id = Message.message_counter
        Message.message_counter += 1

class User:
    def __init__(self, username):
        self.username = username
        self.chatroom = None

    def join_chatroom(self, chatroom):
        if not self.chatroom:
            chatroom.add_user(self)
            self.chatroom = chatroom
            return f"{self.username} joined {chatroom.name}"
        return f"{self.username} is already in a chatroom."

    def leave_chatroom(self):
        if self.chatroom:
            room_name = self.chatroom.name
            self.chatroom.remove_user(self)
            self.chatroom = None
            return f"{self.username} left {room_name}"
        return f"{self.username} is not in any chatroom."

    def send_message(self, content):
        if self.chatroom:
            return self.chatroom.broadcast(self.username, content)
        return f"{self.username} cannot send a message (not in a chatroom)."

class ChatRoom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def broadcast(self, sender_name, content):
        message = Message(sender_name, content)
        self.messages.append(message)
        return message

room = ChatRoom("Python Lounge")
users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie")
}

# Embedded HTML Code directly inside Python
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Lounge Chatroom</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col items-center justify-center p-4">
    <div class="w-full max-w-3xl bg-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col md:flex-row h-[80vh]">
        <div class="w-full md:w-1/3 bg-slate-900/60 border-r border-slate-700/50 p-5 flex flex-col justify-between">
            <div>
                <h1 class="text-xl font-bold text-indigo-400 mb-1"> 🐍Python Lounge</h1>
                <p class="text-xs text-slate-400 mb-6">OOP Web Chatroom</p>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-slate-300 mb-2">Select User:</label>
                    <select id="username" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200">
                        <option value="Alice">Alice</option>
                        <option value="Bob">Bob</option>
                        <option value="Charlie">Charlie</option>
                    </select>
                </div>
                <div class="flex flex-col gap-2">
                    <button onclick="performAction('join')" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-lg text-sm font-medium transition cursor-pointer">Join Room</button>
                    <button onclick="performAction('leave')" class="w-full bg-rose-600 hover:bg-rose-500 text-white py-2 rounded-lg text-sm font-medium transition cursor-pointer">Leave Room</button>
                </div>
            </div>
            <div class="mt-4">
                <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Users in Room:</h3>
                <div id="userList" class="text-sm text-slate-300 italic">None</div>
            </div>
        </div>
        <div class="flex-1 flex flex-col bg-slate-800">
            <div class="p-4 border-b border-slate-700/50 flex justify-between items-center bg-slate-800/80">
                <span id="roomStatus" class="text-xs font-medium text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/20">🔴 Not in Room</span>
            </div>
            <div id="chatBox" class="flex-1 p-4 overflow-y-auto space-y-3 flex flex-col text-sm">
                <div class="m-auto text-center text-slate-500">Select a user and click Join Room to start chatting.</div>
            </div>
            <div class="p-4 border-t border-slate-700/50 bg-slate-900/30 flex gap-2">
                <input type="text" id="msgInput" placeholder="Type a message..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-200 focus:outline-none focus:border-indigo-500">
                <button onclick="performAction('send')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-xl text-sm font-medium transition cursor-pointer">Send</button>
            </div>
        </div>
    </div>
    <script>
        async function performAction(action) {
            const username = document.getElementById("username").value;
            const msgInput = document.getElementById("msgInput");
            const content = msgInput.value;
            if (action === 'send' && !content.trim()) return;
            try {
                const response = await fetch('/api', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, action, content })
                });
                const data = await response.json();
                if (action === 'send') msgInput.value = "";
                updateUI(data);
            } catch (err) {
                alert("Server connection error!");
            }
        }
        function updateUI(data) {
            const chatBox = document.getElementById("chatBox");
            chatBox.innerHTML = "";
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(m => {
                    chatBox.innerHTML += `<div class="p-2.5 bg-slate-700/50 rounded-xl border border-slate-700"><strong class="text-indigo-300">(${m.id}) ${m.sender}:</strong> ${m.content}</div>`;
                });
            } else {
                chatBox.innerHTML = `<div class="m-auto text-center text-slate-500 italic">No messages yet.</div>`;
            }
            const userList = document.getElementById("userList");
            if (data.users && data.users.length > 0) {
                userList.innerHTML = data.users.join(', ');
            } else {
                userList.innerHTML = "None";
            }
            const status = document.getElementById("roomStatus");
            if (data.is_in_room) {
                status.className = "text-xs font-medium text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-full border border-emerald-400/20";
                status.innerText = "🟢 Active in Room";
            } else {
                status.className = "text-xs font-medium text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/20";
                status.innerText = "🔴 Not in Room";
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>"""

class ChatServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        if self.path == '/api':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            username = data.get("username")
            action = data.get("action")
            content = data.get("content", "")

            user = users.get(username)
            if user:
                if action == "join":
                    user.join_chatroom(room)
                elif action == "leave":
                    user.leave_chatroom()
                elif action == "send":
                    user.send_message(content)

            response = {
                "users": [u.username for u in room.users],
                "messages": [{"id": m.id, "sender": m.sender, "content": m.content} for m in room.messages],
                "is_in_room": user.chatroom is not None if user else False
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    PORT = 8000
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, ChatServerHandler)
    print(f"Server started successfully! Open browser at: http://localhost:{PORT}")
    httpd.serve_forever()