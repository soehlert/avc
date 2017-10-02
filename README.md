# AVC (Ansible Variables Checker)

After making countless errors with variable names and trying to figure out what variables in my ansible tasks/templates were undefined, I began working on this to address that issue.

## Examples

```[soehlert@macbookpro: ~/projects/avc (master)]$ python avc.py -r ~/projects/cu-ansible/roles/packages/ -g ~/projects/cu-ansible/group_vars/all/packages.yml
All your variables are accounted for```

```[soehlert@macbookpro: ~/projects/avc (master)]$ python avc.py -r ~/projects/security-ansible/roles/ssh-auditor -g ~/projects/security-ansible/inventories/dev/group_vars/ssh-auditor.yml
Variables missing matches:
ssh_audit_interval```


## Usage

```[soehlert@macbookpro: ~/projects/avc (master)]$ python avc.py -h
usage: avc.py [-h] [-r ROLE_DIR] [-g [GROUP_VARS [GROUP_VARS ...]]]
              [--version]

optional arguments:
  -h, --help            show this help message and exit
  -r ROLE_DIR, --role ROLE_DIR
                        Specify role to check against
  -g [GROUP_VARS [GROUP_VARS ...]], --group_vars [GROUP_VARS [GROUP_VARS ...]]
                        Specify group_vars to check against
  --version             Print version```
