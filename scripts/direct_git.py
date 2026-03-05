import subprocess

commands = [
    ['git', 'add', 'src/api/index.js', 'src/components/admin/BonusManagement.vue'],
    ['git', 'commit', '-m', 'feat: update BonusManagement to use real API'],
    ['git', 'push', 'origin', 'main']
]

for cmd in commands:
    print(' '.join(cmd))
    subprocess.call(cmd, shell=True)
