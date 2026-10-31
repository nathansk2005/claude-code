# iPhone security checklist

A configuration profile can't turn on everything. Install
[`iphone-max-security.mobileconfig`](./iphone-max-security.mobileconfig) first, then work through this list.
Setting names follow current iOS and may move slightly in newer versions.

## 1. Install the profile first

1. Back up your iPhone. The profile erases it after 10 wrong passcode attempts.
2. Open the profile on your iPhone (AirDrop it, or open it from Files).
3. Go to **Settings → Profile Downloaded → Install**.
4. Set the new passcode when asked: at least 6 characters.

Install it before step 3 below: Lockdown Mode blocks installing profiles.

## 2. Apple Account

- **Settings → [your name] → Sign-In & Security**
  - Make sure two-factor authentication is on.
  - **Security Keys**: add two hardware security keys (FIDO, such as YubiKey). Without one of them, nobody can sign in to your Apple Account, including someone who phishes your password and code.
  - **Account Recovery**: add a recovery contact you trust.
- **Settings → [your name] → iCloud → Advanced Data Protection**: on. This end-to-end encrypts almost all of your iCloud data, including backups and Photos.
- **Settings → [your name] → iCloud → Private Relay**: on.
- **Settings → [your name] → Contact Key Verification**: on.

## 3. Device

- **Settings → Privacy & Security → Lockdown Mode**: on. This is Apple's strongest protection against targeted spyware. It turns off some features, such as most message attachments, link previews and some web technologies. You can exclude apps or websites you trust.
- **Settings → Face ID & Passcode → Stolen Device Protection**: on, set to **Always**.
- **Settings → Face ID & Passcode → Allow Access When Locked**: turn everything off, including **Accessories**.
- **Settings → General → Software Update → Automatic Updates**: turn everything on, including security responses.
- **Settings → General → VPN & Device Management**: remove any profile you don't recognize.

## 4. Network

- **Settings → Wi‑Fi**: set **Ask to Join Networks** to **Off** and **Auto-Join Hotspot** to **Never**.
- For each saved Wi‑Fi network, tap **ⓘ** and set **Private Wi‑Fi Address** to **Rotating**. Forget networks you no longer use, especially public ones.
- **Settings → General → AirDrop**: **Receiving Off**, or **Contacts Only**.
- **Settings → Cellular → SIM PIN**: turn on and change it from your carrier's default. Three wrong tries locks the SIM, so write it down somewhere safe.
- In your carrier's app or website, turn on the **number lock / port-out PIN**. This stops SIM-swap attacks that steal your phone number.

## 5. Apps and browsing

- **Settings → Apps → Safari → Advanced → Advanced Tracking and Fingerprinting Protection**: **All Browsing**.
- **Settings → Apps → Safari → Block All Cookies**: on. This is the strictest cookie setting, and some sites may ask you to sign in again.
- **Settings → Apps → Mail → Privacy Protection → Protect Mail Activity**: on.
- **Settings → Apps → Messages**: screen or filter unknown senders.
- **Settings → Apps → Phone**: screen or silence unknown callers.
- **Settings → Privacy & Security → Tracking**: **Allow Apps to Request to Track** off.
- **Passwords app → Security**: fix every weak, reused or leaked password, and switch to passkeys where sites offer them.

## 6. Check regularly

- **Settings → Privacy & Security → Safety Check**: run **Manage Sharing & Access** and review which people, apps and devices have access.
- **Settings → [your name]**: scroll to the device list and remove anything that isn't yours.
- **Settings → [your name] → Find My**: **Find My iPhone**, **Find My network** and **Send Last Location** on.

## What the profile does

| Part | What it does |
|---|---|
| Encrypted DNS | Every website lookup goes to Quad9 over HTTPS. Quad9 blocks known malware, phishing and scam sites, and your network can't see or change your lookups. A VPN, while on, uses its own DNS instead. |
| Passcode | 6+ characters, letters or numbers; locks after 1 minute; asks for the passcode as soon as the screen locks; erases the iPhone after 10 wrong attempts. |
| Lock screen | No Control Center (stops thieves switching on Airplane Mode to hide from Find My), no notifications or widgets (hides sign-in codes), no Siri, voice dialing or Wallet. |
| Web | Blocks all Safari cookies, rejects untrusted HTTPS certificates without asking, forces Safari's fraudulent website warning, and requires trusted TLS for AirPrint. Some sites that need cookies to sign you in may not work. |
| Apps and privacy | Blocks trusting apps from enterprise developer certificates (a common way to sideload malware), stops ad tracking requests and diagnostics, and forces encrypted backups. |

The profile only uses settings that work on a personal iPhone. You can remove it at any time in **Settings → General → VPN & Device Management**. Locking the profile or the DNS setting in place needs a supervised iPhone (set up again with Apple Configurator, which erases the phone), and iOS refuses to install a profile that asks for that on any other iPhone.

The profile isn't signed, so iOS shows it as **Unverified** when you install it. That is expected.
