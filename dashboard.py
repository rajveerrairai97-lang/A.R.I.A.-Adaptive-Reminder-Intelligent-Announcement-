from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
from zoneinfo import ZoneInfo
import scheduler
import deadlines
import learner
from notifier import notify

app = Flask(__name__)
IST = ZoneInfo("Asia/Kolkata")

HTML = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JARVIS Command Center</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#050b14;color:#d9f7ff;font-family:Arial,sans-serif}
.wrap{max-width:1100px;margin:auto;padding:22px}.top,.card{background:#071522;border:1px solid #0b607b;border-radius:16px;box-shadow:0 0 22px #00304466}
.top{padding:20px;display:flex;justify-content:space-between;align-items:center}.card{padding:18px;margin-top:16px}h1{color:#55e8ff;letter-spacing:3px;margin:0}h2{color:#55dfff}
.online{color:#6dffbd;font-weight:bold;margin-top:8px}.clock{font-size:28px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.wide{grid-column:1/-1}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.stat{padding:14px;background:#06111b;border:1px solid #124357;border-radius:10px}.num{font-size:28px;color:#62eaff}
.formgrid{display:grid;grid-template-columns:1fr 150px 150px;gap:8px}input,select{width:100%;padding:10px;background:#07131d;color:#dffaff;border:1px solid #14718d;border-radius:8px;margin-bottom:8px}
button{padding:10px 14px;border-radius:8px;border:1px solid #16a6d1;background:#073246;color:#bff5ff;cursor:pointer}button:hover{background:#0b4b64}
.row{padding:11px 0;border-bottom:1px solid #123341;display:flex;justify-content:space-between;gap:10px;align-items:center}.tag{padding:3px 7px;border:1px solid #176d85;border-radius:15px;font-size:12px}.msg{color:#73ffbd;min-height:20px;margin-top:8px}.empty{color:#779aa5;padding:10px 0}.week{display:flex;gap:10px;flex-wrap:wrap}.week input{width:auto}
@media(max-width:750px){.grid{grid-template-columns:1fr}.wide{grid-column:auto}.top{flex-direction:column;align-items:flex-start;gap:15px}.formgrid{grid-template-columns:1fr}.stats{grid-template-columns:1fr}}
</style></head>
<body><div class="wrap">
<div class="top"><div><h1>🔷 JARVIS</h1><small>PERSONAL COMMAND CENTER</small><div class="online">● SYSTEM ONLINE</div></div><div><div class="clock" id="clock">--:--:--</div><small>India Standard Time</small></div></div>
<div class="grid">
<div class="card wide"><div class="stats">
<div class="stat">ACTIVE REMINDERS<div class="num" id="reminderCount">0</div></div>
<div class="stat">ACTIVE DEADLINES<div class="num" id="deadlineCount">0</div></div>
<div class="stat">LEARNED PATTERNS<div class="num" id="patternCount">0</div></div>
</div></div>

<div class="card"><h2>➕ Create Reminder</h2>
<form id="reminderForm"><div class="formgrid">
<input id="task" placeholder="Task, e.g. Physics class" required>
<input id="time" type="time" required>
<select id="recurrence"><option value="once">One time</option><option value="daily">Daily</option><option value="weekly">Weekly</option></select>
</div>
<div id="dateBox"><input id="date" type="date"></div>
<div id="weekBox" class="week" style="display:none">
<label>Mon <input type="checkbox" value="monday"></label><label>Tue <input type="checkbox" value="tuesday"></label><label>Wed <input type="checkbox" value="wednesday"></label><label>Thu <input type="checkbox" value="thursday"></label><label>Fri <input type="checkbox" value="friday"></label><label>Sat <input type="checkbox" value="saturday"></label><label>Sun <input type="checkbox" value="sunday"></label>
</div><br><button type="submit">Schedule Reminder</button><div id="reminderMsg" class="msg"></div></form></div>

<div class="card"><h2>📅 Create Deadline</h2><form id="deadlineForm">
<input id="deadlineTask" placeholder="Deadline task" required><input id="deadlineDate" type="date" required>
<button type="submit">Add Deadline</button><div id="deadlineMsg" class="msg"></div></form></div>

<div class="card"><h2>⏰ Reminders</h2><div id="reminders">Loading...</div></div>
<div class="card"><h2>🚨 Deadlines</h2><div id="deadlines">Loading...</div></div>
<div class="card"><h2>🧠 Memory</h2><div id="memory">Loading...</div></div>
<div class="card wide"><h2>🤖 JARVIS Test</h2><button onclick="testJarvis()">Test Notification + David Voice</button><div id="testMsg" class="msg"></div></div>
</div></div>
<script>
const $=id=>document.getElementById(id);
function esc(v){return String(v??"").replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]))}
function clock(){ $("clock").textContent=new Date().toLocaleTimeString("en-IN",{hour12:false,timeZone:"Asia/Kolkata"})}
setInterval(clock,1000);clock();

$("recurrence").onchange=()=>{let v=$("recurrence").value;$("dateBox").style.display=v==="once"?"block":"none";$("weekBox").style.display=v==="weekly"?"flex":"none"};

async function loadReminders(){
 let r=await fetch("/api/reminders"),d=await r.json(),a=d.filter(x=>x.active!==false);$("reminderCount").textContent=a.length;
 $("reminders").innerHTML=a.length?a.map(x=>`<div class="row"><div><b>${esc(x.task)}</b><br><span class="tag">${esc(x.time)}</span> <span class="tag">${esc(x.recurrence||"once")}</span></div><button onclick="deleteReminder(${x.id})">Disable</button></div>`).join(""):'<div class="empty">No active reminders.</div>';
}
async function loadDeadlines(){
 let r=await fetch("/api/deadlines"),d=await r.json();$("deadlineCount").textContent=d.length;
 $("deadlines").innerHTML=d.length?d.map(x=>`<div class="row"><div><b>${esc(x.task)}</b><br><span class="tag">${esc(x.date)}</span> <span class="tag">${x.days_remaining} day(s) left</span></div><button onclick="completeDeadline(${x.index})">Complete</button></div>`).join(""):'<div class="empty">No active deadlines.</div>';
}
async function loadMemory(){
 let r=await fetch("/api/memory"),d=await r.json();$("patternCount").textContent=d.pattern_count;
 let h=`<div class="row">Reminder history: <b>${d.history_count}</b></div>`;
 h+=d.patterns.length?d.patterns.map(x=>`<div class="row"><b>${esc(x.task)}</b> at ${x.time} • ${x.occurrences} observations</div>`).join(""):'<div class="empty">No learned patterns yet.</div>';
 $("memory").innerHTML=h;
}
async function loadAll(){await Promise.all([loadReminders(),loadDeadlines(),loadMemory()])}
$("reminderForm").onsubmit=async e=>{e.preventDefault();let rec=$("recurrence").value;let weekdays=[...document.querySelectorAll("#weekBox input:checked")].map(x=>x.value);let body={task:$("task").value.trim(),time:$("time").value,date:$("date").value,recurrence:rec,weekdays:weekdays};let r=await fetch("/api/reminders",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});let d=await r.json();$("reminderMsg").textContent=d.message||d.error||"Done";if(r.ok){e.target.reset();$("weekBox").style.display="none";$("dateBox").style.display="block";loadAll()}};
$("deadlineForm").onsubmit=async e=>{e.preventDefault();let body={task:$("deadlineTask").value.trim(),date:$("deadlineDate").value};let r=await fetch("/api/deadlines",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});let d=await r.json();$("deadlineMsg").textContent=d.message||d.error||"Done";if(r.ok){e.target.reset();loadDeadlines()}};
async function deleteReminder(id){await fetch("/api/reminders/"+id,{method:"DELETE"});loadReminders()}
async function completeDeadline(i){await fetch("/api/deadlines/"+i+"/complete",{method:"POST"});loadDeadlines()}
async function testJarvis(){let r=await fetch("/api/test",{method:"POST"});let d=await r.json();$("testMsg").textContent=d.message||d.error||"Done"}
loadAll();setInterval(loadAll,5000);
</script></body></html>"""

def parse_time(value):
    return datetime.strptime(value, "%H:%M").time()

def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()

@app.get("/")
def index():
    return render_template_string(HTML)

@app.get("/api/reminders")
def api_reminders():
    return jsonify(scheduler.load_reminders())

@app.post("/api/reminders")
def api_create_reminder():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()
    time_value = str(data.get("time", "")).strip()
    recurrence = str(data.get("recurrence", "once")).strip().lower()
    date_value = str(data.get("date", "")).strip()
    weekdays = data.get("weekdays", [])
    if not task or not time_value:
        return jsonify({"error":"Task and time are required."}), 400
    if recurrence not in {"once","daily","weekly"}:
        return jsonify({"error":"Invalid recurrence."}), 400
    try:
        reminder_time = parse_time(time_value)
    except ValueError:
        return jsonify({"error":"Time must be HH:MM."}), 400
    reminder_date = None
    if recurrence == "once":
        if not date_value:
            return jsonify({"error":"A date is required for a one-time reminder."}), 400
        try:
            reminder_date = parse_date(date_value)
        except ValueError:
            return jsonify({"error":"Invalid date."}), 400
    if recurrence == "weekly" and not weekdays:
        return jsonify({"error":"Choose at least one weekday."}), 400
    reminder = scheduler.create_reminder(task, reminder_time, reminder_date, recurrence, weekdays)
    try:
        scheduled_dt = datetime.combine(reminder_date or datetime.now(IST).date(), reminder_time, tzinfo=IST)
        learner.record_reminder(task, scheduled_dt)
    except Exception as error:
        print(f"[LEARNING ERROR] {error}")
    return jsonify({"message":"Reminder scheduled successfully.","reminder":reminder})

@app.delete("/api/reminders/<int:reminder_id>")
def api_delete_reminder(reminder_id):
    if not scheduler.delete_reminder(reminder_id):
        return jsonify({"error":"Reminder not found."}), 404
    return jsonify({"message":"Reminder disabled."})

@app.get("/api/deadlines")
def api_deadlines():
    result = []
    active = deadlines.get_active_deadlines()
    for index, item in enumerate(active):
        copy = dict(item)
        copy["days_remaining"] = deadlines.days_remaining(item)
        copy["index"] = index
        result.append(copy)
    return jsonify(result)

@app.post("/api/deadlines")
def api_create_deadline():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()
    date_value = str(data.get("date", "")).strip()
    if not task or not date_value:
        return jsonify({"error":"Task and date are required."}), 400
    try:
        deadline_date = parse_date(date_value)
    except ValueError:
        return jsonify({"error":"Invalid date."}), 400
    deadline = deadlines.add_deadline(task, deadline_date)
    return jsonify({"message":"Deadline added successfully.","deadline":deadline})

@app.post("/api/deadlines/<int:index>/complete")
def api_complete_deadline(index):
    active = deadlines.get_active_deadlines()
    if index < 0 or index >= len(active):
        return jsonify({"error":"Deadline not found."}), 404
    target = active[index]
    all_deadlines = deadlines.get_deadlines()
    for real_index, item in enumerate(all_deadlines):
        if item.get("task") == target.get("task") and item.get("date") == target.get("date") and not item.get("completed", False):
            if deadlines.mark_completed(real_index):
                return jsonify({"message":"Deadline marked complete."})
    return jsonify({"error":"Deadline not found."}), 404

@app.get("/api/memory")
def api_memory():
    return jsonify(learner.get_learning_summary())

@app.post("/api/test")
def api_test():
    notify("Good evening, sir. JARVIS dashboard test successful. Systems are online.", title="🔷 JARVIS TEST")
    return jsonify({"message":"JARVIS test sent."})

def run_dashboard():
    print("=" * 65)
    print("🔷 JARVIS DASHBOARD ONLINE")
    print("🌐 http://127.0.0.1:5000")
    print("🇮🇳 Timezone: Asia/Kolkata")
    print("=" * 65)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_dashboard()