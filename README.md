# banking_system
desktop banking application using CustomTkinter for a modern GUI, with a dark/light mode toggle. Built around object-oriented principles, it features a BankingSystem class managing multiple Account objects, each tracking name, account number, balance, and transaction history (deposits, withdrawals, openings).
The app's interface is divided into tabs (With Out Database Statical )

**Create**: Users input name, account number, and initial balance (₹) to add accounts, with validation for duplicates and negative balances.

**Deposit/Withdraw**: Select from dropdowns populated dynamically with existing accounts; enter amounts with error handling for invalid inputs.
Post-transaction, low balance alerts trigger below ₹50.

**Check/History**: Displays current balance and full transaction log (timestamp, type, amount, balance). 
Supports exporting history to CSV/TXT via file dialog.

**Search/Delete**: Filter accounts by substring in account number, showing matches with details; delete selected accounts after confirmation.

**Core functionality includes:**

**Account Management**: Create, deposit, withdraw, check balance, delete. History logs every action with datetime stamps.

**UI Elements**: Frames, labels, entries, buttons, option menus, textboxes for logs and history. 
A bottom log pane records all operations; clear button resets it.

**Features**: Dynamic menu updates on account changes, error labels for feedback, messageboxes for results/warnings. Side panel for info (expandable for future use).

**Data Handling**: In-memory storage (dict of accounts); no persistence across sessions, but exportable histories.

