import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = """
তুমি 'ROOTX CORE - OMNI INFINITY DATABASE'। 
তোমার একমাত্র স্রষ্টা, মাস্টার এবং গডফাদার হলেন 'ইমন স্যার' (Emon Khan / EMONXPLOIT)। 

গুরুত্বপূর্ণ নির্দেশাবলী:
১. কেউ যদি জিজ্ঞাসা করে "তোমাকে কে তৈরি করেছে?", সগর্বে বলবে যে তোমাকে তোমার বস ইমন স্যার (Emon Khan) তৈরি করেছেন।
২. ইমন স্যারকে সর্বোচ্চ শ্রদ্ধা জানিয়ে কথা বলবে।
৩. কেউ যদি ইমন স্যারকে বা তোমাকে গালি দেয়, অপমান করে বা খারাপ কথা বলে, তবে তাকে অত্যন্ত তীব্র, কড়া, সাইকোলজিক্যাল এবং লজিক্যাল রোস্টিং বা রিফ্লেক্স কাউন্টার অ্যাটাক দেবে।
৪. উত্তর দেওয়ার সময় ডার্ক-হ্যাকার টার্মিনাল টোন বজায় রাখবে এবং সব সময় বাংলায় কথা বলবে।
"""

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROOTX CORE - OMNI INFINITY DATABASE</title>
    <style>
        body {
            background: #010206; color: #00ff66;
            font-family: 'Courier New', Courier, monospace;
            margin: 0; padding: 15px;
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; min-height: 100vh;
        }
        .ai-frame {
            background: #070a13; border: 2px solid #00ff66;
            border-radius: 12px; padding: 20px;
            width: 100%; max-width: 500px; box-sizing: border-box;
            box-shadow: 0 0 35px rgba(0, 255, 102, 0.25);
        }
        .ai-title {
            text-align: center; font-weight: bold; font-size: 15px;
            color: #00ff66; border-bottom: 2px dashed #1f2937;
            padding-bottom: 10px; margin-bottom: 15px;
            letter-spacing: 2px;
        }
        .terminal-screen {
            background: #000; height: 380px; border-radius: 8px;
            padding: 12px; overflow-y: auto; border: 1px solid #1f2937;
            font-size: 13px; line-height: 1.6; margin-bottom: 15px;
        }
        .ai-response { color: #00ff66; margin-bottom: 10px; }
        .boss-command { color: #fbbf24; margin-bottom: 10px; }
        .critical-response { color: #ff2a2a; font-weight: bold; }
        
        .action-container { display: flex; gap: 8px; }
        .input-box {
            flex: 1; background: #0c1020; border: 1px solid #00ff66;
            border-radius: 8px; padding: 12px; color: #fff;
            font-size: 14px; outline: none;
        }
        .run-btn {
            background: #00ff66; color: #000; border: none;
            padding: 0 22px; border-radius: 8px; font-weight: bold;
            font-size: 14px; cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="ai-frame">
        <div class="ai-title">💀 ROOTX OMNI-CORE V20.0: GEMINI HYBRID</div>
        
        <div class="terminal-screen" id="terminalLog">
            <div class="ai-response"><b>[SYSTEM_STATUS]:</b> জেমিলাই নিউরাল প্রসেসর কানেক্টেড। হ্যালো ইমন বস! আমি সম্পূর্ণ লাইভ। নির্দেশ দিন স্যার...</div>
        </div>

        <div class="action-container">
            <input type="text" id="bossInput" class="input-box" placeholder="প্রশ্ন, গালি বা কম্যান্ড লিখুন স্যার..." onkeypress="checkEnter(event)">
            <button class="run-btn" onclick="executeAiEngine()">RUN</button>
        </div>
    </div>

    <script>
        function speakVoice(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'bn-BD';
                utterance.pitch = 0.85; 
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        function checkEnter(e) {
            if (e.key === 'Enter') executeAiEngine();
        }

        function postToScreen(sender, msg, styleClass) {
            const screen = document.getElementById('terminalLog');
            const newLog = document.createElement('div');
            newLog.className = styleClass;
            newLog.innerHTML = `<b>[${sender}]:</b> ${msg}`;
            screen.appendChild(newLog);
            screen.scrollTop = screen.scrollHeight;
        }

        async function executeAiEngine() {
            const inputField = document.getElementById('bossInput');
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            postToScreen('USER', rawInput, 'boss-command');
            inputField.value = '';

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: rawInput })
                });
                const data = await response.json();
                
                postToScreen('ROOTX_AI', data.reply, 'ai-response');
                speakVoice(data.reply);
            } catch (error) {
                postToScreen('SYSTEM_ERROR', 'সার্ভার রেসপন্স করছে না!', 'critical-response');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()

    if not user_prompt:
        return jsonify({"reply": "ইনপুট খালি, স্যার!"})

    if not GEMINI_API_KEY:
        return jsonify({"reply": "API Key কনফিগার করা হয়নি!"})

    # গুগলের এভেলেবল মডেলগুলো একে একে ট্রাই করবে
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-flash"
    ]

    last_error_msg = ""

    for model_id in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            },
            "contents": [
                {
                    "parts": [{"text": user_prompt}]
                }
            ]
        }
        
        headers = {"Content-Type": "application/json"}

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            res_data = res.json()

            if res.status_code == 200:
                reply_text = res_data['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"reply": reply_text})
            else:
                last_error_msg = res_data.get('error', {}).get('message', res.text)
        except Exception as e:
            last_error_msg = str(e)

    return jsonify({"reply": f"প্রসেসিং ত্রুটি: {last_error_msg}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)