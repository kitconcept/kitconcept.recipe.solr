# -*- coding: utf-8 -*-
import distutils
import os
import urllib2
from hexagonit.recipe.download import Recipe as DownloadRecipe
from shutil import copyfile

import zc.recipe.egg
from zc.buildout import UserError


DEFAULT_DOWNLOAD_URLS = {
    7: 'http://archive.apache.org/dist/lucene/solr/7.2.1/solr-7.2.1.tgz',
    6: 'http://archive.apache.org/dist/lucene/solr/7.2.1/solr-6.6.3.tgz',
    5: 'http://archive.apache.org/dist/lucene/solr/5.1.0/solr-5.1.0.tgz',
    4: 'http://archive.apache.org/dist/lucene/solr/4.10.4/solr-4.10.4.tgz',
}


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options)

        # Check required options
        required_options = [
            'solr-version',
        ]
        for required_option in required_options:
            if required_option not in self.options:
                raise UserError(
                    'Please provide a "%s" in your Solr section "%s"' % (
                    required_option,
                    self.options['recipe']))

        # Set default options
        self.options.setdefault('port', '8983')
        self.options['config'] = os.path.join(
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
        self.files = [parts_directory,
            os.path.join(
                self.buildout['buildout']['bin-directory'],
                self.name
            )
        ]

    @property
    def solr_version(self):
        return int(self.options['solr-version'])

    @property
    def solr_config(self):
        return int(self.options['solr-config'])

    def download_solr(self):
        directory = os.path.join(
            self.buildout['buildout']['parts-directory'],
            self.name
        )

        if not os.path.exists(directory):
            DownloadRecipe(self.buildout, self.name, {
                'url': DEFAULT_DOWNLOAD_URLS[self.solr_version],
                'strip-top-level-dir': 'true',
                'destination': directory,
            }).install()

    def build_solr(self):
        print("Build Solr")

    def create_solr_core(self):
        print("Create Solr core")
        solr_core_name = 'woo'
        solr_cores_directory = os.path.join(
            self.buildout['buildout']['parts-directory'],
            'solr/server/solr',
            solr_core_name
        )
        distutils.dir_util.copy_tree(os.path.join('config'), solr_cores_directory)

    def install(self):
        self.download_solr()
        self.build_solr()
        self.create_solr_core()

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return self.files

    def update(self):
        self.install()



def _write_configuration(config, filename):
    # Backup existing config if it exists
    if os.path.exists(filename):
        print("Create Jenkins job backup at %s.bak" % filename)
        copyfile(filename, "%s.bak" % filename)
    # Write config to file
    print("Write job %s" % filename)
    fileObj = open(filename, "w")
    fileObj.write(config)
    fileObj.close()


def trigger_build_jenkins(options):
    """Trigger a build for a job on Jenkins CI server.
    """
    jenkins_server = _connect(options)
    jenkins_jobname = options['jobname']
    if jenkins_server.job_exists(jenkins_jobname):
        print(
            "Build Jenkins job %s" %
            jenkins_server.get_job_info(jenkins_jobname)['url'])
        try:
            jenkins_server.build_job(jenkins_jobname)
        except jenkins.JenkinsException, e:
            print e
