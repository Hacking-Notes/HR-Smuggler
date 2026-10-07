<div align="center">

<kbd>&nbsp;REQUEST SMUGGLING&nbsp;</kbd> &nbsp; <kbd>&nbsp;HTTP/1.1&nbsp;</kbd> &nbsp; <kbd>&nbsp;HTTP/2&nbsp;</kbd> &nbsp; 

[![Website](https://img.shields.io/badge/WEBSITE-hacking--notes.com-ff3333?style=flat-square&labelColor=000000)](https://hacking-notes.com)

</div>

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
python HR_Smuggler.py -u <target_url> -b <burp_collaborator_url>
python HR_Smuggler.py -f <file_with_urls> -b <burp_collaborator_url>
```

- **-u, --url**: Single URL to test
- **-f, --file**: File containing multiple URLs to test (one URL per line)
- **-b, --burp**: Burp Collaborator URL (required)

## Example

### Testing a Single URL

```bash
python HR_Smuggler.py -u http://example.com -b http://collaborator.com
```

### Testing Multiple URLs from a File

```bash
python HR_Smuggler.py -f urls.txt -b http://collaborator.com
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

<br>

<div align="center">

### ───────────────  HACKING NOTES ECOSYSTEM  ───────────────

[![Website](https://img.shields.io/badge/🌐_WEBSITE-hacking--notes.com-ff3333?style=flat-square&labelColor=000000)](https://hacking-notes.com)
[![Roadmap](https://img.shields.io/badge/🗺_ROADMAP-Hacker--Roadmap-f5f5f5?style=flat-square&labelColor=000000)](https://github.com/Hacking-Notes/Hacker-Roadmap)
[![RedTeam](https://img.shields.io/badge/🔴_RED_TEAM-notes-ff3333?style=flat-square&labelColor=000000)](https://github.com/Hacking-Notes/RedTeam)
[![BlueTeam](https://img.shields.io/badge/🔵_BLUE_TEAM-notes-3388ff?style=flat-square&labelColor=000000)](https://github.com/Hacking-Notes/BlueTeam)

<sub><code>// part of the Hacking Notes toolkit — hacking-notes.com</code></sub>

</div>
