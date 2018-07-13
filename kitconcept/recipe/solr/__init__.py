# -*- coding: utf-8 -*-
import distutils
import os
import subprocess
from hexagonit.recipe.download import Recipe as DownloadRecipe

import zc.recipe.egg
from zc.buildout import UserError


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options)

        # Check required options
        required_options = [
            'src',
        ]
        for required_option in required_options:
            if required_option not in self.options:
                raise UserError(
                    'Please provide a "%s" in your Solr section "%s"' % (
                        required_option,
                        self.options['recipe']
                    )
                )

        # Set default options
        self.options.setdefault('port', '8983')
        self.options.setdefault('solr-core-name', 'plone')
        self.options['solr-config'] = os.path.join(
            self.buildout['buildout']['directory'],
            self.options['solr-config']
        )

        # Figure out default output file
        parts_directory = os.path.join(
            self.buildout['buildout']['parts-directory'],
            __name__
        )
        if not os.path.exists(parts_directory):
            os.makedirs(parts_directory)

        # What files are tracked by this recipe
        self.files = [
            parts_directory,
            os.path.join(
                self.buildout['buildout']['bin-directory'],
                self.name
            )
        ]

    @property
    def src(self):
        return str(self.options['src'])

    @property
    def solr_config(self):
        return str(self.options['solr-config'])

    def download_solr(self):
        directory = os.path.join(
            self.buildout['buildout']['parts-directory'],
            self.name
        )
        DownloadRecipe(self.buildout, self.name, {
            'url': self.src,
            'strip-top-level-dir': 'true',
            'destination': directory,
            'ignore-existing': 'true',
        }).install()

    def create_solr_core(self):
        print("Create Solr core")
        solr_core_name = 'plone'
        solr_cores_directory = os.path.join(
            self.buildout['buildout']['parts-directory'],
            'solr/server/solr',
            solr_core_name
        )
        print("rm {}".format(solr_cores_directory))
        try:
            distutils.dir_util.remove_tree(solr_cores_directory)
        except OSError:
            pass
        print("copy {}".format(
            os.path.join(self.buildout['buildout']
                         ['directory'], self.solr_config)))
        distutils.dir_util.copy_tree(
            os.path.join(self.buildout['buildout']
                         ['directory'], self.solr_config),
            solr_cores_directory
        )

    def install(self):
        self.install_scripts()
        self.download_solr()
        self.create_solr_core()

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return self.files

    def update(self):
        self.install()

    def install_scripts(self):
        """Install Solr scripts in the bin directory.
        """
        zc.buildout.easy_install.scripts(
            [(
                'solr',
                'kitconcept.recipe.solr',
                'solr'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

        zc.buildout.easy_install.scripts(
            [(
                'solr-start',
                'kitconcept.recipe.solr',
                'solr_start'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

        zc.buildout.easy_install.scripts(
            [(
                'solr-restart',
                'kitconcept.recipe.solr',
                'solr_restart'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

        zc.buildout.easy_install.scripts(
            [(
                'solr-foreground',
                'kitconcept.recipe.solr',
                'solr_foreground'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

        zc.buildout.easy_install.scripts(
            [(
                'solr-stop',
                'kitconcept.recipe.solr',
                'solr_stop'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

        zc.buildout.easy_install.scripts(
            [(
                'solr-status',
                'kitconcept.recipe.solr',
                'solr_status'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )


def solr(options):
    subprocess.call(
        ['./solr'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )


def solr_start(options):
    subprocess.call(
        ['./solr', 'start'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )


def solr_foreground(options):
    subprocess.call(
        ['./solr', 'start', '-f'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )


def solr_restart(options):
    subprocess.call(
        ['./solr', 'restart'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )


def solr_stop(options):
    subprocess.call(
        ['./solr', 'stop'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )


def solr_status(options):
    subprocess.call(
        ['./solr', 'status'],
        cwd=options.get('bin-directory') + '/../parts/solr/bin/'
    )
