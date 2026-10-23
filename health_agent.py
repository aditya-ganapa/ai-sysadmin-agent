import psutil
import shutil
import platform
import subprocess
import re
from datetime import datetime
from google import genai

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    disk_percent = (disk.used / disk.total) * 100
    
    metrics_summary = (
        f"System: {platform.system()} {platform.release()}\n"
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory.percent}% (Total: {memory.total / (1024**3):.2f} GB, Used: {memory.used / (1024**3):.2f} GB)\n"
        f"Disk Usage: {disk_percent:.2f}% (Total: {disk.total / (1024**3):.2f} GB, Free: {disk.free / (1024**3):.2f} GB)"
    )
    return metrics_summary

def analyze_with_ai(metrics_text):
    client = genai.Client()
    
    prompt = (
        "You are an expert Linux and Systems Administrator. Analyze the following system health metrics. "
        "1. Explain in plain English the system state and any issues.\n"
        "2. Provide ONE specific, safe terminal command or mitigation step that can address the highest priority issue.\n"
        "Format your response with the analysis first, and then clearly place the proposed fix command inside a standard markdown code block (e.g., ```powershell ... ``` or ```bash ... ```) under a section called 'PROPOSED_FIX:'\n\n"
        f"{metrics_text}"
    )
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    return response.text

def extract_command(ai_response):
    # Use regular expressions to find the first markdown code block in the AI response
    match = re.search(r"```(?:\w+)?\n(.*?)\n```", ai_response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def execute_command(command):
    print(f"\n⚙️ Executing command on host system...")
    try:
        # If running on Windows, execute via PowerShell; otherwise use default shell
        if platform.system() == "Windows":
            completed = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=15)
        else:
            completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            
        if completed.stdout:
            print("\n--- Command Output ---")
            print(completed.stdout.strip())
        if completed.stderr:
            print("\n--- Command Errors/Warnings ---")
            print(completed.stderr.strip())
            
        print("\n✅ Action completed successfully.")
    except Exception as e:
        print(f"❌ Failed to execute command: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print(f"Server Health Agent Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    print("\n[1] Gathering system metrics...")
    metrics = get_system_metrics()
    print(metrics)
    
    print("\n[2] Sending metrics to AI for health analysis...")
    try:
        analysis = analyze_with_ai(metrics)
        print("\n" + "=" * 50)
        print("AI Health Analysis & Recommendations:")
        print("=" * 50)
        print(analysis)
        
        # Extract the executable command from the AI's response markdown
        command_to_run = extract_command(analysis)
        
        # Step 3: Interactive Safety Prompt
        print("\n" + "=" * 50)
        if command_to_run:
            user_approval = input(f"🛡️ Do you want the agent to execute this command? (y/n): ").strip().lower()
            
            if user_approval == 'y':
                execute_command(command_to_run)
            else:
                print("🚫 Operation cancelled by user. No changes made.")
        else:
            print("ℹ️ No executable command code block was found in the AI response.")
            
    except Exception as e:
        print(f"\n[Note] AI analysis skipped. Error: {e}")