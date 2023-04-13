from pseudo_cron.decorators import schedule_job

from auth0_sso import roles


@schedule_job(24 * 60 * 60)
def sync_roles():
    roles.sync_roles()
