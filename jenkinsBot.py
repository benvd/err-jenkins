from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd

from jenkins import Jenkins
from config import JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD


class JenkinsBot(BotPlugin):

    def __init__(self):
        self.jenkins = Jenkins(JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD)

    @botcmd
    def jenkins_list(self, mess, args):
        """List all jobs, optionally filter them using a search term."""
        self.send(mess.getFrom(), u'/me is getting the list of jobs from Jenkins... ', message_type=mess.getType())

        search_term = args.strip().lower()
        jobs = [job for job in self.jenkins.get_jobs() if search_term.lower() in job['name'].lower()]

        return self.format_jobs(jobs)

    @botcmd
    def jenkins_running(self, mess, args):
        """List all running jobs."""
        self.send(mess.getFrom(), u'/me is getting the list of jobs from Jenkins... ', message_type=mess.getType())

        jobs = [job for job in self.jenkins.get_jobs() if 'anime' in job['color']]

        return self.format_running_jobs(jobs)

    def format_jobs(self, jobs):
        if len(jobs) == 0:
            return u'No jobs found.'

        max_length = max([len(job['name']) for job in jobs])
        return '\n'.join(['%s (%s)' % (job['name'].ljust(max_length), job['url']) for job in jobs]).strip()

    def format_running_jobs(self, jobs):
        jobs_info = [self.jenkins.get_job_info(job['name']) for job in jobs]
        return '\n\n'.join(['%s (%s)\n%s' % (job['name'], job['lastBuild']['url'], job['healthReport'][0]['description']) for job in jobs_info]).strip()
