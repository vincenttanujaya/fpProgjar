import sys
import os
import glob
import json
import uuid
from Queue import *


class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.group = {}
        self.users['vincent'] = {'nama': 'Vincent Marcello Dwi Tanujaya', 'negara': 'Indonesia',
                                 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.users['diana'] = {'nama': 'Diana Hudani Kisyono', 'negara': 'Indonesia',
                               'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.users['hatta'] = {'nama': 'M. Hattami', 'negara': 'Indonesia',
                               'password': 'surabaya', 'incoming': {}, 'outgoing': {}}

    def proses(self, data, connection):
        j = data.split(" ")
        try:
            command = j[0].strip()
            print command
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                print "auth {}" . format(username)
                return self.autentikasi_user(username, password)
            elif (command == 'send'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                print "send message from {} to {}" . format(
                    usernamefrom, usernameto)
                return self.send_message(sessionid, usernamefrom, usernameto, message)
            elif (command == 'inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                print "inbox {}" . format(sessionid)
                return self.get_inbox(username)
            elif (command == 'create_group'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                return self.creategroup(sessionid, groupname)
            elif (command == 'list_group'):
                sessionid = j[1].strip()
                print "List Group {}" . format(sessionid)
                return self.list_group()
            elif (command == 'join_group'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                print "List Group {}" . format(sessionid)
                return self.join_group(sessionid, groupname)
            elif (command == 'logout'):
                sessionid = j[1].strip()
                print "Logout Attempt {}" . format(sessionid)
                return self.logout(sessionid)
            elif (command == 'send_group'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                print "send message from {} to {}" . format(
                    usernamefrom, groupname)
                return self.send_group(sessionid, usernamefrom, groupname, message)
            elif (command == 'send_file'):
                sessionid = j[1]
                usernameto = j[2]
                filename = j[3]
                usernamefrom = self.sessions[sessionid]['username']
                print "send_file from {} to {}" . format(
                    usernamefrom, usernameto)
                return self.send_file(sessionid, usernamefrom, usernameto, filename, connection)
            elif (command == 'download_file'):
                sessionid = j[1]
                filename = j[2]
                usernamefrom = self.sessions[sessionid]['username']
                print "{} download_file {}" . format(usernamefrom, filename)
                return self.download_file(sessionid, filename, connection)
            elif (command == 'list_file'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                print "list_file {}" . format(sessionid)
                return self.list_file(username)
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if (username not in self.users):
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}
        if (self.users[username]['password'] != password):
            return {'status': 'ERROR', 'message': 'Password Salah'}
        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {
            'username': username, 'userdetail': self.users[username]}
        return {'status': 'OK', 'tokenid': tokenid}

    def get_user(self, username):
        if (username not in self.users):
            return False
        return self.users[username]

    def get_user_group(self, username):
        if (username not in self.users):
            return False
        return self.users[username]

    def send_message(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = {'msg_from': s_fr['nama'],
                   'msg_to': s_to['nama'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_from].put(message)
        except KeyError:
            outqueue_sender[username_from] = Queue()
            outqueue_sender[username_from].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def send_group(self, sessionid, username_from, groupname, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        g_to = self.group[groupname]

        outqueue_sender = s_fr['outgoing']
        try:
            outqueue_sender[groupname].put(message)
        except KeyError:
            outqueue_sender[groupname] = Queue()
            outqueue_sender[groupname].put(message)
        for username_dest in g_to['users']:
            if username_dest != username_from:
                print username_dest
                s_to = self.get_user(username_dest)

                if (s_fr == False or s_to == False):
                    return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

                message = {'msg_from': s_fr['nama'],
                           'msg_to': groupname, 'msg': message}
                inqueue_receiver = s_to['incoming']
                try:
                    inqueue_receiver[groupname].put(message)
                except KeyError:
                    inqueue_receiver[groupname] = Queue()
                    inqueue_receiver[groupname].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}

    def creategroup(self, sessionid, groupname):
        if (groupname in self.group):
            return {'status': 'ERROR', 'messages': 'Grup Sudah Ada Bro!'}
        else:
            creator = self.sessions[sessionid]['username']
            self.group[groupname] = {'creator': creator, 'users': []}
            self.group[groupname]['users'].append(creator)
            return {'status': 'OK', 'messages': 'Yeay! Berhasil membuat grup'}

    def list_group(self):
        return {'status': 'OK', 'messages': self.group}

    def join_group(self, sessionid, groupname):
        user = self.sessions[sessionid]['username']
        if (groupname not in self.group):
            return {'status': 'ERROR', 'message': 'Grup gaada!'}
        elif (user in self.group[groupname]['users']):
            return {'status': 'ERROR', 'message': 'Kamu sudah join grup ya!'}
        else:
            self.group[groupname]['users'].append(user)
            return {'status': 'OK', 'messages': 'Selamat! Berhasil join group'}

    def logout(self, sessionid):
        self.sessions.pop(sessionid)
        return {'status': 'OK', 'messages': 'Logout Success'}

    def send_file(self, sessionid, username_from, username_dest, filename, connection):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        try:
            if not os.path.exists('file_'+username_dest):
                os.makedirs('file_'+username_dest)
                print "dir created"
            with open(os.path.join('file_'+username_dest, filename), 'wb') as file:
                while True:
                    data = connection.recv(1024)
                    print data
                    if(data[-4:] == 'DONE'):
                        data = data[:-4]
                        file.write(data)
                        break
                    file.write(data)
                file.close()
        except IOError:
            raise

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'],
                   'msg': 'sent/received {}' . format(filename)}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_from].put(message)
        except KeyError:
            outqueue_sender[username_from] = Queue()
            outqueue_sender[username_from].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)

        return {'status': 'OK', 'message': 'File sent'}

    def download_file(self, sessionid, filename, connection):
        username = self.sessions[sessionid]['username']
        print username
        print "{} download {}" . format(username, filename)

        result = connection.sendall("OK")
        while True:
            data = file.read(1024)
            if not data:
                result = connection.sendall("DONE")
                break
            connection.sendall(data)
        file.close()
        return {'status': 'OK', 'message': 'File download'}

    def list_file(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = []
        msgs.extend(glob.glob('file_'+username+'/*'))
        print msgs
        # msgs = {}
        # for users in incoming:
        #     msgs[users] = []
        #     while not incoming[users].empty():
        #         msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}


if __name__ == "__main__":
    # j = Chat()
    # sesi = j.proses("auth messi surabaya")
    # print sesi
    # # sesi = j.autentikasi_user('messi','surabaya')
    # # print sesi
    # tokenid = sesi['tokenid']
    # print j.proses(
    #     "send {} henderson hello gimana kabarnya son " . format(tokenid))
    # # print j.send_message(tokenid,'messi','henderson','hello son')
    # # print j.send_message(tokenid,'henderson','messi','hello si')
    # # print j.send_message(tokenid,'lineker','messi','hello si dari lineker')

    print 'halo'
