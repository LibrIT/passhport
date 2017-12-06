user
=============================

Usages :

.. code-block:: none

  passhport-admin user list
  passhport-admin user search [<pattern>]
  passhport-admin user show [<name>]
  passhport-admin user create [((<name> <sshkey>) [--comment=<comment>])]
  passhport-admin user edit [(<name> [--newname=<name>] [--newsshkey=<sshkey>] [--newcomment=<comment>])]
  passhport-admin user delete [([-f | --force] <name>)]

list
-----

`passhport-admin user list` show all the configured users.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin user list
  admin1@compagny.com
  admin2@compagny.com
  alice@compagny.com
  bob@compagny.com
  admin@bastion:~$

search
---------

`passhport-admin user search [<PATTERN>]` searches in the user list for all user that correspond to the given pattern.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin user search admin
  admin1@compagny.comi
  admin2@compagny.com
  admin@bastion:~#    

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin user search 
  Pattern: alice
  alice@compagny.com
  admin@bastion:~# 

show
-------

`passhport-admin user show <NAME>` shows informations about the user <NAME>.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin user show alice@compagny.com 
  Email: alice@compagny.com
  SSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDFOU5Saf+epkm79BeSniE7VtYMexJeL6BvXUsKUb7m8W4gnD3YTBW93uykO/6ovi9TfYdm+4nKQ9gUGUgzNyD8o7zW8w6wKogoL24UbJKmkZOCU1IgHJSt1QYIs/qHQZ2MR6S6K2f/1J1joYINPtGpQJ475OZfYQbP79fEdRdylupC8L+fvxkka4C0Uxj0I1VjDCVJCjO0md5oXzN75I2aw+RFWuiiL5P/gHRu+2iff2rdhebJZs4ux8u76LQLzYsG9a85Xlagw6N7/aXWnUZ/9gqoF/qVUHfS8ggesTwEJyNnY7EpPcKRUcwnlonn5CIS++Yo8iqjLd93RjFxShUqXlw9Cct4hdh/clW/QYsJRMfN9860mZ9v9dEitM2X1w8HCCD5NAHGqRRrtONM99kZRxmkCQ/Tb+jXvJ+VAl4qffuPPdxY+Bev7wygm4rVnjF2Ac5ioWb4Zd+zIb712VTQDQlRxsu73yWtHSodeSgPpgCWTjCwW/841QbPGkclnE6DKIwQ/vxC0ggSXouc5G6j0gHu90eQ24XL6Gurqr2C11w9saRyzrYRRlS0Ihkp3rMSteVcvrb1Qi4UGmJCHHSBhvP8jRFH4mbdkSGyzsxtjr8puJc8DiQ1UKG3O9X12m8nbOYeNdIofTw615k0YitoQ/60fdEELQyX+kNFQ2VoCw== alice@compagny.com
  Comment: 
  Accessible target list: 

  Details in access:
  Accessible directly: 
  Accessible through usergroups: 
  Accessible through targetgroups: 
  admin@bastion:~#

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin user show
  Name: alice@compagny.com
  Email: alice@compagny.com
  SSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDFOU5Saf+epkm79BeSniE7VtYMexJeL6BvXUsKUb7m8W4gnD3YTBW93uykO/6ovi9TfYdm+4nKQ9gUGUgzNyD8o7zW8w6wKogoL24UbJKmkZOCU1IgHJSt1QYIs/qHQZ2MR6S6K2f/1J1joYINPtGpQJ475OZfYQbP79fEdRdylupC8L+fvxkka4C0Uxj0I1VjDCVJCjO0md5oXzN75I2aw+RFWuiiL5P/gHRu+2iff2rdhebJZs4ux8u76LQLzYsG9a85Xlagw6N7/aXWnUZ/9gqoF/qVUHfS8ggesTwEJyNnY7EpPcKRUcwnlonn5CIS++Yo8iqjLd93RjFxShUqXlw9Cct4hdh/clW/QYsJRMfN9860mZ9v9dEitM2X1w8HCCD5NAHGqRRrtONM99kZRxmkCQ/Tb+jXvJ+VAl4qffuPPdxY+Bev7wygm4rVnjF2Ac5ioWb4Zd+zIb712VTQDQlRxsu73yWtHSodeSgPpgCWTjCwW/841QbPGkclnE6DKIwQ/vxC0ggSXouc5G6j0gHu90eQ24XL6Gurqr2C11w9saRyzrYRRlS0Ihkp3rMSteVcvrb1Qi4UGmJCHHSBhvP8jRFH4mbdkSGyzsxtjr8puJc8DiQ1UKG3O9X12m8nbOYeNdIofTw615k0YitoQ/60fdEELQyX+kNFQ2VoCw== alice@compagny.com
  Comment: 
  Accessible target list: 

  Details in access:
  Accessible directly: 
  Accessible through usergroups: 
  Accessible through targetgroups: 
  admin@bastion:~#

create
----------

`passhport-admin user create [((<name> <sshkey>) [--comment=<comment>])]` creates a new user.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the target to edit

<sshkey>           SSH key of the user (use ``"`` as the below example)

--comment          Comment concerning the user (optional)
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin user create bob@compagny.com "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHTlnhl23T9NiHn06wWaDpT1aJqEY0aOW7E4dfu7kQJsmRqg2SWMld6H8Q+bggwCLSkRKubOWyoJkprAfwOP8OArAGPCIr9PeQfC581EVqaev/yJYbKwwPQEaHpiQoHMaBfsgA2BYS5cNVcrOpLk8nHgKSJGEcdYipbZZxqDrLaeX3lBA== bob@mydesktop"
  OK: "bob@compagny.com" -> created
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin user create bob@compagny.com "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHTlnhl23T9NiHn06wWaDpT1aJqEY0aOW7E4dfu7kQJsmRqg2SWMld6H8Q+bggwCLSkRKubOWyoJkprAfwOP8OArAGPCIr9PeQfC581EVqaev/yJYbKwwPQEaHpiQoHMaBfsgA2BYS5cNVcrOpLk8nHgKSJGEcdYipbZZxqDrLaeX3lBA== bob@mydesktop"
  OK: "bob@compagny.com" -> created
  admin@bastion:~$ passhport-admin user create 
  Email (user name): john@ext-compagny.com
  SSH Key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCs9YpOfP9vgViYa1SSntrydEBLGyWGAr9nvEjqHcMwHQb9JEmhIjvk1ctb8+Kns3/52F0hBrxic6k6UPvvvjbtJX33muFv5dd0k1W4lLcYe4ONTFwLOqCph4Is5r9lbZ5KXxhN/8YC/08jBJow0CoYdc+Yr7MlA51+tEQFwPbuB5vHMUteye0IgmaH9MLzXes/j5BUhnBjDscWVQSvNHY4/PKtHvIdvoI1uKAplstuHI6CDqnb0aJ5P9wME3P1lhRwcVDTm48/AMcfmpp5s+DwOmyDGfGXf+hE0cu7ulAkwHBhR6ciJJg1pz4DqraglxyVyrt+PFq6KDeV/7WwoNEP yann@mylaptop.com 
  Comment: John is a extern expert.
  OK: "john@ext-compagny.com" -> created
  admin@bastion:~$

edit
-----------

`passhport-admin user edit [(<name> [--newname=<name>] [--newsshkey=<sshkey>] [--newcomment=<comment>])]` edits an existing user.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the user to edit

--newname          New name of the user if you want to rename it (optional)

--newsshkey        New SSH key of the user (use ``"`` as the below example) (optional)

--newcomment       New comment concerning the user (optional)
================== ===================================================================

**Example :**

.. code-block:: none

 admin@bastion:~$ passhport-admin user edit john@ext-compagny.com --newname=john.doe@ext-compagny.com --newcomment="John is a extern expert, he'll be here until january 18th."
 OK: "john@ext-compagny.com" -> edited
 admin@bastion:~$

If no argument is given, user enters in interactive mode. It firsts shows all parameters of the user, then displays each parameters for a change. User can keep any previous configured parameter, just by typing "Enter". They only exception is the comment. If user wants to remove the comment, he just type "Enter", and will then be asked if the original comment should be removed or not.

**Example :**

.. code-block:: none

 admin@bastion:~$ passhport-admin user edit 
 Name of the user you want to modify: john.doe@ext-compagny.com
 Email: john.doe@ext-compagny.com
 SSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCs9YpOfP9vgViYa1SSntrydEBLGyWGAr9nvEjqHcMwHQb9JEmhIjvk1ctb8+Kns3/52F0hBrxic6k6UPvvvjbtJX33muFv5dd0k1W4lLcYe4ONTFwLOqCph4Is5r9lbZ5KXxhN/8YC/08jBJow0CoYdc+Yr7MlA51+tEQFwPbuB5vHMUteye0IgmaH9MLzXes/j5BUhnBjDscWVQSvNHY4/PKtHvIdvoI1uKAplstuHI6CDqnb0aJ5P9wME3P1lhRwcVDTm48/AMcfmpp5s+DwOmyDGfGXf+hE0cu7ulAkwHBhR6ciJJg1pz4DqraglxyVyrt+PFq6KDeV/7WwoNEP yann@mylaptop.com
 Comment: John is a extern expert, he'll be here until january 18th.
 Accessible target list: 

 Details in access:
 Accessible directly: 
 Accessible through usergroups: 
 Accessible through targetgroups: 
 New name: 
 New SSH key: 
 New comment: John is a extern expert, he'll be here until february 2nd     
 OK: "john.doe@ext-compagny.com" -> edited
 admin@bastion:~$ 

As you can see above, we only changed the "New comment" entry. If an entry is simply replied with "enter", it keeps the previous value.

delete
-----------

`passhport-admin user delete [([-f | --force] <name>)]` delete a user.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the user to delete

-f or --force      If used, user won't be prompt for confirmation
================== ===================================================================

**Example :**

.. code-block:: none

 admin@bastion:~$ passhport-admin user delete john.doe@ext-compagny.com 
 Email: john.doe@ext-compagny.com
 SSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCs9YpOfP9vgViYa1SSntrydEBLGyWGAr9nvEjqHcMwHQb9JEmhIjvk1ctb8+Kns3/52F0hBrxic6k6UPvvvjbtJX33muFv5dd0k1W4lLcYe4ONTFwLOqCph4Is5r9lbZ5KXxhN/8YC/08jBJow0CoYdc+Yr7MlA51+tEQFwPbuB5vHMUteye0IgmaH9MLzXes/j5BUhnBjDscWVQSvNHY4/PKtHvIdvoI1uKAplstuHI6CDqnb0aJ5P9wME3P1lhRwcVDTm48/AMcfmpp5s+DwOmyDGfGXf+hE0cu7ulAkwHBhR6ciJJg1pz4DqraglxyVyrt+PFq6KDeV/7WwoNEP yann@mylaptop.com
 Comment: John is a extern expert, he'll be here until february 2nd
 Accessible target list: 

 Details in access:
 Accessible directly: 
 Accessible through usergroups: 
 Accessible through targetgroups: 
 Are you sure you want to delete john.doe@ext-compagny.com? [y/N] y
 OK: "john.doe@ext-compagny.com" -> deleted
 admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

 admin@bastion:~$ passhport-admin user delete
 Name: bob@compagny.com
 Email: bob@compagny.com
 SSH key: ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHTlnhl23T9NiHn06wWaDpT1aJqEY0aOW7E4dfu7kQJsmRqg2SWMld6H8Q+bggwCLSkRKubOWyoJkprAfwOP8OArAGPCIr9PeQfC581EVqaev/yJYbKwwPQEaHpiQoHMaBfsgA2BYS5cNVcrOpLk8nHgKSJGEcdYipbZZxqDrLaeX3lBA== bob@mydesktop
 Comment: 
 Accessible target list: 

 Details in access:
 Accessible directly: 
 Accessible through usergroups: 
 Accessible through targetgroups: 
 Are you sure you want to delete bob@compagny.com? [y/N] y
 OK: "bob@compagny.com" -> deleted
 admin@bastion:~$
