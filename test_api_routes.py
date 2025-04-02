import requests

BASE_URL = "http://localhost:8000"
TEST_USER = {"email": "test@example.com", "password": "test123"}
PDF_PATH = "test.pdf"  # Must exist in the same directory


def login():
    print("🔐 Logging in...")
    response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful.")
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None


def test_route(name, method, path, headers=None, **kwargs):
    url = BASE_URL + path
    try:
        response = getattr(requests, method.lower())(url, headers=headers, **kwargs)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {method.upper()} {path} [{response.status_code}]")
        return response
    except Exception as e:
        print(f"❌ ERROR on {method.upper()} {path}: {e}")


if __name__ == "__main__":
    headers = login()
    if not headers:
        exit()

    print("\n🚦 Starting backend route tests...\n")

    # 1. Ping
    test_route("Ping", "GET", "/summarizer/ping", headers=headers)

    # 2. Extract Summary
    print("📄 Uploading PDF and extracting summary...")
    with open(PDF_PATH, "rb") as f:
        files = {"file": f}
        response = test_route("Extract", "POST", "/summarizer/extract?folder=articles", headers=headers, files=files)

    if response and response.status_code == 200:
        summary_data = response.json()
        filename = summary_data.get("filename", "test_summary.json")  # fallback name
        print(f"🧠 Summary extracted. Filename: {filename}")
    else:
        filename = None

    # 3. Save summary (if implemented separately)
    # test_route("Save", "POST", "/summarizer/save", headers=headers, json={"filename": filename, "content": summary_data})

    # 4. List summaries
    test_route("List summaries", "GET", "/summarizer/list", headers=headers)

    # 5. Load summary
    if filename:
        test_route("Load summary", "GET", f"/summarizer/load/{filename}", headers=headers)

    # 6. List uploaded files
    test_route("List files", "GET", "/summarizer/files", headers=headers)

    # 7. Get PDF
    if filename:
        pdf_filename = filename.replace(".json", ".pdf")
        test_route("Get original PDF", "GET", f"/summarizer/pdf/{pdf_filename}", headers=headers)

    # 8. Delete summary
    if filename:
        test_route("Delete summary", "DELETE", f"/summarizer/{filename}", headers=headers)
