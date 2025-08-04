import itertools
import pikepdf
from tqdm import tqdm
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys

def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            yield line.strip()

def try_password(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password):
            print(f"\n[+] Password found: {password}")
            return password
    except pikepdf._core.PasswordError:
        return None
    except Exception as e:
        print(f"[!] Error with the password '{password}': {e}")
        return None

def decrypt_pdf(pdf_file, password_iterable, total_passwords, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        with tqdm(total=total_passwords, desc='Cracking password', unit='pwd') as pbar:
            for password in password_iterable:
                future = executor.submit(try_password, pdf_file, password)
                futures.append((future, password))

                done_futures = []
                for fut, pwd in futures:
                    if fut.done():
                        result = fut.result()
                        pbar.update(1)
                        if result:
                            return result
                        done_futures.append((fut, pwd))

                futures = [f for f in futures if f not in done_futures]

            for future, pwd in futures:
                result = future.result()
                pbar.update(1)
                if result:
                    return result

    print("[-] Impossible to decrypt PDF. Password not found.")
    return None

def estimate_password_space(charset, min_len, max_len):
    return sum(len(charset) ** i for i in range(min_len, max_len + 1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt a password-protected PDF file.")
    parser.add_argument('pdf_file', help='Path to password-protected PDF file.')
    parser.add_argument('-w', '--wordlist', help='Word/Password list file')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate password on the fly.')
    parser.add_argument('-min', '--min_length', type=int, default=1, help='Minimum length of the password.')
    parser.add_argument('-max', '--max_length', type=int, default=5, help='Maximum length of the password.')
    parser.add_argument('-c', '--charset', type=str, default=string.ascii_letters + string.digits, help='Charset that will be used for cracking password (default = chars + numbers).')
    parser.add_argument('--max_workers', type=int, default=4, help='Maximum number of threads to use.')

    args = parser.parse_args()

    if args.generate:
        total = estimate_password_space(args.charset, args.min_length, args.max_length)

        if total > 10**7:
            print(f"[!] Too much space used: {total} passwords to try . Reduce length or number of characters.")
            sys.exit(1)

        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = total

    elif args.wordlist:
        try:
            with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                wordlist = [line.strip() for line in f]
            passwords = iter(wordlist)
            total_passwords = len(wordlist)
        except FileNotFoundError:
            print(f"[!] Wordlist file not found: {args.wordlist}")
            sys.exit(1)
    else:
        print("❌ Specify --wordlist or --generate for password on the fly.")
        sys.exit(1)

    found_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)

    if found_password:
        print(f"[✓] PDF decrypted successfully, Password: {found_password}")
    else:
        print("[-] Impossible to find a password")
