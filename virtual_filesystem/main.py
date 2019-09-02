#!/usr/bin/env python3

# BASED ON CODE FOUND ON https://www.thepythoncorner.com/2017/02/writing-a-fuse-filesystem-in-python/?source=post_page-----5e0f2de3a813----------------------&doing_wp_cron=1566331932.0391271114349365234375

# Depends on fusepy
# install it with "pip3 install fusepy"

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations


import sqlite3
from settings import Settings
import datetime
import time


import threading



class DataSource:
    def __init__(self):
        self.settings = Settings()
        self.connection = sqlite3.connect(self.settings.loaded['database'], detect_types=sqlite3.PARSE_DECLTYPES)

    def is_database_ready():
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        return False if cursor.fetchone() == None else True

    # Retorna todos os eventos ocorridos
    def get_events(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT start_time, end_time, summary FROM events")
        return cursor.fetchall()

    def get_localizations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT idlocalizations, latitude, longitude FROM localizations")
        return_data = cursor.fetchall()
        return return_data

    def close(self):
        if self.connection != None:
            self.connection.close()


class VirtualFileSystem(Operations):
    def __init__(self):
        # TODO: Alterar coisas aqui (database_path antes era 'root')
        self.data_source = DataSource()
        # self.root = self.data_source.settings.loaded['database']

        # Tests
        self.root = "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/virtual_filesystem/mountpoint/"

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def get_mount_point(self):
        return self.data_source.settings.loaded['mountpoint']

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        print("Operação : ACCESS on ", full_path) # FUNCAO COMPLETA
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        print("\n----------------------------")
        full_path = self._full_path(path)
        st = None

        if full_path == self.root:
            print("Buscando arquivos da root")
            # st = os.lstat(full_path)
            st = os.stat_result((
                16877, # Modo (permissoes)
                3672400, # The inode number
                2053, # st_dev (identificador do dispositivo /dev/*)
                3, # st_nlink (number of hard links)
                1000, # st_uid (user ID do dono do arquivo)
                1000, # st_gid (group ID do dono do arquivo)
                4096, # st_size (tamanho do arquivo em Bytes)
                1566354491, # st_atime (timestamp do acesso mais recente)
                1566354473, # st_mtime (timestamp da modificação mais recente)
                1566354473 # st_ctime (timestamp da modificação de metadados mais recente)
                ))
        else:
            # print("Operação : GETATTR on ", full_path)
            st = os.lstat(full_path)

        # print("ST == ", st)

        data = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

        print("DATA == ", data)

        return data

    # Busca o que tem dentro de um diretório (retorna nomes com o yield)
    def readdir(self, path, fh):
        print("\n----- READDIR -----")
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))

        print("dirents == ", dirents)

        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in (
            'f_bavail',
            'f_bfree',
            'f_blocks',
            'f_bsize',
            'f_favail',
            'f_ffree',
            'f_files',
            'f_flag',
            'f_frsize',
            'f_namemax'
        ))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        data = os.open(full_path, flags)
        return data

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print("Operação : READ")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


# def main(mountpoint, database_path):
def main():
    vfs = VirtualFileSystem()
    FUSE(vfs, vfs.get_mount_point(), nothreads=True, foreground=True)

if __name__ == '__main__':
    # mountpoint = sys.argv[2]
    # database_path = sys.argv[1]
    # main(mountpoint, database_path)
    main()





