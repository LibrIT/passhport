Toogle group administrator (PaSSHweb)
=====================================

Explanation
-----------

If you use passhweb, you might want to delegate the right of adding users to someone, like an admin role.
To do so, just call the following API endpoint, in order to toggle the admin role to a specific user :

.. code-block:: none

  # wget --no-check-certificate -qO - https://localhost:5000/user/togglesuperadmin/username
  This user is now: administrator
  # wget --no-check-certificate -qO - https://localhost:5000/user/togglesuperadmin/username
  This user is now: NOT administrator
  #

Of course, you have to replace "username" in the URL above with the username of the user you want to assign the admin role to.
