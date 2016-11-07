# -*- coding: utf-8 -*-
import os
import tempfile
from unittest import TestCase

import shutil


class MockTreeNode(TestCase):
    tree = [
        'dir01', 'dir02', 'dir03',
        'dir01/subdir01', 'dir02/subdir01', 'dir02/subdir02', 'dir02/subdir03',
        'dir01/subdir01/subsubdir01', 'dir01/subdir01/subsubdir02',
        'dir01/subdir01/subsubdir01/subsubsubdir01',
    ]
    files_by_dir = 6

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.create_dirty_files()
        self.create_tree()

    def create_tree(self):
        for d in self.tree:
            self.create_dirty_files(d)

    def create_dirty_files(self, node=''):
        def prefix_lvl(name):
            if not node:
                return name
            return 'lvl%02d_%s' % (len(node.split('/')), name)
        def join_node(name, prefix=True):
            if prefix:
                name = prefix_lvl(name)
            if not node:
                return name
            return os.path.join(node, name)
        self.create_directory(node)
        self.create_file(join_node('empty_file.txt'))
        self.create_file(join_node('empty_file_without_ext'))
        self.create_file(join_node('.hidden_file.txt'))
        self.create_file(join_node('file_01.spam'), 'Spam ' * 256)
        self.create_file(join_node('file_02.eggs'), 'Eggs ' * 512)
        self.create_file(join_node('file_03.spam'), 'Eggs ' * 128)
        self.create_directory(join_node('empty_dir'))
        self.create_directory(join_node('.hidden_empty_dir', False))

    def create_directory(self, name):
        d = os.path.join(self.directory, name)
        if os.path.exists(d):
            return
        os.makedirs(d)

    def create_file(self, name, data=''):
        with open(os.path.join(self.directory, name), 'w') as f:
            f.write(data)

    def list_dir(self, path='', full_path=False):
        path = os.path.join(self.directory, path)
        if full_path:
            return [os.path.join(self.directory, name) for name in os.listdir(path)]
        return os.listdir(path)

    def deep_list_dir(self, path=''):
        path = os.path.join(self.directory, path)
        nodes = set()
        for dirpath, dirnames, filenames in os.walk(path):
            for node in dirnames + filenames:
                nodes.add(os.path.join(dirpath, node))
        return nodes

    def tearDown(self):
        shutil.rmtree(self.directory)
