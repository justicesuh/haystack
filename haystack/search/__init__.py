import warnings

warnings.filterwarnings(
    'ignore',
    r'^pkg_resources is deprecated as an API',
    category=UserWarning,
)
