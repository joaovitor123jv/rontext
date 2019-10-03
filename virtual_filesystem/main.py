#!/usr/bin/env python3

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

        self.root = os.environ['HOME'] + "/Documentos/UFG-CDC/PFC/PFC2/Sistema/virtual_filesystem/mountpoint/"

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        return os.path.join(self.root, partial)

    def get_mount_point(self):
        return self.data_source.settings.loaded['mountpoint']

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        if path == '/actual_context':
            return
        elif len(path) > 16:
            if path[16:] in self.data_source.map:
                if not os.access(self.data_source.map[path[16:]], mode):
                    raise FuseOSError(errno.EACCES)
                return
        if not os.access(self._full_path(path), mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.chmod(self.data_source.map[path[16:]], mode)
        return os.chmod(self._full_path(path), mode)

    def chown(self, path, uid, gid):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.chown(self.data_source.map[path[16:]], uid, gid)
        return os.chown(self._full_path(path), uid, gid)


    def getattr(self, path, fh=None):
        st = None
        virtual_file_or_dir = False
        full_path = self._full_path(path)

        if path in ['/', '/actual_context']: # Correct
            virtual_file_or_dir = True
            st = os.stat_result((
                16877, # Mode (permissions)
                None, # The inode number
                2023, # st_dev (device identifier /dev/*)
                3, # st_nlink (number of hard links)
                os.geteuid(), # st_uid (user ID of the file owner, always the current user)
                os.getegid(), # st_gid (group ID of the file owner, always the related to current user)
                4096, # st_size (file size in Bytes)
                1566354491, # st_atime (last access timestamp)
                1566354473, # st_mtime (last modified timestamp)
                1566354473 # st_ctime (last metadata change timestamp)
            ))
        else:
            if len(path) >= 16: # "/actual_context/file_name"  ->  "file_name"
                if path[16:] in self.data_source.map:
                    st = os.lstat(self.data_source.map[path[16:]])
                else:
                    st = os.lstat(full_path)
            else:
                st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    # Tells FUSE what is inside the requested directory (return file names on yield)
    def readdir(self, path, fh):
        full_path = self._full_path(path)
        dirents = ['.', '..']

        if(full_path == self.root):
            dirents.append('actual_context')
        elif(full_path == (self.root + 'actual_context')):
            database_return = self.data_source.get_files()
            self.data_source.update_file_map(database_return)
            for relative_path in self.data_source.map:
                dirents.append(relative_path)
        for dirent in dirents:
            yield dirent

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"): # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.mknod(self.data_source.map[path[16:]], mode, dev)
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.rmdir(self.data_source.map[path[16:]])
        return os.rmdir(self._full_path(path))

    def mkdir(self, path, mode):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.mkdir(self.data_source.map[path[16:]], mode)
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        stv = None
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                stv = os.statvfs(self.data_source.map[path[16:]])
        if stv == None:
            stv = os.statvfs(self._full_path(path))

        return dict((key, getattr(stv, key)) for key in (
            'f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail',
            'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'
        ))

    def unlink(self, path):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.unlink(self.data_source.map[path[16:]])
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.symlink(name, self.data_source.map[path[16:]])
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.rename(self.data_source.map[path[16:]], self.data_source.map[path[16:]])
        full_path = self._full_path(old)
        return os.rename(full_path, full_path)

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.open(self.data_source.map[path[16:]], flags)
        return os.open(self._full_path(path), flags)

    def create(self, path, mode, fi=None):
        if len(path) > 16:
            if path[16:] in self.data_source.map:
                return os.open(self.data_source.map[path[16:]], os.O_WRONLY | os.O_CREAT, mode)
        return os.open(self._full_path(path), os.O_WRONLY | os.O_CREAT, mode)


    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        with open(self._full_path(path), 'r+') as f:
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





