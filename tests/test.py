from time import time
import repoutils.release

s = time()
r = 'https://havoc.app'
repo = repoutils.release.Release(r)
print(f'-------\nGot repo {r} with label {repo.label} and description {repo.description} on version {repo.version}.\nTook {time() - s} seconds to get repo with {len(repo.packages)} packages.\n-------')

s = time()
r = 'https://repo.chariz.com'
repo = repoutils.release.Release(r)
print(f'-------\nGot repo {r} with label {repo.label} and description {repo.description} on version {repo.version}.\nTook {time() - s} seconds to get repo with {len(repo.packages)} packages.\n-------')