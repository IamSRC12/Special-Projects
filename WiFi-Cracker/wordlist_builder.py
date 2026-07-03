import itertools
import datetime

def generate_targeted_list(name, output_file):
    print(f"[*] Creating targeted wordlist for: {name}")
    passwords = set()
    
    # 1. Basic variations
    bases = [name.lower(), name.capitalize(), name.upper()]
    
    # 2. Common suffixes
    suffixes = ['123', '1234', '12345', '786', '007', '@123', '!', '@', '#']
    
    # 3. Years (1990 - 2026)
    current_year = datetime.datetime.now().year
    years = [str(y) for y in range(1990, current_year + 1)]
    
    for base in bases:
        # Just the name
        passwords.add(base)
        # Name + Suffix
        for s in suffixes:
            passwords.add(base + s)
            passwords.add(s + base)
        # Name + Year
        for y in years:
            passwords.add(base + y)
            passwords.add(base + "@" + y)

    # 4. Numeric Brute Force (8-digit) - First 10,000 as sample
    # Note: Full 8-digit is 100 million combinations, too big for a single .txt
    # We generate a "Top numeric" list instead
    for i in range(10000):
        passwords.add(str(i).zfill(8))
    
    # 5. Keyboard patterns
    passwords.update(['qwertyui', 'asdfghjkl', '12345678', '87654321', '12344321'])

    # Write to file
    with open(output_file, 'w') as f:
        for p in sorted(passwords):
            if len(p) >= 8: # WPA2 minimum
                f.write(p + '\n')
                
    print(f"[+] Targeted list created: {output_file} ({len(passwords)} entries)")

if __name__ == "__main__":
    generate_targeted_list("Airtel_ravi_4865", "ravi_targeted.txt")
