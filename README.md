# PDF Password Cracker

A multithreaded Python tool for cracking password-protected PDF files using brute force or dictionary attacks.

## Features

- **Dual Attack Modes**: Support for both wordlist-based dictionary attacks and brute force password generation
- **Multithreaded Processing**: Configurable thread pool for faster password testing
- **Progress Tracking**: Real-time progress bar showing cracking progress
- **Customizable Character Sets**: Define your own character sets for brute force attacks
- **Safety Limits**: Built-in protection against excessive computation (limits brute force to 10M passwords)
- **Flexible Password Length**: Configurable minimum and maximum password lengths for generation

## Requirements

```bash
pip install pikepdf tqdm
```

## Usage

### Dictionary Attack (Recommended)
Use a wordlist file containing potential passwords:

```bash
python pdf_cracker.py document.pdf -w passwords.txt
```

### Brute Force Attack
Generate passwords on-the-fly with customizable parameters:

```bash
# Basic brute force (letters + numbers, 1-5 characters)
python pdf_cracker.py document.pdf --generate

# Custom length range
python pdf_cracker.py document.pdf --generate --min_length 3 --max_length 6

# Custom character set (numbers only)
python pdf_cracker.py document.pdf --generate --charset 0123456789

# Increase thread count for faster processing
python pdf_cracker.py document.pdf --generate --max_workers 8
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `pdf_file` | Path to the password-protected PDF file | Required |
| `-w, --wordlist` | Path to wordlist/dictionary file | None |
| `-g, --generate` | Enable brute force password generation | False |
| `-min, --min_length` | Minimum password length for generation | 1 |
| `-max, --max_length` | Maximum password length for generation | 5 |
| `-c, --charset` | Character set for brute force | a-z, A-Z, 0-9 |
| `--max_workers` | Number of threads to use | 4 |

## Examples

```bash
# Try common passwords from rockyou.txt
python pdf_cracker.py secret.pdf -w rockyou.txt

# Brute force with only lowercase letters, 4-6 characters
python pdf_cracker.py secret.pdf --generate --charset abcdefghijklmnopqrstuvwxyz --min_length 4 --max_length 6

# High-performance mode with 16 threads
python pdf_cracker.py secret.pdf -w passwords.txt --max_workers 16
```

## How It Works

1. **PDF Testing**: Uses the `pikepdf` library to attempt opening the PDF with each password candidate
2. **Multithreading**: Distributes password attempts across multiple worker threads for improved performance
3. **Progress Tracking**: Displays real-time progress with estimated completion times
4. **Early Termination**: Stops immediately when the correct password is found

## Security & Performance Notes

- **Brute Force Limitation**: Automatically limits brute force attempts to 10,000,000 passwords to prevent excessive resource usage
- **Thread Safety**: Uses thread-safe operations for concurrent password testing
- **Memory Efficient**: Generates passwords on-demand rather than storing them all in memory
- **Error Handling**: Gracefully handles file not found errors and PDF corruption issues

## Legal Disclaimer

This tool is intended for legitimate purposes only, such as:
- Recovering passwords for your own PDF files
- Authorized penetration testing
- Digital forensics investigations

Users are responsible for ensuring they have proper authorization before attempting to crack any PDF files.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

[Add your preferred license here]
