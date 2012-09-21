from fabric.api import *
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm

@task
def schema_diff():
    """
    generate diff file of PostgreSQL schema using apgdiff
    fab schema_diff
    """
    # gather connect info
    old_host = prompt('old host ip?', validate=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    old_db = prompt('old dbname?', validate=r'^[\w-]+')
    new_host = prompt('new host ip?',validate=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    new_db = prompt('new dbname?', validate=r'^[\w-]+')

    if confirm("Do you want to get diff of\n\
        [OLD DB]: %(old_host)s %(old_db)s \n        [NEW DB] %(new_host)s %(new_db)s" % \
        {"old_host":old_host, "old_db":old_db, "new_host":new_host, "new_db":new_db}):
        with settings(warn_only=True):
            print green("dumping old db schema. This might take a while...")
            result = local('pg_dump -v --host %(old_host)s --port 5432 -U \"llxDBA\" -s -f ~/old.sql %(old_db)s' % {"old_host":old_host, "old_db":old_db})
            print green("now dumping new db schema. This might take a while...")
            result = local('pg_dump -v --host %(new_host)s --port 5432 -U \"llxDBA\" -s -f ~/new.sql %(new_db)s' % {"new_host":new_host, "new_db":new_db})
        if result.failed:
            abort("Is postgres bin in your PATH? \n \
                ie: check your .bas_profile and see if you have:\n \
                PATH=\"/Library/PostgreSQL/9.1/bin:${PATH}\"\n \
                export PATH")
        with lcd("~/sysadmin/plugins"):
            print green("generating diff")
            local("java -jar apgdiff-2.4.jar --ignore-start-with ~/old.sql ~/new.sql > ~/diff.sql")
        # cleanup file
        print green("done. generated ~/diff.sql")
        local("rm ~/old.sql; rm ~/new.sql")
        local("open ~/diff.sql")
