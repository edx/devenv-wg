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
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {
        # "SECRET_KEY": "\{\{ 24|random_string \}\}",
    },
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {
        # "PLATFORM_NAME": "My platform",
    },
}

################# Initialization tasks
# To run the script from templates/2u-devdata/tasks/myservice/init, add:
hooks.Filters.COMMANDS_INIT.add_item((
     "cms",
     ("2u-devdata", "tasks", "init.sh"),
))

################# Docker image management
# To build an image with `tutor images build myimage`, add a Dockerfile to templates/2u-devdata/build/myimage and write:
# hooks.Filters.IMAGES_BUILD.add_item((
#     "myimage",
#     ("plugins", "2u-devdata", "build", "myimage"),
#     "docker.io/myimage:\{\{ 2U_DEVDATA_VERSION \}\}",
#     (),
# )
# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:\{\{ 2U_DEVDATA_VERSION \}\}",
# )
# hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:\{\{ 2U_DEVDATA_VERSION \}\}",
# )


################# You don't really have to bother about what's below this line,
################# except maybe for educational purposes :)

# Plugin templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutor_2u_devdata", "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("2u-devdata/build", "plugins"),
        ("2u-devdata/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutor_2u_devdata", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"2U_DEVDATA_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"2U_DEVDATA_{key}", value)
        for key, value in config["unique"].items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
