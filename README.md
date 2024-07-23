![image](https://github.com/user-attachments/assets/842b69ed-75da-47df-abf0-9e40c021bc7b)

# Request Smuggling Detection Tool

This tool is designed to detect potential HTTP request smuggling vulnerabilities in web applications. It supports both HTTP/1.1 and HTTP/2 request smuggling techniques and provides detailed analysis of the responses.

## Features

- **HTTP/1.1 Request Smuggling (TE.CL and CL.TE)**
- **HTTP/2 Request Smuggling**
- **Random User-Agent selection**
- **Detailed response comparison**
- **Interactive mode for single URL or batch processing from file**

## Installation

```bash
git clone https://github.com/Hacking-Notes/HR-Smuggler.git
```

## Usage

```bash
python request_smuggling.py -u <target_url> -b <burp_collaborator_url>
python request_smuggling.py -f <file_with_urls> -b <burp_collaborator_url>
```

- **-u, --url**: Single URL to test
- **-f, --file**: File containing multiple URLs to test (one URL per line)
- **-b, --burp**: Burp Collaborator URL (required)

## Example

### Testing a Single URL

```bash
python request_smuggling.py -u http://example.com -b http://collaborator.com
```

### Testing Multiple URLs from a File

```bash
python request_smuggling.py -f urls.txt -b http://collaborator.com
```

## Detailed Check

The tool compares the responses for potential indicators of request smuggling, including differences in:

- Status codes
- Headers
- Response bodies

If potential request smuggling is detected, further steps are suggested for verification and documentation.

## Next Steps After Detection

1. Check the Burp Collaborator server for unexpected requests.
2. Verify if the Collaborator URL was accessed during the test.
3. Perform additional tests to understand the impact and potential exploitation paths.
4. Document the findings and report the vulnerability if confirmed.

## Author

<a href="https://github.com/hacking-notes">Hacking Notes</a><br>
K<br>
<a href="https://github.com/ShadowByte1">ShadowByte</a>                                                                                             

---

This tool helps security researchers and penetration testers identify and analyze request smuggling vulnerabilities efficiently. Ensure responsible usage and proper reporting of any discovered vulnerabilities.
