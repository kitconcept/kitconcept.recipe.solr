# -*- coding: utf-8 -*-
import os
from shutil import copyfile

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
                    self.options['recipe']))

        # Set default options
        self.options.setdefault('port', '8983')
        self.options.setdefault('config', 'solr_config.xml')
        # self.options['config'] = os.path.join(
        #   self.buildout['buildout']['directory'],
        #   self.options['jobconfig'])

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

    def download_solr(self):
        print("Download Solr")

    def build_solr(self):
        print("Build Solr")

    def install(self):
        self.download_solr()
        self.build_solr()

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
