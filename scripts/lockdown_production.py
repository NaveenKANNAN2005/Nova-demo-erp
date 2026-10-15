import json
import os
import subprocess
import frappe

site = "nova.local"
bench_dir = "/home/naveen/frappe-bench"
site_config_path = os.path.join(bench_dir, "sites", site, "site_config.json")

print("=== STARTING PRODUCTION LOCKDOWN FOR NOVA INDUSTRIES ===")

# 1. Update site_config.json
print("\n[Step 1] Hardening site_config.json...")
with open(site_config_path, "r") as f:
    config = json.load(f)

# Set developer_mode to 0
config["developer_mode"] = 0
config["pause_scheduler"] = 0

with open(site_config_path, "w") as f:
    json.dump(config, f, indent=1)

print("  ✓ developer_mode set to 0 (Schema editing disabled, Desk locked from doc modifications)")
print("  ✓ pause_scheduler set to 0 (Automated background queues enabled)")

# 2. Connect to Frappe site to apply settings & clear cache
print("\n[Step 2] Applying system settings and clearing cache...")
os.chdir(os.path.join(bench_dir, "sites"))
frappe.init(site)
frappe.connect()

# Set System Settings
sys_settings = frappe.get_single("System Settings")
sys_settings.session_expiry = "24:00"
sys_settings.allow_error_traceback = 0
sys_settings.save(ignore_permissions=True)
frappe.db.commit()
print("  ✓ System Settings: session expiry set to 24h, error traceback disabled for end users")

# Clear site cache
frappe.clear_cache()
print("  ✓ Site cache cleared and rebuilt")

# 3. Create Complete Production Snapshot (Database + Files)
print("\n[Step 3] Taking Full Production Backup (Database + Files)...")
frappe.destroy()

cmd = f"/home/naveen/.local/bin/bench --site {site} backup --with-files"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=bench_dir)
print(result.stdout)
if result.stderr:
    print("Stderr:", result.stderr)

# List created backup files
backup_dir = os.path.join(bench_dir, "sites", site, "private", "backups")
if os.path.exists(backup_dir):
    files = sorted(os.listdir(backup_dir), reverse=True)
    print("  ✓ Production Backup Files in:", backup_dir)
    for b in files[:4]:
        size = os.path.getsize(os.path.join(backup_dir, b)) / 1024
        print(f"     - {b} ({size:.1f} KB)")

# 4. Final Security Check
print("\n[Step 4] Final Production Verification:")
with open(site_config_path, "r") as f:
    verified_conf = json.load(f)

print(f"  ✓ Developer Mode: {verified_conf.get('developer_mode')} (0 = Locked)")
print(f"  ✓ Scheduler Paused: {verified_conf.get('pause_scheduler')} (0 = Active)")
print("\n=== NOVA INDUSTRIES IS OFFICIALLY LOCKED AND PRODUCTION READY! ===")
