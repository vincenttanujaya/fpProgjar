### Task
* Log Out
* Group Messaging
* Send/Receive Image/File

### Protokol
- Log In 
  - Melakukan Login sebagai user
  - command: auth [username] [password]
- Log Out
  - Keluar dari session
  - command: logout
- Send Message
  - Mengirimkan pesan ke user lain
  - command: send [username] [message]
- Inbox
  - Mengecek kotak surat yang belum dibaca
  - command: inbox
- Create Group Chat
  - Membuat grup chat
  - command: create_group [groupname]
- List Group
  - Melihat daftar grup yang ada
  - command: list_group
- Join Group
  - Bergabung bersama grup yang ada
  - command: join_group [groupname]
- Send Group
  - Mengirimkan pesan ke grup
  - command: send_group [groupname] [message]
- Send File
  - Mengirimkan file ke user lain
  - command: send_file [username] [filename]
- Download File
  - Mengunduh file yang dikirim orang lain
  - command: download_file [filename]
- List File
  - Melihat semua file yang dikirim dari user lain
  - command: list_file
