# Sonar Ticket Monitor (Terminal-based)

A terminal-based ticket monitor that integrates with [Sonar](https://sonar.software)'s GraphQL API to check for new tickets in real-time and display desktop notifications via `win10toast`.

---

## 🔧 Features

- Polls Sonar's GraphQL API every 30 seconds to check for new tickets
- Filters by ticket group(s) you define in the script
- Displays desktop toast notifications for new tickets
- Designed for **Windows** (due to use of `win10toast`)
- Environment-based configuration for security and flexibility

---

## 🐍 Built With

- Python
- `requests` – for making HTTP calls to the GraphQL API
- `python-dotenv` – to securely load API credentials from a `.env` file
- `win10toast` – for Windows toast notifications

---

## ⚙️ Requirements

- Python 3.6+
- Windows OS (due to `win10toast`)
- A valid Sonar API key
- Your organization's Sonar GraphQL endpoint

---

## 📁 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sonar-ticket-monitor.git
   cd sonar-ticket-monitor
   ```

2. **Create and populate a `.env` file**

   Create a `.env` file in the root of your project and add your credentials:

   ```env
   SONAR_API_KEY=your_sonar_api_key_here
   GRAPHQL_URL=https://YourOrganizationName.sonar.software/api/graphql
   ```

3. **Install Dependencies**

   Use `pip` to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Monitor**

   Start the script from the terminal:

   ```bash
   python src/Sonar_ticket_monitor.py
   ```

---

### 📝 Notes

- You may need to modify the script to specify which ticket group(s) you want to monitor.
- This tool is **currently limited to Windows** due to its use of `win10toast`.
  For cross-platform support, consider swapping in a different notification library.

---

### 🛡️ Disclaimer

This tool is not affiliated with or officially supported by Sonar.
Use at your own discretion and ensure you comply with your organization's data and security policies.

---

### 📃 License

This project is licensed under the [MIT License](LICENSE).
See the `LICENSE` file for full license text.
