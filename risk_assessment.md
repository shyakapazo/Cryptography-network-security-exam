# Risk Assessment

## 1. Assets, Vulnerabilities, and Consequences
1. **Asset:** Student Academic Records
   - **Vulnerability:** Unencrypted file transfers between campuses.
   - **Consequence:** Eavesdropping/interception leading to sensitive student data leaks (breach of privacy).
2. **Asset:** Central Records Server Access
   - **Vulnerability:** Guest network access to the records server.
   - **Consequence:** Unauthorized internal access, data tampering, or data deletion by guests.
3. **Asset:** Administrative & Staff Accounts
   - **Vulnerability:** Weak staff passwords and outdated software.
   - **Consequence:** Credential harvesting, unauthorized administrative access, and exploit execution.

## 2. Risk Ranking (Likelihood and Impact)
1. **High Risk — Unencrypted File Transfers (Likelihood: High | Impact: High)**
   - *Reasoning:* Transferring files unencrypted over inter-campus links makes data capture trivial via sniffing tools.
2. **Medium-High Risk — Guest Network Access to Records Server (Likelihood: Medium | Impact: High)**
   - *Reasoning:* Anyone connected to the guest Wi-Fi can directly reach server ports if network segmentation is absent.
3. **Medium Risk — Weak Staff Passwords & Outdated Software (Likelihood: High | Impact: Medium)**
   - *Reasoning:* Password guessing or unpatched software exploits allow unauthorized access, but require targeted effort.

## 3. Recommended Controls
1. **Control 1 (For File Transfers):** Implement end-to-end encryption using SSH/SFTP or TLS for file transfers.
2. **Control 2 (For Server Access):** Enforce Network Segmentation (VLANs) and firewall filtering rules blocking guest subnets from internal management servers.
3. **Control 3 (For Weak Credentials/Software):** Implement strong Password Policies (MFA), along with automated patch management schedules.
