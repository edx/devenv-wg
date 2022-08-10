from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


################# Configuration
config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "exams:{{ EXAMS_VERSION }}",
        "HOST": "exams.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "exams",
        "MYSQL_USERNAME": "exams",
        "OAUTH2_KEY": "exams",
        "OAUTH2_KEY_DEV": "exams-dev",
        "OAUTH2_KEY_SSO": "exams-sso",
        "OAUTH2_KEY_SSO_DEV": "exams-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {
        # "PLATFORM_NAME": "My platform",
    },
}

################# Initialization tasks
hooks.Filters.COMMANDS_INIT.add_item(
    (
        "mysql",
        ("exams", "tasks", "mysql", "init"),
    )
)
hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("exams", "tasks", "lms", "init"),
    )
)
hooks.Filters.COMMANDS_INIT.add_item(
    (
        "exams",
        ("exams", "tasks", "exams", "init"),
    )
)

################# Docker image management
# To build an image with `tutor images build myimage`, add a Dockerfile to templates/exams/build/myimage and write:
hooks.Filters.IMAGES_BUILD.add_item((
    "exams",
    ("plugins", "exams", "build", "exams"),
    "{{ EXAMS_DOCKER_IMAGE }}",
    (),
))
# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:{{ EXAMS_VERSION }}",
# )
# hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:{{ EXAMS_VERSION }}",
# )


################# You don't really have to bother about what's below this line,
################# except maybe for educational purposes :)

# Plugin templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorexams", "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("exams/build", "plugins"),
        ("exams/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorexams", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"EXAMS_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"EXAMS_{key}", value)
        for key, value in config["unique"].items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
