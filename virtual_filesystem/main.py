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
from data_source import DataSource
import datetime
import time
import localization

import threading

class VirtualFileSystem(Operations):
    def __init__(self):
        self.data_source = DataSource()
        if self.data_source.settings.loaded['use_localization']:
            localization.start_plugin(self.data_source)

        self.root = "/home/joaovitor/Documentos/UFG-CDC/PFC/PFC2/Sistema/virtual_filesystem/mountpoint/"

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        return os.path.join(self.root, partial)
        # return partial

    def get_mount_point(self):
        return self.data_source.settings.loaded['mountpoint']

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        print(f"\n-- ACCESS   path = {path}") # FUNCAO COMPLETA

        # if full_path == self.root:
        #     if not os.access(full_path, mode):
        #         raise FuseOSError(errno.EACCES)
        # if path == '/actual_context':
        if path == '/actual_context':
            return
        elif path[16:] in self.data_source.map:
            if not os.access(self.data_source.map[path[16:]], mode):
                raise FuseOSError(errno.EACCES)
        elif not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.chmod(full_path, mode)
        elif path[16:] in self.data_source.map:
            return os.chmod(self.data_source.map[path[16:]], mode)
        else:
            return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.chown(full_path, uid, gid)
        elif path[16:] in self.data_source.map:
            return os.chown(self.data_source.map[path[16:]], uid, gid)
        else:
            return os.chown(full_path, uid, gid)


    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = None
        virtual_file_or_dir = False

        if path in ['/', '/actual_context']: # Correct
            virtual_file_or_dir = True
            st = os.stat_result((
                16877, # Modo (permissoes)
                None, # The inode number
                2023, # st_dev (identificador do dispositivo /dev/*)
                3, # st_nlink (number of hard links)
                os.geteuid(), # st_uid (user ID do dono do arquivo)
                os.getegid(), # st_gid (group ID do dono do arquivo)
                4096, # st_size (tamanho do arquivo em Bytes)
                1566354491, # st_atime (timestamp do acesso mais recente)
                1566354473, # st_mtime (timestamp da modificação mais recente)
                1566354473 # st_ctime (timestamp da modificação de metadados mais recente)
            ))

        else:
            # if path[16:] in self.data_source.map:
            if len(path) >= 16: # "/actual_context/file_name"  ->  "file_name"
                if path[16:] in self.data_source.map:
                    st = os.lstat(self.data_source.map[path[16:]])
                else:
                    st = os.lstat(full_path)
            else:
                st = os.lstat(full_path)

        data = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        # print(f"-- GETATTR   path = {path}, full_path={full_path}, data = {data}")
        print(f"-- GETATTR   path = {path}, full_path={full_path}")
        return data

    # Busca o que tem dentro de um diretório (retorna nomes com o yield)
    def readdir(self, path, fh):
        full_path = self._full_path(path)
        dirents = ['.', '..']

        if(full_path == self.root):
            dirents.append('actual_context')
        elif(full_path == (self.root + 'actual_context')):
            database_return = self.data_source.get_files()
            self.data_source.update_file_map(database_return)

            for relative_path in self.data_source.map:
                # print("Arquivos = ", path)
                dirents.append(relative_path)

        # if os.path.isdir(full_path):
        #     dirents.extend(os.listdir(full_path))

        print(f"-- READDIR   path = {path}, Dirents = {dirents}")
        for dirent in dirents:
            yield dirent

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.mknod(full_path, mode, dev)
        elif path[16:] in self.data_source.map:
            return os.mknod(self.data_source.map[path[16:]], mode, dev)
        else:
            return os.mknod(full_path, mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.rmdir(full_path)
        elif path[16:] in self.data_source.map:
            return os.rmdir(self.data_source.map[path[16:]])
        else:
            return os.rmdir(full_path)

    def mkdir(self, path, mode):
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.mkdir(full_path, mode)
        elif path[16:] in self.data_source.map:
            return os.mkdir(self.data_source.map[path[16:]], mode)
        else:
            return os.mkdir(full_path, mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        print(f"-- STATFS   path = {path}")
        stv = None

        if full_path == self.root:
            stv = os.statvfs(full_path)
        elif path[16:] in self.data_source.map:
            stv = os.statvfs(self.data_source.map[path[16:]])
        else:
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
        full_path = self._full_path(path)

        if full_path == self.root:
            return os.unlink(full_path)
        elif path[16:] in self.data_source.map:
            return os.unlink(self.data_source.map[path[16:]])
        else:
            return os.unlink(full_path)


    def symlink(self, name, target):
        full_path = self._full_path(target)

        if full_path == self.root:
            return os.symlink(name, full_path)
        elif path[16:] in self.data_source.map:
            return os.symlink(name, self.data_source.map[path[16:]])
        else:
            return os.symlink(name, full_path)

    def rename(self, old, new):
        full_path = self._full_path(old)

        if full_path == self.root:
            return os.rename(full_path, full_path)
        elif path[16:] in self.data_source.map:
            return os.rename(self.data_source.map[path[16:]], self.data_source.map[path[16:]])
        else:
            return os.rename(full_path, full_path)

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        data = None

        if full_path == self.root:
            print(f"-- OPEN   IN ROOT")
            data = os.open(full_path, flags)
        elif path[16:] in self.data_source.map:
            print(f"-- OPEN   FOUND KEY")
            data = os.open(self.data_source.map[path[16:]], flags)
        else:
            print(f"-- OPEN   OTHER")
            data = os.open(full_path, flags)

        print(f"-- OPEN  path: {path}, data = {data}")
        return data

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        data = None

        if full_path == self.root:
            data = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        elif path[16:] in self.data_source.map:
            data = os.open(self.data_source.map[path[16:]], os.O_WRONLY | os.O_CREAT, mode)
        else:
            data = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

        return data

    def read(self, path, length, offset, fh):
        print(f"-- READ   path = {path}")
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


def main():
    vfs = VirtualFileSystem()
    FUSE(vfs, vfs.get_mount_point(), nothreads=True, foreground=True)

if __name__ == '__main__':
    main()





