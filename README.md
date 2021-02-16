# django-backblaze-b2

[![pypi version](https://img.shields.io/pypi/v/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)
[![python version](https://img.shields.io/pypi/pyversions/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)
[![django version](https://img.shields.io/pypi/djversions/django-backblaze-b2)](https://pypi.org/project/django-backblaze-b2/)

A storage backend for Django that uses [Backblaze's B2 APIs](https://www.backblaze.com/b2/cloud-storage.html).

Implementation wraps [Official Python SDK](https://github.com/Backblaze/b2-sdk-python)

## How to use

1. Install from this repo, or install from PyPi: `pip install django-backblaze-b2`
As tested, requires python 3.6 or greater but solely due to type annotations. PRs welcome :)
1. Configure your django `settings`. The absolute minimum config would be:
```python
BACKBLAZE_CONFIG = {
    "application_key_id": os.getenv("BACKBLAZE_KEY_ID"), # however you want to securely retrieve these values
    "application_key": os.getenv("BACKBLAZE_KEY"),
}
```

Theoretically you may now refer to the base storage class as a storage class.  
e.g.
```python
from django_backblaze_b2 import BackblazeB2Storage

class MyModel(models.Model):
    fileField = models.FileField(
        upload_to="uploads",
        storage=BackblazeB2Storage
    )
```

### Public/Logged-In/Private storage

1. Add `django_backblaze_b2` to your `INSTALLED_APPS`
1. Add the urls to your `urlpatterns` in the root `urls.py`:
```python
    urlpatterns = [
        ...
        path('', include('django_backblaze_b2.urls')),
    ]
```

### Configurations 

You may want to use your own bucket name, or set further configuration such as lazy authorization/validation, or specifying file metadata.  
Refer to [the options](./django_backblaze_b2/options.py) for all options.  
You can modify the settings dict, but additionally override any setting with the `opts` keyword argument to the storage classes.

To specify different buckets to use for your public, logged-in, staff storage, you can set the 
`specificBucketNames` attribute of the settings dict.

## Why

There are several Django storage packages out there already which support B2, but none met my needs. These are:

* [django-storages](https://github.com/jschneier/django-storages)
    * Large community engagement ✅
    * Well-tested ✅
    * [Second-class support](https://github.com/jschneier/django-storages/issues/765) via [Apache Libcloud](https://github.com/apache/libcloud) ❌
    * Disconnect in configuration and actual use ❌
    * PR list with low turnaround ❌
* [django-b2](https://github.com/pyutil/django-b2)
    * Similar aim to this project, around official backblaze SDK ✅
    * Mixed goals (storage, scripts) ❌
    * Tests?? ❌
* [django-backblazeb2-storage](https://github.com/royendgel/django-backblazeb2-storage)
    * Simple configuration ✅
    * Not based around python SDK (potentially harder to keep up with version changes) ❌
    * Tests?? ❌

### S3 Compatible API

Backblazed can be used with an [S3-compatible API](https://www.backblaze.com/b2/docs/s3_compatible_api.html)
This is great, but most packages use an older version of the S3 Api (v2). Backblaze uses v4.

### What this package offers

* Type Annotations
* Tested
* No hacks required to get up and running around API deficiencies (any hacks are not exposed in API)
* Support for public/private files, restricted via Django user permissions

## How it works

* A simple implementation of the `django.core.files.storage.Storage` class provides handling for storage behaviour within your Django application
* Three url routes are appended to the root of your application:  
    1. `/b2/`
    2. `/b2l/`
    3. `/b2s/`
These routes act as a proxy/intermediary between the requester and backblaze b2 apis. The public `/b2/` allows exposing files from a private bucket, and the logged-in and staff routes will perform the known validations of a django app to prevent unauthorized access.

### Gotchas

* The original filename + any upload paths is stored in the database. Thus your column name must be of sufficient length to hold that (unchanged behaviour from `FileSystemStorage`)
*  When retrieving files from the `PublicStorage`, `LoggedInStorage` or `StaffStorage`, you may not override the `"bucket"` or authorization options, or else when the app proxies the file download, it will be unable to retrieve the file from the respective bucket.
* Simply using `LoggedInStorage` or `StaffStorage` is not enough to protect your files if your bucket is not public. If any individual gains access to the file ids/urls for these files, there is no authentication around them. It is up to the implementer to ensure the security of their application.
* Once the file is uploaded, and someone obtains a file url (e.g. http://djangodomain.com/b2l/uploads/image.png), the model will no longer be checked for the file. This means that if you share the bucket between multiple use-cases, you could in theory find finds that don't belong to your django app, or similarly if you delete/change your models, the files could still be downloaded. Consider using an app like [django-cleanup](https://github.com/un1t/django-cleanup) if this is important to you

## Contributing

Contributions welcome!

* Please ensure test coverage does not decrease in a meaningful way.
* Ensure formatting is compliant (`make lint`)
* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Setting up for development

### Requires

* python
* pyenv - align local version
* GNU Make
* (optional) docker - run sample app

#### Version compatibility reminder

| Ver  | Status   |  EOL       |
| ---- | -------- | ---------- |
| 3.9  | bugfix   | 2025-10    |
| 3.8  | bugfix   | 2024-10    |
| 3.7  | security | 2023-06-27 |
| 3.6  | security | 2021-12-23 |

### Running

1. `make setup`

* You can run django with `make run-django` to test django app.
* You can run tests with `make test`
* You can view test coverage with `make test-coverage`, then see in the terminal, 
open `test/htmlcov/index.html`
or use `cov.xml` in your favourite IDE like VSCode

### Releasing

1. `make publish-to-pypi`

### Cleanup

1. `make cleanup`