# Network Traffic Filtering Documentation & Test Logs

## 1. Integrated Situation Overview
A security review at the polytechnic institute identified guest network access to the central student records server and repeated unauthorized connection attempts from external IP addresses. To secure the central server, firewall filtering rules were implemented in the laboratory environment to enforce strict access controls.

---

## 2. Network Topology & Addressing Scheme
- **Central Records Server IP:** `10.0.0.5`
- **Protected Service:** SSH / Administration (`Port 22`)
- **Authorised Staff Subnet:** `192.168.10.0/24`
- **Guest Network Subnet:** `192.168.20.0/24`
- **Unfamiliar External IP:** `203.0.113.45`

---

## 3. Firewall Configuration Rules
The following firewall rules were applied using Windows Defender Firewall (via PowerShell with Administrator privileges) to enforce traffic segregation:

```powershell
# Rule 1: Block all inbound traffic from the Guest Subnet to the Records Server
New-NetFirewallRule -DisplayName "Block-Guest-Server-Access" `
                    -Direction Inbound `
                    -RemoteAddress "192.168.20.0/24" `
                    -Action Block

# Rule 2: Permit Authorised Staff Subnet access to the specified service (Port 22)
New-NetFirewallRule -DisplayName "Allow-Staff-SSH" `
                    -Direction Inbound `
                    -LocalPort 22 `
                    -Protocol TCP `
                    -RemoteAddress "192.168.10.0/24" `
                    -Action Allow

# Rule 3: Block all other inbound traffic targeting Port 22
New-NetFirewallRule -DisplayName "Block-Other-Inbound-SSH" `
                    -Direction Inbound `
                    -LocalPort 22 `
                    -Protocol TCP `
                    -Action Block
```
# Connection Test Results
| Test ID | Test Scenario | Source Subnet / Host | Target IP & Port | PowerShell Command Executed | Expected Result | Actual Outcome | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-01** | Staff Network Access | `192.168.10.15` (Staff) | `10.0.0.5:22` | `Test-NetConnection 10.0.0.5 -Port 22` | Connection Permitted | `TcpTestSucceeded : True` | **PASSED** |
| **TEST-02** | Guest Network Isolation | `192.168.20.5` (Guest) | `10.0.0.5:22` | `Test-NetConnection 10.0.0.5 -Port 22` | Connection Blocked | `TcpTestSucceeded : False` | **PASSED** |
| **TEST-03** | External Threat Mitigation | `203.0.113.45` (External) | `10.0.0.5:22` | `Test-NetConnection 10.0.0.5 -Port 22` | Connection Blocked | `TcpTestSucceeded : False` | **PASSED** |
